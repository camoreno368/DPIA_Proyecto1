import pandas as pd
import os
from sentence_transformers import SentenceTransformer, util

    #print(df.head())
    # TODO: Completar esta función para realizar búsquedas semánticas con base en el código del archivo test.ipynb
    # Se borran los Duplicados
def modelo():
    
    try:
        if not os.path.exists('./data/IMDB top 1000.csv'):
            raise FileNotFoundError("El archivo './data/IMDB top 1000.csv' no fue encontrado.")

        df = pd.read_csv('./data/IMDB top 1000.csv')    
        df = df.drop_duplicates(df.columns[1])
        # Se crea una columna Busqueda y se concatena con Description, Cast y Genre par ampliar la vectorizacion
        df['Busqueda']= 'Titulo: '+df['Title']+' | '+'Description: '+df['Description']+'|'+df['Cast']+' | '+'Genre :'+df['Genre']

        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        embeddings = model.encode(df['Busqueda'],batch_size=64,show_progress_bar=True)

        df['embeddings'] = embeddings.tolist()
        return df

    except FileNotFoundError as e:
        print(e)
        return None
    except KeyError as e:
        print(f"Error: Una columna requerida no fue encontrada en el archivo CSV. {e}")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None

def compute_similarity(example, query_embedding):
    embedding = example['embeddings']
    similarity = util.cos_sim(embedding, query_embedding).item()
    return similarity

def main(query,df):
    
    try:
        
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        query_embedding = model.encode(query)
        df['similarity'] = df.apply(lambda x: compute_similarity(x, query_embedding), axis=1)
        df = df.sort_values(by='similarity', ascending=False)
        print('El Top 10 de Las Peliculas de mayor similitud a tu busqueda son: \n ')
        print(df[['Title','Description','similarity']].head(10))

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")    

if __name__ == '__main__':
    
    df = modelo()
    if df is not None:
        while True:
            query = input('\ningresa el termino de busqueda (o Salir para Terminar): ')

            if query.lower() == 'salir':  # Compara la entrada con 'salir' (sin importar mayúsculas)
                print("Programa finalizado.")
                break
            else:   
                main(query,df)