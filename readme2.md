# Buscador de películas semántico

Este Proyecto implementa un modelo de busqueda semantica usando Python y dara un acercamiento al uso de vectores para procesamiento del lenguaje natural (NLP) con hugging face, esta es la tecnología detrás de herramientas como chatgpt, Llama, o incluso google.

En el desarrollo del codigo se atomizaron las funciones que en conjunto conformaban el programa con el fin de que el codigo tuviera alta cohesion ademas se utilizaron clases abstractas para que este tuviera bajo acople logrando asi una baja dependencia de sus funciones

para esto se aplicaron varios principos **SOLID** asi como el patron de diseño **Strategy** el cual permite definir una familia de algoritmos, encapsularlos en clases separadas, y hacer que los algoritmos sean intercambiables, esto hace el sistema más modular, fácil de mantener y escalable.

el detalle donse de usaron los principios SOLID y el Patron de Diseño se documenta en las funciones dentro del archivo main.py

Las instrucciones a continuación lo guiarán para la ejecucion del proyecto de busqueda semantica desde un contenedor Docker 

## Prerequisitos

- Python 3.10 o superior instalado en su maquina
- Git o Github Desktop (Opcional si desea clonar este repositorio)
- Docker Desktop

## Carpetas y Archivos

- data: Contiene la Base de datos de Peliculas (IMDB Top 1000.csv)
- src: Contiene archivo .py del modelo (main_students.py) 
- requirements.txt: Contiene librerias para ejecucion
- semantic_search_students.ipynb:  archivo de pruebas
- .gitignore: contiene las exclusiones al repositorio como es el caso de ambientes virtuales 
- Dockerfile : archivo inicializacion Docker
- test: carpeta con archivos de Prueba

## Archivos de Prueba

para la realizacion de la pruebas se desarrollaron cinco metodos los cual validan las funcionalidades clave del sistema para búsqueda semántica, asegurando que las clases y métodos implementados sigan el comportamiento esperado. para la ejecucion de las pruebas unitarias se utilizó pytest, el cual que facilita la ejecución y mantenimiento de las pruebas.


- ### Creacion del ambiente Virtual para Pruebas
para realizar las pruebas se recomienda crear un ambiente virtual para ejecutar el proyecto debe hacerlo usando los siguientes pasos:

## Windows

    python -m venv venv  

## MacOS or Linux

    python3 -m venv venv

- ### 3. Activacion del ambiente Virtual

Despues de crear el ambiente virtual debe activarlo

## Windows

    venv\Scripts\activate 

## MacOS or Linux

    source venv/bin/activate

- ### 4. Instalacion de Librerias

Una vez activado el ambiente virtual se deben instalar las librerias requeridas usando el archivo **requirements.txt**

    pip install -r requirements.txt

## Ejecucion de Pruebas

- para la implementacion de los metodos se creo el archivo test_sematic.py el cual se encuentra dentro de la carpeta **test**

- Luego de creado el archivo test_sematic.py, para realizar las pruebas de los metodos se uso el siguiente comando:

    pytest  test/test_semantic.py

- se realizaron las respectias correcciones en el codigo para que todos los 5 test marcaran PASS

- para validar la covertura de las pruebas se uso el comando:

    coverage run -m pytest test/test_semantic.py

- para la creacion del reporte se uso el comando:

    coverage report

- para la generacion del archivo html se uso el comando:

    coverage html

este comando crea la carpeta htmlcov en la cual se encuentra el archivo **index.html** el cual muestra de una manera grafica los resultados de la covertura total que para este caso fue del **76%**

![alt text](coverage.JPG)


### Pasos Para la ejecucion en Docker

- ### 1. Clonar Repositorio (Opcional)
    - para clonar el repositorio debe usar el siguiente comando: 

      git clone https://github.com/camoreno368/DPIA_Proyecto1.git

    - ingresas a la carpeta del Repositorio

      cd DPIA_Proyecto1

- ### 2. Ejecucion en Docker
lo siguiente comandos le serviran para crear una imagen en docker y ejecutar el contenedor con la aplicacion de busqueda semantica

## Creacion de Imagen
   - dentro de la carpeta DPIA_Proyecto1 que es donde se encuentra el archivo Dockerfile se ejecuta el siguiente comando:

     docker build -t semantic . 

## captura de ID de imagen

- se ejecuta el siguiente comando para capturar el ID de la imagen previamente creada

    docker images 

## Ejecucion del Contenedor

    docker run -it ID_IMAGEN 

al ejecutar el modelo le solicitara el nombre de la pelicula o descripcion y este retornara los titulos de peliculas que mayor similaridad respecto a la entrada digitada


---
> Nota: 
>* el archivo **semantic_search_students.ipynb** es un notebook el cual se puede ejecutar en collab o jupiter y sirve para probar el modelo y permite visualizar el codigo detallado