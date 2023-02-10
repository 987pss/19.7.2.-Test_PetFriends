import pytest
import pathlib
from pathlib import Path
from app.api import PetFriends
from app.settings import email, password, name, animal_type, age, pet_photo_path, new_name, new_animal_type, new_age, \
    filter_, invalid_api_key_1_char, invalid_api_key_invalid_55_chars, invalid_api_key_56_chars, \
    invalid_api_key_invalid_57_chars, invalid_api_key_1_invalid_char, invalid_age_1_letter, invalid_pet_photo_gif_path, invalid_pet_photo_txt_path

pf = PetFriends()


# Негативное тестирование
def test_get_api_key_empty_password(email=email,
                                    invalid_password=''):
    """Негативное тестирование получения ключа API при верном e-mail, но пустом пароле:
    - код ответа HTTP - 403
    - ключ API не получен"""

    response_status_code, _, api_key = pf.get_api_key(email, invalid_password)

    assert response_status_code == 403
    assert not api_key


def test_add_new_pet_without_photo_empty_auth_key(invalid_auth_key='',
                                                  name=name,
                                                  animal_type=animal_type,
                                                  age=age):
    """Негативное тестирование добавления нового питомца без фото при пустом ключе API:
    - код ответа HTTP - 403
    - питомец не добавлен: id не получено"""

    response_status_code, result, id_new_pet_without_photo = pf.add_new_pet_without_photo(invalid_auth_key, name, animal_type,
                                                                                          age)

    assert response_status_code == 403
    assert not id_new_pet_without_photo


def test_add_new_pet_without_photo_age_is_letter(name=name,
                                                 animal_type=animal_type,
                                                 invalid_age=invalid_age_1_letter):
    """Негативное тестирование добавления нового питомца без фото при верном ключе API, допустимых имене и типе,
    но возрасте, указанном буквой:
    - код ответа HTTP - 400
    - питомец не добавлен: id не получено"""

    _, _, auth_key = pf.get_api_key(email, password)
    response_status_code, result, id_new_pet_without_photo = pf.add_new_pet_without_photo(auth_key, name, animal_type,
                                                                                          invalid_age)

    assert response_status_code == 400
    assert not id_new_pet_without_photo


def test_add_new_pet_with_photo_invalid_auth_key(invalid_auth_key=invalid_api_key_1_char,
                                                 name=name,
                                                 animal_type=animal_type,
                                                 age=age,
                                                 pet_photo_path=pet_photo_path):
    """Негативное тестирование добавления нового питомца c фото при неверном ключе API, состоящем из 1 символа:
    - код ответа HTTP - 403
    - питомец не добавлен: id не получено"""

    response_status_code, result, id_new_pet_with_photo = pf.add_new_pet_with_photo(invalid_auth_key, name, animal_type, age,
                                                                         pet_photo_path)

    assert response_status_code == 403
    assert not id_new_pet_with_photo


def test_add_new_pet_with_photo_invalid_format_of_pet_photo(name=name,
                                                            animal_type=animal_type,
                                                            age=age,
                                                            invalid_pet_photo_path=invalid_pet_photo_gif_path):
    """Негативное тестирование добавления нового питомца c фото при верном ключе API, допустимых имене, типе и
    возрасте, но фото в недопустимом формате .gif:
    - код ответа HTTP - 400
    - питомец не добавлен: id не получено"""

    _, _, auth_key = pf.get_api_key(email, password)
    response_status_code, result, id_new_pet_with_photo = pf.add_new_pet_with_photo(auth_key, name, animal_type, age,
                                                                                    invalid_pet_photo_path)

    assert response_status_code == 400
    assert not id_new_pet_with_photo


def test_get_list_of_pets_invalid_auth_key(invalid_auth_key=invalid_api_key_56_chars):
    """Негативное тестирование получения списка добавленных питомцев при неверном ключе API, состоящем из допустимых 56
    символов:
    - код ответа HTTP - 403
    - в полученном ответе нет данных добавленных питомцев"""

    response_status_code, result, _ = pf.get_list_of_pets(invalid_auth_key, filter_)

    assert response_status_code == 403
    assert 'pets' not in result


def test_update_pet_with_photo_invalid_auth_key(invalid_auth_key=invalid_api_key_invalid_55_chars,
                                                new_name=new_name,
                                                new_animal_type=new_animal_type,
                                                new_age=new_age):
    """Негативное тестирование обновления информации о добавленном питомце с фото при неверном ключе API, состоящем из
    55 символов:
    - код ответа HTTP - 403
    - в полученном ответе нет данных добавленного питомца"""

    _, _, auth_key = pf.get_api_key(email, password)
    _, _, pet_id = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo_path)
    response_status_code, result = pf.update_pet(invalid_auth_key, pet_id, new_name, new_animal_type, new_age)

    assert response_status_code == 403
    assert 'animal_type' not in result


def test_update_pet_with_photo_empty_animal_type(new_name=new_name,
                                                 invalid_animal_type='',
                                                 new_age=new_age):
    """Негативное тестирование обновления информации о добавленном питомце с фото при верном ключе API, допустимых
    имене и возрасте, но пустом типе:
    - код ответа HTTP - 400
    - в полученном ответе нет данных добавленного питомца"""

    _, _, auth_key = pf.get_api_key(email, password)
    _, _, pet_id = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo_path)
    response_status_code, result = pf.update_pet(auth_key, pet_id, new_name, invalid_animal_type, new_age)

    assert response_status_code == 400
    assert 'animal_type' not in result


def test_add_photo_of_pet_without_photo_invalid_auth_key(invalid_auth_key=invalid_api_key_invalid_57_chars):
    """Негативное тестирование добавления фото добавленному питомцу без фото при неверном ключе API, состоящем из 57
    символов:
    - код ответа HTTP - 403
    - в полученном ответе нет данных добавленного питомца"""

    _, _, auth_key = pf.get_api_key(email, password)
    _, _, pet_id = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    response_status_code, result = pf.add_photo_of_pet(invalid_auth_key, pet_id, pet_photo_path)

    assert response_status_code == 403
    assert 'pet_photo' not in result


def test_add_photo_of_pet_without_photo_invalid_data(invalid_pet_photo_path=invalid_pet_photo_txt_path):
    """Негативное тестирование добавления фото добавленному питомцу без фото при верном ключе API, но текстовом файле в
    формате .txt вместо фото:
    - код ответа HTTP - 400
    - в полученном ответе нет данных добавленного питомца"""

    _, _, auth_key = pf.get_api_key(email, password)
    _, _, pet_id = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    response_status_code, result = pf.add_photo_of_pet(auth_key, pet_id, invalid_pet_photo_path)

    assert response_status_code == 400
    assert 'pet_photo' not in result


def test_delete_pet_with_photo_invalid_auth_key(invalid_auth_key=invalid_api_key_1_invalid_char):
    """Негативное тестирование удаления добавленного питомца с фото при неверном ключе API, состоящем из 1 недопустимого
     символа:
    - код ответа HTTP - 403
    - непустой ответ после попытки удаления питомца
    - id удаляемого питомца есть в полученном после попытки удаления ответе с перечнем добавленных питомцев"""

    _, _, auth_key = pf.get_api_key(email, password)
    _, _, pet_id = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo_path)
    response_status_code, result = pf.delete_pet(invalid_auth_key, pet_id)
    _, _, result_text = pf.get_list_of_pets(auth_key, filter_)

    assert response_status_code == 403
    assert result
    assert pet_id in result_text
