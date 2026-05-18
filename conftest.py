"""
conftest.py - Configuración de fixtures para Pytest y Selenium
Este archivo contiene la configuración del WebDriver de Chrome y fixtures reutilizables.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import os
from datetime import datetime


@pytest.fixture(scope="function")
def driver():
    """
    Fixture que configura y devuelve una instancia del WebDriver de Chrome.
    Se ejecuta antes de cada test y se limpia después.
    
    Yields:
        WebDriver: Instancia de Chrome WebDriver
    """
    # Configurar opciones de Chrome
    chrome_options = Options()
    
    # Opciones para mejor compatibilidad
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Descomentar para modo headless (ejecución sin interfaz gráfica)
    # chrome_options.add_argument("--headless")
    
    # Inicializar el driver con webdriver-manager (descarga automática)
    driver = webdriver.Chrome(
        service=None,
        options=chrome_options
    )
    driver.maximize_window()
    
    # Implicitly wait
    driver.implicitly_wait(10)
    
    yield driver
    
    # Cleanup: tomar screenshot en caso de fallo y cerrar navegador
    driver.quit()


@pytest.fixture(scope="session")
def base_url():
    """
    Fixture que devuelve la URL base del sitio a probar.
    
    Returns:
        str: URL base de SauceDemo
    """
    return "https://www.saucedemo.com/"


@pytest.fixture(scope="session")
def valid_credentials():
    """
    Fixture que devuelve credenciales válidas para las pruebas.
    
    Returns:
        dict: Diccionario con usuario y contraseña
    """
    return {
        "username": "standard_user",
        "password": "secret_sauce"
    }


def pytest_configure(config):
    """
    Hook de Pytest que se ejecuta al iniciar.
    Crea la carpeta de reports si no existe.
    """
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(reports_dir, exist_ok=True)
