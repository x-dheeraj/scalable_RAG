# This file is responsible for indexing the data
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings



pdf_path = Path(__file__).parent / "cpumemory.pdf"

# loding the above file in python program
loader = PyPDFLoader(file_path=pdf_path) # loads the pdf
docs = loader.load() # here every page is a doc

# print(docs[10]) # testing the docs ---> prints the content of that particular page

# Chunking ---> text splitters

# Split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 400
)

chunks = text_splitter.split_documents(documents=docs)


# creating Vector Embeddings for the above (chunks)  -----> using bge-m3 throuh ollama

embedding_model= OllamaEmbeddings(
    model="bge-m3",
    base_url="http://localhost:11434"

)

# now the embedding model needs to create chunks and store it in the database

# storing the embeddings in the qdrant database
vector_store = QdrantVectorStore.from_documents(
    documents = chunks,
    embedding = embedding_model,
    url = "http://localhost:6333",
    collection_name = "testing_rag"
)

print("Indexing of documents done...")
