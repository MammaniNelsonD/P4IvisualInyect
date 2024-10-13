# 🕷️ P4IvisualInyect.py - v1.5 - By P4IM0N 🍪

**Herramienta avanzada de escaneo de URLs para pruebas de seguridad**

🔍 **P4IvisualInyect** es una herramienta diseñada para escanear URLs con parámetros de inyección obtenidos mediante GoSpider y luego procesarlas automáticamente en el navegador con Selenium y Firefox. Su objetivo principal es capturar rutas y ejecuciones exitosas de vulnerabilidades como XSS, LFI, RCE, SQLi, y más. Las capturas se generan y se agregan a los reportes del PoC. Además, la herramienta incluye el manejo de cookies extraídas mediante una extensión de Chrome, que deben ser guardadas en un archivo `.json`.

🚀 **¡Ideal para Bug Bounty Hunters y reducir falsos positivos!**

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
