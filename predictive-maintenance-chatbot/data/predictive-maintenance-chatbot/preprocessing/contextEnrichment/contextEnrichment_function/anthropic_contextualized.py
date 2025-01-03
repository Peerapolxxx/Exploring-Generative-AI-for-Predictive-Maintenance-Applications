import os
import anthropic
from tqdm import tqdm
# from tenacity import retry, stop_after_attempt, wait_exponential
from contextEnrichment_function.prompts import (
    CHUNK_CONTEXT_PROMPT,
    DOCUMENT_CONTEXT_PROMPT,
)

os.environ["ANTHROPIC_API_KEY"] = (
    "Enter your key"
)
api_key = os.getenv("ANTHROPIC_API_KEY")

anthropicAi = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)


def anthropic_generate_context(doc, chunk):
    try:
        response = anthropicAi.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            temperature=0.0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": DOCUMENT_CONTEXT_PROMPT.format(doc_content=doc),
                        },
                        {
                            "type": "text",
                            "text": CHUNK_CONTEXT_PROMPT.format(chunk_content=chunk),
                        },
                    ],
                }
            ],
        )
        return response
    except Exception as e:
        print(f"\nError in API call: {str(e)}")
        raise


def anthropic_batch_process(chunks_data):
    """
    ประมวลผลข้อมูล chunks โดยใช้เนื้อหาจากไฟล์ corpus และสร้างเนื้อหาที่มีบริบทเพิ่มเติม
    Parameters:
    chunks_data (list): รายการของข้อมูล chunks แต่ละรายการเป็น dictionary ที่มีคีย์:
        - "chunks" (list): รายการของ chunks แต่ละ chunk เป็น dictionary ที่มีคีย์ "content"
        - "corpus_source" (str): เส้นทางของไฟล์ corpus ที่จะใช้ในการสร้างบริบท
    Returns:
    list: ข้อมูล chunks ที่มีการเพิ่มเนื้อหาที่มีบริบทเพิ่มเติมในคีย์ "contextualized_content"
    หรือ None ถ้าไม่พบไฟล์ corpus
    """

    for data in chunks_data:
        chunks = data["chunks"]
        corpus_source_file = data["corpus_source"]

        if os.path.isfile(corpus_source_file):
            with open(corpus_source_file, "r") as file:
                corpus_content = file.read()
            print(f":: Read the Corpus source Complete ✔️ - Path: {corpus_source_file}")
        else:
            print(f":: Failed ❌ - File not found: {corpus_source_file}")
            return None  # หยุดการทำงานของฟังก์ชัน

        for chunk in tqdm(chunks, total=len(chunks), desc=":: Processing chunks"):
            chunk_content = chunk["content"]
            # print(f"###corpus_content\n{corpus_content}")
            # print(f"###chunk_content\n{chunk_content}")
            # print("-"*100)
            contextualized = anthropic_generate_context(corpus_content, chunk_content)
            chunk["contextualized_content"] = "\n\n".join(
                [contextualized.content[0].text, chunk_content]
            )

    return chunks_data
