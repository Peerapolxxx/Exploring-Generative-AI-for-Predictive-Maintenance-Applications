import pandas as pd
import re


def create_all_models_health_text(
    plant_row, machine_row, component_list_df, all_models_health_df
):
    """สร้างข้อความแสดงข้อมูลสุขภาพของโมเดลเฝ้าติดตาม"""
    # ตรวจสอบว่า DataFrame ว่างหรือไม่
    if all_models_health_df.empty:
        return "No all models health data available."

    # สร้างลิสต์เก็บข้อความของแต่ละแถว
    all_models_healt_data_text_list = []

    # วนลูปผ่านทุกแถวใน DataFrame
    for _, models_health_row in all_models_health_df.iterrows():
        fields = {
            "component_name": (
                f"The {component_list_df.loc[component_list_df['COMPONENT_ID'] == models_health_row['COMPONENT_ID'], 'COMPONENT_NAME'].iloc[0]} component"
                if not component_list_df.loc[
                    component_list_df["COMPONENT_ID"]
                    == models_health_row["COMPONENT_ID"],
                    "COMPONENT_NAME",
                ].empty
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
                f"in the {plant_row['PLANT_NAME']}"
                if pd.notnull(plant_row["PLANT_NAME"])
                else "Unknown plant has a"
            ),
            "model_name": (
                f"is monitored by the model {models_health_row['MODEL_NAME']},"
                if pd.notnull(models_health_row["MODEL_NAME"])
                else "is monitored by the model Unknown,"
            ),
            "model_type": (
                f"which is a {models_health_row['MODEL_TYPE']} model"
                if pd.notnull(models_health_row["MODEL_TYPE"])
                else "which is a Unknown tpye model"
            ),
            "model_class": (
                f"of {models_health_row['MODEL_CLASS']} class."
                if pd.notnull(models_health_row["MODEL_CLASS"])
                else "of Unknown class model."
            ),
            "health_model": (
                f"This model has a health score of {models_health_row['HEALTH']}%,"
                if pd.notnull(models_health_row["HEALTH"])
                else "has a Model Health of N/A."
            ),
        }
        model_health_changes_daily = (
            f"{models_health_row['HEALTH_DIFF_DAY']}"
            if pd.notnull(models_health_row["HEALTH_DIFF_DAY"])
            else "N/A"
        )
        model_health_changes_week = (
            f"{models_health_row['HEALTH_DIFF_WEEK']}"
            if pd.notnull(models_health_row["HEALTH_DIFF_WEEK"])
            else "N/A"
        )
        model_health_changes_month = (
            f"{models_health_row['HEALTH_DIFF_MONTH']}"
            if pd.notnull(models_health_row["HEALTH_DIFF_MONTH"])
            else "N/A"
        )
        fields["model_health_changes"] = (
            f"with health changes recorded at  {model_health_changes_daily}% daily, {model_health_changes_week}% weekly, and {model_health_changes_month}% monthly."
        )

        if (
            pd.notnull(models_health_row["RESIDUAL_DIFF_DAY"])
            and pd.notnull(models_health_row["RESIDUAL_DIFF_WEEK"])
            and pd.notnull(models_health_row["RESIDUAL_DIFF_MONTH"])
        ):

            residual_changes_daily = f"{models_health_row['RESIDUAL_DIFF_DAY']}"
            residual_changes_week_ = f"{models_health_row['RESIDUAL_DIFF_WEEK']}"
            residual_changes_month_ = f"{models_health_row['RESIDUAL_DIFF_MONTH']}"

            fields["residual_changes"] = (
                f"The residual changes are {residual_changes_daily}% daily, {residual_changes_week_}% weekly, and {residual_changes_month_}% monthly."
            )
        else:
            fields["residual_changes"] = f""

        keys_to_join = [
            "component_name",
            "machine_name",
            "machine_tag",
            "plant_name",
            "model_name",
            "model_type",
            "model_class",
            "health_model",
            "model_health_changes",
            "residual_changes",
        ]
        # รวมข้อความของแถวนี้
        row_all_models_healt_data_text = " ".join(
            [fields[key] for key in keys_to_join if key in fields]
        )
        row_all_models_healt_data_text = " ".join(fields.values())
        row_all_models_healt_data_text = re.sub(
            r"\s+", " ", row_all_models_healt_data_text
        ).strip()
        # row_all_models_healt_data_text = (
        #     "[Chunk]" + row_all_models_healt_data_text + "[/Chunk]"
        # )
        row_all_models_healt_data_text = "* " + row_all_models_healt_data_text

        # เพิ่มข้อความลงในลิสต์ถ้าไม่ว่างเปล่า
        if row_all_models_healt_data_text:
            all_models_healt_data_text_list.append(row_all_models_healt_data_text)
    # รวมข้อความทั้งหมดด้วย newline
    all_models_healt_data_text = "\n".join(all_models_healt_data_text_list)

    return all_models_healt_data_text


def allModelsHealth2content(
    plant_row, machine_row, component_list_df, all_models_health_df
):
    machine_name = machine_row["MACHINE_NAME"]
    machine_tag = machine_row["MACHINE_TAG"]
    plant_name = plant_row["PLANT_NAME"]

    title = "[Section]ALL MODEL HEALTH[Section]"
    detailed = (
        f"This section provides a detailed analysis of the health and performance of models monitoring the components of the {machine_name} (Tag: {machine_tag}) at the {plant_name}."
        f"Each model is tracked for health scores and residual changes across daily, weekly, and monthly intervals:"
    )
    all_models_healt_data_text = create_all_models_health_text(
        plant_row, machine_row, component_list_df, all_models_health_df
    )
    all_models_healt_data_text = "\n".join(
        [title, detailed, all_models_healt_data_text]
    )

    return all_models_healt_data_text
