from loguru import logger
from datetime import datetime


async def print_logger_info(input_text: str, predicted):
    """
    print_logger_info - printing logger.
    """
    logger.info({"input_text": input_text, "predicted": predicted})


def return_current_time():
    """
    Example func, return current time.
    """
    return datetime.utcnow().isoformat()
