import logging
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
from queue import Queue
import os
from database import settings

log_queue = Queue()

def setup_logging():

    queue_handler = QueueHandler(log_queue)

    log_dir = os.path.join(settings.BASE_DIR, 'logs')
    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    queue_handler.setFormatter(formatter)

    log_file_path = os.path.join(log_dir, 'async_log.log')

    file_handler = RotatingFileHandler(log_file_path,
        'async_log.log', maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(formatter)

    # Создаем слушателя очереди, который будет обрабатывать логи асинхронно
    listener = QueueListener(log_queue, file_handler)
    listener.start()

    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(queue_handler)

    return logger

logger = setup_logging()