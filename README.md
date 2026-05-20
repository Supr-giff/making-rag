# This is a guide to this project.

# 1-ingestion-pipeline.py file is to convert .txt files into embedding and storing into vectorDB.
Steps are mentioned below:
  i. checks the path and load the documents
  ii. chunks the documents
  iii. embedding model (HuggingFace-sentence-transformers/all-MiniLM-L6-v2)
  iv. creating a vectorDB (ChromaDB)

# 2-retrival-pipeline.py file to do the following things:
  i. load the vectorDB which is created in 1-ingestion-pipeline.py
  ii. input user query
  iii. retrives relevant chunks
  iv. use Ollama (llama3.2) LLM for text generation
  v. generates answer using relevant chunks.

# 3-multi-rag.py will be our main RAG system were we can input files with different types of extensions.
For example, .pdf files with images and tables, web site, videos, audios, etc.

## Until now I've implemented dependencies into it and it's still on progress.....
  
