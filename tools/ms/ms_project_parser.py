import xml.etree.ElementTree as ET
import json
import time
from datetime import datetime


def parse_ms_project(file_path):
    # Загружаем XML-файл
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Ошибка чтения XML-файла: {e}")
        return

    # Пространство имен
    namespace = {'ns': 'http://schemas.microsoft.com/project'}

    tasks = []
    total_tasks = 0
    completion_stats = {
        "100%": 0,
        "75-99%": 0,
        "50-74%": 0,
        "25-49%": 0,
        "1-24%": 0,
        "not_started": 0
    }

    # Текущая дата для определения состояния задач
    current_date = datetime.now()

    # Получаем название проекта
    project_name = "Unnamed Project"
    first_task = root.find(".//ns:Task[ns:UID='0']", namespace)
    if first_task is not None:
        project_name = first_task.find("ns:Name", namespace).text or "Unnamed Project"

    # Обработка задач
    for task in root.findall(".//ns:Task", namespace):
        task_id = task.find("ns:UID", namespace)
        name = task.find("ns:Name", namespace)
        start_date_text = task.find("ns:Start", namespace)
        finish_date_text = task.find("ns:Finish", namespace)
        percent_complete_text = task.find("ns:PercentComplete", namespace)
        cost_text = task.find("ns:Cost", namespace)

        # Пропускаем первую задачу (UID=0) (при сохранении XML в первой Task хранится название проекта)
        if task_id.text == "0":
            continue

        # Проверяем, что все обязательные поля заполнены
        missing_fields = []
        if not (task_id is not None and task_id.text):
            missing_fields.append("UID")
        if not (name is not None and name.text):
            missing_fields.append("Name")
        if not (start_date_text is not None and start_date_text.text):
            missing_fields.append("Start")
        if not (finish_date_text is not None and finish_date_text.text):
            missing_fields.append("Finish")
        if not (percent_complete_text is not None and percent_complete_text.text):
            missing_fields.append("PercentComplete")
        if not (cost_text is not None and cost_text.text):
            missing_fields.append("Cost")

        # Проверка организации
        organization = None
        extended_attributes = task.findall("ns:ExtendedAttribute", namespace)
        for ext_attr in extended_attributes:
            field_id = ext_attr.find("ns:FieldID", namespace).text
            if field_id == "188743731":  # Идентификатор для организации
                organization = ext_attr.find("ns:Value", namespace).text
                break
        if not organization:
            missing_fields.append("Organization")

        if missing_fields:
            print(
                f"Пропущена задача из-за отсутствия следующих полей: {', '.join(missing_fields)}. UID: {task_id.text if task_id is not None else 'N/A'}")
            continue



        # Считываем основные поля
        name = name.text or "Unnamed Task"
        start_date_text = start_date_text.text
        finish_date_text = finish_date_text.text
        cost = cost_text.text or "N/A"
        percent_complete = int(percent_complete_text.text or 0)

        # Конвертируем даты
        start_date = datetime.fromisoformat(start_date_text) if start_date_text else None
        finish_date = datetime.fromisoformat(finish_date_text) if finish_date_text else None

        # Определяем состояние задачи
        if percent_complete == 100:
            status = "Завершено"
        elif current_date < start_date:
            status = "Будущая задача"
        elif start_date <= current_date <= finish_date:
            status = "По графику"
        elif current_date > finish_date:
            status = "Задержка"
        else:
            status = "Неизвестно"

        # Считаем статистику выполнения
        if percent_complete == 100:
            completion_stats["100%"] += 1
        elif 75 <= percent_complete < 100:
            completion_stats["75-99%"] += 1
        elif 50 <= percent_complete < 75:
            completion_stats["50-74%"] += 1
        elif 25 <= percent_complete < 50:
            completion_stats["25-49%"] += 1
        elif 1 <= percent_complete < 25:
            completion_stats["1-24%"] += 1
        else:  # percent_complete == 0
            completion_stats["not_started"] += 1

        # Добавляем задачу в список
        tasks.append({
            "ID": task_id.text,
            "Name": name,
            "Start": start_date_text,
            "Finish": finish_date_text,
            "Cost": cost,
            "PercentComplete": percent_complete,
            "Organization": organization,
            "Status": status
        })

        total_tasks += 1

    # Формируем итоговый JSON
    output_data = {
        "ProjectName": project_name,
        "TotalTasks": total_tasks,
        "CompletionStats": completion_stats,
        "Tasks": tasks
    }

    # Генерируем имя файла с добавлением UNIX-timestamp
    timestamp = int(time.time())
    output_file = f"parsed_tasks_{timestamp}.json"

    # Сохраняем JSON в файл
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)

    print(f"JSON файл успешно сохранен: {output_file}")

if __name__ == "__main__":
    input_file = "пример.xml"  #название XML файла
    if not input_file:
        print("Ошибка: путь к файлу не указан.")
    else:
        parse_ms_project(input_file)
