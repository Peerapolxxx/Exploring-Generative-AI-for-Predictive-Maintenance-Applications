# %load_ext autoreload
# %autoreload 2
import os
import pandas as pd
import json
import re
import uuid
from tqdm import tqdm

from contextEnrichment_function.gpt_contextualized import gpt_batch_process
from contextEnrichment_function.anthropic_contextualized import anthropic_batch_process

def pipeline_contextEnrichment(prepared_data_dir):

    # อ่านรายการโรงงานจากไฟล์ CSV
    file_name = "plant_list.csv"
    plant_list_file = os.path.join(prepared_data_dir, file_name)
    if os.path.isfile(plant_list_file):
        plant_df = pd.read_csv(plant_list_file)
        plant_df = plant_df[1:2]

    else:
        print(f":: Failed ❌")
        print(f"File not found: {plant_list_file}")
        return  # ออกจากฟังก์ชันถ้าไม่พบไฟล์

    # วนลูปผ่านแต่ละโรงงาน
    for _, plant_row in plant_df.iterrows():
        plant_tag = plant_row["PLANT_TAG"]
        plant_name = plant_row["PLANT_NAME"]

        # อ่านรายการเครื่องจักรของแต่ละโรงงาน
        file_name = "machine_list.csv"
        machine_list_file = os.path.join(prepared_data_dir, plant_tag, file_name)
        if os.path.isfile(machine_list_file):
            machine_df = pd.read_csv(machine_list_file)
            machine_df = machine_df.iloc[-1:]
        else:
            print(f":: Failed ❌")
            print(f"File not found: {machine_list_file}")
            break

        # วนลูปผ่านแต่ละเครื่องจักร
        for idx, machine_row in machine_df.iterrows():
            machine_tag = machine_row["MACHINE_TAG"]
            machine_name = machine_row["MACHINE_NAME"]
            print("\n" + "=" * 100)
            print(
                f"#{idx+1} Processing data for {plant_name} (TAG: {plant_tag}) - {machine_name} (TAG: {machine_tag})"
            )
            print("=" * 100)

            # เพิ่มบริบทให้กับเนื้อหาชิ้นต่างๆ
            file_name = f"{plant_tag}_{machine_tag}_chunks.json"
            print(f"\n>> Add contextualization to chunk content - File: {file_name}")
            chunks_file = os.path.join(
                prepared_data_dir, plant_tag, machine_tag, file_name
            )
            if os.path.isfile(chunks_file):

                # Read the JSON file
                with open(chunks_file, "r", encoding="utf-8") as file:
                    chunks_data = json.load(file)
                    print(f":: Read the Chunks data JSON Complete ✔️ - Path: {chunks_file}")

                # เรียกใช้งานฟังก์ชั่นเพื่อใช้ anthropic AI ในการสร้างบริบท
                contextualized_data = anthropic_batch_process(chunks_data)

                # เขียนข้อมูลที่ประมวลผลแล้วกลับลงไฟล์
                contextualized_full_file_path = chunks_file.replace(
                    ".json", "_contextualized.json"
                )
                with open(contextualized_full_file_path, "w", encoding="utf-8") as file:
                    json.dump(contextualized_data, file, ensure_ascii=False, indent=2)
                print(f":: Writing processed data Complete ✔️")

            else:
                print(f":: Failed ❌")
                print(f"File not found: {chunks_file}")

            print("=" * 100)
            print("Complete all Process")
            print("=" * 100)
   
   
            
# กำหนด root directory หลักของโปรเจค
ROOT_DIRECTORY = "D:\Data_sci_internship\Exploring Generative AI for Predictive Maintenance Applications"

# กำหนดชื่อโฟลเดอร์ย่อยต่างๆ
PROJECT_DIRECTORY = "predictive-maintenance-chatbot"    # โฟลเดอร์โปรเจค
DATA_ROOT_DIRECTORY = "data"                            # โฟลเดอร์หลักสำหรับเก็บข้อมูล
PREPARED_DATA_DIRECTORY = "prepared_data"               # โฟลเดอร์สำหรับข้อมูลที่ประมวลผลแล้ว

# สร้าง path เต็มสำหรับโฟลเดอร์ข้อมูลที่ประมวลผลแล้ว
prepared_data_dir = os.path.join(
    ROOT_DIRECTORY, PROJECT_DIRECTORY, DATA_ROOT_DIRECTORY, PREPARED_DATA_DIRECTORY
)

# Call the pipeline_numeric2text function
pipeline_contextEnrichment(prepared_data_dir)