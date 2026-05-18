"""
test_login.py - Pruebas de autenticación en SauceDemo
Casos de prueba para validar el login con credenciales válidas e inválidas.
"""

import pytest
from utils.saucedemo_pages import LoginPage, InventoryPage


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
        
        # Paso 2-3: Realizar login
        login_page = LoginPage(driver)
        login_page.login(valid_credentials["username"], valid_credentials["password"])
        print("✅ Credenciales ingresadas y botón de login presionado")
        
        # Paso 4: Validar que estamos en la página de inventario
        inventory_page = InventoryPage(driver)
        assert inventory_page.is_inventory_page_loaded(), "La página de inventario no se cargó"
        print("✅ Login exitoso - Página de inventario cargada")
        
        # Validación adicional: verificar que hay productos visibles
        items_count = inventory_page.get_inventory_items_count()
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
        login_page = LoginPage(driver)
        login_page.login("usuario_invalido", "contraseña_invalida")
        print("✅ Intentado login con credenciales inválidas")
        
        # Paso 4: Verificar que aparece un mensaje de error
        try:
            error_message = driver.find_element(*LoginPage.ERROR_MESSAGE)
            assert error_message.is_displayed(), "El mensaje de error no se muestra"
            print(f"✅ Mensaje de error mostrado: {error_message.text}")
        except:
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
        login_page = LoginPage(driver)
        login_page.enter_password("secret_sauce")
        login_page.click_login()
        print("✅ Intentado login sin ingresar usuario")
        
        # Paso 4: Verificar error
        try:
            error_message = driver.find_element(*LoginPage.ERROR_MESSAGE)
            assert error_message.is_displayed(), "El mensaje de error no se muestra"
            assert "username" in error_message.text.lower(), "El error no menciona el usuario"
            print(f"✅ Error validado: {error_message.text}")
        except:
            pytest.fail("No se encontró el mensaje de error para usuario requerido")
