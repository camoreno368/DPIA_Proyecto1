# Buscador de películas semántico

Este Proyecto implementa un modelo de busqueda semantica usando Python y dara un acercamiento al uso de vectores para procesamiento del lenguaje natural (NLP) con hugging face, esta es la tecnología detrás de herramientas como chatgpt, Llama, o incluso google.

Las instrucciones a continuación lo guiarán a través de la configuración de un entorno virtual, la instalación de las librerias requeridas y la ejecución del script principal de Python.


## Prerequisitos

- Python 3.10 o superior instalado en su maquina
- Git o Github Desktop (Opcional si desea clonar este repositorio)

## Carpetas y Archivos

- data: Contiene la Base de datos de Peliculas (IMDB Top 1000.csv)
- src: Contiene archivo .py del modelo (main_students.py) 
- requirements.txt: Contiene librerias para ejecucion
- semantic_search_students.ipynb:  archivo de pruebas
- .gitignore: contiene las exclusiones al repositorio como es el caso de ambientes virtuales 


### Pasos Para la ejecucion

- ### 1. Clonar Repositorio (Opcional)
    - para clonar el repositorio debe usar el siguiente comando: 

      git clone https://github.com/camoreno368/DPIA_Proyecto1.git

    - ingresas a la carpeta del Repositorio

      cd DPIA_Proyecto1

- ### 2. Creacion del ambiente Virtual
en caso de que desee crear un ambiente virtual para ejecutar el proyecto debe hacerlo usando los siguientes pasos:

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

- ### 5. Ejecucion del modelo

despues de instalar las librerias se ejecuta el modelo usando el archivo **main_students.py**

    python .\src\main_students.py

al ejecutar el modelo le solicitara el nombre de la pelicula o descripcion y este retornara los titulos de peliculas que mayor similaridad respecto a la entrada digitada

---
> Nota: 
>* el archivo **semantic_search_students.ipynb** es un notebook el cual se puede ejecutar en collab o jupiter y sirve para probar el modelo y permite visualizar el codigo detallado