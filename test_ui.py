import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from config import BASE_URL

@pytest.mark.ui
def test_confirm_city():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 5)
    with allure.step("Подтверждение города"):
        try:
            confirm_button = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[text()='Да, я здесь']/ancestor::button")
            ))
            driver.execute_script("arguments[0].click();", confirm_button)
        except TimeoutException:
            pass
    driver.quit()

@pytest.mark.ui
def test_open_books_section_via_catalog():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    with allure.step("Открытие каталога"):
        catalog_button = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button.catalog-btn.header-sticky__catalog-menu")
        ))
        driver.execute_script("arguments[0].click();", catalog_button)
    with allure.step("Переход в раздел 'Книги'"):
        books_item = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='Книги']/ancestor::div[contains(@class,'categories-level-menu__item-root')]")
        ))
        books_item.click()
    with allure.step("Проверка заголовка раздела"):
        header = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "p.head-categories-menu__title")
        ))
        assert "Книги" in header.text
    driver.quit()

@pytest.mark.ui
def test_open_cart():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    with allure.step("Открытие корзины"):
        cart_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.header-controls__btn[aria-label='Корзина']")
        ))
        cart_button.click()
    with allure.step("Проверка заголовка корзины"):
        header = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "h1.cart-page__title")
        ))
        assert "КОРЗИНА" in header.text.upper()
    driver.quit()

@pytest.mark.ui
def test_search_book_count():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 15)
    with allure.step("Поиск книги"):
        search_input = wait.until(EC.presence_of_element_located((By.NAME, "search")))
        search_input.send_keys("Гарри Поттер")
        search_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.search-form__button-search")
        ))
        search_button.click()
    with allure.step("Проверка количества найденных товаров"):
        total_text = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.catalog-products-total")
        )).text
        assert "товар" in total_text
    driver.quit()

@pytest.mark.ui
def test_accept_cookies():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    with allure.step("Закрытие уведомления о cookie"):
        button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class,'chg-app-button__content') and contains(., 'Понятно, закрыть')]")
        ))
        driver.execute_script("arguments[0].click();", button)
    driver.quit()
