import pandas as pd
from sentence_transformers import SentenceTransformer, util

    #print(df.head())
    # TODO: Completar esta función para realizar búsquedas semánticas con base en el código del archivo test.ipynb
    # Se borran los Duplicados
def modelo():
    df = pd.read_csv('./data/IMDB top 1000.csv')    
    df = df.drop_duplicates(df.columns[1])
    # Se crea una columna Busqueda y se concatena con Descripcio, Cast y Genre
    df['Busqueda']= 'Titulo: '+df['Title']+' | '+'Description: '+df['Description']+'|'+df['Cast']+' | '+'Genre :'+df['Genre']

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    embeddings = model.encode(df['Busqueda'],batch_size=64,show_progress_bar=True)

    df['embeddings'] = embeddings.tolist()
    return df

def compute_similarity(example, query_embedding):
    embedding = example['embeddings']
    similarity = util.cos_sim(embedding, query_embedding).item()
    return similarity

def main(query,df):
    


    #while True:
   # entrada = input("Introduce patron busqueda (o escribe 'salir' para terminar): ")

    #if query.lower() == 'salir':  # Compara la entrada con 'salir' (sin importar mayúsculas)
     #   print("Programa finalizado.")
        #break  # Sale del bucle si el usuario escribe 'salir'

    try:
        #nombre = (entrada)  # Intenta convertir la entrada a un número
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        query_embedding = model.encode(query)
        df['similarity'] = df.apply(lambda x: compute_similarity(x, query_embedding), axis=1)
        df = df.sort_values(by='similarity', ascending=False)
        print(df[['Title','Description','similarity']].head())
        # Aquí puedes añadir más lógica según lo que necesites hacer con el número
    except ValueError:
        print("Por favor, PATRON busqueda o 'salir'.")

if __name__ == '__main__':
    
    df = modelo()
    while True:
     query = input('ingresa el termino de busqueda (o Salir para Terminar): ')

     if query.lower() == 'salir':  # Compara la entrada con 'salir' (sin importar mayúsculas)
        print("Programa finalizado.")
        break
     else:   
        main(query,df)