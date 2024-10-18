import pandas as pd
import numpy as np
import os
from sentence_transformers import SentenceTransformer, util
from abc import ABC, abstractmethod

# **Principio DI (Dependency Inversion): Creación de una abstracción para la estrategia de similitud de embeddings**
class SimilarityStrategy(ABC):
    '''
    La Clase SimilarityStrategy es una interfaz abstracta que define el metodo compute_similarity
    Esta interfaz se usa en la clase SemanticSearch y permite desacoplar la lógica de búsqueda semántica 
    de la forma en que se calcula la similitud, permitiendo usar diferentes algoritmos de similitud sin cambiar el código del sistema principal.
    '''
    @abstractmethod
    def compute_similarity(self, embedding, query_embedding):
        pass

# **Aplicación del Patrón Strategy: Estrategia para calcular la similitud utilizando cos_sim**
class CosineSimilarityStrategy(SimilarityStrategy):
    '''
    la Clase CosineSimilarityStrategy Implementa la estrategia concreta para calcular la similitud utilizando la función cos_sim de la librería sentence_transformers. 
    Al heredar de la clase abstracta SimilarityStrategy, puede ser usada de forma intercambiable sin modificar el comportamiento de la clase SemanticSearch.
    '''
    def compute_similarity(self, embedding, query_embedding):
        return util.cos_sim(embedding, query_embedding).item()

# **Principio SR (Single Responsability): Clase para cargar y preparar los datos**
class DataLoader:
    '''
    La Clase DataLoader tiene como única responsabilidad cargar y preparar los datos a partir de un archivo CSV, eliminando duplicados y creando una columna de búsqueda.
    '''
    def __init__(self, filepath):
        self.filepath = filepath
   
    def load_data(self):
        """Carga el archivo CSV y lo prepara eliminando duplicados y creando la columna de búsqueda."""
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"El archivo '{self.filepath}' no fue encontrado.")
        
        df = pd.read_csv(self.filepath)
        df = df.drop_duplicates(subset=df.columns[1])  # Elimina duplicados basados en una columna específica
        df['Busqueda'] = 'Titulo: ' + df['Title'] + ' | ' + 'Description: ' + df['Description'] + '|' + df['Cast'] + ' | ' + 'Genre :' + df['Genre']
        return df

# **Principio SR (Single Responsability): Clase para manejar el modelo y generar embeddings**
class EmbeddingModel:
    '''
     la Clase EmbeddingModel se encarga de generar los embeddings a partir de los datos cargados en el DataFrame.
    '''
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    
    def generate_embeddings(self, df, column='Busqueda'):
        """Genera embeddings a partir de una columna del DataFrame y los almacena."""
        embeddings = self.model.encode(df[column], batch_size=64, show_progress_bar=True)
        df['embeddings'] = [embedding.astype(np.float32) for embedding in embeddings]
        #df['embeddings'] = embeddings.tolist()
        return df

# **Principio OC (Open Closed): Clase que realiza la búsqueda semántica. Se puede extender sin modificar el código original**
class SemanticSearch:
    '''
    La Clase SemanticSearch: Utiliza la interfaz SimilarityStrategy para calcular la similitud, 
    lo que permite que otras estrategias (por ejemplo, EuclideanSimilarityStrategy) se añadan sin cambiar esta clase.
    '''
    def __init__(self, model: SentenceTransformer, similarity_strategy: SimilarityStrategy):
        self.model = model
        self.similarity_strategy = similarity_strategy
    
    def search(self, df, query):
        """Realiza una búsqueda semántica utilizando la estrategia de similitud proporcionada."""
        #query_embedding = self.model.encode(query)  # Generamos los embeddings para la consulta
        query_embedding = self.model.encode(query).astype(np.float32)
        df['similarity'] = df.apply(lambda x: self.similarity_strategy.compute_similarity(x['embeddings'], query_embedding), axis=1)
        df = df.sort_values(by='similarity', ascending=False)
        return df[['Title', 'Description', 'similarity']].head(10)

# **Principio SR (Single Responsability): Clase para manejar la interfaz de usuario se separan en metodos la entrada y salida**
class UserInterface:
    '''
    La Clase UserInterface se encarga de interactuar con el usuario para obtener las busquedas y mostrar los resultados.
    '''
    @staticmethod
    def get_user_query():
        """Obtiene la busqueda del usuario."""
        return input('\nIngresa el término de búsqueda (o Salir para terminar): ')
    
    @staticmethod
    def display_results(results):
        """Muestra los resultados de la búsqueda."""
        print('El Top 10 de las películas de mayor similitud a tu búsqueda son: \n')
        print(results)

# **Función principal utilizando las clases diseñadas**
def main():
    data_loader = DataLoader('./data/IMDB top 1000.csv')
    embedding_model = EmbeddingModel()  # Instanciamos el modelo
    
    try:
        # Cargar y preparar los datos
        df = data_loader.load_data()
        df = embedding_model.generate_embeddings(df)
        
        # Instanciar la búsqueda semántica con la estrategia de similitud (Patrón Strategy)
        search_engine = SemanticSearch(embedding_model.model, CosineSimilarityStrategy())  # Pasamos el modelo y la estrategia
        
        # Interfaz de usuario para obtener las consultas y mostrar resultados
        while True:
            query = UserInterface.get_user_query()
            if query.lower() == 'salir':
                print("Programa finalizado.")
                break
            
            results = search_engine.search(df, query)
            UserInterface.display_results(results)
    
    except FileNotFoundError as e:
        print(e)
    except KeyError as e:
        print(f"Error: Una columna requerida no fue encontrada en el archivo CSV. {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == '__main__':
    main()
