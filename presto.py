from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

driver_path = "C:/Users/Cobos/OneDrive/Documentos/chromedriver-win64/chromedriver.exe"
service = Service(driver_path)

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(service=service, options=options)
try:
    print("Iniciando automatización de Presto")  
    presto_url = "https://www.presto.com.pe/"
    driver.get(presto_url)
    print(f"Página de Presto cargada: {presto_url}")
   
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceptar')]"))
        )
        cookie_button.click()
        print("Cookies aceptadas")
    except:
        print(" No se encontró botón de cookies")
    try:
        carta_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "comp-lv2guaz13label"))
        )
        carta_button.click()
        print(" Clic en 'Carta' exitoso (por ID)")     
    except Exception as e:
        print(f"Error al hacer clic por ID: {str(e)}. Intentando con class...")
        try: 
            carta_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "JS78Uv"))
            )
            carta_button.click()
            print("Clic en 'Carta' exitoso (por class)")
        except Exception as e:
            print(f"Error al hacer clic por class: {str(e)}. Intentando con XPath combinado...")
            try:
                
                carta_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='comp-lv2guaz13label' and contains(@class, 'JS78Uv')]"))
                )
                carta_button.click()
                print("Clic en 'Carta' exitoso (por XPath combinado)")
            except Exception as e:
                print(f"Error crítico: No se pudo encontrar 'Carta'. Detalle: {str(e)}")
                driver.save_screenshot("error_carta.png")
                print("Captura de pantalla guardada como 'error_carta.png'")   
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Entradas') or contains(text(), 'Platos Principales')]"))
        )
        print("Confirmación: Se cargó la sección de la carta")
    except:
        print("Advertencia: No se pudo confirmar la carga de la carta") 
    
    print("Esperando 15 segundos antes de cerrar...")
    time.sleep(15)
    
except Exception as e:
    print(f"Error crítico general: {str(e)}")
    driver.save_screenshot("error_general.png")
    
finally:
    driver.quit()
    print("Navegador cerrado correctamente")