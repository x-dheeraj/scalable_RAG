from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_qdrant import QdrantVectorStore


# Vector Embeddings
embedding_model = OllamaEmbeddings(
    model="bge-m3",
    base_url="http://localhost:11434",
)

llm = ChatOllama(
    model="qwen2.5:7b",
    base_url="http://localhost:11434",
)

# creating a connection to database
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="testing_rag",
    embedding=embedding_model,
)


def process_query(query: str):
    print("Searching Chunks", query)
    search_results = vector_db.similarity_search(query=query, k=5)

    context = "\n\n".join(
        [
            f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}"
            for result in search_results
        ]
    )

    system_prompt = f"""
  You are a helpful AI Assistant who answers users query based on the available context retrieved from a PDF file along with page_contents and page number.
  You should only answer the user based on the following context and navigate the user to open the right page number to know more.

  Context:
  {context}
"""

    response = llm.invoke([
        ("system", system_prompt),
        ("user", query),
    ])

    print(f"\n🤖: {response.content}")

    # Return the response so RQ saves it in the database
    return response.content

    



    