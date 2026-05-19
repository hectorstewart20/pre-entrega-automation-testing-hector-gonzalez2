"""
conftest.py - Configuración de fixtures para Pytest y Selenium
Este archivo contiene la configuración del WebDriver de Chrome y fixtures reutilizables.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service 
import os
from datetime import datetime


@pytest.fixture(scope="function")
def driver():

    # Configurar opciones de Chrome
    chrome_options = Options()
    
    # Preferencias para desactivar gestor de contraseñas y popups asociados
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "credentials_enable_autosignin": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Opciones para mejor compatibilidad
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # Flags para evitar popups, notificaciones y extensiones que interfieran con pruebas
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-background-timer-throttling")
    # Bloquear notificaciones por pref (0=ask, 1=allow, 2=block)
    prefs["profile.default_content_setting_values.notifications"] = 2
    chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument("--headless")
    # Dejar que Selenium Manager gestione el driver automáticamente
    driver = webdriver.Chrome(
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
    return "https://www.saucedemo.com/"


@pytest.fixture(scope="session")
def valid_credentials():
    return {
        "username": "standard_user",
        "password": "secret_sauce"
    }


def pytest_configure(config):
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(reports_dir, exist_ok=True)
