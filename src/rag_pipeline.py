import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class MedicalRAG:
    """
    Retrieval-Augmented Generation pipeline for Clinica-LENS.
    Reads medical literature (PDFs), vectorizes them, and grounds LLM explanations.
    """
    def __init__(self, data_dir=None, vector_db_path=None):
        # Use absolute paths relative to this file's location (src folder)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = data_dir or os.path.join(base_dir, 'data', 'medical_literature')
        self.vector_db_path = vector_db_path or os.path.join(base_dir, 'models', 'faiss_index')
        
        # Load lightweight embeddings suitable for medical text (BioBERT or standard MiniLM)
        print("Loading embedding model...")
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        self.vectorstore = None
        self.llm = None
        self.qa_chain = None

    def ingest_documents(self):
        """Loads PDFs, splits them, and creates a FAISS vector database."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"Created directory: {self.data_dir}. Please place medical PDFs here.")
            return

        print("Loading documents...")
        loader = DirectoryLoader(self.data_dir, glob="*.*", loader_cls=PyPDFLoader if "*.pdf" else None)
        # Note: DirectoryLoader with default handles text files automatically if loader_cls is omitted for them.
        # Let's use a simpler approach for the demo:
        from langchain_community.document_loaders import TextLoader
        
        documents = []
        for file in os.listdir(self.data_dir):
            if file.endswith(".pdf"):
                loader = PyPDFLoader(os.path.join(self.data_dir, file))
                documents.extend(loader.load())
            elif file.endswith(".txt"):
                loader = TextLoader(os.path.join(self.data_dir, file))
                documents.extend(loader.load())

        if not documents:
            print("No documents found to ingest.")
            return

        print(f"Splitting {len(documents)} documents...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = text_splitter.split_documents(documents)

        print("Building Vector DB...")
        self.vectorstore = FAISS.from_documents(texts, self.embeddings)
        self.vectorstore.save_local(self.vector_db_path)
        print(f"Vector DB saved to {self.vector_db_path}")

    def load_vector_db(self):
        """Loads an existing FAISS vector database."""
        if os.path.exists(self.vector_db_path):
            self.vectorstore = FAISS.load_local(self.vector_db_path, self.embeddings, allow_dangerous_deserialization=True)
            print("Vector DB loaded successfully.")
        else:
            print("Vector DB not found. Run ingest_documents() first.")

    def setup_llm(self, model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        """Initializes a local HuggingFace LLM for text generation."""
        print(f"Loading LLM: {model_id} (This may take a while)...")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id)

        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=256,
            temperature=0.1,
            top_p=0.9,
            repetition_penalty=1.1
        )
        self.llm = HuggingFacePipeline(pipeline=pipe)

        # Create the RAG prompt template
        template = """Use the following pieces of medical context to explain the potential diagnosis. 
        If you don't know the answer, just say you don't know. Keep the explanation concise and clinical.

        Context: {context}

        Patient Symptoms & Image Findings: {question}

        Clinical Explanation:"""
        PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])

        # Create the retrieval chain
        if self.vectorstore:
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
                return_source_documents=True,
                chain_type_kwargs={"prompt": PROMPT}
            )
            print("RAG QA Chain initialized successfully.")
        else:
            print("Cannot setup QA Chain: Vector DB is not loaded.")

    def explain_diagnosis(self, query):
        """Generates an explanation based on the query and retrieved context."""
        if not self.qa_chain:
            return "QA chain is not initialized."
        
        print(f"Analyzing query: {query}")
        result = self.qa_chain({"query": query})
        
        return {
            "explanation": result["result"],
            "sources": [doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]
        }

if __name__ == "__main__":
    # Test initialization
    rag = MedicalRAG()
    print("MedicalRAG module is ready.")
