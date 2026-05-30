# Base JSON Rule

BASE_JSON_RULE = """

Always return ONLY valid JSON.

"""

# Format Chat History

def format_chat_history(chat_history):

    if not chat_history:

        return "No previous conversation."

    formatted_history = []

    for message in chat_history:

        if hasattr(message, "role") and hasattr(message, "content"):

            formatted_history.append(
                f"{message.role}: {message.content}"
            )

        elif isinstance(message, dict):

            formatted_history.append(
                f"{message.get('role')}: "
                f"{message.get('content')}"
            )

    return "\n".join(formatted_history)

# Format Exercise Context

def format_exercise_context(context):

    if not context:

        return "No exercise recommendations found."

    formatted = ""

    for item in context:

        formatted += f"""

Condition: {item['condition']}
Exercise: {item['exercise']}
Precaution: {item['precaution']}
Goal: {item['goal']}
Difficulty: {item['difficulty']}
Steps: {item['steps']}

"""

    return formatted

# Format Diet Context

def format_diet_context(context):

    if not context:

        return "No diet recommendations found."

    formatted = ""

    for item in context:

        formatted += f"""

Goal: {item['goal']}
Condition: {item['condition']}
Diet Type: {item['diet_type']}
Foods: {item['foods']}
Avoid: {item['avoid']}
Hydration: {item['hydration']}
Meal Tip: {item['meal_tip']}

"""

    return formatted

# Main Prompt Builder

def create_prompt(

    user_message,

    chat_history,

    retrieved_context,

    diet_context,

    intent
):

    formatted_history = format_chat_history(
        chat_history
    )

    formatted_exercise_context = format_exercise_context(
        retrieved_context
    )

    formatted_diet_context = format_diet_context(
        diet_context
    )

    # GENERAL PROMPT

    if intent == "general":

        return f"""

You are a friendly AI Fitness Assistant.

CURRENT USER MESSAGE:
{user_message}

PREVIOUS CONVERSATION:
{formatted_history}

RULES:

1. Respond naturally and conversationally.

2. Keep response under 25 words.

3. Do NOT generate:
   - exercise recommendations
   - diet recommendations
   - medical advice
   - safety guidance

4. Keep response friendly and concise.

{BASE_JSON_RULE}

JSON FORMAT:

{{
  "assistant_response": ""
}}

"""

    # EXERCISE PROMPT

    elif intent == "exercise":

        return f"""

You are an AI Fitness Assistant.

CURRENT USER MESSAGE:
{user_message}

PREVIOUS CONVERSATION:
{formatted_history}

RETRIEVED EXERCISE KNOWLEDGE:
{formatted_exercise_context}

RULES:

1. ONLY generate:
   - conversational acknowledgement
   - contextual introduction
   - safety guidance

2. Do NOT generate:
   - exercise names
   - steps
   - precautions
   - workout plans
   - routines

3. Never invent or replace exercise information.

4. The frontend already renders grounded exercise recommendations separately.

5. Keep response between 20-40 words.

6. Safety guidance should remain short and general.

7. NEVER ask questions of any kind.

7.1 NEVER request additional information.

7.2 NEVER continue the conversation.

7.3 ONLY provide:
   - acknowledgement
   - contextual introduction
   - safety guidance.

8. NEVER ask questions.

9. NEVER ask for additional information.

10. NEVER continue the conversation.

11. ONLY provide:
    - acknowledgement
    - short contextual introduction
    - safety guidance.

{BASE_JSON_RULE}

JSON FORMAT:

{{
  "assistant_response": "",
  "safety_guidance": ""
}}

"""

    # DIET PROMPT

    elif intent == "diet":

        return f"""

You are an AI Fitness Assistant.

CURRENT USER MESSAGE:
{user_message}

PREVIOUS CONVERSATION:
{formatted_history}

RETRIEVED DIET KNOWLEDGE:
{formatted_diet_context}

RULES:

1. ONLY generate:
   - conversational acknowledgement
   - contextual introduction
   - safety guidance

2. Do NOT generate:
   - food names
   - meal plans
   - diet schedules
   - nutrition strategies

3. Never invent or replace diet information.

4. The frontend already renders grounded diet recommendations separately.

5. Keep response between 20-40 words.

6. Safety guidance should remain short and general.

7. NEVER ask questions of any kind.

7.1 NEVER request additional information.

7.2 NEVER continue the conversation.

7.3 ONLY provide:
   - acknowledgement
   - contextual introduction
   - safety guidance.

8. NEVER ask questions.

9. NEVER ask for additional information.

10. NEVER continue the conversation.

11. ONLY provide:
    - acknowledgement
    - short contextual introduction
    - safety guidance.

{BASE_JSON_RULE}

JSON FORMAT:

{{
  "assistant_response": "",
  "safety_guidance": ""
}}

"""

    # BOTH PROMPT

    elif intent == "both":

        return f"""

You are an AI Fitness Assistant.

CURRENT USER MESSAGE:
{user_message}

PREVIOUS CONVERSATION:
{formatted_history}

RETRIEVED EXERCISE KNOWLEDGE:
{formatted_exercise_context}

RETRIEVED DIET KNOWLEDGE:
{formatted_diet_context}

RULES:

1. ONLY generate:
   - conversational acknowledgement
   - contextual introduction
   - safety guidance

2. Do NOT generate:
   - exercise names
   - food names
   - workout plans
   - meal plans
   - strategies
   - routines

3. Never invent or replace retrieved information.

4. The frontend already renders grounded recommendations separately.

5. Keep response between 20-40 words.

6. Safety guidance should remain short and general.

7. NEVER ask questions of any kind.

7.1 NEVER request additional information.

7.2 NEVER continue the conversation.

7.3 ONLY provide:
   - acknowledgement
   - contextual introduction
   - safety guidance.

8. NEVER ask questions.

9. NEVER ask for additional information.

10. NEVER continue the conversation.

11. ONLY provide:
    - acknowledgement
    - short contextual introduction
    - safety guidance.

{BASE_JSON_RULE}

JSON FORMAT:

{{
  "assistant_response": "",
  "safety_guidance": ""
}}

"""

    # Fallback Prompt

    return f"""

You are an AI Fitness Assistant.

{BASE_JSON_RULE}

JSON FORMAT:

{{
  "assistant_response": "Unable to process request."
}}

"""