import os
import pathlib
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# URL-адреса
base_url = 'https://petfriends.skillfactory.ru'
get_api_key_url = '/api/key'
add_new_pet_without_photo_url = '/api/create_pet_simple'
add_new_pet_with_photo_url = '/api/pets'
get_list_of_pets_url = '/api/pets'
update_pet_url = f'/api/pets/'  # {pet_id} добавляется внутри метода: /api/pets/{pet_id}
add_photo_of_pet_url = '/api/pets/set_photo/'  # {pet_id} добавляется внутри метода: /api/pets/set_photo/{pet_id}
delete_pet_url = f'/api/pets/'  # {pet_id} добавляется внутри метода: /api/pets/{pet_id}

# Данные для авторизации
email = os.getenv('email')
password = os.getenv('password')

# Данные для добавления нового питомца
name = 'Мася'
animal_type = 'кошка'
age = '12'
pet_photo_path = str(Path('..', 'images', 'Masya.jpg'))

# Данные для обновления информации о добавленном питомце
new_name = 'Вася'
new_animal_type = 'кот'
new_age = '7'

# Данные фильтра для получения списка добавленных питомцев
filter_ = 'my_pets'

# Данные для негативного тестирования
invalid_api_key_1_char = '0'
invalid_api_key_invalid_55_chars = 'h45647cd3ad770dfgb351af4cb202ed1237ff1661e9dfgh0c4v3f56'
invalid_api_key_56_chars = 'gh45647cd3ad770dfgb351af4cb202ed1237ff1661e9dfgh0c4v3f56'
invalid_api_key_invalid_57_chars = 'gh45647cd3ad770dfgb351af4cb202ed1237ff1661e9dfgh0c4v3f567'
invalid_api_key_1_invalid_char = '\\'
invalid_age_1_letter = 'a'
invalid_pet_photo_gif_path = str(Path('..', 'images', 'Masya_gif.gif'))
invalid_pet_photo_txt_path = str(Path('..', 'images', 'text_txt.txt'))
