from utils.llm import LLM
from utils.build_rag import RAG
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import RetrievalQA

def predict_rag(qns: str, history=None) -> str:
    llm = LLM().get_llm_together()
    retriever = RAG().get_retriever()
    
    # Improved prompt template with better instructions
    template = """You are a helpful AI assistant. Answer the question based on the provided context.
    If the context doesn't contain relevant information, say "I don't have enough information about that topic."
    
    Context:
    {context}
    
    Question: {question}
    
    Answer: """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Set up the retrieval chain
    retrieval_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # For debugging
    # docs = retriever.get_relevant_documents(qns)
    # print(f"Retrieved {len(docs)} documents")
    # for i, doc in enumerate(docs):
    #     print(f"Document {i+1}: {doc.page_content[:100]}...")
    
    result = retrieval_chain.invoke(qns)
    return result