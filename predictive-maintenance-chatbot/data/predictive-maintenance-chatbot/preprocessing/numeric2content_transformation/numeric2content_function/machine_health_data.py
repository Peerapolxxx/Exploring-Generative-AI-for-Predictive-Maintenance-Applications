import pandas as pd
import re

def create_machine_health_text(plant_row, machine_health_df):
    """สร้างข้อความสำหรับ machine health data โดยรวมข้อมูลจากทุกแถว"""
    # ตรวจสอบว่า DataFrame ว่างหรือไม่
    if machine_health_df.empty:
        return "No machine health data available."

    # สร้างลิสต์เก็บข้อความของแต่ละแถว
    machine_health_data_text_list = []

    # วนลูปผ่านทุกแถวใน DataFrame
    for _, machine_health_row in machine_health_df.iterrows():
        # สร้าง dictionary เก็บข้อมูลของแต่ละแถว
        fields = {
            "machine_name": (
                f"The {machine_health_row['MACHINE_NAME']}"
                if pd.notnull(machine_health_row["MACHINE_NAME"])
                else "Unknown machine"
            ),
            "machine_tag": (
                f"(Tag: {machine_health_row['MACHINE_TAG']})"
                if pd.notnull(machine_health_row["MACHINE_TAG"])
                else "(Tag: Unknown)"
            ),
            "plant_name": (
                f"in the {plant_row['PLANT_NAME']} has a"
                if pd.notnull(plant_row["PLANT_NAME"])
                else "in Unknown plant has a "
            ),
            "performance_health": (
                f"Performance Health of {machine_health_row['PERFORMANCE_HEALTH']}% and"
                if pd.notnull(machine_health_row["PERFORMANCE_HEALTH"])
                else "Performance Health of N/A,"
            ),
            "condition_health": (
                f"Condition Health of {machine_health_row['CONDITION_HEALTH']}%."
                if pd.notnull(machine_health_row["CONDITION_HEALTH"])
                else "Condition Health of N/A."
            ),
            "critical_status": (
                f"The machine is currently in a {'Critical' if machine_health_row['CRITICAL_STATUS'] else 'Non-Critical'} status."
                if pd.notnull(machine_health_row["CRITICAL_STATUS"])
                else "The machine is currently in a N/A status."
            ),
        }

        # ตรวจสอบและเพิ่มข้อมูลการเปลี่ยนแปลงของ performance
        performance_changes_daily = (
            f"{machine_health_row['PERFORMANCE_DIFF_DAY']}"
            if pd.notnull(machine_health_row["PERFORMANCE_DIFF_DAY"])
            else "N/A "
        )
        performance_changes_weekly = (
            f"{machine_health_row['PERFORMANCE_DIFF_WEEK']}"
            if pd.notnull(machine_health_row["PERFORMANCE_DIFF_WEEK"])
            else "N/A "
        )
        performance_Changes_monthly = (
            f"{machine_health_row['PERFORMANCE_DIFF_MONTH']}"
            if pd.notnull(machine_health_row["PERFORMANCE_DIFF_MONTH"])
            else "N/A "
        )
        fields["performance_change"] = (
            f"The Performance changes are {performance_changes_daily}% daily, {performance_changes_weekly}% weekly, and {performance_Changes_monthly}% monthly."
        )

        # ตรวจสอบและเพิ่มข้อมูลการเปลี่ยนแปลงของ condition
        condition_changes_daily = (
            f"{machine_health_row['CONDITION_DIFF_DAY']}"
            if pd.notnull(machine_health_row["CONDITION_DIFF_DAY"])
            else "N/A"
        )
        condition_changes_weekl = (
            f"{machine_health_row['CONDITION_DIFF_WEEK']}"
            if pd.notnull(machine_health_row["CONDITION_DIFF_WEEK"])
            else "N/A"
        )
        condition_Changes_monthly = (
            f"{machine_health_row['CONDITION_DIFF_MONTH']}"
            if pd.notnull(machine_health_row["CONDITION_DIFF_MONTH"])
            else "N/A"
        )
        fields["condition_change"] = (
            f"The Condition changes are {condition_changes_daily}% daily, {condition_changes_weekl}% weekly, and {condition_Changes_monthly}% monthly."
        )

        # กำหนดคีย์ที่จะใช้ในการรวมข้อความ
        keys_to_join = [
            "machine_name",
            "machine_tag",
            "plant_name",
            "performance_health",
            "condition_health",
            "critical_status",
            "performance_change",
            "condition_change",
        ]

        # รวมข้อความของแต่ละแถว
        row_machine_health_data_text = " ".join(
            [fields[key] for key in keys_to_join if key in fields]
        )
        row_machine_health_data_text = re.sub(
            r"\s+", " ", row_machine_health_data_text
        ).strip()
        row_machine_health_data_text = "* " + row_machine_health_data_text

        # เพิ่มข้อความลงในลิสต์ถ้าไม่ว่างเปล่า
        if row_machine_health_data_text:
            machine_health_data_text_list.append(row_machine_health_data_text)

    # รวมข้อความทั้งหมดด้วย newline
    machine_health_data_text = "\n".join(machine_health_data_text_list)

    return machine_health_data_text

def machineHealth2content(plant_row, machine_health_df):
    # กำหนดหัวข้อของ section
    title = "[Section]MACHINE HEALTH DATA[Section]\n"
    # สร้างข้อความ machine health data
    machine_health_data_text = create_machine_health_text(plant_row, machine_health_df)
    # รวมหัวข้อกับข้อความ
    machine_health_data_text = title + machine_health_data_text

    return machine_health_data_text
