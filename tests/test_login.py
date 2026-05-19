"""
test_login.py - Pruebas de autenticación en SauceDemo
Casos de prueba para validar el login con credenciales válidas e inválidas.
"""

import sys
import os
# Asegurar que la carpeta raíz del proyecto esté en sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLogin:
    """Casos de prueba para la funcionalidad de login"""
    
    def test_login_exitoso(self, driver, base_url, valid_credentials):
        """
        Caso de prueba: Login exitoso
        Objetivo: Validar que un usuario puede iniciar sesión con credenciales válidas
        y es redirigido a la página de inventario.
        
        Pasos:
        1. Navegar a la página de login de SauceDemo
        2. Ingresar credenciales válidas
        3. Hacer clic en el botón de login
        4. Verificar que la página de inventario se cargó correctamente
        """
        # Paso 1: Navegar a la página
        driver.get(base_url)
        print("✅ Navegado a la página de login")
        
        # Paso 2-3: Realizar login usando selectores directos
        wait = WebDriverWait(driver, 10)
        username_field = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
        username_field.clear()
        username_field.send_keys(valid_credentials["username"])

        password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        password_field.clear()
        password_field.send_keys(valid_credentials["password"])

        login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
        login_button.click()
        print("✅ Credenciales ingresadas y botón de login presionado")

        # Paso 4: Validar que estamos en la página de inventario
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item")))
        print("✅ Login exitoso - Página de inventario cargada")

        # Validación adicional: verificar que hay productos visibles
        items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        items_count = len(items)
        assert items_count > 0, "No se encontraron productos en el inventario"
        print(f"✅ Se encontraron {items_count} productos en la página")
    
    def test_login_con_credenciales_invalidas(self, driver, base_url):
        """
        Caso de prueba: Login con credenciales inválidas
        Objetivo: Validar que el sistema rechaza credenciales incorrectas
        
        Pasos:
        1. Navegar a la página de login
        2. Ingresar credenciales inválidas
        3. Hacer clic en el botón de login
        4. Verificar que aparece un mensaje de error
        """
        # Paso 1: Navegar a la página
        driver.get(base_url)
        print("✅ Navegado a la página de login")
        
        # Paso 2-3: Intentar login con credenciales inválidas
        wait = WebDriverWait(driver, 10)
        username_field = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
        username_field.clear()
        username_field.send_keys("usuario_invalido")

        password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        password_field.clear()
        password_field.send_keys("contraseña_invalida")

        login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
        login_button.click()
        print("✅ Intentado login con credenciales inválidas")

        # Paso 4: Verificar que aparece un mensaje de error
        try:
            error_message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "error-message-container")))
            assert error_message.is_displayed(), "El mensaje de error no se muestra"
            print(f"✅ Mensaje de error mostrado: {error_message.text}")
        except Exception:
            pytest.fail("No se encontró el mensaje de error")
    
    def test_login_sin_ingresar_usuario(self, driver, base_url):
        """
        Caso de prueba: Intento de login sin ingresar usuario
        Objetivo: Validar validación de campos requeridos
        
        Pasos:
        1. Navegar a la página de login
        2. No ingresar usuario, solo contraseña
        3. Hacer clic en login
        4. Verificar error
        """
        # Paso 1: Navegar a la página
        driver.get(base_url)
        print("✅ Navegado a la página de login")
        
        # Paso 2-3: Intentar login sin usuario
        wait = WebDriverWait(driver, 10)
        password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        password_field.clear()
        password_field.send_keys("secret_sauce")

        login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
        login_button.click()
        print("✅ Intentado login sin ingresar usuario")

        # Paso 4: Verificar error
        try:
            error_message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "error-message-container")))
            assert error_message.is_displayed(), "El mensaje de error no se muestra"
            assert "username" in error_message.text.lower(), "El error no menciona el usuario"
            print(f"✅ Error validado: {error_message.text}")
        except Exception:
            pytest.fail("No se encontró el mensaje de error para usuario requerido")
