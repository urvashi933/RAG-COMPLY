import os 
from utils.document_loader import load_document 
from utils.text_chunker import chunk_text 
from utils.embedding import get_embedding 
from utils.faiss_indexer import build_faiss_index
 
# Define which folders correspond to which sectors 
SECTORS = { 
    "legal": "data/legal", 
    "workforce": "data/workforce" 
} 
 
for sector, folder_path in SECTORS.items(): 
        print(f"\nIndexing Sector: {sector}") 
         
        embeddings = [] 
        metadatas = [] 
 
 
        for filename in os.listdir(folder_path): 
            file_path = os.path.join(folder_path, filename) 
            print(f"     Processing: {filename}...") 
 
            # 1. Load context 
            text = load_document(file_path) 
             
            # 2. Chunk text 
            chunks = chunk_text(text) 
 
            # 3. Embed & Metadata 
            for idx, chunk in enumerate(chunks): 
                embedding = get_embedding(chunk) 

                embeddings.append(embedding) 
                metadatas.append({ 
                    "sector":sector,
                    "document":filename,
                    "chunk_id":idx,
                    "source": f"File: {filename}, Chunk ID: {idx}",
                    "text": chunk
                })
        build_faiss_index(
            embeddings,
            metadatas,
            save_path=f"vector_store/{sector}_faiss"
            )

        print(f"✅{sector} indexing completed")