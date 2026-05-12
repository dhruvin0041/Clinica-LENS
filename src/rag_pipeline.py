import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterCharacterSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFacePipeline
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class MedicalRAG:
    """
    Upgraded Retrieval-Augmented Generation pipeline for Clinica-LENS.
    Uses SapBERT for medical embeddings and Hybrid Search (BM25 + FAISS).
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
        self.vectorstore = None
        self.bm25_retriever = None
        self.ensemble_retriever = None
        self.llm = None
        self.qa_chain = None

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

        from langchain_text_splitters import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = text_splitter.split_documents(documents)

        # 2. Setup Hybrid Search (FAISS + BM25)
        print("Building Hybrid Search indexes...")
        self.vectorstore = FAISS.from_documents(texts, self.embeddings)
        self.vectorstore.save_local(self.vector_db_path)
        
        self.bm25_retriever = BM25Retriever.from_documents(texts)
        self.bm25_retriever.k = 3
        
        faiss_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, faiss_retriever],
            weights=[0.4, 0.6] # Favor semantic search slightly
        )
        print("Hybrid Search ready.")

    def load_vector_db(self):
        """Loads existing FAISS and reconstructs BM25 index from stored docs."""
        if os.path.exists(self.vector_db_path):
            self.vectorstore = FAISS.load_local(
                self.vector_db_path, self.embeddings, allow_dangerous_deserialization=True
            )
            
            # Reconstruct BM25 from FAISS documents
            # Note: In production, we'd save BM25 separately, but here we can derive it.
            docs = list(self.vectorstore.docstore._dict.values())
            self.bm25_retriever = BM25Retriever.from_documents(docs)
            self.bm25_retriever.k = 3
            
            faiss_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
            self.ensemble_retriever = EnsembleRetriever(
                retrievers=[self.bm25_retriever, faiss_retriever],
                weights=[0.4, 0.6]
            )
            print("Hybrid Search loaded successfully.")

    def setup_llm(self, model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        """Initializes a local LLM and the RAG chain."""
        print(f"Loading LLM: {model_id}...")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id)
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=256, temperature=0.1)
        self.llm = HuggingFacePipeline(pipeline=pipe)

        template = """Context: {context}
        Question: {question}
        Explain the potential diagnosis based ONLY on the context above. If unsure, say 'I cannot verify this'.
        Clinical Explanation:"""
        PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])

        if self.ensemble_retriever:
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.ensemble_retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": PROMPT}
            )

    def verify_explanation(self, context, explanation):
        """Phase 5: Self-Correction Loop / Hallucination Guardrail."""
        verification_prompt = f"""Compare the Following Explanation against the provided Clinical Context.
        Context: {context}
        Explanation: {explanation}
        
        Does the explanation contain any medical claims NOT supported by the context? 
        Answer 'SAFE' if verified, or 'WARNING: [reason]' if unverified claims exist.
        Verification Status:"""
        
        # Use a raw LLM call for verification
        if self.llm:
            status = self.llm(verification_prompt)
            return status.strip()
        return "Verification Unavailable"

    def explain_diagnosis(self, query):
        """Generates a verified explanation."""
        if not self.qa_chain:
            return {"explanation": "RAG not initialized", "status": "Error"}
        
        result = self.qa_chain({"query": query})
        context_text = "\n".join([doc.page_content for doc in result["source_documents"]])
        
        # Run verification loop
        status = self.verify_explanation(context_text, result["result"])
        
        return {
            "explanation": result["result"],
            "status": status,
            "sources": list(set([doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]))
        }
