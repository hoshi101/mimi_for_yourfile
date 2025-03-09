from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter,TokenTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

class RAG:
    def __init__(self) -> None:
        # Use default values if environment variables are not set
        self.pdf_folder_path = os.environ.get('SOURCE_DATA', './source_data')
        self.emb_model_path = os.environ.get('EMBED_MODEL', 'BAAI/bge-base-en-v1.5')
        self.vector_store_path = os.environ.get('VECTOR_STORE', './vectorestore')
        
        # Print paths for debugging
        print(f"PDF folder path: {self.pdf_folder_path}")
        print(f"Embedding model: {self.emb_model_path}")
        print(f"Vector store path: {self.vector_store_path}")
        
        self.emb_model = self.get_embedding_model(self.emb_model_path)

    # without docker
    # def load_docs(self,path:str) -> PyPDFDirectoryLoader:
    #     loader = PyPDFDirectoryLoader(path)
    #     docs = loader.load()
    #     return docs

    def load_docs(self, path: str):
        documents = []
        
        # Load PDFs if any
        try:
            pdf_loader = PyPDFDirectoryLoader(path)
            pdf_docs = pdf_loader.load()
            documents.extend(pdf_docs)
            print(f"Loaded {len(pdf_docs)} PDF documents")
        except Exception as e:
            print(f"No PDF documents found or error loading PDFs: {e}")
        
        # Load text files
        try:
            for txt_file in glob.glob(os.path.join(path, "*.txt")):
                loader = TextLoader(txt_file)
                txt_docs = loader.load()
                documents.extend(txt_docs)
                print(f"Loaded text file: {txt_file}")
        except Exception as e:
            print(f"Error loading text files: {e}")
            
        return documents
    
    def get_embedding_model(self,emb_model) -> HuggingFaceBgeEmbeddings :
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity
        embeddings_model = HuggingFaceBgeEmbeddings(
            model_name=emb_model,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )
        return embeddings_model
    
    def split_docs(self,docs)-> TokenTextSplitter:
        text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=0)
        documents = text_splitter.split_documents(docs)
        return documents
    
    def populate_vector_db(self) -> None:
        # load embeddings into Chroma - need to pass docs , embedding function and path of the db

        self.doc = self.load_docs(self.pdf_folder_path)
        self.documents = self.split_docs(self.doc)
        
        db = Chroma.from_documents(self.documents,
                                   embedding=self.emb_model,
                                   persist_directory=self.vector_store_path)
        
        db.persist()
    
    def load_vector_db(self)-> Chroma:
        #to load back the embeddings from disk 
        db = Chroma(persist_directory=self.vector_store_path,embedding_function=self.emb_model)
        return db
    
    def get_retriever(self) -> Chroma:
        return self.load_vector_db().as_retriever()