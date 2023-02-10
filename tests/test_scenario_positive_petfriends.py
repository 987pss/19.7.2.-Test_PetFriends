import pytest
import pathlib
from pathlib import Path
from app.api import PetFriends
from app.settings import email, password, name, animal_type, age, pet_photo_path, new_name, new_animal_type, new_age, \
    filter_, invalid_api_key_1_char, invalid_api_key_invalid_55_chars, invalid_api_key_56_chars, \
    invalid_api_key_invalid_57_chars, invalid_api_key_1_invalid_char, invalid_age_1_letter, invalid_pet_photo_gif_path, invalid_pet_photo_txt_path

pf = PetFriends()


# Сценарное позитивное тестирование
def test_add_update_delete_pet_with_photo_valid_data_valid_auth_key_scenario():
    """Сценарное позитивное тестирование: добавление нового питомца с фото, обновление информации о добавленном питомце
    с фото, удаление добавленного питомца с фото"""

    """Позитивное тестирование добавления нового питомца с фото:
    - код ответа HTTP - 200
    - получено id добавленного питомца
    - имя добавленного питомца совпадает с именем, переданным при добавлении питомца
    - тип питомца совпадает с типом, переданным при добавлении питомца
    - возраст питомца совпадает с возрастом, переданным при добавлении питомца
    - у добавленного питомца есть фото"""
    _, _, auth_key = pf.get_api_key(email, password)
    _, _, pet_id = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo_path)
    response_status_code, result, id_new_pet = pf.add_new_pet_with_photo(auth_key, name, animal_type, age,
                                                                         pet_photo_path)

    assert response_status_code == 200
    assert id_new_pet
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['pet_photo']

    """Позитивное тестирование обновления информации о добавленном питомце с фото:
    - код ответа HTTP - 200
    - имя питомца было изменено и совпадает с именем, переданным при обновлении информации о добавленном питомце
    - тип питомца был изменён и совпадает с типом, переданным при обновлении информации о добавленном питомце
    - возраст питомца был изменён и совпадает с возрастом, переданным при обновлении информации о добавленном питомце"""
    response_status_code, result = pf.update_pet(auth_key, id_new_pet, new_name, new_animal_type, new_age)

    assert response_status_code == 200
    assert result['name'] == new_name
    assert result['animal_type'] == new_animal_type
    assert result['age'] == new_age

    """Позитивное тестирование удаления добавленного питомца с фото:
    - код ответа HTTP - 200
    - пустой ответ после удаления питомца
    - id удалённого питомца нет в полученном после удаления ответе с перечнем добавленных питомцев"""
    response_status_code, result = pf.delete_pet(auth_key, id_new_pet)
    _, _, result_text = pf.get_list_of_pets(auth_key, filter_)

    assert response_status_code == 200
    assert not result
    assert id_new_pet not in result_text
