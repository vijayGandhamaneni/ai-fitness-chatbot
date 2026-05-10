from app.rag import retrieve_context

query = "I have leg joint pain"

results = retrieve_context(query)

print("RESULTS:")
print(results)
print(type(results))