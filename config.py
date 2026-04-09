import os
# Get your key from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
# AI Model Configuration
EMBEDDING_MODEL = "text-embedding-004" # High accuracy embedding
GENERATIVE_MODEL = "gemini-2.0-flash" # Fast and smart generation
# Processing Config
CHUNK_SIZE = 600 # Words per block
CHUNKS_TO_RETRIEVE = 4 # Number of sources to show
# Storage
VECTOR_STORE_PATH = "vector_store"
DB_PATH = "sqlite:///data/incubator.db"