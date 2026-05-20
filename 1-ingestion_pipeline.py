import os 
from langchain_community.document_loaders import TextLoader, DirectoryLoader, PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
#from langchain_openai import OpenAIEmbeddings -- need subscription for api key
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma 
from dotenv import load_dotenv


load_dotenv()

# 1️⃣ Check the folder and file exists. Then load the files. 
def load_documents(docs_path="docs"):
	"""Load all text files from the docs directory"""
	
	#Check if docs directory exists
	if not os.path.exists(docs_path):
		raise FileNotFoundError(f"The directory {docs_path} does not exists. Please create a folder and import some files.")

	#load all .txt files from the docs directory
	txt_loader = DirectoryLoader(
		docs_path,
		glob="**/*.txt",
		loader_cls=TextLoader,
		loader_kwargs={"encoding": "utf-8"}
	)

	# load all .pdf files from the directory
	pdf_loader = DirectoryLoader(
		docs_path,
		glob="**/*.pdf",
		loader_cls=PyPDFLoader
	) 

	txt_docs = txt_loader.load()
	pdf_docs = pdf_loader.load()

	documents = txt_docs + pdf_docs

	print(f"Documnts loaded form {docs_path} ✅")

	if len(documents) == 0:
		raise FileNotFoundError(f"No .txt files found in {docs_path}. Please add txt file in docs folder.")

	for i, doc in enumerate(documents[:2]): #Show first 2 documents
		print(f"\nDocument {i+1} loaded:")
		print(f" Source: {doc.metadata['source']}")
		print(f" Content length: {len(doc.page_content)} characters")
		print(f" Content preview: {doc.page_content[:100]}...")
		print(f" Metadata: {doc.metadata}")

	return documents
    
# 2️⃣ Text Chuncking using CharacterTextSplitter method
def split_documents(documents, chunk_size=800, chunk_overlap=0):
	"""Split documents into smaller chunks with overpal"""
	print("*" * 50)
	print("🪓Splitting documents into chunks...🪓")

	text_splitter = CharacterTextSplitter(
		chunk_size=chunk_size,
		chunk_overlap=chunk_overlap
		)

	chunks = text_splitter.split_documents(documents)

	if chunks:

		for i, chunk in enumerate(chunks[:5]):
			print(f"\n--- Chunk {i+1} ---")
			print(f"Source: {chunk.metadata['source']}")
			print(f"Length: {len(chunk.page_content)} characters")
			print(f"Content:")
			print(chunk.page_content)
			print("=" * 50)

		if len(chunks) > 5:
			print(f"\n... and {len(chunks) - 5} more chunks")

	return chunks

# 3️⃣ Implementing "model_name" for embedding vector and storing into a vector database

def create_vector_store(chunks, persist_directory="database/chroma_db"):
	"""Create and presist ChromaDB vector store"""
	print("Creating embedding and storing in ChromaDB...")

	embedding_model = HuggingFaceEmbeddings(
		model_name="sentence-transformers/all-MiniLM-L6-v2",
		#modelnane="BAAI/bge-small-en-v1.5",
		model_kwargs={"device": "cpu"},
		encode_kwargs={"normalize_embeddings": True})

	#create chromaDB vector store
	print("--- 🐢Creating vector store --- 🐢")
	vectorStore = Chroma.from_documents(
		documents=chunks,
		embedding=embedding_model,
		persist_directory=persist_directory,
		collection_metadata={"hnsw:space": "cosine"} #algorithm to compare chunks and retrieve 
		)

	print("--- Finished creating vector storage/ VectorDB ✅⚡")
	print(f"--- Vector store created and saved to {persist_directory}✅😎")

	return vectorStore

def main():
	print("Hello Main function!😊")

	# inside this main function, we will write sub-function:
	# 1. to load files
	#2. Chunk the files
	#3. embedding and storing

	#1. loading the files
	documents = load_documents(docs_path="docs")

	#2. chunck the files
	chunks = split_documents(documents)

	#3. Embedding and storing
	vectorStore = create_vector_store(chunks)

if __name__ == "__main__":
	main()