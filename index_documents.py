import os 
from utils.document_loader import extract_text 
from utils.text_chunker import chunk_text 
from utils.embedding import get_embedding 
from utils.faiss_indexer import save_index 
 
# Define which folders correspond to which sectors 
SECTORS = { 
    "legal": "data/legal", 
    "workforce": "data/workforce" 
} 
 
def run_indexing(): 
    for sector, folder_path in SECTORS.items(): 
        print(f"        Logic Initialized for Sector: {sector}") 
         
        all_embeddings = [] 
        all_metadata = [] 
 
        if not os.path.exists(folder_path): 
            print(f"    Folder {folder_path} missing. Skipping...") 
            continue 
 
        for filename in os.listdir(folder_path): 
            file_path = os.path.join(folder_path, filename) 
            print(f"     Processing: {filename}...") 
 
            # 1. Load context 
            text = extract_text(file_path) 
             
            # 2. Chunk text 
            chunks = chunk_text(text) 
 
            # 3. Embed & Metadata 
            for i, chunk in enumerate(chunks): 
                embedding = get_embedding(chunk) 
                all_embeddings.append(embedding) 
                all_metadata.append({ 
                    "text": chunk, 
                    "source": filename, 
                    "sector": sector, 
                    "chunk_id": i 
                }) 
 
        # 4. Save to FAISS 
        if all_embeddings: 
            save_index(all_embeddings, all_metadata, f"vector_store/{sector}") 
            print(f"   Indexed {len(all_metadata)} chunks for {sector}.") 
 
if __name__ == "__main__": 
    run_indexing()