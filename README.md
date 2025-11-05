# Автоматизация тестирования

Задача:
Автоматизация UI- и API-тестов для проекта на основе финальной работы по ручному тестированию.

Проект включает:
-UI-тесты для проверки функционала сайта.
-API-тесты для проверки работы корзины и товаров через API.

В файле config.py указаны:

BASE_URL — URL сайта для UI-тестов.

API_BASE_URL — URL API для тестирования корзины.

HEADERS — заголовки для API-запросов (Authorization, Content-Type).

Запуск тестов:
Только UI-тесты - pytest -m ui --alluredir=allure-results
Только API-тесты - pytest -m api --alluredir=allure-results
Все тесты - pytest --alluredir=allure-results
Allure отчет - allure serve allure-results

Финальный проект по ссылке: https://amnyam007.yonote.ru/collection/finalnyj-proekt-po-ruchnomu-testirovaniyu-QRpO69RdFS