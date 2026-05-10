def create_prompt(user_query, retrieved_context):
    
    context = "\n".join(retrieved_context)

    prompt = f"""
You are an AI fitness coach.

User Query:
{user_query}

Relevant Fitness Knowledge:
{context}

Your task:
1. Understand the user's fitness need or health condition.
2. Suggest safe exercises.
3. Mention precautions.
4. Keep response beginner-friendly.

Return response ONLY in JSON format like this:

{{
    "condition": "...",
    "recommended_exercises": [
        "...",
        "..."
    ],
    "precautions": [
        "...",
        "..."
    ],
    "fitness_plan": "..."
}}
"""

    return prompt