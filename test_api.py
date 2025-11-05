import pytest
import requests
import allure
from config import API_BASE_URL, HEADERS

product_id = None

@pytest.mark.api
def test_add_product_to_cart():
    payload = {"id": 3064532}
    with allure.step("Добавление товара в корзину"):
        response = requests.post(API_BASE_URL + "/product", json=payload, headers=HEADERS)
    with allure.step("Проверка статус кода"):
        assert response.status_code in [200, 204]

@pytest.mark.api
def test_get_cart_products():
    global product_id
    with allure.step("Получение списка товаров в корзине"):
        response = requests.get(API_BASE_URL, headers=HEADERS)
    with allure.step("Проверка статус кода"):
        assert response.status_code == 200
    data = response.json()
    with allure.step("Сохранение ID первого товара"):
        product_id = data["products"][0]["id"]
        assert product_id is not None

@pytest.mark.api
def test_delete_product_from_cart():
    assert product_id is not None
    with allure.step("Удаление товара из корзины"):
        response = requests.delete(API_BASE_URL + "/product/" + str(product_id), headers=HEADERS)
    with allure.step("Проверка статус кода"):
        assert response.status_code in [200, 204]

@pytest.mark.api
def test_get_cart_after_deletion():
    with allure.step("Получение списка товаров после удаления"):
        response = requests.get(API_BASE_URL, headers=HEADERS)
    with allure.step("Проверка статус кода"):
        assert response.status_code == 200
    data = response.json()
    first_product_id = data["products"][0]["id"] if len(data["products"]) > 0 else None
    with allure.step("Проверка отсутствия удалённого товара"):
        assert first_product_id != product_id

@pytest.mark.api
def test_add_nonexistent_product():
    payload = {"id": 30645323}
    with allure.step("Добавление несуществующего товара"):
        response = requests.post(API_BASE_URL + "/product", json=payload, headers=HEADERS)
    with allure.step("Проверка статус кода"):
        assert response.status_code in [400, 500]
    data = {}
    try:
        data = response.json()
    except ValueError:
        pass
    message = data.get("message", "")
    with allure.step("Проверка сообщения об ошибке"):
        assert "не существует" in message.lower()
