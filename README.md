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

- Dado un tamaño de pañal, obtener el precio por unidad de pañal de los mejores sitios de venta de pañales de Montevideo (Ver lista) y realizar.

## Etapas

Vamos a empezar de a poco e ir mejorando la solucion en las siguientes iteraciones:

1. **v1**. Instalación & presentación de [Scrapy](https://docs.scrapy.org/en/latest/topics/commands.html).
2. **v2**. Agregamos scrapers apuntando a los sitios selecionados.
3. **v3**. Incorporamos expresiones regulares para segmentación de datos.
4. **v4**. Agregamos calculo de precio por unidad.
5. **v5**. Almacenemos los datos!!! 🙊
6. **v6**. ¿Y ahora? Armemos una API!

Comencemossss 🏎

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

```
pip install Scrapy
```

#### Creando proyecto

Ahora que instalamos todo, comencemos creando un proyecto de cero. Para ello utilizaremos los comandos que brinda `scrapy` (similares a los que tiene `Django`). 

Primero inicializamos un proyecto con:

```
scrapy startproject DPaaS_v1
```

Una vez inicializado creamos un crawler bien básico.

```
cd DPaaS_v1
touch DPaaS_v1/spiders/example.py
```

Y agregamos el siguiente contenido en `DPaaS_v1/spiders/example.py`. El cual es un scraper que realiza una petición `GET` a `http://example.com/` y extrae el titulo y el primer parrafo de la página utilizando Xpath.

```
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

Para correr el scraper es fácil, sobre la carpeta del proyecto que creamos (`DPaaS_v1`) corremos el siguiente comando, el cual ejecutará el scraper y guardará el contenido en `data.json`:

```
scrapy crawl example -O data.json
```

Ahora vemos el contenido, para chequear que corrió bien:

```
$ cat data.json | jq
[
  {
    "title": "Example Domain",
    "description": "This domain is for use in illustrative examples in documents. You may use this\n    domain in literature without prior coordination or asking for permission."
  }
]
```
