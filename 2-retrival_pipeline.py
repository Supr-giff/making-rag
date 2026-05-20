from langchain_chroma import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_ollama import ChatOllama 
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

persist_directory = "database/chroma_db"

#loading embedding and vector database
embeddings = HuggingFaceEmbeddings(
	model_name="sentence-transformers/all-MiniLM-L6-v2")

db = Chroma(
	persist_directory=persist_directory,
	embedding_function=embeddings,
	collection_metadata={"hnsw:space": "cosine"}
	)

# Search for relevant documents
#userQuery = "When was Cristiano Ronaldo born and where?\n Full name of Ronaldo?"
#userQuery = "Who is Nikolas Tesla know for?"
#userQuery = "Are there any relation between Tesla Inc and Nikolas Tesla?"
#userQuery = "Provide me some early carrer about ronaldo."
userQuery = "Provide me information about Nikolas Tesla."

retriever = db.as_retriever(search_kwargs={"k":2})

relevant_docs = retriever.invoke(userQuery)

print(f"🟢📝🧑‍🎨User Query: {userQuery}")

#Displaying results
print("---📜 Context ---📜")
for i, doc in enumerate(relevant_docs, 1):
	print(f"🟢Chunk doucment {i}:\n{doc.page_content}\n")

print("⚡" * 50 )

combined_input = f"""Based on the following documents, please answer this question: {userQuery}

Documents:
{chr(10).join([f"- {doc.page_content}" for doc in relevant_docs])}

Please proide a clear, helpful answer using only the information from these documents. If you can't find the answer in the content say, I don't have relevant answer for this {userQuery}
"""

# Creating a Ollama LLM model
modelName = ChatOllama(
	model="llama3.2",
	temperature=0
	)

#Define the message for the model
messages = [
SystemMessage(content="Yor are a helpful assistant. Answer only using the provided documents."),
HumanMessage(content=combined_input),
]

#Invoke the model with the combined input
result = modelName.invoke(messages)

#Display the full result and content only
print("\n--- ✅🤖Generated Resposne ---")
print(f"🧑‍🎨{userQuery}❓")
print("📜Content only:")
print(f"➡️ {result.content}")
print("✅")
