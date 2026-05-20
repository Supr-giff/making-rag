# This is a guide to this project.

# 1-ingestion-pipeline.py file is to convert .txt files into embedding and storing into vectorDB.
Steps are mentioned below:\n
  i. checks the path and load the documents\n
  ii. chunks the documents\n
  iii. embedding model (HuggingFace-sentence-transformers/all-MiniLM-L6-v2)\n
  iv. creating a vectorDB (ChromaDB)\n\n

# 2-retrival-pipeline.py file to do the following things:\n
  i. load the vectorDB which is created in 1-ingestion-pipeline.py\n
  ii. input user query\n
  iii. retrives relevant chunks\n
  iv. use Ollama (llama3.2) LLM for text generation\n
  v. generates answer using relevant chunks.\n

# 3-multi-rag.py will be our main RAG system were we can input files with different types of extensions.\n
For example, .pdf files with images and tables, web site, videos, audios, etc.\n

## Until now I've implemented dependencies into it and it's still on progress.....
  
