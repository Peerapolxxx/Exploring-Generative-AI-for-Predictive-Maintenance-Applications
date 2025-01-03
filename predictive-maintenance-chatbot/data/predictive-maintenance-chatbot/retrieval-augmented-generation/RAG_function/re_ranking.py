import json
import os
import cohere
from tqdm import tqdm

# ตั้งค่าตัวแปรสภาพแวดล้อม COHERE_API_KEY
os.environ["COHERE_API_KEY"] = (
    "cSXFt2t90CiczNoUERMMTljkhKrWKHzW9QEv6Y5A"
)
# เริ่มต้นไคลเอนต์ Cohere ด้วยคีย์ API
co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))

def re_ranking(top_docs_rrf, query, top_k=3):
    """
    จัดอันดับเอกสารที่ดีที่สุดใหม่ตามความเกี่ยวข้องกับคำค้นหาโดยใช้โมเดล rerank ของ Cohere

    อาร์กิวเมนต์:
        top_docs_rrf (list): รายการเอกสารที่ดีที่สุดพร้อมเนื้อหาและข้อมูลเมตา
        query (str): สตริงคำค้นหาที่จะจัดอันดับเอกสาร
        top_k (int): จำนวนเอกสารที่ดีที่สุดที่จะส่งคืนหลังจากการจัดอันดับใหม่

    ส่งคืน:
        list: รายการเอกสารที่จัดอันดับใหม่พร้อมเนื้อหา คะแนนความคล้ายคลึง อันดับ และข้อมูลเมตา
    """
    # ดึงเนื้อหาของหน้าออกจากเอกสารที่ดีที่สุด
    docs = [docs["page_content"] for docs in top_docs_rrf]

    # ใช้โมเดล rerank ของ Cohere เพื่อจัดอันดับเอกสารใหม่ตามคำค้นหา
    response = co.rerank(
        model="rerank-v3.5",
        query=query,
        documents=docs,
        top_n=top_k,
    )
    
    results = []
    # วนซ้ำผ่านผลลัพธ์ที่จัดอันดับใหม่และสร้างผลลัพธ์
    for rank, res in enumerate(response.results):
        index = res.index
        result = {
            "page_content": top_docs_rrf[index]['page_content'],
            "similarity_score": round(float(res.relevance_score), 9),
            "rank": rank + 1,
            "metadata": top_docs_rrf[index]["metadata"]
        }
        results.append(result)
        
    return results
