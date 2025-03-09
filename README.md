# "mimi" RAG LLM Application

A Retrieval-Augmented Generation (RAG) application built with FastAPI and Gradio that uses Large Language Models to answer questions based on your documents.

## Overview

This project implements a question-answering system that uses the RAG (Retrieval-Augmented Generation) approach to provide accurate answers based on your source documents. The application uses Mistral-7B as the language model and integrates with FastAPI for backend services and Gradio for the user interface.

## Architecture

The application follows this architecture:
1. **Document Processing**: Source documents are loaded, split into chunks, and embedded into a vector database
2. **Query Processing**: When a user asks a question, the system retrieves relevant document chunks
3. **Answer Generation**: The LLM generates an answer based on the retrieved context and the question
![diagram](https://github.com/user-attachments/assets/7c9eae5d-7b9f-477d-9573-d7602d19d5c9)
[Architecture diagram]

## Features

- Document processing for PDF and text files
- Vector database for efficient document retrieval
- FastAPI backend for API endpoints
- Gradio interface for user-friendly interaction
- Docker support for easy deployment

## Installation Dependencies

### Manual Installation (window)
1. Clone the repository:
   ```bash
   git clone https://github.com/hoshi101/mimi_for_yourfile.git
   cd mimi2_forurfile
    ```
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
    ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
    ```
4. Download the Mistral-7B model:
   
   ```bash
   # Download from Hugging Face (link in .txt file in model folder.)
   # Place the model file in the model/ directory
    ```
5. Run the application:
   ```bash
   python main.py
    ```

### Using Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/hoshi101/mimi_for_yourfile.git
   cd mimi2_forurfile

2. Download the Mistral-7B model:
   ```bash
    # Download from Hugging Face (link in .txt file in model folder.)
    # Place the model file in the model/ directory
    # The model file should be named: mistral-7b-instruct-v0.1.Q2_K.gguf

3. Place your source documents in the source_data/ directory:
    ```bash
    # Add PDF or text files containing information you want to query

4. Build and run the Docker container:
    ```bash
    docker-compose up --build
     ```
5. Access the application:
- Gradio UI: http://localhost:7860
- API endpoint: http://localhost:7860/docs


## Usage
### Adding Documents
Place your documents in the source_data/ directory. The system supports:

- PDF files
- Text files
When you add new documents, the vector database will be automatically rebuilt when you restart the application.

### Asking Questions
1. Open the Gradio interface at http://localhost:7860
2. Type your question in the input box
3. The system will retrieve relevant information from your documents and generate an answer

## Example Queries

![2025-03-09 02-59-26_2](https://github.com/user-attachments/assets/d4fbf9b0-7f4b-4fc5-a69b-a296430e80ea)

in Docker

![GIF2_01](https://github.com/user-attachments/assets/bf6fc4ad-ecd4-4636-9a10-eafb332f7d07)

[Example Queries and Responses edit by hoshi😊]
