from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import  TextLoader
import os
class vector_db_manager:
    def __init__(self,chunk_size=1000,chunk_overlap=150) -> None:
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
        self.embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2",model_kwargs={"device":"cuda"},encode_kwargs={"normalize_embeddings":False})
        self.user_stores = set()
        self.db = Chroma(embedding_function=self.embedding_function,collection_metadata={"hnsw:space":"cosine"})
    
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

    def get_context(self,user_id,query,top_k=5,max_cosine=0.6):
        if user_id not in self.user_stores:
            return []
        docs_with_distances = sorted(self.db.similarity_search_with_score(query,k=top_k,filter={'user_id': user_id}),key=lambda x: x[1],reverse=True)
        return [{"source":os.path.split(x[0].metadata["source"])[-1],"content":x[0].page_content} for x in docs_with_distances if x[1] < max_cosine]
    
    def delete_user_store(self,user_id):
        self.user_stores.remove(user_id)
        user_docs = self.db.get(where={'user_id': user_id})
        user_doc_ids = user_docs['ids']
        self.db.delete(user_doc_ids)

    def delete_user_file(self,user_id,doc_path):
        docs = self.db.get(
            where={
                'user_id': user_id,
                'source':doc_path
                })
        doc_ids = docs['ids']
        self.db.delete(doc_ids)
    
if __name__ == "__main__":
    db_manager = vector_db_manager()
    db_manager.add_user_store("test",["./server/test.txt"])
    db_manager.add_user_store("test2",["./server/test2.txt"])
    print(db_manager.get_context("test","Who was isaac?"))
    print("Done!")