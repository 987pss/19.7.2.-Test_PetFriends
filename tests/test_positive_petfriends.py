import pytest
import pathlib
from pathlib import Path
from app.api import PetFriends
from app.settings import email, password, name, animal_type, age, pet_photo_path, new_name, new_animal_type, new_age, \
    filter_, invalid_api_key_1_char, invalid_api_key_invalid_55_chars, invalid_api_key_56_chars, \
    invalid_api_key_invalid_57_chars, invalid_api_key_1_invalid_char, invalid_age_1_letter, invalid_pet_photo_gif_path, invalid_pet_photo_txt_path

pf = PetFriends()


# Позитивное тестирование
def test_get_api_key_valid_user(email=email,
                                password=password):
    """Позитивное тестирование получения ключа API:
    - код ответа HTTP - 200
    - получен ключ API"""

    response_status_code, _, api_key = pf.get_api_key(email, password)

    assert response_status_code == 200
    assert api_key


def test_add_new_pet_without_photo_valid_data_valid_auth_key(name=name,
                                                             animal_type=animal_type,
                                                             age=age):
    """Позитивное тестирование добавления нового питомца без фото:
    - код ответа HTTP - 200
    - получено id добавленного питомца
    - имя добавленного питомца совпадает с именем, переданным при добавлении питомца
    - тип питомца совпадает с типом, переданным при добавлении питомца
    - возраст питомца совпадает с возрастом, переданным при добавлении питомца
    - у добавленного питомца нет фото"""

    _, _, auth_key = pf.get_api_key(email, password)
    response_status_code, result, id_new_pet_without_photo = pf.add_new_pet_without_photo(auth_key, name, animal_type,
                                                                                          age)

    assert response_status_code == 200
    assert id_new_pet_without_photo
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert not result['pet_photo']


def test_add_new_pet_with_photo_valid_data_valid_auth_key(name=name,
                                                          animal_type=animal_type,
                                                          age=age,
                                                          pet_photo_path=pet_photo_path):
    """Позитивное тестирование добавления нового питомца с фото:
    - код ответа HTTP - 200
    - получено id добавленного питомца
    - имя добавленного питомца совпадает с именем, переданным при добавлении питомца
    - тип питомца совпадает с типом, переданным при добавлении питомца
    - возраст питомца совпадает с возрастом, переданным при добавлении питомца
    - у добавленного питомца есть фото"""

    _, _, auth_key = pf.get_api_key(email, password)
    response_status_code, result, id_new_pet_with_photo = pf.add_new_pet_with_photo(auth_key, name, animal_type, age,
                                                                         pet_photo_path)

    assert response_status_code == 200
    assert id_new_pet_with_photo
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['pet_photo']


def test_get_list_of_pets_valid_auth_key():
    """Позитивное тестирование получения списка добавленных питомцев:
    - код ответа HTTP - 200
    - в полученном результате питомцев больше 0"""

    _, _, auth_key = pf.get_api_key(email, password)
    response_status_code, result, _ = pf.get_list_of_pets(auth_key, filter_)

    assert response_status_code == 200
    assert len(result['pets']) > 0


def test_update_pet_with_photo_valid_data_valid_auth_key(new_name=new_name,
                                                         new_animal_type=new_animal_type,
                                                         new_age=new_age):
    """Позитивное тестирование обновления информации о добавленном питомце с фото:
    - код ответа HTTP - 200
    - имя питомца было изменено и совпадает с именем, переданным при обновлении информации о добавленном питомце
    - тип питомца был изменён и совпадает с типом, переданным при обновлении информации о добавленном питомце
    - возраст питомца был изменён и совпадает с возрастом, переданным при обновлении информации о добавленном питомце"""

    _, _, auth_key = pf.get_api_key(email, password)
    _, _, pet_id = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo_path)
    response_status_code, result = pf.update_pet(auth_key, pet_id, new_name, new_animal_type, new_age)

    assert response_status_code == 200
    assert pet_id in result['id']
    assert result['name'] == new_name
    assert result['animal_type'] == new_animal_type
    assert result['age'] == new_age


def test_add_photo_of_pet_without_photo_valid_data_valid_auth_key():
    """Позитивное тестирование добавления фото добавленному питомцу без фото:
    - код ответа HTTP - 200
    - у добавленного питомца есть фото"""

    _, _, auth_key = pf.get_api_key(email, password)
    _, _, pet_id = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    response_status_code, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo_path)

    assert response_status_code == 200
    assert result['pet_photo']


def test_delete_pet_with_photo_valid_auth_key():
    """Позитивное тестирование удаления добавленного питомца с фото:
    - код ответа HTTP - 200
    - пустой ответ после удаления питомца
    - id удалённого питомца нет в полученном после удаления ответе с перечнем добавленных питомцев"""

    _, _, auth_key = pf.get_api_key(email, password)
    _, _, pet_id = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo_path)
    response_status_code, result = pf.delete_pet(auth_key, pet_id)
    _, _, result_text = pf.get_list_of_pets(auth_key, filter_)

    assert response_status_code == 200
    assert not result
    assert pet_id not in result_text
