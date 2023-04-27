import yadisk
from settings import YA_TOKEN, ROOT_DIRECTORY
import random
from datetime import datetime

y = yadisk.YaDisk(token=YA_TOKEN)

# Проверяет, валиден ли токен
print(y.check_token())

# Получает общую информацию о диске
print(y.get_disk_info())

def set_list_organizations():
    pass