"""
test_navigation.py - Pruebas de navegación y visualización del catálogo
Casos de prueba para validar la correcta presentación del catálogo de productos.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.saucedemo_pages import LoginPage, InventoryPage


class TestNavigation:
    """Casos de prueba para la navegación del catálogo de productos"""
    
    def setup_method(self, method):
        """
        Preparación para cada test: realizar login
        Este método se ejecuta antes de cada caso de prueba
        """
        self.setup_done = False
    
    def _login_and_go_to_inventory(self, driver, base_url, valid_credentials):
        """
        Método auxiliar para realizar login y navegar al inventario
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        login_page.login(valid_credentials["username"], valid_credentials["password"])
        
        # Esperar a que se cargue la página de inventario
        inventory_page = InventoryPage(driver)
        assert inventory_page.is_inventory_page_loaded(), "La página de inventario no se cargó"
        print("✅ Login completado - Página de inventario cargada")
        
        return inventory_page
    
    def test_inventario_page_loaded(self, driver, base_url, valid_credentials):
        """
        Caso de prueba: Verificación de carga de página de inventario
        Objetivo: Validar que después del login, la página de inventario se carga correctamente
        
        Pasos:
        1. Realizar login con credenciales válidas
        2. Verificar que se cargó la página de inventario
        3. Validar que el título de la página sea "Products"
        """
        # Pasos 1-2: Realizar login
        inventory_page = self._login_and_go_to_inventory(driver, base_url, valid_credentials)
        
        # Paso 3: Validar el título de la página
        page_title = driver.find_element(By.CLASS_NAME, "title").text
        assert page_title == "Products", f"El título esperado es 'Products' pero se encontró '{page_title}'"
        print(f"✅ Título de página validado: '{page_title}'")
    
    def test_productos_visibles_en_catalogo(self, driver, base_url, valid_credentials):
        """
        Caso de prueba: Verificación de productos visibles
        Objetivo: Validar que hay productos visibles en el catálogo
        
        Pasos:
        1. Realizar login
        2. Verificar que al menos hay 1 producto visible
        3. Verificar que hay múltiples productos (la página tiene 6 por defecto)
        4. Validar que cada producto tiene nombre y precio
        """
        # Pasos 1: Realizar login
        inventory_page = self._login_and_go_to_inventory(driver, base_url, valid_credentials)
        
        # Paso 2: Verificar cantidad de productos
        items_count = inventory_page.get_inventory_items_count()
        assert items_count >= 1, "No hay productos visibles en el catálogo"
        print(f"✅ Se encontraron {items_count} productos en el catálogo")
        
        # Paso 3: Verificar que hay múltiples productos
        assert items_count >= 6, f"Se esperaban al menos 6 productos, se encontraron {items_count}"
        print(f"✅ El catálogo contiene el número esperado de productos: {items_count}")
        
        # Paso 4: Validar que cada producto tiene nombre y precio
        items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        for idx, item in enumerate(items, 1):
            product_name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            product_price = item.find_element(By.CLASS_NAME, "inventory_item_price").text
            
            assert product_name, f"Producto {idx} no tiene nombre"
            assert product_price, f"Producto {idx} no tiene precio"
            print(f"  ✓ Producto {idx}: {product_name} - {product_price}")
        
        print("✅ Todos los productos tienen nombre y precio validados")
    
    def test_interfaz_tiene_elementos_importantes(self, driver, base_url, valid_credentials):
        """
        Caso de prueba: Verificación de elementos importantes de la interfaz
        Objetivo: Validar que los elementos principales de la interfaz estén presentes
        
        Pasos:
        1. Realizar login
        2. Verificar presencia del menú hamburguesa
        3. Verificar presencia del carrito de compras
        4. Verificar presencia del selector de ordenamiento
        """
        # Paso 1: Realizar login
        inventory_page = self._login_and_go_to_inventory(driver, base_url, valid_credentials)
        
        # Paso 2: Verificar menú hamburguesa
        burger_menu = driver.find_element(By.ID, "react-burger-menu-btn")
        assert burger_menu.is_displayed(), "El menú hamburguesa no está visible"
        print("✅ Menú hamburguesa está visible")
        
        # Paso 3: Verificar carrito de compras
        shopping_cart = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        assert shopping_cart.is_displayed(), "El carrito de compras no está visible"
        print("✅ Carrito de compras está visible")
        
        # Paso 4: Verificar selector de ordenamiento
        sort_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
        assert sort_dropdown.is_displayed(), "El selector de ordenamiento no está visible"
        print("✅ Selector de ordenamiento está visible")
        
        print("✅ Todos los elementos importantes de la interfaz están presentes")
    
    def test_navegacion_con_click_en_producto(self, driver, base_url, valid_credentials):
        """
        Caso de prueba: Navegación al detalle de un producto
        Objetivo: Validar que se puede ver el detalle de un producto
        
        Pasos:
        1. Realizar login
        2. Hacer clic en el nombre de un producto
        3. Verificar que se abre la página de detalle del producto
        4. Validar que la página de detalle contiene información del producto
        """
        # Pasos 1: Realizar login
        inventory_page = self._login_and_go_to_inventory(driver, base_url, valid_credentials)
        
        # Paso 2: Hacer clic en el nombre del primer producto
        first_product = driver.find_element(By.CLASS_NAME, "inventory_item_name")
        product_name = first_product.text
        first_product.click()
        print(f"✅ Se hizo clic en el producto: {product_name}")
        
        # Paso 3: Verificar que se abrió la página de detalle
        wait = WebDriverWait(driver, 10)
        back_button = wait.until(EC.visibility_of_element_located((By.ID, "back-to-products")))
        assert back_button.is_displayed(), "No se abrió la página de detalle del producto"
        print("✅ Página de detalle del producto cargada")
        
        # Paso 4: Validar información del producto
        detail_name = driver.find_element(By.CLASS_NAME, "inventory_details_name").text
        detail_price = driver.find_element(By.CLASS_NAME, "inventory_details_price").text
        
        assert detail_name == product_name, "El nombre del producto no coincide"
        assert detail_price, "El precio del producto no está disponible"
        print(f"✅ Información del producto validada: {detail_name} - {detail_price}")
        
        # Volver a la página de inventario
        back_button.click()
        inventory_page.is_inventory_page_loaded()
        print("✅ Vuelto a la página de inventario")
