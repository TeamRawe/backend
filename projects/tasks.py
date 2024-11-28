import os
import time
from celery import shared_task
from tools.ms.ms_project_parser import *


@shared_task
def process_project_file(file_path):
    """Задача Celery для обработки XML-файла."""
    if not os.path.exists(file_path):
        return {"error": f"File {file_path} does not exist."}

    # Обработка файла
    try:
        result_file = parse_ms_project(file_path)
        return {"status": "success", "output_file": result_file}
    except Exception as e:
        return {"status": "error", "message": str(e)}