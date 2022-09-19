# Introducción a Selenium
Selenium es una API que nos permite controlar un navegador web, y nos permite interactuar con los sitios como si fueramos usuarios humanos, pero de forma totalmente automatizada.

## Instalación
En un entorno virtual de python, necesitamos instalar la libreria:
1.- Usando pypi:

```console
$ python -m pip install -U selenium
```

2.- Usando conda:

```console
$ conda install selenium
```

Adicionalmente, Selenium requiere un *driver* como interface para interactuar con el navegador especifico que elijamos para trabajar. 

Actualmente hay soporte para: Chrome, Chromium, Firefox, Edge, Safari.

Instalamos el manejador de driver como sigue:

```console
$ python -m pip install webdriver-manager
```

Y este manejador nos instalará en automatico los drivers que requiramos según el navegador.

## Ejemplo de uso
### Importamos la libreria de selenium


```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
```

### Los pasos que debemos seguir para usarlo como web scraper

#### 1.- Instanciamos el ***driver*** para nuestro navegador en particular


```python
service = ChromeService(ChromeDriverManager().install())
```

Agregamos algunas opciones al abrir el navegador


```python
options = webdriver.ChromeOptions()

# Opción para el navegador en Modo Incognito
options.add_argument("--incognito")

# Opción para no abrir el Graphical User Interface del navegador.
#options.add_argument("--headless")
```


```python
driver = webdriver.Chrome(service=service, options=options)
```

#### 2.- Hacemos que el navegador haga la petición a la dirección url de nuestra elección


```python
url = "https://jkanime.net/amagami-ss/"
```


```python
driver.get(url)
```

#### 3.- Extraemos la información de la página

3.1.- Usando expresiones XPath, podemos usar el método `find_elements`, `get_attribute`, `text` para traer los elementos con dicha etiqueta:


```python
ELEMENTOS = '//div[@id="episodes-content"]//div[@class="anime__item"]/a'
```


```python
elementos = driver.find_elements(by=By.XPATH, value=ELEMENTOS).get
len(elementos)
```


```python
capitulo = elementos[0].find_element(by=By.XPATH, value='.//span').text
link = elementos[0].get_attribute('href')
```


```python
print(f"Nombre: {capitulo} \nLink:  {link}")
```


```python
capitulos = []
for elemento in elementos:
    capitulo = elemento.find_element(by=By.XPATH, value='.//span').text
    link = elemento.get_attribute('href')
    
    capitulos.append({"Nombre": capitulo, "Link": link})
    
capitulos
```

3.2.- Para obtener información de menús emergentes al click en un botón, necesitamos interactuar y enviar esa acción al driver de la siguiente manera:


```python
url_cap= 'https://jkanime.net/amagami-ss/10/'
driver = webdriver.Chrome(service=service, options=options)
driver.get(url_cap)
```


```python
download_video_menu = driver.find_element(by=By.XPATH, value='//a[@class="video-download"]')
```

Desplegamos el menú emergente dando `click` al enlace o botón.


```python
download_video_menu.click()
```

Ahora buscamos dentro del menú emergente para encontrar el enlace de descarga, o en su caso, el botón de descarga.


```python
download_video_boton = driver.find_element(by=By.XPATH, value='//a[@id="jkdown"]')
```


```python
download_video_boton.click()
```

Hay que aclarar que puede generar error, ya que otro elemento entrometido puede capturar el click, un elemento de publicidad.
**************

Adicional a esto, al ejecutar todo el código en un script, puede suceder que no le demos tiempo al navegador (driver) de cargar todo el contenido de la página. Por lo que nos lanzará errores o no nos traerá la información completo.

Para solucionar esto, es necesario agregarle *Demoras inteligentes* que esperen hasta que se alcancé o se lancé alguna señal, para continuar con la ejecución del siguiente código.


```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
```


```python
# Tiempo máximo de espera para que la página termine de cargar
timeout = 30 

# El código XPath del elemento que debe aparecer o debe cargar para que continue la ejecución
XPATH_ELEMENT_WAIT = '//' 

try:
    elemento = WebDriverWait(
                    driver, 
                    timeout=timeout
                ).until(EC.presence_of_element_located((By.XPATH, XPATH_ELEMENT_WAIT)))
    # EC tiene muchos otros métodos para monitorear muchos elementos o acciones que esperará encontrar.
except TimeoutException:
    print("Timeout sobrepasado. La página no terminó de cargar.")
    
```

#### 4.- Cerramos el navegador


```python
driver.close()
```

### Si quisieramos ejecutarlo en Firefox


```python
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
```

1.- Instacioamos el servicio y el driver especifico para Firefox


```python
service = FirefoxService(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)
```

2.- Hacemos la consulta de la página web en el driver


```python
driver.get(url)
```

3.- Extraemos la información

4.- Cerramos el driver


```python
driver.close()
```
