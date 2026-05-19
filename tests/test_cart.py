"""
test_cart.py - Pruebas de funcionalidad del carrito de compras
Casos de prueba para validar la adición, visualización y gestión del carrito.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException
# Reemplazado POM por selectores inline: ya no se importa utils.saucedemo_pages


class TestCart:
    """Casos de prueba para la funcionalidad del carrito de compras"""
    
    def _login_and_go_to_inventory(self, driver, base_url, valid_credentials):
        """
        Método auxiliar para realizar login y navegar al inventario
        """
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)

        username_field = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
        username_field.clear()
        username_field.send_keys(valid_credentials["username"])

        password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        password_field.clear()
        password_field.send_keys(valid_credentials["password"])

        login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
        login_button.click()

        # Esperar a que se cargue la página de inventario
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item")))
        print("✅ Login completado - Página de inventario cargada")

        return driver

def wait_for_cart_page(driver, timeout=10):
    """Esperar de forma robusta a que la página del carrito se considere cargada.
    Acepta cualquiera de estas señales: existencia de `cart_item`, contenedor `cart_contents_container`, o URL que contenga 'cart'.
    """
    end = time.time() + timeout
    while time.time() < end:
        try:
            if driver.find_elements(By.CLASS_NAME, "cart_item"):
                return
            if driver.find_elements(By.ID, "cart_contents_container"):
                return
            if "cart" in driver.current_url:
                return
        except Exception:
            pass
        time.sleep(0.5)
    raise TimeoutException("La página del carrito no se cargó dentro del timeout")

def open_burger_and_click_logout(driver, wait, retries=3):
    """Intentar abrir el menú burger y hacer logout con reintentos y fallback JS."""
    for _ in range(retries):
        try:
            burger = wait.until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn")))
            burger.click()
            logout = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link")))
            logout.click()
            return
        except Exception:
            time.sleep(0.5)
    # Fallback: intentar con JS
    try:
        driver.execute_script("document.getElementById('react-burger-menu-btn').click();")
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))).click()
        return
    except Exception:
        raise

def wait_for_login_page(driver, base_url, timeout=10):
    """Esperar señales de la página de login: botón `login-button`, campo `user-name` o URL raíz."""
    end = time.time() + timeout
    while time.time() < end:
        try:
            if driver.find_elements(By.ID, "login-button"):
                return
            if driver.find_elements(By.ID, "user-name"):
                return
            if driver.current_url.rstrip('/') == base_url.rstrip('/'):
                return
        except Exception:
            pass
        time.sleep(0.5)
    raise TimeoutException("La página de login no se detectó dentro del timeout")
    
    def test_agregar_producto_al_carrito(self, driver, base_url, valid_credentials):
        """
        Caso de prueba: Agregar un producto al carrito
        Objetivo: Validar que se puede añadir un producto al carrito correctamente
        
        Pasos:
        1. Realizar login
        2. Hacer clic en el botón "Add to cart" del primer producto
        3. Verificar que aparece el badge del carrito con el contador
        4. Validar que el contador muestra "1"
        """
        # Paso 1: Realizar login
        driver = self._login_and_go_to_inventory(driver, base_url, valid_credentials)

        # Paso 2: Agregar el primer producto al carrito
        first_product_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        add_buttons = driver.find_elements(By.XPATH, "//button[contains(@data-test, 'add-to-cart')]")
        if add_buttons:
            add_buttons[0].click()
        print(f"✅ Botón 'Add to cart' presionado para: {first_product_name}")

        # Paso 3-4: Verificar que el badge del carrito aparece y muestra "1"
        try:
            badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
            badge_count = badge.text
        except:
            badge_count = None
        assert badge_count == "1", f"Se esperaba contador '1' pero se encontró '{badge_count}'"
        print(f"✅ Badge del carrito muestra correctamente: {badge_count} producto(s)")
    
    def test_agregar_multiples_productos_al_carrito(self, driver, base_url, valid_credentials):
        """
        Caso de prueba: Agregar múltiples productos al carrito
        Objetivo: Validar que se pueden añadir varios productos y el contador se incrementa
        
        Pasos:
        1. Realizar login
        2. Agregar tres productos al carrito
        3. Verificar que el contador del carrito es "3"
        """
        # Paso 1: Realizar login
        driver = self._login_and_go_to_inventory(driver, base_url, valid_credentials)

        # Paso 2: Agregar tres productos
        add_buttons = driver.find_elements(By.XPATH, "//button[contains(@data-test, 'add-to-cart')]")
        for i in range(min(3, len(add_buttons))):
            add_buttons[i].click()
            print(f"✅ Producto {i+1} agregado al carrito")

        # Paso 3: Verificar contador
        try:
            badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
            badge_count = badge.text
        except:
            badge_count = None
        assert badge_count == "3", f"Se esperaba '3' productos pero el contador muestra '{badge_count}'"
        print(f"✅ Contador del carrito validado: {badge_count} productos")
    
    def test_navegar_al_carrito_y_verificar_producto(self, driver, base_url, valid_credentials):
        """
        Caso de prueba: Navegar al carrito y verificar que contiene el producto
        Objetivo: Validar que al navegar al carrito, el producto añadido está presente
        
        Pasos:
        1. Realizar login
        2. Agregar un producto al carrito
        3. Hacer clic en el ícono del carrito
        4. Verificar que la página del carrito se cargó
        5. Validar que el producto está en el carrito
        """
        # Paso 1: Realizar login
        driver = self._login_and_go_to_inventory(driver, base_url, valid_credentials)

        # Paso 2: Agregar un producto
        first_product_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        add_buttons = driver.find_elements(By.XPATH, "//button[contains(@data-test, 'add-to-cart')]")
        if add_buttons:
            add_buttons[0].click()
        print(f"✅ Producto agregado: {first_product_name}")

        # Paso 3: Navegar al carrito
        cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_link.click()
        print("✅ Se hizo clic en el carrito de compras")

        # Paso 4: Verificar que la página del carrito se cargó (robusto)
        wait_for_cart_page(driver, timeout=10)
        print("✅ Página del carrito cargada correctamente")

        # Paso 5: Validar que el producto está en el carrito
        items = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        cart_items = [i.text for i in items]
        assert first_product_name in cart_items, f"El producto '{first_product_name}' no está en el carrito"
        print(f"✅ Producto validado en carrito: {first_product_name}")
    
    def test_cantidad_de_articulos_en_carrito(self, driver, base_url, valid_credentials):
        """
        Caso de prueba: Verificar cantidad de artículos en el carrito
        Objetivo: Validar que la cantidad de artículos en la página del carrito coincide
        
        Pasos:
        1. Realizar login
        2. Agregar dos productos
        3. Navegar al carrito
        4. Verificar que hay 2 productos en el carrito
        """
        # Paso 1: Realizar login
        driver = self._login_and_go_to_inventory(driver, base_url, valid_credentials)

        # Paso 2: Agregar dos productos
        add_buttons = driver.find_elements(By.XPATH, "//button[contains(@data-test, 'add-to-cart')]")
        for i in range(2):
            add_buttons[i].click()
        print("✅ Dos productos agregados al carrito")

        # Paso 3: Navegar al carrito
        cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_link.click()
        # Esperar al carrito: puede estar vacío (sin cart_item). Intentar comprobaciones robustas.
        wait_for_cart_page(driver, timeout=10)

        # Paso 4: Verificar cantidad de productos
        items = driver.find_elements(By.CLASS_NAME, "cart_item")
        items_count = len(items)
        assert items_count == 2, f"Se esperaban 2 productos en el carrito pero hay {items_count}"
        print(f"✅ Cantidad de productos en el carrito validada: {items_count}")
    
    def test_carrito_vacio_al_iniciar(self, driver, base_url, valid_credentials):
        """
        Caso de prueba: Verificar que el carrito está vacío al iniciar
        Objetivo: Validar que no hay badge visible cuando no hay productos
        
        Pasos:
        1. Realizar login
        2. Verificar que NO existe el badge del carrito (carrito vacío)
        3. Navegar al carrito
        4. Validar que está vacío
        """
        # Paso 1: Realizar login
        driver = self._login_and_go_to_inventory(driver, base_url, valid_credentials)

        # Paso 2: Verificar que no existe badge
        try:
            badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
            badge_count = badge.text
        except:
            badge_count = None
        assert badge_count is None, f"Se esperaba que el carrito estuviera vacío pero muestra '{badge_count}'"
        print("✅ Carrito vacío al iniciar - No hay badge visible")

        # Paso 3: Navegar al carrito
        cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_link.click()
        wait_for_cart_page(driver, timeout=10)
        print("✅ Página del carrito cargada")

        # Paso 4: Validar que está vacío
        items = driver.find_elements(By.CLASS_NAME, "cart_item")
        items_count = len(items)
        assert items_count == 0, f"Se esperaba 0 productos pero hay {items_count}"
        print(f"✅ Carrito validado vacío: {items_count} productos")
    
    def test_flujo_completo_login_carrito_logout(self, driver, base_url, valid_credentials):
        """
        Caso de prueba: Flujo completo - Login, agregar producto, carrito y logout
        Objetivo: Validar el flujo completo del usuario desde login hasta logout
        
        Pasos:
        1. Realizar login
        2. Agregar un producto al carrito
        3. Navegar al carrito
        4. Verificar el producto
        5. Realizar logout
        6. Verificar que volvemos a la página de login
        """
        # Paso 1: Realizar login
        driver = self._login_and_go_to_inventory(driver, base_url, valid_credentials)
        print("✅ Flujo iniciado: Login completado")

        # Paso 2: Agregar producto
        first_product_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        add_buttons = driver.find_elements(By.XPATH, "//button[contains(@data-test, 'add-to-cart')]")
        if add_buttons:
            add_buttons[0].click()
        print(f"✅ Producto agregado: {first_product_name}")

        # Paso 3: Navegar al carrito
        cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_link.click()
        wait = WebDriverWait(driver, 10)
        from selenium.common.exceptions import TimeoutException
        try:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cart_item")))
        except TimeoutException:
            try:
                wait.until(EC.visibility_of_element_located((By.ID, "cart_contents_container")))
            except TimeoutException:
                wait.until(lambda d: "cart" in d.current_url)
        print("✅ Carrito visualizado")

        # Paso 4: Verificar producto
        items = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        cart_items = [i.text for i in items]
        assert first_product_name in cart_items, "Producto no está en carrito"
        print(f"✅ Producto verificado en carrito: {first_product_name}")

        # Paso 5: Volver a inventario y realizar logout
        driver.find_element(By.ID, "continue-shopping").click()
        # logout (con reintentos y fallback)
        open_burger_and_click_logout(driver, wait)
        print("✅ Logout realizado")

        # Paso 6: Verificar que estamos en la página de login
        wait_for_login_page(driver, base_url, timeout=12)
        print("✅ Flujo completado correctamente - Página de login verificada")
