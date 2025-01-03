import json
import os

import re
from rank_bm25 import BM25Okapi
import pickle  # Import the pickle module

def tokenization(text):
    """Tokenizes text by lowering case, removing unwanted characters, and splitting by spaces."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove unwanted characters
    return text.split()


def create_BM25Store(index_data, field, buildingBase_data_dir):
    
    # แปลงเอกสารจาก index_data เป็น Document
    documents = [
        {
            "page_content": data[field],
            "content_tokenizer": tokenization(data[field]),
            "metadata": {
                "doc_id": data["doc_id"],
                "original_uuid": data["original_uuid"],
                "corpus_source": data["corpus_source"],
                "chunk_id": data["chunk_id"],
                "chunk_uuid": data["chunk_uuid"],
                "original_index": data["original_index"],
                "content": data["content"],
                "contextualized_content": data["contextualized_content"]
            }
        }
        for data in index_data
    ]
    
    # สร้าง Tokenized corpus
    tokenized_corpus  = [item['content_tokenizer'] for item in documents] 
    
    # สร้าง BM25 Model
    BM25Model = BM25Okapi(tokenized_corpus)
    
    # ตั้งค่า directory สำหรับบันทึก BM25 Store
    field_to_dir = {
        "contextualized_content": os.path.join("bm25_index", "contextualized_index"),
        "content": os.path.join("bm25_index", "originalcontext_index"),
    }
    if field not in field_to_dir:
        raise ValueError(f"Unsupported field: {field}")

    save_BM25Store_dir = os.path.join(buildingBase_data_dir, field_to_dir[field])
    os.makedirs(save_BM25Store_dir, exist_ok=True)
    
    # บันทึก BM25Model 
    BM25Model_full_file_path = os.path.join(save_BM25Store_dir, "BM25Model.pkl")
    with open(BM25Model_full_file_path, 'wb') as f:
        pickle.dump(BM25Model, f)
    
    # บันทึก Document
    documents_full_file_path = os.path.join(save_BM25Store_dir, "documents.json")
    with open(documents_full_file_path, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=4)
    
    # บันทึก Tokenized corpus 
    tokenized_corpus_full_file_path = os.path.join(save_BM25Store_dir, "tokenized_corpus.json")
    with open(tokenized_corpus_full_file_path, "w", encoding="utf-8") as f:
        json.dump(tokenized_corpus, f, ensure_ascii=False, indent=4)
        
    print(f"Saved BM25 store Complete ✔️ - To: {save_BM25Store_dir}")

    return None


def create_BM25Indexing(index_data, buildingBase_data_dir):
    # สร้าง contextualized vector store
    field = "contextualized_content"
    contextualized_BM25Store = create_BM25Store(
        index_data, field, buildingBase_data_dir
    )

     # สร้าง original context vector store
    field = "content"
    originalcontext_BM25Store = create_BM25Store(
        index_data, field, buildingBase_data_dir
    )

    return None
