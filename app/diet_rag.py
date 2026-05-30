import pandas as pd
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

# Load Embedding Model

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Load Dataset

df = pd.read_csv(
    "data/cleaned_diet_data.csv"
)

# Create Semantic Documents

df["document"] = df.apply(

    lambda row: f"""
Goal: {row['goal']}
Condition: {row['condition']}
Diet Type: {row['diet_type']}
Foods: {row['foods']}
Avoid: {row['avoid']}
Hydration: {row['hydration']}
Meal Tip: {row['meal_tip']}
""",

    axis=1
)

# Generate Global Embeddings

documents = df["document"].tolist()

document_embeddings = embedding_model.encode(

    documents,

    convert_to_numpy=True
)

# Create Global FAISS Index

dimension = document_embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(document_embeddings)

# Structured Formatter

def format_result(row):

    return {

        "goal": row["goal"],

        "condition": row["condition"],

        "diet_type": row["diet_type"],

        "foods": row["foods"],

        "avoid": row["avoid"],

        "hydration": row["hydration"],

        "meal_tip": row["meal_tip"]
    }

# Semantic Ranking Helper

def semantic_rank(

    query,

    filtered_df,

    top_k=1
):

    filtered_documents = filtered_df[
        "document"
    ].tolist()

    filtered_embeddings = embedding_model.encode(

        filtered_documents,

        convert_to_numpy=True
    )

    temp_index = faiss.IndexFlatL2(

        filtered_embeddings.shape[1]
    )

    temp_index.add(filtered_embeddings)

    query_embedding = embedding_model.encode(

        [query],

        convert_to_numpy=True
    )

    distances, indices = temp_index.search(

        query_embedding,

        min(top_k, len(filtered_documents))
    )

    results = []

    seen = set()

    for i in indices[0]:

        row = filtered_df.iloc[i]

        structured_result = format_result(
            row
        )

        result_key = str(structured_result)

        if result_key not in seen:

            results.append(
                structured_result
            )

            seen.add(result_key)

    return results

# Full Structured Retrieval

def retrieve_diet_context(

    query,

    extracted,

    top_k=1
):

    # STEP 1:
    # FULL Exact Structured Filtering

    exact_df = df.copy()

    searchable_columns = [

        "goal",
        "condition",
        "diet_type",
        "foods",
        "avoid",
        "hydration",
        "meal_tip"
    ]

    applied_filters = 0

    for column in searchable_columns:

        value = extracted.get(column)

        if value:

            exact_df = exact_df[

                exact_df[column]

                .astype(str)

                .str.lower()

                == value.lower()
            ]

            applied_filters += 1

    # Exact Structured Match Found

    if not exact_df.empty:

        # ONLY ONE Exact Match

        if len(exact_df) == 1:

            return [

                format_result(
                    exact_df.iloc[0]
                )
            ]

        # Multiple Exact Matches
        # Use Semantic Ranking

        return semantic_rank(

            query=query,

            filtered_df=exact_df,

            top_k=top_k
        )

    # STEP 2:
    # Partial Structured Fallback

    fallback_df = df.copy()

    fallback_filters = 0

    for column in searchable_columns:

        value = extracted.get(column)

        if value:

            fallback_df = fallback_df[

                fallback_df[column]

                .astype(str)

                .str.lower()

                .str.contains(value.lower(), na=False)
            ]

            fallback_filters += 1

    if not fallback_df.empty:

        return semantic_rank(

            query=query,

            filtered_df=fallback_df,

            top_k=top_k
        )

    # STEP 3:
    # Global Semantic Fallback

    query_embedding = embedding_model.encode(

        [query],

        convert_to_numpy=True
    )

    distances, indices = index.search(

        query_embedding,

        top_k
    )

    results = []

    seen = set()

    for i in indices[0]:

        row = df.iloc[i]

        structured_result = format_result(
            row
        )

        result_key = str(structured_result)

        if result_key not in seen:

            results.append(
                structured_result
            )

            seen.add(result_key)

    return results