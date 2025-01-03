import pandas as pd
import re


def create_all_component_health_text(plant_row, machine_row, all_components_health_df):
    """สร้างข้อความแสดงข้อมูลสุขภาพของส่วนประกอบ"""
    # ตรวจสอบว่า DataFrame ว่างหรือไม่
    if all_components_health_df.empty:
        return "No all components health data available."

    # สร้างลิสต์เก็บข้อความของแต่ละแถว
    all_component_health_data_text_list = []

    # วนลูปผ่านทุกแถวใน DataFrame
    for _, components_health_row in all_components_health_df.iterrows():
        fields = {
            "component_name": (
                f"The {components_health_row['COMPONENT_NAME']} component"
                if pd.notnull(components_health_row["COMPONENT_NAME"])
                else "Unknown component"
            ),
            "machine_name": (
                f"of {machine_row['MACHINE_NAME']}"
                if pd.notnull(machine_row["MACHINE_NAME"])
                else "Unknown machine"
            ),
            "machine_tag": (
                f"(Tag: {machine_row['MACHINE_TAG']})"
                if pd.notnull(machine_row["MACHINE_TAG"])
                else "(Tag: Unknown)"
            ),
            "plant_name": (
                f"in the {plant_row['PLANT_NAME']} has a"
                if pd.notnull(plant_row["PLANT_NAME"])
                else "Unknown plant has a"
            ),
            "performance_health": (
                f"Performance Health of {components_health_row['PERFORMANCE_HEALTH']}% and"
                if pd.notnull(components_health_row["PERFORMANCE_HEALTH"])
                else ""
            ),
            # 'condition_health': f"Condition Health: {components_health_row['CONDITION_HEALTH']}%." if pd.notnull(components_health_row['CONDITION_HEALTH']) else "Condition Health: N/A.",
            "condition_health": (
                f"Condition Health of {components_health_row['CONDITION_HEALTH']}%."
                if pd.notnull(components_health_row["CONDITION_HEALTH"])
                else ""
            ),
            # 'timestamp': (
            #    f"At the time {components_health_row['TimeStamp']}."
            #    if pd.notnull(components_health_row['TimeStamp'])
            #    else ""
            # ),
        }

        if (
            pd.notnull(components_health_row["PERFORMANCE_DIFF_DAY"])
            and pd.notnull(components_health_row["PERFORMANCE_DIFF_WEEK"])
            and pd.notnull(components_health_row["PERFORMANCE_DIFF_MONTH"])
        ):
            performance_changes_daily = (
                f"{components_health_row['PERFORMANCE_DIFF_DAY']}"
            )
            performance_changes_weekly = (
                f"{components_health_row['PERFORMANCE_DIFF_WEEK']}"
            )
            performance_Changes_monthly = (
                f"{components_health_row['PERFORMANCE_DIFF_MONTH']}"
            )

            fields["performance_changes"] = (
                f"The Performance changes are {performance_changes_daily}% daily, {performance_changes_weekly}% weekly, and {performance_Changes_monthly}% monthly."
            )
        else:
            fields["performance_changes"] = f""

        if (
            pd.notnull(components_health_row["CONDITION_DIFF_DAY"])
            and pd.notnull(components_health_row["CONDITION_DIFF_WEEK"])
            and pd.notnull(components_health_row["CONDITION_DIFF_MONTH"])
        ):
            condition_changes_daily = f"{components_health_row['CONDITION_DIFF_DAY']}"
            condition_changes_weekl = f"{components_health_row['CONDITION_DIFF_WEEK']}"
            condition_Changes_monthly = (
                f"{components_health_row['CONDITION_DIFF_MONTH']}"
            )

            fields["condition_changes"] = (
                f"The Condition changes are {condition_changes_daily}% daily, {condition_changes_weekl}% weekly, and {condition_Changes_monthly}% monthly."
            )
        else:
            fields["condition_changes"] = f""

        keys_to_join = [
            "component_name",
            "machine_name",
            "machine_tag",
            "plant_name",
            "performance_health",
            "condition_health",
            "performance_changes",
            "condition_changes",
            # 'timestamp'
        ]
        # รวมข้อความของแถวนี้
        row_all_component_health_data_text = " ".join(
            [fields[key] for key in keys_to_join if key in fields]
        )
        row_all_component_health_data_text = re.sub(
            r"\s+", " ", row_all_component_health_data_text
        ).strip()
        # row_all_component_health_data_text = (
        #     "[Chunk]" + row_all_component_health_data_text + "[/Chunk]"
        # )
        row_all_component_health_data_text = "* " + row_all_component_health_data_text

        # เพิ่มข้อความลงในลิสต์ถ้าไม่ว่างเปล่า
        if row_all_component_health_data_text:
            all_component_health_data_text_list.append(
                row_all_component_health_data_text
            )

    # รวมข้อความทั้งหมดด้วย newline
    all_component_health_data_text = "\n".join(all_component_health_data_text_list)
    return all_component_health_data_text


def allComponentsHealth2content(
    plant_row, machine_row, all_components_health_df
):
    machine_name = machine_row["MACHINE_NAME"]
    machine_tag = machine_row["MACHINE_TAG"]
    plant_name = plant_row["PLANT_NAME"]

    title = "[Section]ALL COMPONENT HEALTH[Section]"
    detailed = (
        f"Here is a detailed report on the health status of each component within the {machine_name} (Tag: {machine_tag}) at the {plant_name}."
        f"The data reflects current Condition Health scores along with observed daily, weekly, and monthly changes. Each component's performance and stability are monitored for precision:"
    )

    all_component_health_data_text = create_all_component_health_text(
        plant_row, machine_row, all_components_health_df
    )
    all_component_health_data_text = "\n".join(
        [title, detailed, all_component_health_data_text]
    )

    return all_component_health_data_text
