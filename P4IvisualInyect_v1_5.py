# P4IvisualInyect.py - v1.5 - By P4IM0N - COOKIES - TOOL de scaneo de urls con parametros de inyecion optenidas con GOSPIDER y luego procesadas en navegador automaticamente con selenium y firefox para capturar las rutas y ejecuciones positivas de inyecciones XSS,LFI,RCE,SQL,y mas para luego agregar la captura a reportes del POC, ya se agrego el manejo de COOKIES comprobado las cuales las deben extraer con una extension de crhome y pasarlas a un archivo .json, en proxima actualizacion se añadira la inyeccion por metodo POST y el analisis de capturas de imagen con APIKEY de GPT y asi evitar aun mas los falsos positivos.

#--------------------------------------------------------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import requests
import time
import subprocess
from playsound import playsound
from tqdm import tqdm
import os
import pyautogui
import re
import hashlib
import platform
import json


#--------------------------------------------------------------------------------------------------------------------------------
# Defino colores
AZUL = "\033[34m"
ROJO = "\033[31m"
VIOLETA = "\033[35m"
AMARILLO = "\033[33m"
NARANJA_FUERTE = "\033[38;5;208m"
CIAN = "\033[36m"
MORADO = "\033[35m"
BLANCO = "\033[37m"
RESET = "\033[0m" 

#--------------------------------------------------------------------------------------------------------------------------------
banner = f'''
                        {BLANCO}⠄⠄⢀⣀⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣄⣀⠄⠄
                        ⠄⠠⣿⢿⣿⢿⣯⣿⣽⢯⣟⡿⣽⢯⣿⣽⣯⣿⣽⣟⣟⣗⠄
                        ⠄⢸⡻⠟⡚⡛⠚⠺⢟⣿⣗⣿⢽⡿⡻⠇⠓⠓⠓⠫⢷⢳⠄
                        ⠄⢼⡺⡽⣟⡿⣿⣦⡀⡈⣫⣿⡏⠁⢀⣰⣾⢿⣟⢟⢮⢱⡀
                        ⠄⣳⠑{RESET}{ROJO}⠝⠌⠊⠃⠃{RESET}{BLANCO}⢏⢆⣺⣿⣧⢘⠎{RESET}{ROJO}⠋⠊⠑⠨{RESET}{BLANCO}⠣⠑⣕⠂
                        ⠄⢷⣿⣯⣦⣶⣶⣶⡶⡯⣿⣿⡯⣟⣶⣶⣶⣶⣦⣧⣷⣾⠄
                        ⠄⢹⢻⢯⢟⣟⢿⢯⢿⡽⣯⣿⡯⣗⡿⡽⡯⣟⡯⣟⠯⡻⠂
                        ⠄⠢⡑⡑⠝⠜⣑⣭⠻⢝⠿⡿⡯⠫⠯⣭⣊⠪⢊⠢⢑⠰⠁
                        ⠄⠈⢹⣔⡘⢿⣿⣿⣶⠄⠁⠑⠈⠠⣵⣿⡿⡯⠂⣠⡞⡈⠄
                        ⠄⠄⠨⢻⡆⢄⣀⢩⠄⠄⠴⠕⠄⠄⠈⠉⣀⠠⢢⡟⢌⠄⠄
                        ⠄⠄⠈⠐⡝⣧⠈⡉⡙⢛⠛⠛⠛⠛⢋⠉⡀⡼⠩⡂⠁⠄⠄
                        ⠄⠄⠄⠄⠈⠪⡻⣔⣮⣷⡆⠄⢰⣿⢦⣣⢞⠅⠁⠄⠄⠄⠄
                        ⠄⠄⠄⠄⠄⠄⠈⠓⣷⣿⡅⠄⢸⣿⡗⠇⠁⠄⠄⠄⠄⠄⠄{RESET}

{CIAN}__________  _____ .___      .__                    .__  .___                            __   
\______   \/  |  ||   |__  _|__| ________ _______  |  | |   | ____ ___.__. ____   _____/  |_ 
 |     ___/   |  ||   \  \/ /  |/  ___/  |  \__  \ |  | |   |/    <   |  |/ __ \_/ ___\   __!
 |    |  /    ^   /   |\   /|  |\___ \|  |  // __ \|  |_|   |   |  \___  \  ___/\  \___|  |  
 |____|  \____   ||___| \_/ |__/____  >____/(____  /____/___|___|  / ____|\___  >\___  >__|  
              |__|                  \/           \/              \/\/         \/     \/{RESET}      
                                                                 {ROJO}by P4IM0N{RESET}'''
                                                                 
print(banner)                                                                 

#--------------------------------------------------------------------------------------------------------------------------------
def sonido_alerta():
    # Ruta al archivo de audio
    audio_file = "alerta.mp3"  
    playsound(audio_file)

#--------------------------------------------------------------------------------------------------------------------------------
def main():
    
    # solicitamos al usuario el dominio
    print('-----------------------------------------------------------------------')
    opcion = input(f'''|{MORADO}____________________MANITO ESCRIBI LA OPCION NUMERICA QUE QUERES:________________________________________{RESET}|
                       | {ROJO}1{RESET} - Busquemos URL con la SPIDER a partir de una URL que me des, (ejem: http://testphp.vulnweb.com/)             |
                       | {ROJO}2{RESET} - Ejecutar Inyeccion directamente en una URL en puntual que me des, (ejem: http://testphp.vulnweb.com/)       | 
                        {AMARILLO}----------->>{RESET}: ''')
    print('-----------------------------------------------------------------------')
    
    if opcion == '1':
        
        # solicitamos al usuario el dominio para el comando spider
        print('-----------------------------------------------------------------------')
        dominio_spider = input(f"{MORADO}Introduci el dominio completo Manito {RESET}(ejem: http://testphp.vulnweb.com/){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        print('-----------------------------------------------------------------------')
        payload_txt = input(f"{MORADO}Introduci el nombre de la lista de PAYLOAD TXT que tengas en este directorio o usaremos por defecto: {RESET}(ejem: listXSScodificadosYpoliglotasGITHUByGPT.txt){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        opcion_uno(dominio_spider,payload_txt)
    elif opcion == '2':
        # solicitamos al usuario el dominio unico
        print('-----------------------------------------------------------------------')
        dominio_unico = input(f"{MORADO}Introduci el dominio completo Manito ((AGREGA {AMARILLO}FUZZ{RESET} en el parametro puntual que quieres inyectar)) {RESET}(ejem: http://testphp.vulnweb.com/search?q={AMARILLO}FUZZ{RESET}&pp=53265){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        print('-----------------------------------------------------------------------')
        payload_txt = input(f"{MORADO}Introduci el nombre de la lista de PAYLOAD TXT que tengas en este directorio o usaremos por defecto: {RESET}(ejem: listXSScodificadosYpoliglotasGITHUByGPT.txt){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        opcion_dos(dominio_unico,payload_txt)
    else:
        # solicitamos al usuario una opcion correcta
        print('-----------------------------------------------------------------------')
        print(f"{MORADO}Introduci una opcion numerica correcta Manito {RESET}(ejem: 1){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
            

#--------------------------------------------------------------------------------------------------------------------------------
#OPCION 1:
def opcion_uno(dominio_spider,payload_txt):
    
    # nuevo comando especial para optener url con parametros inyectables y guardarlo con redirección a url.txt
    comando = f'gospider -s {dominio_spider} -c 10 -d 10 --blacklist ".(jpg|jpeg|gif|css|tif|tiff|png|ttf|woff|woff2|ico|pdf|svg|txt)" | grep -Eo "(http|https)://[^&]+\\?.*=" | awk \'!seen[$0]++\' | grep "^{dominio_spider}" > url.txt'
    
    print('-----------------------------------------------------------------------')
    print(f'{MORADO}COMANDO SPIDER: {comando}{RESET}')
    print('-----------------------------------------------------------------------')
    
    # Ejecuta el comando
    proceso_Gospider = subprocess.Popen(comando, shell=True)
    time.sleep(10)
    proceso_Gospider.wait()
    
    # Verifica el código de retorno
    if proceso_Gospider.returncode == 0:
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        print("GoSpider ejecutado con éxito Manito.")
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
    else:
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        print(f"{ROJO}Error al ejecutar GoSpider Manito.{RESET}")
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}') 
        
    # Asegurar que todas las URLs se han guardado
    time.sleep(6)  # Ajusta el tiempo si es necesario

    # Lee las URLs desde el archivo urls.txt
    with open('url.txt', 'r') as archivo_urls:
        urls_a_inyectar = archivo_urls.read().splitlines()
    
    # Muestra las URLs encontradas
    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
    print("URLs encontradas:")
    print(urls_a_inyectar)
    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')

    if not urls_a_inyectar:
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        print(f"{ROJO}No se encontraron URLs Manito. Verifica la ejecución de GoSpider.{RESET}")
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        return

#--------------------------------------------------------------------------------------------------------------------------------
    if payload_txt:
        with open(payload_txt, 'r', encoding='utf-8') as archivo_payloads_XSS:
            payloads_XSS = archivo_payloads_XSS.read().splitlines()
     
    else:
        with open('listXSScodificadosYpoliglotasGITHUByGPT.txt', 'r', encoding='utf-8') as archivo_payloads_XSS:
            payloads_XSS = archivo_payloads_XSS.read().splitlines()
        

#--------------------------------------------------------------------------------------------------------------------------------
    # Configura el controlador del navegador FIREFOX 
    firefox_options = Options()
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    # Crear el directorio de reportes si no existe
    if not os.path.exists('reportes'):
        os.makedirs('reportes')

    # Solicitar las cookies al usuario
    print('-----------------------------------------------------------------------')
    cookies_input = input(f"{MORADO}Creaste el archivo de cookies del usuario en formato JSON ?? RESP: {AMARILLO}s{RESET} / {ROJO}n{RESET} {RESET}(ejem: con extencion COOKIE EDITOR exportalas en JSON y asi las pegas en un archivo llamndolo cookies.json, por cualquier error tener en cuenta en el parametro SameSite porner en Lax){MORADO} : {RESET} ")
    print('-----------------------------------------------------------------------')
    
    if cookies_input == 's':
        # cargamos las cookies desde el archivo JSON
        with open('cookies.json', 'r') as f:
            user_cookies = json.load(f)
            
        # Solicitar las cookies al usuario
        print('-----------------------------------------------------------------------')
        dominio_base = input(f"{MORADO}Manito porfavor dame el DOMINIO BASE al que pertenesen las COOKIES asi termino de CONFIGURAR, (ejem: http://testphp.vulnweb.com/){MORADO} : {RESET} ")
        print('-----------------------------------------------------------------------')
            
        # Navegar a una página en blanco para configurar las cookies
        driver.get(dominio_base)
        
        # Modificar el valor de SameSite a 'Lax'
        for cookie in user_cookies:
            cookie['sameSite'] = 'Lax'
        
        for cookie in user_cookies:
            driver.add_cookie(cookie)

    total_payloads = len(urls_a_inyectar) * len(payloads_XSS)
    
    # >>>>> TU HEADER CUSTOM DE BUGHUNTER  <<<<<
    headers = {
        'X-HackerOne-Research': 'p4im0n'
    }

#--------------------------------------------------------------------------------------------------------------------------------
    with tqdm(total=total_payloads, desc="Ejecutando payloads") as pbar:
        for url_inyectada in urls_a_inyectar:
            for payload in payloads_XSS:
                try:
                    # realiza cada request osea cada solicitud con mi header custom de bug hunter
                    response = requests.get(url_inyectada + payload, headers=headers)
                    
                    # imprime los detalles de la solicitud
                    print(f"URL solicitada: {response.request.url}")
                    print(f"Método de solicitud: {response.request.method}")
                    print("Encabezados enviados:")
                    for key, value in response.request.headers.items():
                        print(f"{key}: {value}")

                    # imprime el cuerpo de la respuesta
                    print(f"Estado de la respuesta: {response.status_code}")
                    print(f"Cuerpo de la respuesta: {response.text[:500]}...")
                    
                    # verifica que se envio el header custom
                    if 'X-HackerOne-Research' in response.request.headers:
                        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
                        print(f"{MORADO}Header personalizado enviado: {response.request.headers['X-HackerOne-Research']}{RESET}")
                        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
                        
                    # si la solicitud fue exitosa, pasa la URL a selenium
                    if response.status_code == 200:
                        driver.get(url_inyectada + payload)
                        time.sleep(3)  # esperamos que la pagina se cargue completamente
                        # nombre del directorio de las capturas de firefox
                        directorio_capturas = 'capturas_web'

                        # creamos el directorio si no existe con el nombre que le definimos
                        os.makedirs(directorio_capturas, exist_ok=True)
                        
                        archivo_captura = re.sub(r'[^\w\-_\. ]', '_', url_inyectada) + ".png"
                        
                        # unimos la path osea ruta con el nombre del archivo de captura firefox
                        ruta_archivo = os.path.join(directorio_capturas, archivo_captura)

                        # Guardar la captura de pantalla en el directorio especificado
                        driver.save_screenshot(ruta_archivo)
                        print(f'{AZUL}- [{url_inyectada}]![ {payload} ] - captura]({archivo_captura}){RESET}')
                    else:
                        print(f'{NARANJA_FUERTE}Manito dio error la solicitud con {url_inyectada + payload} {RESET}')
                except Exception as e:
                    print(f'---------------------------{ROJO}-------------------{RESET}--------------------------------')
                    print(f'---------------------------{ROJO}-------------------{RESET}--------------------------------')
                    print(f'{VIOLETA}- [{url_inyectada}]![ {payload} ] - captura]({archivo_captura}){RESET}')
                    print(f'{ROJO}///POC///: {CIAN}COPIA aqui-->{RESET} {url_inyectada + payload} {CIAN}<--COPIA aqui{RESET} :{RESET}')
                    print(f'{ROJO}Fallo Manito o Tenemos un XSS Exitoso 8D :{RESET}  {AMARILLO}{url_inyectada}{RESET}: {ROJO}---SCRIPT EJECUTADO-->{RESET} {NARANJA_FUERTE}{payload}{RESET} {ROJO}-->{RESET} {CIAN}{e}{RESET}')
                    print(f'---------------------------{ROJO}-------------------{RESET}--------------------------------')
                    print(f'---------------------------{ROJO}-------------------{RESET}--------------------------------')
                    
                    # limito el largo del nombre del archivo captura de reporte vulnerable
                    max_length = 80
                    # genero un nombre de archivo basado en la URL y el payload
                    nombre_base_del_archivo = "{}_{}_VULNERABLE".format(re.sub(r'[^\w\-_\. ]', '_', url_inyectada), re.sub(r'[^\w\-_\. ]', '_', payload))
                    # acortar el nombre si excede el máximo
                    if len(nombre_base_del_archivo) > max_length:
                        nombre_final_del_archivo = nombre_base_del_archivo[:max_length]
                    
                    # Captura de pantalla del escritorio con payload POC VULNERABLE
                    captura_de_escritorio = f"reportes/{nombre_final_del_archivo}.png"

                    # captura de pantalla del escritorio payload exitoso
                    pyautogui.screenshot(captura_de_escritorio)

                    # sonido de alerta
                    sonido_alerta()
                
                # barra de progreso de payloads
                pbar.update(1)
    
    driver.quit()
    

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------    
#--------------------------------------------------------------------------------------------------------------------------------
#OPCION 2:
def opcion_dos(dominio_unico,payload_txt):
    
    # Muestra las URLs encontradas
    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
    print("URLs OBJETIVO:")
    print(dominio_unico)
    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')

    if not dominio_unico:
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        print(f"{ROJO}No se encontraron URLs Manito.{RESET}")
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        return

#--------------------------------------------------------------------------------------------------------------------------------
    if payload_txt:
        with open(payload_txt, 'r', encoding='utf-8') as archivo_payloads_XSS:
            payloads_XSS = archivo_payloads_XSS.read().splitlines()
     
    else:
        with open('listXSScodificadosYpoliglotasGITHUByGPT.txt', 'r', encoding='utf-8') as archivo_payloads_XSS:
            payloads_XSS = archivo_payloads_XSS.read().splitlines()       

#--------------------------------------------------------------------------------------------------------------------------------
    # Configura el controlador del navegador FIREFOX 
    firefox_options = Options()
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    # Crear el directorio de reportes si no existe
    if not os.path.exists('reportes'):
        os.makedirs('reportes')

    # Solicitar las cookies al usuario
    print('-----------------------------------------------------------------------')
    cookies_input = input(f"{MORADO}Creaste el archivo de cookies del usuario en formato JSON ?? RESP: {AMARILLO}s{RESET} / {ROJO}n{RESET} {RESET}(ejem: con extencion COOKIE EDITOR exportalas en JSON y asi las pegas en un archivo llamndolo cookies.json, por cualquier error tener en cuenta en el parametro SameSite porner en Lax){MORADO} : {RESET} ")
    print('-----------------------------------------------------------------------')
    
    if cookies_input == 's':
        # cargamos las cookies desde el archivo JSON
        with open('cookies.json', 'r') as f:
            user_cookies = json.load(f)
    
        # Solicitar las cookies al usuario
        print('-----------------------------------------------------------------------')
        dominio_base = input(f"{MORADO}Manito porfavor dame el DOMINIO BASE al que pertenesen las COOKIES asi termino de CONFIGURAR, (ejem: http://testphp.vulnweb.com/){MORADO} : {RESET} ")
        print('-----------------------------------------------------------------------')
            
        # Navegar a una página en blanco para configurar las cookies
        driver.get(dominio_base)
        
        # Modificar el valor de SameSite a 'Lax'
        for cookie in user_cookies:
            cookie['sameSite'] = 'Lax'
        
        for cookie in user_cookies:
            driver.add_cookie(cookie)
        driver.get(dominio_unico)
    
    total_payloads = 1 * len(payloads_XSS)
    
    # >>>>> TU HEADER CUSTOM DE BUGHUNTER  <<<<<
    headers = {
        'X-HackerOne-Research': 'p4im0n'
    }

#--------------------------------------------------------------------------------------------------------------------------------
    with tqdm(total=total_payloads, desc="Ejecutando payloads") as pbar:
        
        for payload in payloads_XSS:
            dominio_fuzz_payload = dominio_unico.replace('FUZZ', payload)
            print(dominio_fuzz_payload)
            
            try:
                
                # realiza cada request osea cada solicitud con mi header custom de bug hunter
                response = requests.get(dominio_fuzz_payload, headers=headers)
                
                # imprime los detalles de la solicitud
                print(f"URL solicitada: {response.request.url}")
                print(f"Método de solicitud: {response.request.method}")
                print("Encabezados enviados:")
                for key, value in response.request.headers.items():
                    print(f"{key}: {value}")

                # imprime el cuerpo de la respuesta
                print(f"Estado de la respuesta: {response.status_code}")
                print(f"Cuerpo de la respuesta: {response.text[:500]}...")
                
                # verifica que se envio el header custom
                if 'X-HackerOne-Research' in response.request.headers:
                    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
                    print(f"{MORADO}Header personalizado enviado: {response.request.headers['X-HackerOne-Research']}{RESET}")
                    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
                    
                # si la solicitud fue exitosa, pasa la URL a selenium
                if response.status_code == 200:
                    
                    driver.get(dominio_fuzz_payload)
                    time.sleep(3)  # esperamos que la pagina se cargue completamente
                    
                    # nombre del directorio de las capturas de firefox
                    directorio_capturas = 'capturas_web'

                    # creamos el directorio si no existe con el nombre que le definimos
                    os.makedirs(directorio_capturas, exist_ok=True)
                    
                    archivo_captura = re.sub(r'[^\w\-_\. ]', '_', dominio_fuzz_payload) + ".png"
                    
                    # unimos la path osea ruta con el nombre del archivo de captura firefox
                    ruta_archivo = os.path.join(directorio_capturas, archivo_captura)

                    # Guardar la captura de pantalla en el directorio especificado
                    driver.save_screenshot(ruta_archivo)
                    print(f'{AZUL}- [{dominio_fuzz_payload}]![ {payload} ] - captura]({archivo_captura}){RESET}')
                
                else:
                    print(f'{NARANJA_FUERTE}Manito dio error la solicitud con {dominio_fuzz_payload + payload} {RESET}')
            
            except Exception as e:
                print(f'---------------------------{ROJO}-------------------{RESET}--------------------------------')
                print(f'---------------------------{ROJO}-------------------{RESET}--------------------------------')
                print(f'{VIOLETA}- [{dominio_fuzz_payload}]![ {payload} ] - captura]({archivo_captura}){RESET}')
                print(f'{ROJO}///POC///: {CIAN}COPIA aqui-->{RESET} {dominio_fuzz_payload + payload} {CIAN}<--COPIA aqui{RESET} :{RESET}')
                print(f'{ROJO}Fallo Manito o Tenemos un XSS Exitoso 8D :{RESET}  {AMARILLO}{dominio_fuzz_payload}{RESET}: {ROJO}---SCRIPT EJECUTADO-->{RESET} {NARANJA_FUERTE}{payload}{RESET} {ROJO}-->{RESET} {CIAN}{e}{RESET}')
                print(f'---------------------------{ROJO}-------------------{RESET}--------------------------------')
                print(f'---------------------------{ROJO}-------------------{RESET}--------------------------------')
                
                # limito el largo del nombre del archivo captura de reporte vulnerable
                max_length = 80
                # genero un nombre de archivo basado en la URL y el payload
                nombre_base_del_archivo = "{}_{}_VULNERABLE".format(re.sub(r'[^\w\-_\. ]', '_', dominio_fuzz_payload), re.sub(r'[^\w\-_\. ]', '_', payload))
                # acortar el nombre si excede el máximo
                if len(nombre_base_del_archivo) > max_length:
                    nombre_final_del_archivo = nombre_base_del_archivo[:max_length]
                
                # Captura de pantalla del escritorio con payload POC VULNERABLE
                captura_de_escritorio = f"reportes/{nombre_final_del_archivo}.png"

                # captura de pantalla del escritorio payload exitoso
                pyautogui.screenshot(captura_de_escritorio)

                # sonido de alerta
                sonido_alerta()
            
            # barra de progreso de payloads
            pbar.update(1)
    
    driver.quit()    

#--------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        print('Gracias Manito por usar P4IvisualInyect_v1.4.py ')
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        exit()
        
#-------------------------------------------------------------------------------------------------------------------------------- 
