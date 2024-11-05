# 🕷️ P4IvisualInyect.py - v3.1 - By P4IM0N 🍪

**Herramienta avanzada de escaneo de URLs para pruebas de seguridad WEB**

🔍 **P4IvisualInyect** es una herramienta diseñada para escanear URLs con parámetros de inyección obtenidos mediante GoSpider 🕷️ y luego procesarlas automáticamente de manera visual en el navegador con Selenium y Firefox 🌐 para ver el comportamiento del sitio web. Su objetivo principal es capturar rutas y ejecuciones exitosas de vulnerabilidades como XSS, LFI, RCE, SQLi ⚠️, y más. Las capturas 📸 se generan y se agregan a los reportes del PoC y son analizadas con la API de OCR space 🧠. Además, la herramienta incluye el manejo de cookies 🍪 extraídas mediante una extensión de Chrome, que deben ser guardadas en un archivo .json. También ofrece la opción de inyecciones por método GET y POST 🚀. Otra opción importante añadida es la de inyección de payloads en headers (User-Agent, etc.) de las request. Y podemos ejecutarla y dejarla trabajando tranquilos 💤 esperando que nos notifique con nuestro bot de Telegram configurado 📲, con un mensaje informando la vulnerabilidad encontrada, payload exitoso y captura de pantalla.

🚀 **¡Ideal para Bug Bounty Hunters y reducir falsos positivos!**

---

📹 **Tutorial en Video**
A continuación, un video donde explico detalladamente el uso de la herramienta:

[![Video de YouTube - Uso de P4IvisualInyect](https://img.youtube.com/vi/k4_FR2o45CA/0.jpg)](https://www.youtube.com/watch?v=k4_FR2o45CA)


---

⚠️ **Disclaimer**  
No me hago responsable por el mal uso de esta herramienta.  
Está diseñada exclusivamente para fines educativos y de uso ético.

---

🆕 **Próxima Actualización - v1.6**  
- Añadiremos la opción visual de inyección por el método POST.  
- Integración con la API Key de GPT para analizar capturas de pantalla y reducir aún más los falsos positivos.

---

🛠️ **Instalación de Dependencias**  
Para usar correctamente esta herramienta, necesitas instalar las siguientes dependencias.

### 1. Requerimientos básicos
Ejecuta el script `setup.sh` para instalar las dependencias necesarias:

```bash
./setup.sh
```

## Configurar el bot de Telegram

### Paso 1: Crear un Bot en Telegram
1. Abre Telegram y busca el usuario `@BotFather`.
2. Usa el comando `/newbot` para crear un nuevo bot y sigue las instrucciones.
3. Al finalizar, `@BotFather` te proporcionará un **token de API** que necesitarás para enviar mensajes.

### Paso 2: Obtener el ID del Chat
Necesitarás el **ID del chat** al que quieres enviar el mensaje. Esto puede ser tu chat personal o un grupo.

1. Busca tu bot en Telegram y envíale un mensaje para iniciar la conversación.
2. Luego, visita la siguiente URL en tu navegador, reemplazando `<TOKEN>` con el token de tu bot:
```text
http://testphp.vulnweb.com/
```
3. Verás una respuesta en formato JSON que contiene el **ID del chat**. Usa ese ID para enviar mensajes a tu cuenta.



### 2. Instalación manual (en caso de problemas)
Si tienes algún problema de ejecución, asegúrate de que las siguientes dependencias estén correctamente instaladas. Si continúas con problemas, repórtalos para una solución.

#### Dependencias de Python
- **webdriver_manager**: Para manejar la configuración automática de los drivers de Selenium.

```bash
pip install webdriver_manager
```

- **Selenium**: La librería que permite la automatización del navegador.

```bash
pip install selenium
```

### Instalación de Geckodriver
Para que Selenium funcione con Firefox, puede ser necesario instalar Geckodriver. Descarga la versión compatible con tu versión de Firefox desde el sitio oficial de Geckodriver.

### Instalar y configurar GoSpider
GoSpider es la herramienta utilizada para rastrear y recopilar URLs. Para instalarlo:

- Instala GoSpider:

```bash
GO111MODULE=on go install github.com/jaeles-project/gospider@latest
```

- Mueve el binario de GoSpider a `/usr/bin` para facilitar su acceso:

```bash
sudo cp ~/go/bin/gospider /usr/bin
```

---

💻 **Ejecución del Script**  
Una vez instaladas todas las dependencias, puedes ejecutar el script principal:

```bash
python3 P4IvisualInyect.py
```

### Entrada del dominio
Cuando el script te pida `"Introduce el dominio completo, Manito"`, ingresa la URL completa del sitio que deseas escanear. Por ejemplo:

```text
http://testphp.vulnweb.com/
```

### Resultado esperado
El script ejecutará GoSpider para recopilar URLs, filtrará los resultados y los guardará en el archivo `url.txt`. Luego, usará Selenium para inyectar payloads de XSS en esas URLs y capturar capturas de pantalla de las inyecciones exitosas.

---

📈 **Características y Funcionalidades**
- 🕵️‍♂️ **Escaneo de vulnerabilidades**: Inyección automática de payloads de XSS, LFI, RCE, SQLi, y más.
- 📸 **Capturas de pantalla**: Toma capturas de las inyecciones exitosas para documentar el PoC.
- 🍪 **Manejo de cookies**: Extrae y maneja cookies desde un archivo `.json`.
- 🔄 **Actualizaciones continuas**: Funcionalidades adicionales como el análisis mediante API Key de GPT para una mayor precisión.

---

🤝 **Contribuciones**  
Si tienes ideas para mejorar la herramienta o encuentras algún bug, ¡no dudes en contribuir!

🚀 **Herramienta testeada en Kali Linux**. Asegúrate de verificar las rutas de ejecución en tu sistema.

---

🐞 **Reporte de problemas**  
Si experimentas algún problema, verifica las dependencias anteriores. Si el problema persiste, repórtalo con un mensaje claro a la herramienta GPT para su solución.

---

**¡Gracias por usar P4IvisualInyect.py! Happy Hacking!** 🎯
