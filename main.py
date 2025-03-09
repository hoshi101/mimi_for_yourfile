import uvicorn
import os
import gradio as gr
from utils.inference import predict_rag
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from utils.build_rag import RAG

load_dotenv()

# Initialize vector store if needed
vector_store_path = os.getenv('VECTOR_STORE')
if not os.path.exists(vector_store_path):
    print("Initializing vector store...")
    rag = RAG()
    rag.populate_vector_db()
    print("Vector store initialized!")

app = FastAPI()

class Request(BaseModel):
    prompt: str

class Response(BaseModel):
    response: str

@app.post("/", response_model=Response)
async def predict_api(prompt: Request):
    response = predict_rag(prompt.prompt)  # Fixed: use prompt.prompt
    return Response(response=response)  # Fixed: wrap response in Response model

# Create Gradio interface
demo = gr.ChatInterface(
    fn=predict_rag,
    textbox=gr.Textbox(
        placeholder="Ask a question", container=False, lines=1, scale=8
    ),
    title="LLM App",
)

# Mount Gradio interface to FastAPI
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    # mounting at the root path
    uvicorn.run(
        app="main:app",
        host=os.getenv("UVICORN_HOST"),  
        port=int(os.getenv("UVICORN_PORT"))
    )

