import pandas as pd
import re


def create_component_list_text(plant_row, machine_row, component_list_df):
    """สร้างข้อความสำหรับรายชื่อส่วนประกอบของเครื่องจักร"""
    component_names = ", ".join(component_list_df["COMPONENT_NAME"].dropna())
    component_list_text = f"The {machine_row['MACHINE_NAME']} (Tag: {machine_row['MACHINE_TAG']}) in the {plant_row['PLANT_NAME']} consists of the following components: {component_names}"
    # component_list_text = "[Chunk]" + component_list_text + "[/Chunk]"
    component_list_text = "* " + component_list_text

    return component_list_text


def componentList2content(plant_row, machine_row, component_list_df):

    title = "[Section]COMPONENT LIST[Section]\n"
    component_list_text = create_component_list_text(
        plant_row, machine_row, component_list_df
    )
    component_list_text = title + component_list_text

    return component_list_text
