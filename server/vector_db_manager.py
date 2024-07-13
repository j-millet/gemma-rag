from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import  TextLoader

class vector_db_manager:
    def __init__(self,chunk_size=1000,chunk_overlap=150) -> None:
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
        self.embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2",model_kwargs={"device":"cuda"},encode_kwargs={"normalize_embeddings":False})
        self.user_stores = set()
        self.db = Chroma(embedding_function=self.embedding_function)
    
    def add_user_store(self,user_id,doc_paths):
        self.user_stores.add(user_id)
        for doc_path in doc_paths:
            self.db.add_documents(self.process_file(doc_path,user_id))

    def process_file(self,doc_path,user_id):
        doc_loader = TextLoader(doc_path)
        doc_files = self.text_splitter.split_documents(doc_loader.load())
        for doc_file in doc_files:
            doc_file.metadata["user_id"] = user_id
        return doc_files

    def get_context(self,user_id,query,top_k=5):
        if user_id not in self.user_stores:
            return []
        retriever = self.db.as_retriever(search_type="mmr",search_kwargs={'k': top_k, 'fetch_k': 20,'filter': {'user_id': user_id}})
        return retriever.invoke(query)
    
    def get_context_as_text(self,user_id,query,top_k=5):
        return "\n".join([x.page_content for x in self.get_context(user_id,query,top_k)])
    
if __name__ == "__main__":
    db_manager = vector_db_manager()
    db_manager.add_user_store("test",["./server/test.txt"])
    db_manager.add_user_store("test2",["./server/test2.txt"])
    print(db_manager.get_context("test","Who was isaac?"))
    print(db_manager.get_context_as_text("test2","Who was isaac?"))
    print("Done!")