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
    response = predict_rag(prompt.prompt)
    return Response(response=response)

# Create Gradio interface
demo = gr.ChatInterface(
    fn=predict_rag,
    textbox=gr.Textbox(
        placeholder="Ask a question", container=False, lines=1, scale=8
    ),
    title="MIMI",
)

# Mount Gradio interface to FastAPI
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    # mounting at the root path
    host = os.environ.get("UVICORN_HOST", "0.0.0.0")
    port = int(os.environ.get("UVICORN_PORT", 7860))
    print(f"Starting server on {host}:{port}")
    uvicorn.run(
        app="main:app",
        host=host,
        port=port
    )

