import pandas as pd
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load CSV data
df = pd.read_csv("data/fitness_data.csv")

# Convert rows into documents
documents = df.apply(
    lambda row: f"""
    Condition: {row['condition']}
    Exercise: {row['exercise']}
    Precaution: {row['precaution']}
    """,
    axis=1
).tolist()

# Create embeddings
document_embeddings = embedding_model.encode(documents)

# Convert to numpy array
document_embeddings = np.array(document_embeddings)

# Create FAISS index
dimension = document_embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

# Add embeddings into FAISS
index.add(document_embeddings)


# Retrieval function
def retrieve_context(user_query, top_k=2):

    # Convert query into embedding
    query_embedding = embedding_model.encode([user_query])

    query_embedding = np.array(query_embedding)

    # Search similar vectors
    distances, indices = index.search(query_embedding, top_k)

    # Retrieve matching docs
    results = [documents[i] for i in indices[0]]

    return results