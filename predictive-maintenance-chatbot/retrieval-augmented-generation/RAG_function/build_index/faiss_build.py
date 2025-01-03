import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

class FAISS_build:
    def __init__(self):
        self.vector_store = None
        self.documents = None
        self.embeddings = None  # เก็บ Embedding ที่โหลดมา

    def load_embeddings(self, load_vectorStores_dir):
        # กำหนด directory สำหรับเก็บ model cache
        build_root_dir = os.path.dirname(os.path.dirname(load_vectorStores_dir))
        print(f"Build Root directory: {build_root_dir}")
        
        # ระบุโฟลเดอร์ MODELHUB_DIRECTOR
        MODELHUB_DIRECTOR = None
        for folder in os.listdir(build_root_dir):
            folder_path = os.path.join(build_root_dir, folder)
            if os.path.isdir(folder_path) and folder == "ModelHub":
                MODELHUB_DIRECTOR = folder_path
                print(f"ModelHub directory found: {folder_path}")
                break

        if not MODELHUB_DIRECTOR:
            raise FileNotFoundError("ModelHub directory not found in the root directory.")
        
        # ฟังก์ชันค้นหาโมเดลในโฟลเดอร์
        def find_model_path(base_dir):
            for root, dirs, files in os.walk(base_dir):
                # ตรวจสอบว่ามีไฟล์โมเดลหลัก (เช่น config.json) อยู่ใน snapshots
                if "config.json" in files and "model.safetensors" in files:
                    return root  # คืนค่าพาธของโมเดล
            return None

        # ค้นหาโมเดลแรกที่พบ
        MODEL_PATH = find_model_path(MODELHUB_DIRECTOR)
        if not MODEL_PATH:
            raise FileNotFoundError("No valid model found in ModelHub directory.")
        
        print("Models found:", MODEL_PATH)
                    
        # โหลด embeddings โดยใช้ HuggingFaceEmbeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=MODEL_PATH,  # ใช้พาธโมเดลที่พบ
            cache_folder=MODELHUB_DIRECTOR  # ยืนยันตำแหน่ง cache_folder
        )
        print("Embeddings loaded successfully.")
        
        # คืนค่า embeddings
        return self.embeddings

    def load_vector_store(self, load_vectorStores_dir):
        print(f"Directory exists: {load_vectorStores_dir}")
        # โหลด Embeddings
        embeddings = self.load_embeddings(load_vectorStores_dir)
        print("Embeddings are ready to use.")
        
        self.vector_store = FAISS.load_local(load_vectorStores_dir, embeddings, allow_dangerous_deserialization=True)
        print(f"Loaded vector store from {load_vectorStores_dir}")
        

    def vector_search(self, query, n=1):
        # ตรวจสอบว่า vector_store ถูกโหลดก่อนเรียก search
        if self.vector_store is None:
            raise ValueError("Vector store not loaded. Call load_vector_store() first.")
        
        # ค้นหาเอกสารที่ตรงกับ query ที่สุด
        doc_scores = self.vector_store.similarity_search_with_score(query, k=n)
        
        # สร้างผลลัพธ์พร้อมคะแนน (จัดการข้อมูลให้ JSON-friendly)
        results = []
        for rank, (res, score) in enumerate(doc_scores):
            # แปลงข้อมูลให้รองรับ JSON
            result = {
                "page_content": res.page_content,
                "distance_score": round(float(score), 9),
                # "distance_score": float(score),
                "rank": rank + 1,
                "metadata": res.metadata 
            }
            results.append(result)
        
        return results
    