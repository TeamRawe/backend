from celery import shared_task
from tools.comapny.search_company import get_info
from database.logger import logger

@shared_task
def get_company_task(ogrn: int):
    try:
        created_object = get_info(ogrn)
        #logger.info(created_object)
        created_object.save()
        logger.info(f"Создан объект GovernmentalCompany c названием {created_object.title}, ОГРН: {created_object.ogrn}")
    except Exception as e:
        logger.error(f"Возникла ошибка {e} при создании объекта по {ogrn}")


