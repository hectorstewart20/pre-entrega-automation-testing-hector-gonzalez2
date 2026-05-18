"""
saucedemo_pages.py - Localizadores y funciones auxiliares para SauceDemo
Contiene clases con localizadores (By) y funciones para interactuar con elementos.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Localizadores y métodos para la página de login"""
    
    # Localizadores
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message-container")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def enter_username(self, username):
        """Ingresa el nombre de usuario"""
        username_field = self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        username_field.clear()
        username_field.send_keys(username)
    
    def enter_password(self, password):
        """Ingresa la contraseña"""
        password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_field.clear()
        password_field.send_keys(password)
    
    def click_login(self):
        """Hace clic en el botón de login"""
        login_button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_button.click()
    
    def login(self, username, password):
        """Realiza el flujo completo de login"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()


class InventoryPage:
    """Localizadores y métodos para la página de inventario"""
    
    # Localizadores
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    INVENTORY_TITLE = (By.CLASS_NAME, "title")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(@data-test, 'add-to-cart')]")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    BURGER_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    PRODUCT_SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def is_inventory_page_loaded(self):
        """Verifica que la página de inventario está cargada"""
        try:
            self.wait.until(EC.visibility_of_element_located(self.INVENTORY_ITEMS))
            return True
        except:
            return False
    
    def get_inventory_items_count(self):
        """Obtiene la cantidad de productos visibles"""
        items = self.driver.find_elements(*self.INVENTORY_ITEMS)
        return len(items)
    
    def add_product_to_cart(self):
        """Añade el primer producto al carrito"""
        add_button = self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON))
        add_button.click()
    
    def get_cart_badge_count(self):
        """Obtiene el contador del carrito"""
        try:
            badge = self.wait.until(EC.visibility_of_element_located(self.SHOPPING_CART_BADGE))
            return badge.text
        except:
            return None
    
    def click_shopping_cart(self):
        """Hace clic en el carrito de compras"""
        cart_link = self.wait.until(EC.element_to_be_clickable(self.SHOPPING_CART_LINK))
        cart_link.click()
    
    def logout(self):
        """Realiza el logout"""
        burger_menu = self.wait.until(EC.element_to_be_clickable(self.BURGER_MENU_BUTTON))
        burger_menu.click()
        logout_link = self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK))
        logout_link.click()


class CartPage:
    """Localizadores y métodos para la página del carrito"""
    
    # Localizadores
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def is_cart_page_loaded(self):
        """Verifica que la página del carrito está cargada"""
        try:
            self.wait.until(EC.visibility_of_element_located(self.CART_ITEMS))
            return True
        except:
            return False
    
    def get_cart_items_count(self):
        """Obtiene la cantidad de productos en el carrito"""
        items = self.driver.find_elements(*self.CART_ITEMS)
        return len(items)
    
    def get_cart_item_names(self):
        """Obtiene los nombres de todos los productos en el carrito"""
        items = self.driver.find_elements(*self.CART_ITEM_NAME)
        return [item.text for item in items]
