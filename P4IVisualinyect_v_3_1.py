# P4IvisualInyect.py - v3.1 - By P4IM0N - COOKIES - TOOL de escaneo de URLs con parámetros de inyección obtenidas con GOSPIDER y luego procesadas en navegador automáticamente con Selenium y Firefox para capturar las rutas y ejecuciones positivas de inyecciones XSS, LFI, RCE, SQL, por método GET y se añadió recientemente por POST para luego agregar la captura a reportes del POC, y analizar capturas de pantalla usando OCR Space API para análisis de vulnerabilidad (https://ocr.space/ocrapi) deben cargar su API permite mail temporal el sitio ;D, se le sumo inyeccion de headers y notificacion por mensaje sobre vulnerabilidad enconrada y captura de pantalla a traves de bot de telegram

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
import requests
import sys
import select
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
import base64


#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
# Defino colores para el texto en la consola
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
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
# Banner que se muestra al iniciar el script
banner = f'''
                        {BLANCO}⠄⠄⢀⣀⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣄⣀⠄⠄
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
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#Funcion para reproducir el sonido de alerta

def sonido_alerta(sonido):
    # segun la situacion sonido a reproducirse
    if sonido == 'bienvenida':
        audio = 'pip.mp3'
        voz = 'bienvenida.mp3'
    elif sonido == 'sql':
        audio = 'sonido_alarma_sql.mp3'
        voz = 'posible_sql.mp3'
    elif sonido == 'xss':
        audio = 'sonido_alarma_xss.mp3'
        voz = 'posible_xss.mp3'
    elif sonido == 'comando':
        audio = 'sonido_alarma_ejecucion_de_comandos.mp3'
        voz = 'posible_ejecucion_de_comandos.mp3'
    elif sonido == 'lfi':
        audio = 'sonido_alarma_lfi.mp3'
        voz = 'posible_lfi.mp3'
    elif sonido == 'uno': #---
        audio = 'pip.mp3'
        voz = 'opcion_uno.mp3'
    elif sonido == 'dos':
        audio = 'pip.mp3'
        voz = 'opcion_dos.mp3'
    elif sonido == 'tres':
        audio = 'pip.mp3'
        voz = 'opcion_tres.mp3'
    elif sonido == 'cuatro':
        audio = 'pip.mp3'
        voz = 'opcion_cuatro.mp3'
    elif sonido == 'novalido':
        audio = 'pip.mp3'
        voz = 'opcion_novalida.mp3'
    elif sonido == 'hunter':
        audio = 'pip.mp3'
        voz = 'bug_hunter.mp3'                                
    #Reproduccion de los sonidos  
    playsound(audio)  # Reproduce el archivo de sonido para alertar al usuario
    time.sleep(2)
    playsound(voz)

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
# Función para analizar una captura de pantalla en busca de errores utilizando OCR Space API

def analizar_captura(payload,file_path):
    api_key = "TU_API_KEY_DE_OCR_SPACE"  # Reemplazar con tu API Key de OCR Space
    with open(file_path, "rb") as f:
        image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")
    
    # Realizar la solicitud POST a OCR Space
    url = "https://api.ocr.space/parse/image"
    headers = {
        "apikey": api_key
    }
    data = {
        "base64Image": f"data:image/png;base64,{image_base64}",
        "language": "eng"
    }
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        result = response.json()
        parsed_text = result.get("ParsedResults", [{}])[0].get("ParsedText", "")
        print(f'------------------------------------------------------------------------------')
        print(f"{AZUL}Texto detectado en la imagen utilizando OCR Space API:{RESET}\n{parsed_text}")
        print(f'------------------------------------------------------------------------------')
        
#--------------------------------------------------------------------------------------------------------------------------------

        #Lista de patrones de errores comunes
        patrones = r"\b(sql syntax|database error|syntax error|command not found|unrecognized command|xss detected|csrf token error|unauthorized access|file not found|segmentation fault|buffer overflow|invalid input|lfi detected|rfi detected|shell injection|unauthorized shell access|directory traversal detected|server misconfiguration|soap fault)\b"

        #Lista de patrones de ejecuciones exitosas
        indicadores_exitosos = [
            r"\b(root|root:x|user:x|daemon:x|admin|uid=\d+|gid=\d+|/bin/bash|flag{.+}|whoami)\b",  #Comandos
            r"<.*script.*>",  #XSS
            r"SELECT.*FROM|INSERT.*INTO|UPDATE.*SET|DELETE.*FROM",  #SQL
            r"/etc/passwd|/etc/shadow|/home/|/root",  #LFI/RFI
        ]

        # Buscar patrones de error en el texto
        coincidencias = re.findall(patrones, parsed_text, re.IGNORECASE)

        # Buscar ejecuciones exitosas específicas
        coincidencias_exitosas = []
        for indicador in indicadores_exitosos:
            if re.search(indicador, parsed_text, re.IGNORECASE):
                coincidencias_exitosas.append(indicador)

#--------------------------------------------------------------------------------------------------------------------------------

        # Verificar y mostrar cada tipo de vulnerabilidad por separado
        if coincidencias:
            
            print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
            print(f'---------------------------{ROJO}------///ATENCION///------{RESET}--------------------------------')
            print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')

            if re.search(r"\b(sql syntax|database error|sql error|invalid query)\b", parsed_text, re.IGNORECASE):
                print(f"{ROJO}ALERTA: Posible vulnerabilidad de inyección SQL detectada.{RESET}")
                vulnerabilidad = 'sql'
                sonido_alerta(vulnerabilidad)
                #cuando se detecta una vulnerabilidad o  excepcion envia notificacion por TELEGRAM
                enviar_mensaje_telegram(vulnerabilidad, payload, response.request.url, file_path)

            if re.search(r"\b(command not found|shell error|unrecognized command|shell injection|unauthorized shell access)\b", parsed_text, re.IGNORECASE):
                print(f"{ROJO}ALERTA: Posible inyección de comandos detectada.{RESET}")
                vulnerabilidad = 'comando'
                sonido_alerta(vulnerabilidad)
                #cuando se detecta una vulnerabilidad o  excepcion envia notificacion por TELEGRAM
                enviar_mensaje_telegram(vulnerabilidad, payload, response.request.url, file_path)

            if re.search(r"\b(xss detected|cross-site scripting|<.*script.*>)\b", parsed_text, re.IGNORECASE):
                print(f"{ROJO}ALERTA: Posible ejecución de XSS detectada.{RESET}")
                vulnerabilidad = 'xss'
                sonido_alerta(vulnerabilidad)
                #cuando se detecta una vulnerabilidad o  excepcion envia notificacion por TELEGRAM
                enviar_mensaje_telegram(vulnerabilidad, payload, response.request.url, file_path)

            if re.search(r"\b(lfi detected|rfi detected|file disclosure|directory traversal)\b", parsed_text, re.IGNORECASE):
                print(f"{ROJO}ALERTA: Posible vulnerabilidad de LFI/RFI detectada.{RESET}")
                vulnerabilidad = 'lfi'
                sonido_alerta(vulnerabilidad)
                #cuando se detecta una vulnerabilidad o  excepcion envia notificacion por TELEGRAM
                enviar_mensaje_telegram(vulnerabilidad, payload, response.request.url, file_path)

        # Verificar y mostrar las coincidencias de ejecuciones exitosas
        if coincidencias_exitosas:
            
            print(f"{ROJO}ALERTA: Ejecuciones exitosas detectadas.{RESET}")
            for indicador in coincidencias_exitosas:
                if re.search(indicador, parsed_text, re.IGNORECASE):
                    print(f"{ROJO}- {re.search(indicador, parsed_text).group()}{RESET}")

                print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
        else:
            print(f'{AMARILLO}------------------------------------------------------------------------------{RESET}')
            print(f'               LA CAPTURA NO PRESENTA VULNERABILIDAD EXPLOTADA MANITO                         ')
            print(f'{AMARILLO}------------------------------------------------------------------------------{RESET}')
    else:
        print(f'---------------------------{AMARILLO}-------------------{RESET}--------------------------------')
        print(f"{AMARILLO}Error al analizar la imagen. Código de estado: {response.status_code}{RESET}")
        print(f'---------------------------{AMARILLO}-------------------{RESET}--------------------------------')



#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#MANEJO DE OPCIONES PRINCIPALES DEL PROGRAMA

def main():
    #Saludo de bienvenida
    sonido_alerta('bienvenida') 
    #Solicitamos al usuario la opción que desea ejecutar
    print('-----------------------------------------------------------------------')
    opcion = input(f'''|{MORADO}____________________MANITO ESCRIBI LA OPCION NUMERICA QUE QUERES:________________________________________{RESET}|
                       | {ROJO}1{RESET} - Busquemos URL con la SPIDER a partir de una URL que me des, (ejem: http://testphp.vulnweb.com/)                    |
                       | {ROJO}2{RESET} - Ejecutar Inyeccion directamente en una URL en puntual que me des, (ejem: http://testphp.vulnweb.com/)              |
                       | {ROJO}3{RESET} - Realizar inyecciones por POST en una URL con formulario (ejem: http://testphp.vulnweb.com/login)                   |
                       | {ROJO}4{RESET} - Realizar inyecciones de payloads a headers especificos de una solicitud (ejem: User-Agent: SE_INYECTARA_PAYLOADS)  |
                        {AMARILLO}----------->>{RESET}: ''')
    print('-----------------------------------------------------------------------')

#--------------------------------------------------------------------------------------------------------------------------------
    
    # Dependiendo de la opción ingresada, ejecutamos la funcionalidad correspondiente
    if opcion == '1':
        #sonido del menu
        opcion_elejida = 'uno'
        sonido_alerta(opcion_elejida)
        # Solicitamos al usuario el dominio para el comando spider
        print('-----------------------------------------------------------------------')
        dominio_spider = input(f"{MORADO}Introduci el dominio completo Manito {RESET}(ejem: http://testphp.vulnweb.com/){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        print('-----------------------------------------------------------------------')
        payload_txt = input(f"{MORADO}Introduci el nombre de la lista de PAYLOAD TXT que tengas en este directorio o usaremos por defecto: {RESET}(ejem: listXSScodificadosYpoliglotasGITHUByGPT.txt){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        opcion_uno(dominio_spider, payload_txt)
    elif opcion == '2':
        #sonido del menu
        opcion_elejida = 'dos'
        sonido_alerta(opcion_elejida)
        # Solicitamos al usuario el dominio único
        print('-----------------------------------------------------------------------')
        dominio_unico = input(f"{MORADO}Introduci el dominio completo Manito ((AGREGA {AMARILLO}FUZZ{RESET} en el parametro puntual que quieres inyectar)) {RESET}(ejem: http://testphp.vulnweb.com/search?q={AMARILLO}FUZZ{RESET}&pp=53265){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        print('-----------------------------------------------------------------------')
        payload_txt = input(f"{MORADO}Introduci el nombre de la lista de PAYLOAD TXT que tengas en este directorio o usaremos por defecto: {RESET}(ejem: listXSScodificadosYpoliglotasGITHUByGPT.txt){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        opcion_dos(dominio_unico, payload_txt)
    elif opcion == '3':
        #sonido del menu
        opcion_elejida = 'tres'
        sonido_alerta(opcion_elejida)
        # Solicitamos al usuario la URL para inyección por POST
        print('-----------------------------------------------------------------------')
        url_post = input(f"{MORADO}Introduci el dominio completo Manito {RESET}(ejem: http://testphp.vulnweb.com/login){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        print('-----------------------------------------------------------------------')
        payload_txt = input(f"{MORADO}Introduci el nombre de la lista de PAYLOAD TXT que tengas en este directorio o usaremos por defecto: {RESET}(ejem: listXSScodificadosYpoliglotasGITHUByGPT.txt){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        # Pedir al usuario los nombres de los campos del formulario
        parametroYvalorAgregadoPOST = {}
        while True:
            nombre_de_parametro_POST = input(f"{MORADO}Introduce el nombre del campo adicional del formulario (deja vacío para terminar){MORADO}:{RESET} ")
            if not nombre_de_parametro_POST:
                break
            valor_parametro_POST = input(f"{MORADO}Introduce el valor para el campo '{nombre_de_parametro_POST}' (puede ser vacío o con valor fijo si quiere darlo){MORADO}:{RESET} ")
            parametroYvalorAgregadoPOST[nombre_de_parametro_POST] = valor_parametro_POST
        print('-----------------------------------------------------------------------')
        opcion_tres(url_post, payload_txt, parametroYvalorAgregadoPOST)
    elif opcion == '4':
        #sonido del menu
        opcion_elejida = 'cuatro'
        sonido_alerta(opcion_elejida)
        # Solicitamos al usuario el dominio único
        print('-----------------------------------------------------------------------')
        dominio_unico = input(f"{MORADO}Introduci el dominio completo Manito {RESET}(ejem: http://testphp.vulnweb.com/){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        print('-----------------------------------------------------------------------')
        payload_txt = input(f"{MORADO}Introduci el nombre de la lista de PAYLOAD TXT que tengas en este directorio o usaremos por defecto: {RESET}(ejem: listXSScodificadosYpoliglotasGITHUByGPT.txt){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        opcion_cuatro(dominio_unico, payload_txt)    
    else:
        #sonido del menu
        opcion_elejida = 'novalido'
        sonido_alerta(opcion_elejida)
        # Si la opción ingresada no es válida
        print('-----------------------------------------------------------------------')
        print(f"{MORADO}Introduci una opcion numerica correcta Manito {RESET}(ejem: 1){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#CONFIGURAMOS DEMAS PARAMETROS:
sonido_alerta('hunter')
print('-----------------------------------------------------------------------')
header_bug_hunter = input(f'{MORADO}Manito dame tu encabezado de usuario BUGHUNTER: (Ej:p4im0n) {RESET}')
print('-----------------------------------------------------------------------')


#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#OPCION 1 FUZZING DE URL EN BUSCA DE RUTAS CON PARAMETROS INYECTABLES:
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
        with open('listaXSS_bypass_y_poliglota.txt', 'r', encoding='utf-8') as archivo_payloads_XSS:
            payloads_XSS = archivo_payloads_XSS.read().splitlines()
        

#--------------------------------------------------------------------------------------------------------------------------------
    # Configura el controlador del navegador FIREFOX 
    firefox_options = Options()
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    # Crear el directorio de reportes si no existe
    if not os.path.exists('reportes'):
        os.makedirs('reportes')

#--------------------------------------------------------------------------------------------------------------------------------

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
        'X-HackerOne-Research': header_bug_hunter
    }

#--------------------------------------------------------------------------------------------------------------------------------
    with tqdm(total=total_payloads, desc=f"{MORADO}PROGRESO DE PAYLOAD EJECUTADOS: {RESET}") as pbar:
        
        for url_inyectada in urls_a_inyectar:
            
            for payload in payloads_XSS:

                # Escuchar si se presiona 's' sin detener el script
                print("Presiona 's' y Enter para saltar a la siguiente URL o espera para continuar...")
                i, _, _ = select.select([sys.stdin], [], [], 0.5)  # Escucha con timeout de 0.5 segundos
                if i:
                    user_input = sys.stdin.read(1).strip()
                    if user_input.lower() == 's':
                        print(f"{AMARILLO}Saltando a la siguiente URL...{RESET}")
                        break  # Salta a la siguiente URL
                
                try:
                    
                    # realiza cada request osea cada solicitud con mi header custom de bug hunter
                    response = requests.get(url_inyectada + payload, headers=headers)
                    
                    # imprime los detalles de la solicitud REQUEST
                    print(f"URL solicitada: {response.request.url}")
                    print(f"Método de solicitud: {response.request.method}")
                    print(f'{AZUL}///////////////////////////REQUEST y RESPONSE//////////////////////////{RESET}')
                    print(f"{AMARILLO}REQUEST:{RESET}")
                    for key, value in response.request.headers.items():
                        print(f"{NARANJA_FUERTE}#{RESET}{AMARILLO}{key}: {value}{RESET}")

                    # imprime el cuerpo de la respuesta RESPONSE
                    print(f"{AMARILLO}RESPONSE:{RESET}")
                    print(f"{NARANJA_FUERTE}#{RESET}Estado de la respuesta: {AMARILLO}{response.status_code}{RESET}")
                    print(f"{NARANJA_FUERTE}#{RESET}Cuerpo de la respuesta: {AMARILLO}{response.text[:500]}...{RESET}")
                    
                    # verifica que se envio el header custom
                    if 'X-HackerOne-Research' in response.request.headers:
                        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
                        print(f"{MORADO}Header personalizado enviado: {response.request.headers['X-HackerOne-Research']}{RESET}")
                        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
                        print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                        print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                        print(f'{MORADO}////////////////////////////NUEVA INYECCION////////////////////////////{RESET}')
                        print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                        print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                        
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

                        print(f'{AZUL}///////////////////////////ANALISIS INYECCION//////////////////////////{RESET}')
                        print(f'------------------------------------------------------------------------------')
                        print(f'{AZUL}- [PAYLOAD: {payload}] {AMARILLO}-{RESET} captura guardada en {archivo_captura}{RESET}')
                        print(f'------------------------------------------------------------------------------')
                        # Analizar la captura de pantalla
                        analizar_captura(payload,ruta_archivo)

                    else:
                        print(f'{NARANJA_FUERTE}Manito dio error la solicitud con {url_inyectada + payload} {RESET}')
                except Exception as e:
                    print(f'-------------------********{ROJO}******///////******{RESET}********------------------------')
                    print(f'---------------------------{ROJO}------///ATENCION///------{RESET}--------------------------------')
                    print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                    print(f'{VIOLETA}- [{url_inyectada}]![ {payload} ] - captura]({archivo_captura}){RESET}')
                    print(f'{ROJO}///POC///: {CIAN}COPIA aqui-->{RESET} {url_inyectada + payload} {CIAN}<--COPIA aqui{RESET} :{RESET}')
                    print(f'{ROJO}Fallo Manito o Tenemos un XSS Exitoso 8D :{RESET}  {AMARILLO}{url_inyectada}{RESET}: {ROJO}---SCRIPT EJECUTADO-->{RESET} {NARANJA_FUERTE}{payload}{RESET} {ROJO}-->{RESET} {CIAN}{e}{RESET}')
                    print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                    print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                    print(f'-------------------********{ROJO}******///////******{RESET}********------------------------')
                    
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

                    #cuando se detecta una vulnerabilidad o  excepcion envia notificacion por TELEGRAM
                    enviar_mensaje_telegram(e, payload, response.request.url, captura_de_escritorio)

                    print(f'{AZUL}///////////////////////////ANALISIS INYECCION EXITOSA//////////////////////////{RESET}')
                    print(f'------------------------------------------------------------------------------')
                    print(f'{AZUL}- [PAYLOAD INYECTADO: {payload}] {AMARILLO}-{RESET} captura guardada en {archivo_captura}{RESET}')
                    print(f'------------------------------------------------------------------------------')
                    # Analizar la captura de pantalla
                    analizar_captura(payload,captura_de_escritorio)

                    # sonido de alerta
                    sonido_alerta('xss')
                
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
        with open('listaXSS_bypass_y_poliglota.txt', 'r', encoding='utf-8') as archivo_payloads_XSS:
            payloads_XSS = archivo_payloads_XSS.read().splitlines()       

#--------------------------------------------------------------------------------------------------------------------------------
    # Configura el controlador del navegador FIREFOX 
    firefox_options = Options()
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    # Crear el directorio de reportes si no existe
    if not os.path.exists('reportes'):
        os.makedirs('reportes')

#--------------------------------------------------------------------------------------------------------------------------------

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
        'X-HackerOne-Research': header_bug_hunter
    }

#--------------------------------------------------------------------------------------------------------------------------------
    with tqdm(total=total_payloads, desc=f"{MORADO}PROGRESO DE PAYLOAD EJECUTADOS: {RESET}") as pbar:
        
        for payload in payloads_XSS:
            dominio_fuzz_payload = dominio_unico.replace('FUZZ', payload)
            print(dominio_fuzz_payload)
            
            try:
                
                # realiza cada request osea cada solicitud con mi header custom de bug hunter
                response = requests.get(dominio_fuzz_payload, headers=headers)
                
                # imprime los detalles de la solicitud REQUEST
                print(f"URL solicitada: {response.request.url}")
                print(f"Método de solicitud: {response.request.method}")
                print(f'{AZUL}///////////////////////////REQUEST y RESPONSE//////////////////////////{RESET}')
                print(f"{AMARILLO}REQUEST:{RESET}")
                for key, value in response.request.headers.items():
                    print(f"{NARANJA_FUERTE}#{RESET}{AMARILLO}{key}: {value}{RESET}")

                # imprime el cuerpo de la respuesta RESPONSE
                print(f"{AMARILLO}RESPONSE:{RESET}")
                print(f"{NARANJA_FUERTE}#{RESET}Estado de la respuesta: {AMARILLO}{response.status_code}{RESET}")
                print(f"{NARANJA_FUERTE}#{RESET}Cuerpo de la respuesta: {AMARILLO}{response.text[:500]}...{RESET}")
                
                # verifica que se envio el header custom
                if 'X-HackerOne-Research' in response.request.headers:
                    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
                    print(f"{MORADO}Header personalizado enviado: {response.request.headers['X-HackerOne-Research']}{RESET}")
                    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
                    print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                    print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                    print(f'{MORADO}////////////////////////////NUEVA INYECCION////////////////////////////{RESET}')
                    print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                    print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                    
                # si la solicitud fue exitosa, pasa la URL a selenium
                if response.status_code == 200:
                    
                    # Navegar a la URL de destino con Selenium para visualizar la reacción
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
                    
                    print(f'{AZUL}///////////////////////////ANALISIS INYECCION//////////////////////////{RESET}')
                    print(f'------------------------------------------------------------------------------')
                    print(f'{AZUL}- [PAYLOAD: {payload}] {AMARILLO}-{RESET} captura guardada en {archivo_captura}{RESET}')
                    print(f'------------------------------------------------------------------------------')
                    
                    # Analizar la captura de pantalla
                    analizar_captura(payload,ruta_archivo)

                else:
                    print(f'{AMARILLO}------------------------------------------------------------------------------{RESET}')
                    print(f'{NARANJA_FUERTE}Manito dio error la solicitud con {dominio_fuzz_payload + payload} {RESET}')
            
            except Exception as e:
                print(f'-------------------********{ROJO}******///////******{RESET}********------------------------')
                print(f'---------------------------{ROJO}------///ATENCION///------{RESET}--------------------------------')
                print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                print(f'{VIOLETA}- [{dominio_fuzz_payload}]![ {payload} ] - captura]({archivo_captura}){RESET}')
                print(f'{ROJO}///POC///: {CIAN}COPIA aqui-->{RESET} {dominio_fuzz_payload + payload} {CIAN}<--COPIA aqui{RESET} :{RESET}')
                print(f'{ROJO}Fallo Manito o Tenemos un XSS Exitoso 8D :{RESET}  {AMARILLO}{dominio_fuzz_payload}{RESET}: {ROJO}---SCRIPT EJECUTADO-->{RESET} {NARANJA_FUERTE}{payload}{RESET} {ROJO}-->{RESET} {CIAN}{e}{RESET}')
                print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                print(f'-------------------********{ROJO}******///////******{RESET}********------------------------')
                
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

                #cuando se detecta una vulnerabilidad o  excepcion envia notificacion por TELEGRAM
                enviar_mensaje_telegram(e, payload, response.request.url, captura_de_escritorio)

                print(f'{AZUL}///////////////////////////ANALISIS INYECCION EXITOSA//////////////////////////{RESET}')
                print(f'------------------------------------------------------------------------------')
                print(f'{AZUL}- [PAYLOAD: {payload}] {AMARILLO}-{RESET} captura guardada en {archivo_captura}{RESET}')
                print(f'------------------------------------------------------------------------------')
                # Analizar la captura de pantalla
                analizar_captura(payload,captura_de_escritorio)

                # sonido de alerta
                sonido_alerta('xss')
            
            # barra de progreso de payloads
            pbar.update(1)
    
    driver.quit()    

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
# OPCION 3

def opcion_tres(url_post, payload_txt, additional_fields):
    # Muestra la URL objetivo
    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
    print("URL OBJETIVO (POST):")
    print(url_post)
    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')

    # Verificamos si se proporcionó una URL válida
    if not url_post:
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        print(f"{ROJO}No se encontró una URL Manito.{RESET}")
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        return

#--------------------------------------------------------------------------------------------------------------------------------

    # Leer los payloads desde el archivo proporcionado o usar uno por defecto
    if payload_txt:
        with open(payload_txt, 'r', encoding='utf-8') as archivo_payloads_XSS:
            payloads_XSS = archivo_payloads_XSS.read().splitlines()
    else:
        with open('listaXSS_bypass_y_poliglota.txt', 'r', encoding='utf-8') as archivo_payloads_XSS:
            payloads_XSS = archivo_payloads_XSS.read().splitlines()

    # Configura el controlador del navegador Firefox
    firefox_options = Options()
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    # Crear el directorio de reportes si no existe
    if not os.path.exists('reportes'):
        os.makedirs('reportes')

#--------------------------------------------------------------------------------------------------------------------------------

    # Cargar cookies si están disponibles
    print('-----------------------------------------------------------------------')
    cookies_input = input(f"{MORADO}Creaste el archivo de cookies del usuario en formato JSON ?? RESP: {AMARILLO}s{RESET} / {ROJO}n{RESET} {RESET}(ejem: con extension COOKIE EDITOR exportalas en JSON y asi las pegas en un archivo llamándolo cookies.json, por cualquier error tener en cuenta en el parametro SameSite poner en Lax){MORADO} : {RESET} ")
    print('-----------------------------------------------------------------------')

    if cookies_input == 's':
        with open('cookies.json', 'r') as f:
            user_cookies = json.load(f)

        # Navegar al dominio base y cargar cookies
        dominio_base = input(f"{MORADO}Manito por favor dame el DOMINIO BASE al que pertenecen las COOKIES asi termino de CONFIGURAR, (ejem: http://testphp.vulnweb.com/){MORADO} : {RESET} ")
        print('-----------------------------------------------------------------------')
        driver.get(dominio_base)

        for cookie in user_cookies:
            cookie['sameSite'] = 'Lax'
            driver.add_cookie(cookie)
        driver.get(url_post)

#--------------------------------------------------------------------------------------------------------------------------------

    # Utiliza tqdm para mostrar una barra de progreso durante la ejecución de los payloads
    with tqdm(total=len(payloads_XSS), desc=f"{MORADO}PROGRESO DE PAYLOAD EJECUTADOS por POST: {RESET}") as pbar:
        for payload in payloads_XSS:
            try:
                # Navegar a la página con el formulario
                driver.get(url_post)
                time.sleep(2)  # Esperar que la página se cargue completamente

                # Llenar cada uno de los campos del formulario con el payload o valores adicionales proporcionados
                for field_name, field_value in additional_fields.items():
                    if not field_value:  # Si no hay valor proporcionado, usa el payload
                        field_value = payload

                    # Encontrar el elemento por el atributo 'name' y llenar con el valor
                    try:
                        input_element = driver.find_element(By.NAME, field_name)
                        input_element.clear()
                        input_element.send_keys(field_value)
                    except Exception as e:
                        print(f"{ROJO}No se pudo encontrar el campo {field_name} para inyectar. Error: {e}{RESET}")

                # Enviar el formulario
                try:
                    submit_button = driver.find_element(By.XPATH, "//input[@type='submit' or @type='button']")  # Intentar localizar el botón de envío
                    submit_button.click()
                except Exception as e:
                    print(f"{ROJO}No se encontró un botón de envío automático. Error: {e}{RESET}")
                    continue

                # Esperar unos segundos para que se procese la respuesta después del envío
                time.sleep(3)

                # Crear el directorio para almacenar las capturas de pantalla
                directorio_capturas = 'capturas_web'
                os.makedirs(directorio_capturas, exist_ok=True)

                # Guardar la captura de pantalla
                archivo_captura = re.sub(r'[^\w\-_\. ]', '_', payload) + ".png"
                ruta_archivo = os.path.join(directorio_capturas, archivo_captura)
                driver.save_screenshot(ruta_archivo)
                
                print(f'{AZUL}- [{url_post}]![ {payload} ] - captura]({archivo_captura}){RESET}')
                print(f'{AZUL}///////////////////////////ANALISIS INYECCION POST//////////////////////////{RESET}')
                print(f'------------------------------------------------------------------------------')
                print(f'{AZUL}- [PAYLOAD POST: {payload}] {AMARILLO}-{RESET} captura guardada en {archivo_captura}{RESET}')
                print(f'------------------------------------------------------------------------------')

                # Analizar la captura de pantalla
                analizar_captura(payload, ruta_archivo)

            except Exception as e:
                # Si hay un error, mostramos la información relevante y capturamos el estado del sistema
                print(f'-------------------********{ROJO}******///////******{RESET}********------------------------')
                print(f'---------------------------{ROJO}------///ATENCION///------{RESET}--------------------------------')
                print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                print(f'{ROJO}///POC///: {CIAN}Payload ejecutado-->{RESET} {payload} {CIAN}<--COPIA aqui{RESET} :{RESET}')
                print(f'{ROJO}Fallo Manito o Tenemos un XSS Exitoso 8D :{RESET}  {AMARILLO}{url_post}{RESET}: {ROJO}---SCRIPT EJECUTADO-->{RESET} {NARANJA_FUERTE}{payload}{RESET} {ROJO}-->{RESET} {CIAN}{e}{RESET}')
                print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                print(f'-------------------********{ROJO}******///////******{RESET}********------------------------')

            # Actualizamos la barra de progreso
            pbar.update(1)

    # Cerramos el navegador al finalizar
    driver.quit()



#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#Funcion para seleccionar y modificar headers especificos para ser inyectados

#OPCION 4:
# OPCION 4:
def opcion_cuatro(dominio_unico, payload_txt):
    # >>>>> TU HEADER CUSTOM DE BUGHUNTER <<<<<
    headers_propio_de_cazador = {
        'X-HackerOne-Research': header_bug_hunter
    }
    
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
    
    # Seleccionar el header a modificar
    print(f"\n{MORADO}Seleccione los headers que desea modificar o agregar para inyectar:{RESET}")
    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
    print(f"{MORADO}1{RESET} - User-Agent\n{MORADO}2{RESET} - Referer\n{MORADO}3{RESET} - Cookie\n{MORADO}4{RESET} - Host\n{MORADO}5{RESET} - Origin\n{MORADO}6{RESET} - Custom Header\n{MORADO}7{RESET} - Finalizar selección")
    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
    opcion_header = input("Ingrese el número del header a modificar o '7' para finalizar: ")

    if opcion_header == '7':
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        print(f"{ROJO}Selección finalizada. No se realizarán inyecciones.{RESET}")
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        return  

#--------------------------------------------------------------------------------------------------------------------------------

    # Cargar los payloads
    if payload_txt:
        with open(payload_txt, 'r', encoding='utf-8') as archivo_payloads_XSS:
            payloads_XSS = archivo_payloads_XSS.read().splitlines()
    else:
        with open('listaXSS_bypass_y_poliglota.txt', 'r', encoding='utf-8') as archivo_payloads_XSS:
            payloads_XSS = archivo_payloads_XSS.read().splitlines()

    # Configurar el controlador del navegador Firefox
    firefox_options = Options()
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    # Crear el directorio de reportes si no existe
    if not os.path.exists('reportes'):
        os.makedirs('reportes')


#--------------------------------------------------------------------------------------------------------------------------------

    # Solicitar las cookies al usuario
    print('-----------------------------------------------------------------------')
    cookies_input = input(f"{MORADO}Creaste el archivo de cookies del usuario en formato JSON ?? RESP: {AMARILLO}s{RESET} / {ROJO}n{RESET} {RESET}(ejem: con extensión COOKIE EDITOR exportalas en JSON y así las pegas en un archivo llamándolo cookies.json, por cualquier error tener en cuenta en el parámetro SameSite poner en Lax){MORADO} : {RESET} ")
    print('-----------------------------------------------------------------------')
    
    if cookies_input == 's':
        # Cargar las cookies desde el archivo JSON
        with open('cookies.json', 'r') as f:
            user_cookies = json.load(f)
    
        # Solicitar el dominio base para las cookies
        print('-----------------------------------------------------------------------')
        dominio_base = input(f"{MORADO}Manito por favor dame el DOMINIO BASE al que pertenecen las COOKIES para terminar de CONFIGURAR, (ejem: http://testphp.vulnweb.com/){MORADO} : {RESET} ")
        print('-----------------------------------------------------------------------')
            
        # Navegar a una página en blanco para configurar las cookies
        driver.get(dominio_base)
        
        # Modificar el valor de SameSite a 'Lax' para cada cookie
        for cookie in user_cookies:
            cookie['sameSite'] = 'Lax'
        
        for cookie in user_cookies:
            driver.add_cookie(cookie)
        driver.get(dominio_unico)
    
    total_payloads = len(payloads_XSS)


#--------------------------------------------------------------------------------------------------------------------------------
    # Mostrar barra de progreso y ejecutar las inyecciones
    with tqdm(total=total_payloads, desc=f"{MORADO}PROGRESO DE PAYLOAD EJECUTADOS: {RESET}") as pbar:
        for payload in payloads_XSS:
            headers_a_inyectar = headers_propio_de_cazador.copy()

            if opcion_header == '1':
                headers_a_inyectar['User-Agent'] = payload
            elif opcion_header == '2':
                headers_a_inyectar['Referer'] = payload
            elif opcion_header == '3':
                headers_a_inyectar['Cookie'] = payload
            elif opcion_header == '4':
                headers_a_inyectar['Host'] = payload
            elif opcion_header == '5':
                headers_a_inyectar['Origin'] = payload
            elif opcion_header == '6':
                nombre_de_header = input("Ingrese el nombre del header personalizado: ")
                valor_de_header = input(f"Ingrese el valor para {nombre_de_header}: ")
                headers_a_inyectar[nombre_de_header] = valor_de_header

            try:
                # Realizar la solicitud
                response = requests.get(dominio_unico, headers=headers_a_inyectar)
                
                # Imprimir detalles de la solicitud y respuesta
                print(f"URL solicitada: {response.request.url}")
                print(f"Método de solicitud: {response.request.method}")
                print(f'{AZUL}///////////////////////////REQUEST y RESPONSE//////////////////////////{RESET}')
                print(f"{AMARILLO}REQUEST:{RESET}")
                for key, value in response.request.headers.items():
                    print(f"{NARANJA_FUERTE}#{RESET}{AMARILLO}{key}: {value}{RESET}")

                print(f"{AMARILLO}RESPONSE:{RESET}")
                print(f"{NARANJA_FUERTE}#{RESET}Estado de la respuesta: {AMARILLO}{response.status_code}{RESET}")
                print(f"{NARANJA_FUERTE}#{RESET}Cuerpo de la respuesta: {AMARILLO}{response.text[:800]}...{RESET}")

                # Verificar el envío del header personalizado
                if 'X-HackerOne-Research' in response.request.headers:
                    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
                    print(f"{MORADO}Header personalizado enviado: {response.request.headers['X-HackerOne-Research']}{RESET}")
                    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
                    print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                    print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                    print(f'{MORADO}////////////////////////////NUEVA INYECCION////////////////////////////{RESET}')
                    print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                    print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')

                # Si la solicitud es exitosa, usar Selenium
                if response.status_code == 200:
                    driver.get(dominio_unico)
                    time.sleep(3)
                    
                    directorio_capturas = 'capturas_web'
                    os.makedirs(directorio_capturas, exist_ok=True)
                    
                    archivo_captura = re.sub(r'[^\w\-_\. ]', '_', dominio_unico) + ".png"
                    ruta_archivo = os.path.join(directorio_capturas, archivo_captura)
                    driver.save_screenshot(ruta_archivo)

                    print(f'{AZUL}- [{dominio_unico}]![ HEADERS: {headers_a_inyectar}: {payload} ] - captura]({archivo_captura}){RESET}')
                    analizar_captura(payload, ruta_archivo)

                else:
                    print(f'{AMARILLO}------------------------------------------------------------------------------{RESET}')
                    print(f'{NARANJA_FUERTE}Manito dio error la solicitud con {dominio_unico + payload} {RESET}')

            except Exception as e:
                print(f'-------------------********{ROJO}******///////******{RESET}********------------------------')
                print(f'{ROJO}Fallo Manito o tenemos un XSS exitoso 8D: {RESET}{e}')
                
                max_length = 80
                nombre_base_del_archivo = "{}_{}_VULNERABLE".format(re.sub(r'[^\w\-_\. ]', '_', dominio_unico), re.sub(r'[^\w\-_\. ]', '_', payload))
                nombre_final_del_archivo = nombre_base_del_archivo[:max_length]
                
                captura_de_escritorio = f"reportes/{nombre_final_del_archivo}.png"
                pyautogui.screenshot(captura_de_escritorio)

                enviar_mensaje_telegram(e, payload, response.request.url, captura_de_escritorio)
                analizar_captura(payload, captura_de_escritorio)
                sonido_alerta('xss')

            # Actualizar la barra de progreso
            pbar.update(1)

    driver.quit()



#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#ENVIO DE MENSAJES POR TELEGRAM INFORMANDO VULNERABILIDADES ENCONTRADAS


def enviar_mensaje_telegram(vulnerabilidad, payload, request, captura):
    # Datos del bot y el chat
    bot_token = 'TU_TOKEN_BOT_TELEGRAM'
    chat_id = 'TU_ID_DEL_CHAT_TELEGRAM'
    
    # Mensaje a enviar
    mensaje = f'POSIBLE VULNERABILIDAD ENCONTRADA:\nVulnerabilidad: {vulnerabilidad}\nPayload: {payload}\nRequest: {request}'
    
    # URL para enviar el mensaje
    url_mensaje = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    datos = {
        'chat_id': chat_id,
        'text': mensaje
    }

#--------------------------------------------------------------------------------------------------------------------------------
    
    # Enviar el mensaje
    response = requests.post(url_mensaje, data=datos)
    
    # Enviar la captura si existe
    if captura:
        url_archivo = f'https://api.telegram.org/bot{bot_token}/sendDocument'
        with open(captura, 'rb') as archivo:
            archivos = {'document': archivo}
            datos_archivo = {
                'chat_id': chat_id,
                'caption': 'Captura de pantalla relacionada con la vulnerabilidad.'
            }
            response = requests.post(url_archivo, data=datos_archivo, files=archivos)

#--------------------------------------------------------------------------------------------------------------------------------
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        print(f"Mensaje enviado a Telegram correctamente MANITO.")
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
    else:
        print(f'{ROJO}-----------------------------------------------------------------------{RESET}')
        print(f"Error al enviar el mensaje a Telegram: {response.status_code}")
        print(f'{ROJO}-----------------------------------------------------------------------{RESET}')


#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
# Inicio del script
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Manejar la interrupción del usuario (Ctrl + C)
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        print('Gracias Manito por usar P4IvisualInyect_v3.1.py ')
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        exit()
#--------------------------------------------------------------------------------------------------------------------------------


































































# P4IvisualInyect.py - v3.1 - By P4IM0N - COOKIES - TOOL de escaneo de URLs con parámetros de inyección obtenidas con GOSPIDER y luego procesadas en navegador automáticamente con Selenium y Firefox para capturar las rutas y ejecuciones positivas de inyecciones XSS, LFI, RCE, SQL, por método GET y se añadió recientemente por POST para luego agregar la captura a reportes del POC, y analizar capturas de pantalla usando OCR Space API para análisis de vulnerabilidad (https://ocr.space/ocrapi) deben cargar su API permite mail temporal el sitio ;D, se le sumo inyeccion de headers y notificacion por mensaje sobre vulnerabilidad enconrada y captura de pantalla a traves de bot de telegram

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
import requests
import sys
import select
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
import base64


#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
# Defino colores para el texto en la consola
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
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
# Banner que se muestra al iniciar el script
banner = f'''
                        {BLANCO}⠄⠄⢀⣀⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣄⣀⠄⠄
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
              |__|                  \/           \/              \/\/         \/     \/{RESET}v3.1_      
                                                                 {ROJO}by P4IM0N{RESET}'''
                                                                 
print(banner)                                                                 


#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#Funcion para reproducir el sonido de alerta

def sonido_alerta(sonido):
    # segun la situacion sonido a reproducirse
    if sonido == 'bienvenida':
        audio = 'pip.mp3'
        voz = 'bienvenida.mp3'
    elif sonido == 'sql':
        audio = 'sonido_alarma_sql.mp3'
        voz = 'posible_sql.mp3'
    elif sonido == 'xss':
        audio = 'sonido_alarma_xss.mp3'
        voz = 'posible_xss.mp3'
    elif sonido == 'comando':
        audio = 'sonido_alarma_ejecucion_de_comandos.mp3'
        voz = 'posible_ejecucion_de_comandos.mp3'
    elif sonido == 'lfi':
        audio = 'sonido_alarma_lfi.mp3'
        voz = 'posible_lfi.mp3'
    elif sonido == 'uno': #---
        audio = 'pip.mp3'
        voz = 'opcion_uno.mp3'
    elif sonido == 'dos':
        audio = 'pip.mp3'
        voz = 'opcion_dos.mp3'
    elif sonido == 'tres':
        audio = 'pip.mp3'
        voz = 'opcion_tres.mp3'
    elif sonido == 'cuatro':
        audio = 'pip.mp3'
        voz = 'opcion_cuatro.mp3'
    elif sonido == 'novalido':
        audio = 'pip.mp3'
        voz = 'opcion_novalida.mp3'
    elif sonido == 'hunter':
        audio = 'pip.mp3'
        voz = 'bug_hunter.mp3'                                
    #Reproduccion de los sonidos  
    playsound(audio)  # Reproduce el archivo de sonido para alertar al usuario
    time.sleep(2)
    playsound(voz)

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
# Función para analizar una captura de pantalla en busca de errores utilizando OCR Space API

def analizar_captura(payload,file_path):
    api_key = "TU_API_KEY_DE_OCR_SPACE_MANITO"  # Reemplazar con tu API Key de OCR Space
    with open(file_path, "rb") as f:
        image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")
    
    # Realizar la solicitud POST a OCR Space
    url = "https://api.ocr.space/parse/image"
    headers = {
        "apikey": api_key
    }
    data = {
        "base64Image": f"data:image/png;base64,{image_base64}",
        "language": "eng"
    }
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        result = response.json()
        parsed_text = result.get("ParsedResults", [{}])[0].get("ParsedText", "")
        print(f'------------------------------------------------------------------------------')
        print(f"{AZUL}Texto detectado en la imagen utilizando OCR Space API:{RESET}\n{parsed_text}")
        print(f'------------------------------------------------------------------------------')
        
#--------------------------------------------------------------------------------------------------------------------------------

        #Lista de patrones de errores comunes
        patrones = r"\b(sql syntax|database error|syntax error|command not found|unrecognized command|xss detected|csrf token error|unauthorized access|file not found|segmentation fault|buffer overflow|invalid input|lfi detected|rfi detected|shell injection|unauthorized shell access|directory traversal detected|server misconfiguration|soap fault)\b"

        #Lista de patrones de ejecuciones exitosas
        indicadores_exitosos = [
            r"\b(root|root:x|user:x|daemon:x|admin|uid=\d+|gid=\d+|/bin/bash|flag{.+}|whoami)\b",  #Comandos
            r"<.*script.*>",  #XSS
            r"SELECT.*FROM|INSERT.*INTO|UPDATE.*SET|DELETE.*FROM",  #SQL
            r"/etc/passwd|/etc/shadow|/home/|/root",  #LFI/RFI
        ]

        # Buscar patrones de error en el texto
        coincidencias = re.findall(patrones, parsed_text, re.IGNORECASE)

        # Buscar ejecuciones exitosas específicas
        coincidencias_exitosas = []
        for indicador in indicadores_exitosos:
            if re.search(indicador, parsed_text, re.IGNORECASE):
                coincidencias_exitosas.append(indicador)

#--------------------------------------------------------------------------------------------------------------------------------

        # Verificar y mostrar cada tipo de vulnerabilidad por separado
        if coincidencias:
            
            print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
            print(f'---------------------------{ROJO}------///ATENCION///------{RESET}--------------------------------')
            print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')

            if re.search(r"\b(sql syntax|database error|sql error|invalid query)\b", parsed_text, re.IGNORECASE):
                print(f"{ROJO}ALERTA: Posible vulnerabilidad de inyección SQL detectada.{RESET}")
                vulnerabilidad = 'sql'
                sonido_alerta(vulnerabilidad)
                #cuando se detecta una vulnerabilidad o  excepcion envia notificacion por TELEGRAM
                enviar_mensaje_telegram(vulnerabilidad, payload, response.request.url, file_path)

            if re.search(r"\b(command not found|shell error|unrecognized command|shell injection|unauthorized shell access)\b", parsed_text, re.IGNORECASE):
                print(f"{ROJO}ALERTA: Posible inyección de comandos detectada.{RESET}")
                vulnerabilidad = 'comando'
                sonido_alerta(vulnerabilidad)
                #cuando se detecta una vulnerabilidad o  excepcion envia notificacion por TELEGRAM
                enviar_mensaje_telegram(vulnerabilidad, payload, response.request.url, file_path)

            if re.search(r"\b(xss detected|cross-site scripting|<.*script.*>)\b", parsed_text, re.IGNORECASE):
                print(f"{ROJO}ALERTA: Posible ejecución de XSS detectada.{RESET}")
                vulnerabilidad = 'xss'
                sonido_alerta(vulnerabilidad)
                #cuando se detecta una vulnerabilidad o  excepcion envia notificacion por TELEGRAM
                enviar_mensaje_telegram(vulnerabilidad, payload, response.request.url, file_path)

            if re.search(r"\b(lfi detected|rfi detected|file disclosure|directory traversal)\b", parsed_text, re.IGNORECASE):
                print(f"{ROJO}ALERTA: Posible vulnerabilidad de LFI/RFI detectada.{RESET}")
                vulnerabilidad = 'lfi'
                sonido_alerta(vulnerabilidad)
                #cuando se detecta una vulnerabilidad o  excepcion envia notificacion por TELEGRAM
                enviar_mensaje_telegram(vulnerabilidad, payload, response.request.url, file_path)

        # Verificar y mostrar las coincidencias de ejecuciones exitosas
        if coincidencias_exitosas:
            
            print(f"{ROJO}ALERTA: Ejecuciones exitosas detectadas.{RESET}")
            for indicador in coincidencias_exitosas:
                if re.search(indicador, parsed_text, re.IGNORECASE):
                    print(f"{ROJO}- {re.search(indicador, parsed_text).group()}{RESET}")

                print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
        else:
            print(f'{AMARILLO}------------------------------------------------------------------------------{RESET}')
            print(f'               LA CAPTURA NO PRESENTA VULNERABILIDAD EXPLOTADA MANITO                         ')
            print(f'{AMARILLO}------------------------------------------------------------------------------{RESET}')
    else:
        print(f'---------------------------{AMARILLO}-------------------{RESET}--------------------------------')
        print(f"{AMARILLO}Error al analizar la imagen. Código de estado: {response.status_code}{RESET}")
        print(f'---------------------------{AMARILLO}-------------------{RESET}--------------------------------')



#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#MANEJO DE OPCIONES PRINCIPALES DEL PROGRAMA

def main():
    #Saludo de bienvenida
    sonido_alerta('bienvenida') 
    #Solicitamos al usuario la opción que desea ejecutar
    print('-----------------------------------------------------------------------')
    opcion = input(f'''|{MORADO}____________________MANITO ESCRIBI LA OPCION NUMERICA QUE QUERES:________________________________________{RESET}|
                       | {ROJO}1{RESET} - Busquemos URL con la SPIDER a partir de una URL que me des, (ejem: http://testphp.vulnweb.com/)                    |
                       | {ROJO}2{RESET} - Ejecutar Inyeccion directamente en una URL en puntual que me des, (ejem: http://testphp.vulnweb.com/listproducts.php?cat=FUZZ)              |
                       | {ROJO}3{RESET} - Realizar inyecciones por POST en una URL con formulario (ejem: http://testphp.vulnweb.com/login)                   |
                       | {ROJO}4{RESET} - Realizar inyecciones de payloads a headers especificos de una solicitud (ejem: User-Agent: SE_INYECTARA_PAYLOADS)  |
                        {AMARILLO}----------->>{RESET}: ''')
    print('-----------------------------------------------------------------------')

#--------------------------------------------------------------------------------------------------------------------------------
    
    # Dependiendo de la opción ingresada, ejecutamos la funcionalidad correspondiente
    if opcion == '1':
        #sonido del menu
        opcion_elejida = 'uno'
        sonido_alerta(opcion_elejida)
        # Solicitamos al usuario el dominio para el comando spider
        print('-----------------------------------------------------------------------')
        dominio_spider = input(f"{MORADO}Introduci el dominio completo Manito {RESET}(ejem: http://testphp.vulnweb.com/){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        print('-----------------------------------------------------------------------')
        payload_txt = input(f"{MORADO}Introduci el nombre de la lista de PAYLOAD TXT que tengas en este directorio o usaremos por defecto: {RESET}(ejem: listXSScodificadosYpoliglotasGITHUByGPT.txt){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        opcion_uno(dominio_spider, payload_txt)
    elif opcion == '2':
        #sonido del menu
        opcion_elejida = 'dos'
        sonido_alerta(opcion_elejida)
        # Solicitamos al usuario el dominio único
        print('-----------------------------------------------------------------------')
        dominio_unico = input(f"{MORADO}Introduci el dominio completo Manito ((AGREGA {AMARILLO}FUZZ{RESET} en el parametro puntual que quieres inyectar)) {RESET}(ejem: http://testphp.vulnweb.com/listproducts.php?cat={AMARILLO}FUZZ{RESET}&pp=53265){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        print('-----------------------------------------------------------------------')
        payload_txt = input(f"{MORADO}Introduci el nombre de la lista de PAYLOAD TXT que tengas en este directorio o usaremos por defecto: {RESET}(ejem: listXSScodificadosYpoliglotasGITHUByGPT.txt){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        opcion_dos(dominio_unico, payload_txt)
    elif opcion == '3':
        #sonido del menu
        opcion_elejida = 'tres'
        sonido_alerta(opcion_elejida)
        # Solicitamos al usuario la URL para inyección por POST
        print('-----------------------------------------------------------------------')
        url_post = input(f"{MORADO}Introduci el dominio completo Manito {RESET}(ejem: http://testphp.vulnweb.com/login){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        print('-----------------------------------------------------------------------')
        payload_txt = input(f"{MORADO}Introduci el nombre de la lista de PAYLOAD TXT que tengas en este directorio o usaremos por defecto: {RESET}(ejem: listXSScodificadosYpoliglotasGITHUByGPT.txt){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        # Pedir al usuario los nombres de los campos del formulario
        parametroYvalorAgregadoPOST = {}
        while True:
            nombre_de_parametro_POST = input(f"{MORADO}Introduce el nombre del campo adicional del formulario (deja vacío para terminar){MORADO}:{RESET} ")
            if not nombre_de_parametro_POST:
                break
            valor_parametro_POST = input(f"{MORADO}Introduce el valor para el campo '{nombre_de_parametro_POST}' (puede ser vacío o con valor fijo si quiere darlo){MORADO}:{RESET} ")
            parametroYvalorAgregadoPOST[nombre_de_parametro_POST] = valor_parametro_POST
        print('-----------------------------------------------------------------------')
        opcion_tres(url_post, payload_txt, parametroYvalorAgregadoPOST)
    elif opcion == '4':
        #sonido del menu
        opcion_elejida = 'cuatro'
        sonido_alerta(opcion_elejida)
        # Solicitamos al usuario el dominio único
        print('-----------------------------------------------------------------------')
        dominio_unico = input(f"{MORADO}Introduci el dominio completo Manito {RESET}(ejem: http://testphp.vulnweb.com/){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        print('-----------------------------------------------------------------------')
        payload_txt = input(f"{MORADO}Introduci el nombre de la lista de PAYLOAD TXT que tengas en este directorio o usaremos por defecto: {RESET}(ejem: listXSScodificadosYpoliglotasGITHUByGPT.txt){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')
        opcion_cuatro(dominio_unico, payload_txt)    
    else:
        #sonido del menu
        opcion_elejida = 'novalido'
        sonido_alerta(opcion_elejida)
        # Si la opción ingresada no es válida
        print('-----------------------------------------------------------------------')
        print(f"{MORADO}Introduci una opcion numerica correcta Manito {RESET}(ejem: 1){MORADO}:{RESET} ")
        print('-----------------------------------------------------------------------')

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#CONFIGURAMOS DEMAS PARAMETROS:
sonido_alerta('hunter')
print('-----------------------------------------------------------------------')
header_bug_hunter = input(f'{MORADO}Manito dame tu encabezado de usuario BUGHUNTER: (Ej:P4imON) {RESET}')
print('-----------------------------------------------------------------------')


#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#OPCION 1 FUZZING DE URL EN BUSCA DE RUTAS CON PARAMETROS INYECTABLES:
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
        with open('listaXSS_bypass_y_poliglota.txt', 'r', encoding='utf-8') as archivo_payloads_XSS:
            payloads_XSS = archivo_payloads_XSS.read().splitlines()
        

#--------------------------------------------------------------------------------------------------------------------------------
    # Configura el controlador del navegador FIREFOX 
    firefox_options = Options()
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    # Crear el directorio de reportes si no existe
    if not os.path.exists('reportes'):
        os.makedirs('reportes')

#--------------------------------------------------------------------------------------------------------------------------------

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
        'X-HackerOne-Research': header_bug_hunter
    }

#--------------------------------------------------------------------------------------------------------------------------------
    with tqdm(total=total_payloads, desc=f"{MORADO}PROGRESO DE PAYLOAD EJECUTADOS: {RESET}") as pbar:
        
        for url_inyectada in urls_a_inyectar:
            
            for payload in payloads_XSS:

                # Escuchar si se presiona 's' sin detener el script
                print("Presiona 's' y Enter para saltar a la siguiente URL o espera para continuar...")
                i, _, _ = select.select([sys.stdin], [], [], 0.5)  # Escucha con timeout de 0.5 segundos
                if i:
                    user_input = sys.stdin.read(1).strip()
                    if user_input.lower() == 's':
                        print(f"{AMARILLO}Saltando a la siguiente URL...{RESET}")
                        break  # Salta a la siguiente URL
                
                try:
                    
                    # realiza cada request osea cada solicitud con mi header custom de bug hunter
                    response = requests.get(url_inyectada + payload, headers=headers)
                    
                    # imprime los detalles de la solicitud REQUEST
                    print(f"URL solicitada: {response.request.url}")
                    print(f"Método de solicitud: {response.request.method}")
                    print(f'{AZUL}///////////////////////////REQUEST y RESPONSE//////////////////////////{RESET}')
                    print(f"{AMARILLO}REQUEST:{RESET}")
                    for key, value in response.request.headers.items():
                        print(f"{NARANJA_FUERTE}#{RESET}{AMARILLO}{key}: {value}{RESET}")

                    # imprime el cuerpo de la respuesta RESPONSE
                    print(f"{AMARILLO}RESPONSE:{RESET}")
                    print(f"{NARANJA_FUERTE}#{RESET}Estado de la respuesta: {AMARILLO}{response.status_code}{RESET}")
                    print(f"{NARANJA_FUERTE}#{RESET}Cuerpo de la respuesta: {AMARILLO}{response.text[:500]}...{RESET}")
                    
                    # verifica que se envio el header custom
                    if 'X-HackerOne-Research' in response.request.headers:
                        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
                        print(f"{MORADO}Header personalizado enviado: {response.request.headers['X-HackerOne-Research']}{RESET}")
                        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
                        print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                        print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                        print(f'{MORADO}////////////////////////////NUEVA INYECCION////////////////////////////{RESET}')
                        print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                        print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                        
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

                        print(f'{AZUL}///////////////////////////ANALISIS INYECCION//////////////////////////{RESET}')
                        print(f'------------------------------------------------------------------------------')
                        print(f'{AZUL}- [PAYLOAD: {payload}] {AMARILLO}-{RESET} captura guardada en {archivo_captura}{RESET}')
                        print(f'------------------------------------------------------------------------------')
                        # Analizar la captura de pantalla
                        analizar_captura(payload,ruta_archivo)

                    else:
                        print(f'{NARANJA_FUERTE}Manito dio error la solicitud con {url_inyectada + payload} {RESET}')
                except Exception as e:
                    print(f'-------------------********{ROJO}******///////******{RESET}********------------------------')
                    print(f'---------------------------{ROJO}------///ATENCION///------{RESET}--------------------------------')
                    print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                    print(f'{VIOLETA}- [{url_inyectada}]![ {payload} ] - captura]({archivo_captura}){RESET}')
                    print(f'{ROJO}///POC///: {CIAN}COPIA aqui-->{RESET} {url_inyectada + payload} {CIAN}<--COPIA aqui{RESET} :{RESET}')
                    print(f'{ROJO}Fallo Manito o Tenemos un XSS Exitoso 8D :{RESET}  {AMARILLO}{url_inyectada}{RESET}: {ROJO}---SCRIPT EJECUTADO-->{RESET} {NARANJA_FUERTE}{payload}{RESET} {ROJO}-->{RESET} {CIAN}{e}{RESET}')
                    print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                    print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                    print(f'-------------------********{ROJO}******///////******{RESET}********------------------------')
                    
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

                    #cuando se detecta una vulnerabilidad o  excepcion envia notificacion por TELEGRAM
                    enviar_mensaje_telegram(e, payload, response.request.url, captura_de_escritorio)

                    print(f'{AZUL}///////////////////////////ANALISIS INYECCION EXITOSA//////////////////////////{RESET}')
                    print(f'------------------------------------------------------------------------------')
                    print(f'{AZUL}- [PAYLOAD INYECTADO: {payload}] {AMARILLO}-{RESET} captura guardada en {archivo_captura}{RESET}')
                    print(f'------------------------------------------------------------------------------')
                    # Analizar la captura de pantalla
                    analizar_captura(payload,captura_de_escritorio)

                    # sonido de alerta
                    sonido_alerta('xss')
                
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
        with open('listaXSS_bypass_y_poliglota.txt', 'r', encoding='utf-8') as archivo_payloads_XSS:
            payloads_XSS = archivo_payloads_XSS.read().splitlines()       

#--------------------------------------------------------------------------------------------------------------------------------
    # Configura el controlador del navegador FIREFOX 
    firefox_options = Options()
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    # Crear el directorio de reportes si no existe
    if not os.path.exists('reportes'):
        os.makedirs('reportes')

#--------------------------------------------------------------------------------------------------------------------------------

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
        'X-HackerOne-Research': header_bug_hunter
    }

#--------------------------------------------------------------------------------------------------------------------------------
    with tqdm(total=total_payloads, desc=f"{MORADO}PROGRESO DE PAYLOAD EJECUTADOS: {RESET}") as pbar:
        
        for payload in payloads_XSS:
            dominio_fuzz_payload = dominio_unico.replace('FUZZ', payload)
            print(dominio_fuzz_payload)
            
            try:
                
                # realiza cada request osea cada solicitud con mi header custom de bug hunter
                response = requests.get(dominio_fuzz_payload, headers=headers)
                
                # imprime los detalles de la solicitud REQUEST
                print(f"URL solicitada: {response.request.url}")
                print(f"Método de solicitud: {response.request.method}")
                print(f'{AZUL}///////////////////////////REQUEST y RESPONSE//////////////////////////{RESET}')
                print(f"{AMARILLO}REQUEST:{RESET}")
                for key, value in response.request.headers.items():
                    print(f"{NARANJA_FUERTE}#{RESET}{AMARILLO}{key}: {value}{RESET}")

                # imprime el cuerpo de la respuesta RESPONSE
                print(f"{AMARILLO}RESPONSE:{RESET}")
                print(f"{NARANJA_FUERTE}#{RESET}Estado de la respuesta: {AMARILLO}{response.status_code}{RESET}")
                print(f"{NARANJA_FUERTE}#{RESET}Cuerpo de la respuesta: {AMARILLO}{response.text[:500]}...{RESET}")
                
                # verifica que se envio el header custom
                if 'X-HackerOne-Research' in response.request.headers:
                    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
                    print(f"{MORADO}Header personalizado enviado: {response.request.headers['X-HackerOne-Research']}{RESET}")
                    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
                    print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                    print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                    print(f'{MORADO}////////////////////////////NUEVA INYECCION////////////////////////////{RESET}')
                    print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                    print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                    
                # si la solicitud fue exitosa, pasa la URL a selenium
                if response.status_code == 200:
                    
                    # Navegar a la URL de destino con Selenium para visualizar la reacción
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
                    
                    print(f'{AZUL}///////////////////////////ANALISIS INYECCION//////////////////////////{RESET}')
                    print(f'------------------------------------------------------------------------------')
                    print(f'{AZUL}- [PAYLOAD: {payload}] {AMARILLO}-{RESET} captura guardada en {archivo_captura}{RESET}')
                    print(f'------------------------------------------------------------------------------')
                    
                    # Analizar la captura de pantalla
                    analizar_captura(payload,ruta_archivo)

                else:
                    print(f'{AMARILLO}------------------------------------------------------------------------------{RESET}')
                    print(f'{NARANJA_FUERTE}Manito dio error la solicitud con {dominio_fuzz_payload + payload} {RESET}')
            
            except Exception as e:
                print(f'-------------------********{ROJO}******///////******{RESET}********------------------------')
                print(f'---------------------------{ROJO}------///ATENCION///------{RESET}--------------------------------')
                print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                print(f'{VIOLETA}- [{dominio_fuzz_payload}]![ {payload} ] - captura]({archivo_captura}){RESET}')
                print(f'{ROJO}///POC///: {CIAN}COPIA aqui-->{RESET} {dominio_fuzz_payload + payload} {CIAN}<--COPIA aqui{RESET} :{RESET}')
                print(f'{ROJO}Fallo Manito o Tenemos un XSS Exitoso 8D :{RESET}  {AMARILLO}{dominio_fuzz_payload}{RESET}: {ROJO}---SCRIPT EJECUTADO-->{RESET} {NARANJA_FUERTE}{payload}{RESET} {ROJO}-->{RESET} {CIAN}{e}{RESET}')
                print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                print(f'-------------------********{ROJO}******///////******{RESET}********------------------------')
                
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

                #cuando se detecta una vulnerabilidad o  excepcion envia notificacion por TELEGRAM
                enviar_mensaje_telegram(e, payload, response.request.url, captura_de_escritorio)

                print(f'{AZUL}///////////////////////////ANALISIS INYECCION EXITOSA//////////////////////////{RESET}')
                print(f'------------------------------------------------------------------------------')
                print(f'{AZUL}- [PAYLOAD: {payload}] {AMARILLO}-{RESET} captura guardada en {archivo_captura}{RESET}')
                print(f'------------------------------------------------------------------------------')
                # Analizar la captura de pantalla
                analizar_captura(payload,captura_de_escritorio)

                # sonido de alerta
                sonido_alerta('xss')
            
            # barra de progreso de payloads
            pbar.update(1)
    
    driver.quit()    

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
# OPCION 3

def opcion_tres(url_post, payload_txt, additional_fields):
    # Muestra la URL objetivo
    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
    print("URL OBJETIVO (POST):")
    print(url_post)
    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')

    # Verificamos si se proporcionó una URL válida
    if not url_post:
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        print(f"{ROJO}No se encontró una URL Manito.{RESET}")
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        return

#--------------------------------------------------------------------------------------------------------------------------------

    # Leer los payloads desde el archivo proporcionado o usar uno por defecto
    if payload_txt:
        with open(payload_txt, 'r', encoding='utf-8') as archivo_payloads_XSS:
            payloads_XSS = archivo_payloads_XSS.read().splitlines()
    else:
        with open('listaXSS_bypass_y_poliglota.txt', 'r', encoding='utf-8') as archivo_payloads_XSS:
            payloads_XSS = archivo_payloads_XSS.read().splitlines()

    # Configura el controlador del navegador Firefox
    firefox_options = Options()
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    # Crear el directorio de reportes si no existe
    if not os.path.exists('reportes'):
        os.makedirs('reportes')

#--------------------------------------------------------------------------------------------------------------------------------

    # Cargar cookies si están disponibles
    print('-----------------------------------------------------------------------')
    cookies_input = input(f"{MORADO}Creaste el archivo de cookies del usuario en formato JSON ?? RESP: {AMARILLO}s{RESET} / {ROJO}n{RESET} {RESET}(ejem: con extension COOKIE EDITOR exportalas en JSON y asi las pegas en un archivo llamándolo cookies.json, por cualquier error tener en cuenta en el parametro SameSite poner en Lax){MORADO} : {RESET} ")
    print('-----------------------------------------------------------------------')

    if cookies_input == 's':
        with open('cookies.json', 'r') as f:
            user_cookies = json.load(f)

        # Navegar al dominio base y cargar cookies
        dominio_base = input(f"{MORADO}Manito por favor dame el DOMINIO BASE al que pertenecen las COOKIES asi termino de CONFIGURAR, (ejem: http://testphp.vulnweb.com/){MORADO} : {RESET} ")
        print('-----------------------------------------------------------------------')
        driver.get(dominio_base)

        for cookie in user_cookies:
            cookie['sameSite'] = 'Lax'
            driver.add_cookie(cookie)
        driver.get(url_post)

#--------------------------------------------------------------------------------------------------------------------------------

    # Utiliza tqdm para mostrar una barra de progreso durante la ejecución de los payloads
    with tqdm(total=len(payloads_XSS), desc=f"{MORADO}PROGRESO DE PAYLOAD EJECUTADOS por POST: {RESET}") as pbar:
        for payload in payloads_XSS:
            try:
                # Navegar a la página con el formulario
                driver.get(url_post)
                time.sleep(2)  # Esperar que la página se cargue completamente

                # Llenar cada uno de los campos del formulario con el payload o valores adicionales proporcionados
                for field_name, field_value in additional_fields.items():
                    if not field_value:  # Si no hay valor proporcionado, usa el payload
                        field_value = payload

                    # Encontrar el elemento por el atributo 'name' y llenar con el valor
                    try:
                        input_element = driver.find_element(By.NAME, field_name)
                        input_element.clear()
                        input_element.send_keys(field_value)
                    except Exception as e:
                        print(f"{ROJO}No se pudo encontrar el campo {field_name} para inyectar. Error: {e}{RESET}")

                # Enviar el formulario
                try:
                    submit_button = driver.find_element(By.XPATH, "//input[@type='submit' or @type='button']")  # Intentar localizar el botón de envío
                    submit_button.click()
                except Exception as e:
                    print(f"{ROJO}No se encontró un botón de envío automático. Error: {e}{RESET}")
                    continue

                # Esperar unos segundos para que se procese la respuesta después del envío
                time.sleep(3)

                # Crear el directorio para almacenar las capturas de pantalla
                directorio_capturas = 'capturas_web'
                os.makedirs(directorio_capturas, exist_ok=True)

                # Guardar la captura de pantalla
                archivo_captura = re.sub(r'[^\w\-_\. ]', '_', payload) + ".png"
                ruta_archivo = os.path.join(directorio_capturas, archivo_captura)
                driver.save_screenshot(ruta_archivo)
                
                print(f'{AZUL}- [{url_post}]![ {payload} ] - captura]({archivo_captura}){RESET}')
                print(f'{AZUL}///////////////////////////ANALISIS INYECCION POST//////////////////////////{RESET}')
                print(f'------------------------------------------------------------------------------')
                print(f'{AZUL}- [PAYLOAD POST: {payload}] {AMARILLO}-{RESET} captura guardada en {archivo_captura}{RESET}')
                print(f'------------------------------------------------------------------------------')

                # Analizar la captura de pantalla
                analizar_captura(payload, ruta_archivo)

            except Exception as e:
                # Si hay un error, mostramos la información relevante y capturamos el estado del sistema
                print(f'-------------------********{ROJO}******///////******{RESET}********------------------------')
                print(f'---------------------------{ROJO}------///ATENCION///------{RESET}--------------------------------')
                print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                print(f'{ROJO}///POC///: {CIAN}Payload ejecutado-->{RESET} {payload} {CIAN}<--COPIA aqui{RESET} :{RESET}')
                print(f'{ROJO}Fallo Manito o Tenemos un XSS Exitoso 8D :{RESET}  {AMARILLO}{url_post}{RESET}: {ROJO}---SCRIPT EJECUTADO-->{RESET} {NARANJA_FUERTE}{payload}{RESET} {ROJO}-->{RESET} {CIAN}{e}{RESET}')
                print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                print(f'---------------------------{ROJO}------///////------{RESET}--------------------------------')
                print(f'-------------------********{ROJO}******///////******{RESET}********------------------------')

            # Actualizamos la barra de progreso
            pbar.update(1)

    # Cerramos el navegador al finalizar
    driver.quit()



#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#Funcion para seleccionar y modificar headers especificos para ser inyectados

#OPCION 4:
# OPCION 4:
def opcion_cuatro(dominio_unico, payload_txt):
    # >>>>> TU HEADER CUSTOM DE BUGHUNTER <<<<<
    headers_propio_de_cazador = {
        'X-HackerOne-Research': header_bug_hunter
    }
    
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
    
    # Seleccionar el header a modificar
    print(f"\n{MORADO}Seleccione los headers que desea modificar o agregar para inyectar:{RESET}")
    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
    print(f"{MORADO}1{RESET} - User-Agent\n{MORADO}2{RESET} - Referer\n{MORADO}3{RESET} - Cookie\n{MORADO}4{RESET} - Host\n{MORADO}5{RESET} - Origin\n{MORADO}6{RESET} - Custom Header\n{MORADO}7{RESET} - Finalizar selección")
    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
    opcion_header = input("Ingrese el número del header a modificar o '7' para finalizar: ")

    if opcion_header == '7':
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        print(f"{ROJO}Selección finalizada. No se realizarán inyecciones.{RESET}")
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        return  

#--------------------------------------------------------------------------------------------------------------------------------

    # Cargar los payloads
    if payload_txt:
        with open(payload_txt, 'r', encoding='utf-8') as archivo_payloads_XSS:
            payloads_XSS = archivo_payloads_XSS.read().splitlines()
    else:
        with open('listaXSS_bypass_y_poliglota.txt', 'r', encoding='utf-8') as archivo_payloads_XSS:
            payloads_XSS = archivo_payloads_XSS.read().splitlines()

    # Configurar el controlador del navegador Firefox
    firefox_options = Options()
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    # Crear el directorio de reportes si no existe
    if not os.path.exists('reportes'):
        os.makedirs('reportes')


#--------------------------------------------------------------------------------------------------------------------------------

    # Solicitar las cookies al usuario
    print('-----------------------------------------------------------------------')
    cookies_input = input(f"{MORADO}Creaste el archivo de cookies del usuario en formato JSON ?? RESP: {AMARILLO}s{RESET} / {ROJO}n{RESET} {RESET}(ejem: con extensión COOKIE EDITOR exportalas en JSON y así las pegas en un archivo llamándolo cookies.json, por cualquier error tener en cuenta en el parámetro SameSite poner en Lax){MORADO} : {RESET} ")
    print('-----------------------------------------------------------------------')
    
    if cookies_input == 's':
        # Cargar las cookies desde el archivo JSON
        with open('cookies.json', 'r') as f:
            user_cookies = json.load(f)
    
        # Solicitar el dominio base para las cookies
        print('-----------------------------------------------------------------------')
        dominio_base = input(f"{MORADO}Manito por favor dame el DOMINIO BASE al que pertenecen las COOKIES para terminar de CONFIGURAR, (ejem: http://testphp.vulnweb.com/){MORADO} : {RESET} ")
        print('-----------------------------------------------------------------------')
            
        # Navegar a una página en blanco para configurar las cookies
        driver.get(dominio_base)
        
        # Modificar el valor de SameSite a 'Lax' para cada cookie
        for cookie in user_cookies:
            cookie['sameSite'] = 'Lax'
        
        for cookie in user_cookies:
            driver.add_cookie(cookie)
        driver.get(dominio_unico)
    
    total_payloads = len(payloads_XSS)


#--------------------------------------------------------------------------------------------------------------------------------
    # Mostrar barra de progreso y ejecutar las inyecciones
    with tqdm(total=total_payloads, desc=f"{MORADO}PROGRESO DE PAYLOAD EJECUTADOS: {RESET}") as pbar:
        for payload in payloads_XSS:
            headers_a_inyectar = headers_propio_de_cazador.copy()

            if opcion_header == '1':
                headers_a_inyectar['User-Agent'] = payload
            elif opcion_header == '2':
                headers_a_inyectar['Referer'] = payload
            elif opcion_header == '3':
                headers_a_inyectar['Cookie'] = payload
            elif opcion_header == '4':
                headers_a_inyectar['Host'] = payload
            elif opcion_header == '5':
                headers_a_inyectar['Origin'] = payload
            elif opcion_header == '6':
                nombre_de_header = input("Ingrese el nombre del header personalizado: ")
                valor_de_header = input(f"Ingrese el valor para {nombre_de_header}: ")
                headers_a_inyectar[nombre_de_header] = valor_de_header

            try:
                # Realizar la solicitud
                response = requests.get(dominio_unico, headers=headers_a_inyectar)
                
                # Imprimir detalles de la solicitud y respuesta
                print(f"URL solicitada: {response.request.url}")
                print(f"Método de solicitud: {response.request.method}")
                print(f'{AZUL}///////////////////////////REQUEST y RESPONSE//////////////////////////{RESET}')
                print(f"{AMARILLO}REQUEST:{RESET}")
                for key, value in response.request.headers.items():
                    print(f"{NARANJA_FUERTE}#{RESET}{AMARILLO}{key}: {value}{RESET}")

                print(f"{AMARILLO}RESPONSE:{RESET}")
                print(f"{NARANJA_FUERTE}#{RESET}Estado de la respuesta: {AMARILLO}{response.status_code}{RESET}")
                print(f"{NARANJA_FUERTE}#{RESET}Cuerpo de la respuesta: {AMARILLO}{response.text[:800]}...{RESET}")

                # Verificar el envío del header personalizado
                if 'X-HackerOne-Research' in response.request.headers:
                    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
                    print(f"{MORADO}Header personalizado enviado: {response.request.headers['X-HackerOne-Research']}{RESET}")
                    print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
                    print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                    print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                    print(f'{MORADO}////////////////////////////NUEVA INYECCION////////////////////////////{RESET}')
                    print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')
                    print(f'{MORADO}///////////////////////////////////////////////////////////////////////{RESET}')

                # Si la solicitud es exitosa, usar Selenium
                if response.status_code == 200:
                    driver.get(dominio_unico)
                    time.sleep(3)
                    
                    directorio_capturas = 'capturas_web'
                    os.makedirs(directorio_capturas, exist_ok=True)
                    
                    archivo_captura = re.sub(r'[^\w\-_\. ]', '_', dominio_unico) + ".png"
                    ruta_archivo = os.path.join(directorio_capturas, archivo_captura)
                    driver.save_screenshot(ruta_archivo)

                    print(f'{AZUL}- [{dominio_unico}]![ HEADERS: {headers_a_inyectar}: {payload} ] - captura]({archivo_captura}){RESET}')
                    analizar_captura(payload, ruta_archivo)

                else:
                    print(f'{AMARILLO}------------------------------------------------------------------------------{RESET}')
                    print(f'{NARANJA_FUERTE}Manito dio error la solicitud con {dominio_unico + payload} {RESET}')

            except Exception as e:
                print(f'-------------------********{ROJO}******///////******{RESET}********------------------------')
                print(f'{ROJO}Fallo Manito o tenemos un XSS exitoso 8D: {RESET}{e}')
                
                max_length = 80
                nombre_base_del_archivo = "{}_{}_VULNERABLE".format(re.sub(r'[^\w\-_\. ]', '_', dominio_unico), re.sub(r'[^\w\-_\. ]', '_', payload))
                nombre_final_del_archivo = nombre_base_del_archivo[:max_length]
                
                captura_de_escritorio = f"reportes/{nombre_final_del_archivo}.png"
                pyautogui.screenshot(captura_de_escritorio)

                enviar_mensaje_telegram(e, payload, response.request.url, captura_de_escritorio)
                analizar_captura(payload, captura_de_escritorio)
                sonido_alerta('xss')

            # Actualizar la barra de progreso
            pbar.update(1)

    driver.quit()



#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#ENVIO DE MENSAJES POR TELEGRAM INFORMANDO VULNERABILIDADES ENCONTRADAS


def enviar_mensaje_telegram(vulnerabilidad, payload, request, captura):
    # Datos del bot y el chat
    bot_token = 'TU_TOKEN_DEL_BOT_de_TELEGRAM_MANITO'
    chat_id = 'TU_ID_DEL_CHAT_MANITO'
    
    # Mensaje a enviar
    mensaje = f'POSIBLE VULNERABILIDAD ENCONTRADA:\nVulnerabilidad: {vulnerabilidad}\nPayload: {payload}\nRequest: {request}'
    
    # URL para enviar el mensaje
    url_mensaje = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    datos = {
        'chat_id': chat_id,
        'text': mensaje
    }

#--------------------------------------------------------------------------------------------------------------------------------
    
    # Enviar el mensaje
    response = requests.post(url_mensaje, data=datos)
    
    # Enviar la captura si existe
    if captura:
        url_archivo = f'https://api.telegram.org/bot{bot_token}/sendDocument'
        with open(captura, 'rb') as archivo:
            archivos = {'document': archivo}
            datos_archivo = {
                'chat_id': chat_id,
                'caption': 'Captura de pantalla relacionada con la vulnerabilidad.'
            }
            response = requests.post(url_archivo, data=datos_archivo, files=archivos)

#--------------------------------------------------------------------------------------------------------------------------------
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        print(f"Mensaje enviado a Telegram correctamente MANITO.")
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
    else:
        print(f'{ROJO}-----------------------------------------------------------------------{RESET}')
        print(f"Error al enviar el mensaje a Telegram: {response.status_code}")
        print(f'{ROJO}-----------------------------------------------------------------------{RESET}')


#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
# Inicio del script
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Manejar la interrupción del usuario (Ctrl + C)
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        print('Gracias Manito por usar P4IvisualInyect_v3.1.py ')
        print(f'{MORADO}-----------------------------------------------------------------------{RESET}')
        exit()
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
