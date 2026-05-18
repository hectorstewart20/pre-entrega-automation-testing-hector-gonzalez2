from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver          #Importamos la librería que permite controlar el navegador
import time                             #Para hacer pausas visibles (solo demo)

driver = webdriver.Chrome()             #Creamos la instancia del driver → abre una ventana de Chrome vacía

try:
    driver.get('https://www.saucedemo.com')  #Navegamos a la URL de Sauce Demo (pantalla de login)
    driver.find_element(By.ID, 'user-name').send_keys('standard_user')
    driver.find_element(By.ID, 'password').send_keys('secret_sauce')
    driver.find_element(By.ID, 'login-button').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'inventory_list')))
    print('Título:', driver.title)      #Leemos el título de la pestaña → debería salir "Swag Labs"
    assert driver.title == 'Swag Labs'  #Validamos que el título sea el esperado (asegura que cargó bien)

    time.sleep(20)                       #Pausa de 2 s para que lo veas (luego la quitaremos)
finally:
    driver.quit()                       #Cierre limpio: mata la sesión y la ventana