import json
import os
import uuid

import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings


def create_vectorStore(index_data, field, embeddings, buildingBase_data_dir):
    # ตรวจสอบและตั้งค่าขนาดเวกเตอร์
    vector_dim = len(embeddings.embed_query("hello world"))
    index = faiss.IndexFlatL2(vector_dim)
    docstore = InMemoryDocstore()

    # สร้าง Vector Store
    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=docstore,
        index_to_docstore_id={},
    )

    # แปลงเอกสารจาก index_data เป็น Document
    documents = [
        Document(page_content=item[field], metadata=item) for item in index_data
    ]
    uuids = [item["chunk_uuid"] for item in index_data]
    vector_store.add_documents(documents=documents, ids=uuids)

    # ตั้งค่า directory สำหรับบันทึก Vector Store
    field_to_dir = {
        "contextualized_content": os.path.join("faiss_index", "contextualized_index"),
        "content": os.path.join("faiss_index", "originalcontext_index"),
    }
    if field not in field_to_dir:
        raise ValueError(f"Unsupported field: {field}")

    save_vectorStore_dir = os.path.join(buildingBase_data_dir, field_to_dir[field])
    os.makedirs(save_vectorStore_dir, exist_ok=True)
    vector_store.save_local(save_vectorStore_dir)
    print(f"Saved vector store Complete ✔️ - To: {save_vectorStore_dir}")

    return vector_store

def load_embeddings(model_name, buildingBase_data_dir):
    # กำหนด directory สำหรับเก็บ model cache
    MODELHUB = "ModelHub"
    MODELHUB_DIRECTOR = os.path.join(buildingBase_data_dir, MODELHUB)
    os.makedirs(MODELHUB_DIRECTOR, exist_ok=True)
    
    # โหลด embeddings โดยใช้ HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,  
        cache_folder=MODELHUB_DIRECTOR  
    )
    return embeddings

def create_FaissIndexing(index_data, model_name, buildingBase_data_dir):
    
    embeddings = load_embeddings(model_name, buildingBase_data_dir)
    
    # สร้าง contextualized vector store
    field = "contextualized_content"
    contextualized_vectorStore = create_vectorStore(
        index_data, field, embeddings, buildingBase_data_dir
    )

    # สร้าง original context vector store
    field = "content"
    originalcontext_vectorStore = create_vectorStore(
        index_data, field, embeddings, buildingBase_data_dir
    )

    return None
