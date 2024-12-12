import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

class FAISSIndexManager:
    def __init__(self, index_path, embedding_model):
        self.index_path = index_path
        self.embedding_model = embedding_model
        self.vectorstore = None
        self._load_or_initialize_index()

    def _load_or_initialize_index(self):
        if os.path.exists(self.index_path):
            # print("Loading existing FAISS index...")
            self.vectorstore = FAISS.load_local(
                self.index_path, 
                self.embedding_model, 
                allow_dangerous_deserialization=True
            )
        else:
            # print("Initializing a new FAISS index...")
            self.vectorstore = None

    def add_documents(self, pdf_paths):
        for pdf_path in pdf_paths:
            print(f"Processing: {pdf_path}")
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()

            text_splitter = CharacterTextSplitter(
                separator='\n',
                chunk_size=500,
                chunk_overlap=100,
                length_function=len
            )
            texts = text_splitter.split_documents(documents)

            if self.vectorstore is None:
                self.vectorstore = FAISS.from_documents(texts, self.embedding_model)
            else:
                self.vectorstore.add_documents(texts)

        self._save_index()

    def search(self, query, top_k=1):
        if self.vectorstore is None:
            print("No FAISS index available. Please add documents first.")
            return []

        print(f"===== DB 에서 답변 검색을 시작합니다. =====")
        print(f"Searching for: {query}")
        faiss_retriever = self.vectorstore.as_retriever(search_kwargs={"k": top_k})
        search_results = faiss_retriever.invoke(query)
        print(f"검색결과: {search_results}")
        print(f"===== DB 에서 답변 검색이 완료되었습니다. =====")
        
        return search_results

    def _save_index(self):
        if self.vectorstore is not None:
            self.vectorstore.save_local(self.index_path)
            print(f"FAISS index saved at {self.index_path}")