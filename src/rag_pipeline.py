import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFacePipeline
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from transformers import AutoModelForSequenceClassification

class MedicalRAG:
    """
    Upgraded Retrieval-Augmented Generation pipeline for Clinica-LENS.
    Uses SapBERT for medical embeddings and Hybrid Search (BM25 + FAISS) 
    with BGE Cross-Encoder Re-ranking.
    """
    def __init__(self, data_dir=None, vector_db_path=None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = data_dir or os.path.join(base_dir, 'data', 'medical_literature')
        self.vector_db_path = vector_db_path or os.path.join(base_dir, 'models', 'faiss_index')
        
        # 1. Use SapBERT for domain-specific medical embeddings
        print("Loading SapBERT medical embedding model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="cambridgeltl/SapBERT-from-PubMedBERT-fulltext"
        )
        
        # 2. Setup Re-ranker
        print("Loading BGE Cross-Encoder re-ranker...")
        self.reranker_model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
        self.compressor = CrossEncoderReranker(model=self.reranker_model, top_n=3)

        # 3. NLI Model for Fact Checking (Phase 2 Upgrade)
        print("Loading NLI model for verification...")
        self.nli_tokenizer = AutoTokenizer.from_pretrained("cross-encoder/nli-deberta-v3-small")
        self.nli_model = AutoModelForSequenceClassification.from_pretrained("cross-encoder/nli-deberta-v3-small")

        self.vectorstore = None
        self.bm25_retriever = None
        self.ensemble_retriever = None
        self.compression_retriever = None
        self.llm = None
        self.qa_chain = None
        self.chat_history = [] 

    def ingest_documents(self):
        """Loads PDFs, splits them, and creates Hybrid Search indexes."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            return

        documents = []
        for file in os.listdir(self.data_dir):
            file_path = os.path.join(self.data_dir, file)
            if file.endswith(".pdf"):
                documents.extend(PyPDFLoader(file_path).load())
            elif file.endswith(".txt"):
                documents.extend(TextLoader(file_path).load())

        if not documents:
            print("No documents found.")
            return

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = text_splitter.split_documents(documents)

        # 2. Setup Hybrid Search (FAISS + BM25)
        print("Building Hybrid Search indexes...")
        self.vectorstore = FAISS.from_documents(texts, self.embeddings)
        self.vectorstore.save_local(self.vector_db_path)
        
        self.bm25_retriever = BM25Retriever.from_documents(texts)
        self.bm25_retriever.k = 5
        
        faiss_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.bm25_retriever, faiss_retriever],
            weights=[0.4, 0.6] 
        )

        # Apply Re-ranking
        self.compression_retriever = ContextualCompressionRetriever(
            base_compressor=self.compressor, base_retriever=self.ensemble_retriever
        )
        print("Hybrid Search with Re-ranking ready.")

    def load_vector_db(self):
        """Loads existing FAISS and reconstructs BM25 index from stored docs."""
        if os.path.exists(self.vector_db_path):
            self.vectorstore = FAISS.load_local(
                self.vector_db_path, self.embeddings, allow_dangerous_deserialization=True
            )
            docs = list(self.vectorstore.docstore._dict.values())
            self.bm25_retriever = BM25Retriever.from_documents(docs)
            self.bm25_retriever.k = 5
            
            faiss_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
            self.ensemble_retriever = EnsembleRetriever(
                retrievers=[self.bm25_retriever, faiss_retriever],
                weights=[0.4, 0.6]
            )
            self.compression_retriever = ContextualCompressionRetriever(
                base_compressor=self.compressor, base_retriever=self.ensemble_retriever
            )
            print("Hybrid Search with Re-ranking loaded.")

    def setup_llm(self, model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        """Initializes a local LLM and the RAG chain."""
        print(f"Loading LLM: {model_id}...")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id)
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=256, temperature=0.1)
        self.llm = HuggingFacePipeline(pipeline=pipe)

        template = """You are a senior radiologist. Based on the clinical context provided, generate a structured radiology report.
        Strictly follow this format:
        FINDINGS: <Detailed observations from the context>
        IMPRESSION: <Your clinical conclusion>
        
        If the context doesn't have the answer, say 'Insufficient literature context'.
        
        Context: {context}
        Question: {question}
        
        Structured Radiology Report:"""
        PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])

        if self.compression_retriever:
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.compression_retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": PROMPT}
            )

    def verify_explanation(self, context, explanation):
        """Phase 2: NLI-based Fact Checking."""
        # Split explanation into sentences
        sentences = [s.strip() for s in explanation.split('.') if len(s.strip()) > 10]
        if not sentences:
            return "SAFE"
            
        warnings = []
        for sent in sentences:
            # Pair each sentence with context
            features = self.nli_tokenizer(context, sent, truncation=True, return_tensors="pt")
            with torch.no_grad():
                logits = self.nli_model(**features).logits
                # labels: 0: contradiction, 1: neutral, 2: entailment
                probs = torch.softmax(logits, dim=1).squeeze()
                
            if probs[0] > 0.5: # Contradiction detected
                warnings.append(f"Sentence '{sent[:30]}...' contradicts literature.")
            elif probs[2] < 0.3: # Low entailment
                warnings.append(f"Sentence '{sent[:30]}...' is not grounded in literature.")
        
        return "SAFE" if not warnings else "WARNING: " + "; ".join(warnings[:2])

    def explain_diagnosis(self, query):
        """Generates a verified structured report."""
        if not self.qa_chain:
            return {"explanation": "RAG not initialized", "status": "Error"}
        
        result = self.qa_chain({"query": query})
        output = result["result"]
        context_text = "\n".join([doc.page_content for doc in result["source_documents"]])
        
        # Parse Structured Report
        findings = "N/A"
        impression = "N/A"
        if "FINDINGS:" in output and "IMPRESSION:" in output:
            parts = output.split("IMPRESSION:")
            findings = parts[0].replace("FINDINGS:", "").strip()
            impression = parts[1].strip()
        
        # Run verification loop
        status = self.verify_explanation(context_text, output)
        
        # Store initial context in chat history for VQA (Phase 4)
        self.chat_history = [("System", f"Context: {context_text}")]
        
        return {
            "findings": findings,
            "impression": impression,
            "full_report": output,
            "status": status,
            "sources": list(set([doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]))
        }

    def chat_vqa(self, user_query):
        """Phase 4: Conversational Visual QA loop."""
        if not self.llm:
            return "LLM not initialized."
        
        # Construct chat context
        history_str = "\n".join([f"{role}: {msg}" for role, msg in self.chat_history[-5:]])
        prompt = f"""You are a medical assistant helping a radiologist interrogate a chest X-ray. 
        Answer the following question based on the previous context and report.
        
        History:
        {history_str}
        
        User Question: {user_query}
        Assistant Answer:"""
        
        response = self.llm(prompt)
        self.chat_history.append(("User", user_query))
        self.chat_history.append(("Assistant", response))
        
        return response
