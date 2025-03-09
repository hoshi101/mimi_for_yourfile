from utils.build_rag import RAG
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    # Clear existing vector store if it exists
    vector_store_path = os.getenv('VECTOR_STORE')
    if os.path.exists(vector_store_path):
        print(f"Removing existing vector store at {vector_store_path}")
        shutil.rmtree(vector_store_path)
    
    # Create and populate new vector store
    print("Creating new vector store...")
    rag = RAG()
    rag.populate_vector_db()
    print("Vector store created successfully!")