import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from google import genai

load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME", "code-debugger-memory")

if not pinecone_api_key:
    raise ValueError("Missing PINECONE_API_KEY in .env")

if not gemini_api_key:
    raise ValueError("Missing GEMINI_API_KEY in .env")

# First get the real embedding dimension from Gemini so the Pinecone index matches it.
client = genai.Client(api_key=gemini_api_key)
embedding_response = client.models.embed_content(
    model="gemini-embedding-001",
    contents="test embedding for code debugger"
)

dimension = len(embedding_response.embeddings[0].values)
print(f"Detected Gemini embedding dimension: {dimension}")

pc = Pinecone(api_key=pinecone_api_key)

existing = [index["name"] for index in pc.list_indexes()]
if index_name in existing:
    print(f"Index '{index_name}' already exists.")
else:
    pc.create_index(
        name=index_name,
        vector_type="dense",
        dimension=dimension,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ),
        deletion_protection="disabled"
    )
    print(f"Created Pinecone index: {index_name}")
