# Query Classifier

def classify_query(message):
    
    message = message.lower()

    greetings = [
        "hi",
        "hello",
        "hey",
        "thanks",
        "thank you",
        "good morning",
        "good evening"
    ]

    if any(message.startswith(greet) for greet in greetings):
        return "general"

    exercise_keywords = [
        "exercise",
        "exercises",
        "workout",
        "workouts",
        "stretch",
        "stretching",
        "training",
        "gym",
        "mobility",
        "flexibility",
        "rehabilitation",
        "pain relief"
    ]

    diet_keywords = [
        "diet",
        "food",
        "foods",
        "meal",
        "meals",
        "nutrition",
        "eat",
        "eating",
        "protein",
        "calories"
    ]

    exercise_detected = any(
        keyword in message
        for keyword in exercise_keywords
    )

    diet_detected = any(
        keyword in message
        for keyword in diet_keywords
    )

    if exercise_detected and diet_detected:
        return "both"

    elif exercise_detected:
        return "exercise"

    elif diet_detected:
        return "diet"

    return "general"
