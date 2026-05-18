"""
driver_manager.py - Gestión del WebDriver de Chrome
Contiene funciones auxiliares para la configuración y manejo del navegador.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    """
    Configura y devuelve una instancia del WebDriver de Chrome.
    
    Returns:
        WebDriver: Instancia de Chrome WebDriver configurado
    """
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    return driver
