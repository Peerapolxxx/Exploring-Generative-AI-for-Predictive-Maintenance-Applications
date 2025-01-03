import os
import uuid
import pandas as pd
import json


def merge_json_files(prepared_data_dir, input_files, buildingBase_data_dir):
    merged_data = []

    # อ่านรายการโรงงานจากไฟล์ CSV
    file_name = "plant_list.csv"
    plant_list_file = os.path.join(prepared_data_dir, file_name)
    if os.path.isfile(plant_list_file):
        plant_df = pd.read_csv(plant_list_file)

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
        else:
            print(f":: Failed ❌")
            print(f"File not found: {machine_list_file}")
            break

        # วนลูปผ่านแต่ละเครื่องจักร
        for idx, machine_row in machine_df.iterrows():
            machine_tag = machine_row["MACHINE_TAG"]
            machine_name = machine_row["MACHINE_NAME"]

            # ค้นหาไฟล์ JSON ที่เกี่ยวข้อง
            machine_dir = os.path.join(prepared_data_dir, plant_tag, machine_tag)
            for file_name in os.listdir(machine_dir):
                if file_name in input_files and file_name.endswith(".json"):
                    json_file_path = os.path.join(machine_dir, file_name)
                    with open(json_file_path, "r", encoding="utf-8") as f:
                        try:
                            data = json.load(f)
                            if isinstance(data, list):
                                merged_data.extend(data)
                            elif isinstance(data, dict):
                                merged_data.append(data)
                            else:
                                print(
                                    f"File : The file {file_name} does not contain any supported JSON data (list or dict)."
                                )
                        except json.JSONDecodeError:
                            print(f"The file {file_name} cannot be read as JSON.")

    # บันทึกข้อมูลรวมลงไฟล์ใหม่

    file_name = f"merged.json"
    save_to_dir = os.path.join(buildingBase_data_dir)
    os.makedirs(save_to_dir, exist_ok=True)

    output_file = os.path.join(save_to_dir, file_name)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)

    print(f"Save the Merged data JSON Complete ✔️ - Path: {output_file}")

    return merged_data


# ฟังก์ชันสร้าง chunk_uuid จาก chunk_id
def generate_chunk_uuid(chunk_id):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk_id))


# ฟังก์ชันแปลงโครงสร้างข้อมูล JSON
def transform_json(data, buildingBase_data_dir):
    index_data = []

    for item in data:
        doc_id = item.get("doc_id")
        original_uuid = item.get("original_uuid")
        corpus_source = item.get("corpus_source")

        for chunk in item.get("chunks", []):
            transformed_item = {
                "doc_id": doc_id,
                "original_uuid": original_uuid,
                "corpus_source": corpus_source,
                "chunk_id": chunk.get("chunk_id"),
                "chunk_uuid": generate_chunk_uuid(chunk.get("chunk_id")),
                "original_index": chunk.get("original_index"),
                "content": chunk.get("content"),
                "contextualized_content": chunk.get("contextualized_content"),
            }
            index_data.append(transformed_item)

    # บันทึกข้อมูลรวมลงไฟล์ใหม่

    file_name = f"index_data.json"
    save_to_dir = os.path.join(buildingBase_data_dir)
    os.makedirs(save_to_dir, exist_ok=True)

    output_file = os.path.join(save_to_dir, file_name)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=4)
    print(f"Save the Index data JSON Complete ✔️ - Path: {output_file}")

    return index_data


def create_indexingData(prepared_data_dir, input_files, buildingBase_data_dir):

    merge_json_data = merge_json_files(
        prepared_data_dir, input_files, buildingBase_data_dir
    )
    index_data = transform_json(merge_json_data, buildingBase_data_dir)
    return index_data
