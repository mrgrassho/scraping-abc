# De Scraping ABC a DPaaS (_Diaper price as a service_)

Para aprender a realizar scraping no se me ocurre mejor idea que primero plantear un problema y luego a partir de allí ir realizando pequeñas iteraciones sobre como podemos mejorar nuestra solución e incorporar mas funcionalidad.

## Problema

Una integrante del equipo de Prometeo (no daré nombres 😂) nos plantea un problema interesante:

> – Sabes que estaria bueno, poder conseguir el mejor precio por unidad de pañales de Montevideo.<br>
> – ¿Pañales?¿WTF?<br>
> – Si Pañales! No sabes la cantidad de plata que los padres gastan en pañales. Pero ojo! Quiero saber el precio por unidad no por paquete, es decir que se deberia obtener el precio total y dividirlo por la cantidad de pañales que vienen en el paquete. Y tambien... quiero poder filtrar solo por el tamaño que usan mis hijos, y... ya que estamos diferenciar por marca también.<br>
> – Para, para! Vamos por partes jaja

## Pañales al mejor precio 💩

Ahora que tenemos nuestro problema, vamos a interiorizarnos en la mundo pañalero y definiremos los requerimientos que deberá tener nuestro scraper.

### Calculo por Unidad

Para los desconocedores del rubro (me incluyo), los pañales suelen venir en paquetes con diferentes cantidades segun el tamaño (¿Sorprendente no? 😂)

<img width="1198" alt="Screen Shot 2022-04-08 at 18 44 33" src="https://user-images.githubusercontent.com/20926292/162485928-03c00ad5-4f01-42f8-895e-4498909d3f6c.png">

Por ejemplo, el precio por unidad de Pampers Confort XG es `17.29 UYU` (1002.99/58)

### Requerimientos

- Obtener el precio por unidad de pañal de los mejores sitios de venta de pañales de Montevideo (Ver lista).

#### Lista de sitios:
- [panaleraencasa.com](https://panaleraencasa.com/?s=pa%C3%B1al&post_type=product&product_cat=0)
- [botiga.com](https://www.botiga.com.uy/panales-en-oferta-bebes.html?dir=asc&order=price)
- [pigalle.com.uy](https://www.pigalle.com.uy/bebes_panales-y-toallitas)

## Etapas

Vamos a empezar de a poco e ir mejorando la solucion en las siguientes iteraciones:

1. **v1**. Instalación & presentación de [Scrapy](https://docs.scrapy.org/en/latest/topics/commands.html).
2. **v2**. Agregamos scrapers apuntando a los sitios selecionados.
3. **v3**. Incorporamos expresiones regulares para segmentación de datos.
4. **v4**. Agregamos calculo de precio por unidad.
5. **v5**. Almacenemos los datos!!! 🙊
6. **v6**. ¿Y ahora? Armemos una API!

---

### v1 - Instalación & presentación de [Scrapy](https://docs.scrapy.org/en/latest/topics/commands.html).

Como dijimos vamos a comenzar armando la base de nuestros scrapers. Para ello utilizaremos [Scrapy](https://docs.scrapy.org/en/latest/topics/commands.html)  y los comandos que brinda para inicializar un proyecto.

#### Setup

Primero comezaremos haciendo el setup del entorno virtual de python. Perdonen _haters_, pero no voy a utilizar `virtualenv`, yo soy fan de [conda](https://docs.conda.io/projects/conda/en/latest/). Creamos un entorno de python 3.8 con `conda` de la siguiente manera:

```bash
conda create -n scraping-abc python=3.8
```

Una vez instalado, activamos el entorno virtual. Que de paso vale la pena aclarar, el entorno virtual lo debemos activar cada vez que cerremos la terminal donde estemos trabajando!

```bash
conda activate scraping-abc
```

Luego instalamos `scrapy`

```bash
pip install Scrapy
```

#### Creando proyecto

Ahora que instalamos todo, comencemos creando un proyecto de cero. Para ello utilizaremos los comandos que brinda `scrapy` (similares a los que tiene `Django`). 

Primero inicializamos un proyecto con:

```
scrapy startproject DPaaS_v1
```

Una vez inicializado creamos un crawler bien básico.

```bash
cd DPaaS_v1
touch DPaaS_v1/spiders/example.py
```

Y agregamos el siguiente contenido en `DPaaS_v1/spiders/example.py`. El cual es un scraper que realiza una petición `GET` a `http://example.com/` y extrae el titulo y el primer parrafo de la página utilizando Xpath.

```python
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    start_urls = ['http://example.com/']

    def parse(self, response):
        return {
            "title": response.xpath("//h1/text()").get(),
            "description": response.xpath("//p[1]/text()").get(),
        }

```

> No entiendo una \*!@#\*! ¿Qué es XPATH? XPath es un selector de HTML/XML similar a los selectores de css. Aca te dejo una [cheatsheet de Xpath](https://devhints.io/xpath) para tener a mano.

#### Corriendo los scrapers

Correr el scraper es fácil, sobre la carpeta del proyecto que creamos (`DPaaS_v1`) pegamos el siguiente comando, el cual ejecutará el scraper y guardará el contenido en `data.json`:

```
scrapy crawl example -O data.json
```

Ahora vemos el contenido, para chequear que corrió bien:

```json
$ cat data.json | jq
[
  {
    "title": "Example Domain",
    "description": "This domain is for use in illustrative examples in documents. You may use this\n    domain in literature without prior coordination or asking for permission."
  }
]
```

### v2 - Agregamos scrapers apuntando a los sitios selecionados

Primero inicializamos un proyecto nuevo para tener un comienzo mas ordenado:

```bash
scrapy startproject DPaaS_v2
```

#### [panaleraencasa.com](https://panaleraencasa.com/?s=pa%C3%B1al&post_type=product&product_cat=0)

Analizamos el sitio y buscamos donde estan los datos importantes utilizando las dev tools del navegador:

<img width="1195" alt="Screen Shot 2022-04-08 at 21 47 42" src="https://user-images.githubusercontent.com/20926292/162516843-3613416b-fec6-4d5f-820c-f2970a834602.png">

Ahora que sabemos donde buscar utilizamos el comando `scrapy shell <URL>`, el cual dispara una request hacia la URL seleccionada y nos permite interactuar con la respuesta.

```bash
scrapy shell 'https://panaleraencasa.com/?s=pa%C3%B1al&post_type=product&product_cat=0'
```

```
...
2022-04-08 21:16:08 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://panaleraencasa.com/?s=pa%C3%B1al&post_type=product&product_cat=0> (referer: None)
[s] Available Scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x7fb1409231f0>
[s]   item       {}
[s]   request    <GET https://panaleraencasa.com/?s=pa%C3%B1al&post_type=product&product_cat=0>
[s]   response   <200 https://panaleraencasa.com/?s=pa%C3%B1al&post_type=product&product_cat=0>
[s]   settings   <scrapy.settings.Settings object at 0x7fb1409232e0>
[s]   spider     <DefaultSpider 'default' at 0x7fb1514bd4c0>
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
[s]   fetch(req)                  Fetch a scrapy.Request and update local objects
[s]   shelp()           Shell help (print this help)
[s]   view(response)    View response in a browser
```

Una vez adentro de la shell de `scrapy` (similar a una sesion de python interactiva), armamos las expresiones de xpath para obtener los datos. Primero obtenemos los contenedores de cada item dentro de la lista de resultados:

```python
>>> response.xpath("//div[@class='product-information']")[0].get()
'<div class="product-information">\n\t\t<h3 class="product-title"><a href="https://panaleraencasa.com/product/huggies-flex-comfort-xxg-x-100/">Pañales HUGGIES Flex Comfort XXG x 100</a></h3>\t\t\t\t<div class="product-rating-price">\n\t\t\t<div class="wrapp-product-price">\n\t\t\t\t\n\t<span class="price"><span class="woocommerce-Price-amount amount"><span class="woocommerce-Price-currencySymbol">$</span>1,187.00</span></span>\n\t\t\t</div>\n\t\t</div>\n\t\t<div class="fade-in-block">\n\t\t\t<div class="hover-content woodmart-more-desc">\n\t\t\t\t<div class="hover-content-inner woodmart-more-desc-inner">\n\t\t\t\t\t\t\t\t\t</div>\n\t\t\t</div>\n\t\t\t<div class="woodmart-buttons">\n\t\t\t\t<div class="wrap-wishlist-button">\t\t\t<div class="woodmart-wishlist-btn ">\n\t\t\t\t<a href="https://panaleraencasa.com/product/huggies-flex-comfort-xxg-x-100/" data-key="4be7af5d21" data-product-id="460173" data-added-text="Browse Wishlist">Agregar a la lista de deseos</a>\n\t\t\t</div>\n\t\t</div>\n\t\t\t\t<div class="woodmart-add-btn"><a href="?add-to-cart=460173" data-quantity="1" class="button product_type_simple add_to_cart_button ajax_add_to_cart add-to-cart-loop" data-product_id="460173" data-product_sku="127220" aria-label="Agregá “Pañales HUGGIES Flex Comfort XXG x 100” a tu carrito" rel="nofollow"><span>Añadir al Carrito</span></a></div>\n\t\t\t\t<div class="wrap-quickview-button">\t\t\t<div class="quick-view">\n\t\t\t\t<a href="https://panaleraencasa.com/product/huggies-flex-comfort-xxg-x-100/" class="open-quick-view" data-id="460173">Vista rápida</a>\n\t\t\t</div>\n\t\t</div>\n\t\t\t</div>\n\t\t\t\t\t\t\n\t\t\t\t\t</div>\n\t</div>'
>>> item1 = response.xpath("//div[@class='product-information']")[0]
```

Luego de prueba y error obtenemos las dos expresiones para la descripción y para el precio:

```python
>>> item1.xpath(".//a[1]/text()").get()
'Pañales HUGGIES Flex Comfort XXG x 100'
>>> item1.xpath(".//span[@class='price']/span/text()").get()
'1,187.00'
```

Ahora armemos el scraper de `panalera_en_casa`

```bash
scrapy genspider panalera_en_casa 'https://panaleraencasa.com'
```

Incorporamos los Xpath que armamos previamente, y un casteo para el precio del item.

```python
import scrapy


class PanaleraEnCasaSpider(scrapy.Spider):
    name = 'panalera_en_casa'
    allowed_domains = ['panaleraencasa.com']
    start_urls = ['https://panaleraencasa.com/?s=pa%C3%B1al&post_type=product&product_cat=0']

    def parse(self, response):
        for item in response.xpath("//div[@class='product-information']"):
            price = item.xpath(".//span[@class='price']/span/text()").get()
            yield {
                "description": item.xpath(".//a[1]/text()").get(),
                "price": float(price.replace(",",""))
            }

```

Ahora vemos el contenido, para chequear que corrió bien:

```json
$ cat data.json | jq
[
  {
    "description": "Pañales HUGGIES Flex Comfort XXG x 100",
    "price": 1187.0
  },
  {
    "description": "Pañales HUGGIES Flex Comfort XG x 104",
    "price": 1187.0
  },
  {
    "description": "Pañales HUGGIES Flex Conmfort M x 136",
    "price": 1187.0
  },
  ...
]
```

Eso es todo? Nop! Nos falta revisar el paginado, para ello volvemos a las dev tools del navegador.

<img width="1108" alt="Screen Shot 2022-04-08 at 22 54 20" src="https://user-images.githubusercontent.com/20926292/162528922-0d3b77e1-2a92-4c82-8ae0-75c3ce1ae7db.png">


Agregamos el link de la página al final de la método `parse(self, response)`


```python
    def parse(self, response):
        ...
        next_page = response.xpath("//a[contains(@class, 'next')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

```

Ahora si! Scraper completo:

```python
import scrapy


class PanaleraEnCasaSpider(scrapy.Spider):
    name = 'panalera_en_casa'
    allowed_domains = ['panaleraencasa.com']
    start_urls = ['https://panaleraencasa.com/?s=pa%C3%B1al&post_type=product&product_cat=0']

    def parse(self, response):
        for item in response.xpath("//div[@class='product-information']"):
            price = item.xpath(".//span[@class='price']/span/text()").get()
            yield {
                "description": item.xpath(".//a[1]/text()").get(),
                "price": float(price.replace(",",""))
            }
        next_page = response.xpath("//a[contains(@class, 'next')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

```

#### [pigalle.com.uy](https://www.pigalle.com.uy/bebes_panales-y-toallitas)

<img width="1108" alt="Screen Shot 2022-04-08 at 23 41 35" src="https://user-images.githubusercontent.com/20926292/162535967-a1626255-b05c-4f09-afcd-f02ac67c9ab2.png">




```python
>>> item = response.xpath("//div[contains(@class, 'item-box')]")
>>> item.xpath("//h2/text()").get()
'\r\n\t\t\tBABYSEC PACK BIENVENIDA PAÑAL RN + PAÑAL P + TOALLITAS HUMEDAS 3 uni. [40+40+80 uni.]\r\n\t\t'
>>> item.xpath("//div[contains(@class, 'prod-box__current-price')]/text()").get()
'\r\n\t\t\t$1.569\r\n\t\t'
```

```python
import scrapy


class PigalleSpider(scrapy.Spider):
    name = 'pigalle'
    allowed_domains = ['www.pigalle.com.uy']
    start_urls = ['https://www.pigalle.com.uy/bebes_panales-y-toallitas']

    def parse(self, response):
        for item in response.xpath("//div[contains(@class, 'item-box')]"):
            price = item.xpath("//div[contains(@class, 'prod-box__current-price')]/text()").get()
            yield {
                "description": item.xpath("//h2/text()").get().strip(),
                "price": float(price.strip().replace(".", "").replace("$",""))
            }
        next_page = response.xpath("//li[@class='next-page']/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
```


```json
$ cat pigalle.json | jq
[
  {
    "description": "BABYSEC PACK BIENVENIDA PAÑAL RN + PAÑAL P + TOALLITAS HUMEDAS 3 uni. [40+40+80 uni.]",
    "price": 1569
  },
  {
    "description": "BABYSEC PACK BIENVENIDA PAÑAL RN + PAÑAL P + TOALLITAS HUMEDAS 3 uni. [40+40+80 uni.]",
    "price": 1569
  },
  {
    "description": "BABYSEC PACK BIENVENIDA PAÑAL RN + PAÑAL P + TOALLITAS HUMEDAS 3 uni. [40+40+80 uni.]",
    "price": 1569
  },
  ...
]
```
