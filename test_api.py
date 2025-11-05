import pytest
import requests
import allure
from config import API_BASE_URL, HEADERS

@pytest.fixture
def product_in_cart():
    payload = {"id": 3064532}
    with allure.step("Добавление товара в корзину"):
        response = requests.post(f"{API_BASE_URL}/product", json=payload, headers=HEADERS)
        assert response.status_code in [200, 204]
    with allure.step("Получение ID добавленного товара"):
        response = requests.get(API_BASE_URL, headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        product_id = data["products"][0]["id"]
        assert product_id is not None
    yield product_id
    with allure.step("Удаление товара из корзины после теста"):
        response = requests.delete(f"{API_BASE_URL}/product/{product_id}", headers=HEADERS)
        if response.status_code not in [200, 204, 404]:
            assert False, f"Failed to delete product in teardown, status code: {response.status_code}"

@pytest.mark.api
def test_add_product_to_cart():
    payload = {"id": 3064532}
    with allure.step("Добавление товара в корзину"):
        response = requests.post(f"{API_BASE_URL}/product", json=payload, headers=HEADERS)
    with allure.step("Проверка статус кода"):
        assert response.status_code in [200, 204]

@pytest.mark.api
def test_get_cart_products(product_in_cart):
    product_id = product_in_cart
    with allure.step("Получение списка товаров в корзине"):
        response = requests.get(API_BASE_URL, headers=HEADERS)
        assert response.status_code == 200
    data = response.json()
    with allure.step("Проверка наличия добавленного товара"):
        ids = [prod["id"] for prod in data["products"]]
        assert product_id in ids

@pytest.mark.api
def test_delete_product_from_cart(product_in_cart):
    product_id = product_in_cart
    with allure.step("Удаление товара из корзины"):
        response = requests.delete(f"{API_BASE_URL}/product/{product_id}", headers=HEADERS)
    with allure.step("Проверка статус кода"):
        assert response.status_code in [200, 204]

@pytest.mark.api
def test_get_cart_after_deletion():
    with allure.step("Получение списка товаров после удаления"):
        response = requests.get(API_BASE_URL, headers=HEADERS)
        assert response.status_code == 200
    data = response.json()
    with allure.step("Проверка, что корзина может быть пустой"):
        assert isinstance(data["products"], list)

@pytest.mark.api
def test_add_negative_quantity():
    payload = {"id": 3064532, "quantity": -1}
    with allure.step("Попытка добавить отрицательное количество товара"):
        response = requests.post(f"{API_BASE_URL}/product", json=payload, headers=HEADERS)
    with allure.step("Проверка статус кода"):
        assert response.status_code == 200

    with allure.step("Проверка, что количество товара не изменилось"):
        response = requests.get(f"{API_BASE_URL}", headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        for prod in data.get("products", []):
            if prod["id"] == 3064532:
                assert prod["quantity"] >= 0
