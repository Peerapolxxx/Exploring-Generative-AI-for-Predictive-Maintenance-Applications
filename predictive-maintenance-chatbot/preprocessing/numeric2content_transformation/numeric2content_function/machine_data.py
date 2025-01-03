import pandas as pd
import re


def create_machine_data_text(plant_row, machine_row):
    """สร้างข้อความสำหรับ machine_data"""
    fields = {
        "machine_name": (
            f"The {machine_row['MACHINE_NAME']}"
            if pd.notnull(machine_row["MACHINE_NAME"])
            else "Unknown machine"
        ),
        "machine_tag": (
            f"(Tag: {machine_row['MACHINE_TAG']})"
            if pd.notnull(machine_row["MACHINE_TAG"])
            else "(Tag: Unknown)"
        ),
        "plant_name": (
            f"in the {plant_row['PLANT_NAME']}"
            if pd.notnull(plant_row["PLANT_NAME"])
            else "in Unknown plant"
        ),
        "running_status": (
            f"is currently {machine_row['RUNNING_STATUS']}."
            if pd.notnull(machine_row["RUNNING_STATUS"])
            else ""
        ),
        "status_sensor": (
            f"It is monitored by the associated sensor {machine_row['STATUS_SENSOR']},"
            if pd.notnull(machine_row["STATUS_SENSOR"])
            else ""
        ),
        "stop_threshold": (
            f"with a stop threshold set at {machine_row['STOP_IF_LOWER_THAN']}."
            if pd.notnull(machine_row["STOP_IF_LOWER_THAN"])
            else ""
        ),
        "component_count": (
            f"The machine consists of {machine_row['COMPONENT_COUNT']} components and"
            if pd.notnull(machine_row["COMPONENT_COUNT"])
            else ""
        ),
        "model_count": (
            f"{machine_row['MODEL_COUNT']} models."
            if pd.notnull(machine_row["MODEL_COUNT"])
            else ""
        ),
        "description": (
            f"The description is as follows: {machine_row['DESCRIPTION']}."
            if pd.notnull(machine_row["DESCRIPTION"])
            else ""
        ),
    }

    keys_to_join = [
        "machine_name",
        "machine_tag",
        "plant_name",
        "running_status",
        "status_sensor",
        "stop_threshold",
        "component_count",
        "model_count",
        "description",
    ]

    machines_data_text = " ".join(
        [fields[key] for key in keys_to_join if key in fields]
    )
    machines_data_text = re.sub(r"\s+", " ", machines_data_text).strip()
    # machines_data_text = "[Chunk]" + machines_data_text + "[/Chunk]"
    machines_data_text = "* " + machines_data_text
    return machines_data_text


def machine2content(plant_row, machine_row):

    title = "[Section]MACHINE DATA[Section]\n"
    machines_data_text = create_machine_data_text(plant_row, machine_row)
    machines_data_text = title + machines_data_text

    return machines_data_text
