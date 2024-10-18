import pytest
import numpy as np
import pandas as pd
from src.main import DataLoader, CosineSimilarityStrategy, EmbeddingModel, SemanticSearch

def test_file_not_found():
    '''
    Descripción: Se crea una instancia de DataLoader con un archivo inexistente ('non_existent_file.csv'),
                 se espera que al intentar cargar los datos, se lance una excepción FileNotFoundError. 
                 Utiliza pytest.raises para verificar que la excepción es lanzada adecuadamente.

    Verificación: Si la excepción es lanzada, la prueba pasa; de lo contrario, falla.
    '''
    loader = DataLoader('non_existent_file.csv')
    with pytest.raises(FileNotFoundError):
        loader.load_data()

def test_load_data():
    '''
    Descripción: Esta prueba utiliza un archivo CSV existente ('./data/IMDB top 1000.csv') para cargar los datos.
    Valida que el archivo se cargue correctamente como un DataFrame y que se haya añadido la columna 'Busqueda'.
    
    Verificación:Se asegura de que el objeto devuelto sea un DataFrame.
    Valida que la columna 'Busqueda' esté presente en los datos cargados.
    '''
    loader = DataLoader('./data/IMDB top 1000.csv')
    df = loader.load_data()
    assert isinstance(df, pd.DataFrame)
    assert 'Busqueda' in df.columns

def test_cosine_similarity():
    '''
    Descripción: Probar que la estrategia de similitud coseno (CosineSimilarityStrategy) funcione correctamente calculando la similitud entre dos vectores (embeddings).
    Esta prueba usa dos embeddings sencillos, [1.0, 0.0, 0.0] y [1.0, 0.0, 0.0], los cuales son idénticos. La similitud coseno entre estos dos vectores debería ser exactamente 1.0.

    Verificación: Se asegura de que el valor de similitud sea 1.0 para estos vectores.
    '''
    strategy = CosineSimilarityStrategy()
    embedding = [1.0, 0.0, 0.0]
    query_embedding = [1.0, 0.0, 0.0]
    similarity = strategy.compute_similarity(embedding, query_embedding)
    assert similarity == 1.0

def test_generate_embeddings():
    '''
    Descripción: Esta prueba utiliza un DataFrame con una única fila que contiene una cadena de búsqueda. Se pasa este DataFrame al método generate_embeddings del EmbeddingModel.
    La prueba asegura que la columna embeddings haya sido añadida al DataFrame.

    Verificación: Se asegura de que la columna 'embeddings' exista en el DataFrame después de la generación de embeddings.
    '''
    df = pd.DataFrame({'Busqueda': ['pelicula de ciencia ficcion']})
    model = EmbeddingModel()
    df = model.generate_embeddings(df)
    assert 'embeddings' in df.columns

def test_search():
    '''
    Descripción: Se simula un DataFrame con datos de una película y sus embeddings pre-generados.
    se ejecuta una búsqueda con la palabra clave 'matrix' utilizando la clase SemanticSearch y la estrategia de similitud coseno. 
    La prueba verifica que el resultado contenga una fila y que incluya una columna de similitud.

    Verificación: Se asegura de que el número de resultados sea 1. Verifica que la columna 'similarity' esté presente en el resultado.
    '''
    df = pd.DataFrame({
        'Title': ['Matrix Recargado'],
        'Description': ['pelicula de ciencia ficcion'],
        'Cast': ['Keanu reeves'],
        'Genre': ['Ficcion'],
        'embeddings': [np.random.rand(384).astype(np.float32)]
    })
    query = 'matrix'
    model = EmbeddingModel().model
    search_engine = SemanticSearch(model, CosineSimilarityStrategy())
    result = search_engine.search(df, query)
    assert len(result) == 1
    assert 'similarity' in result.columns

