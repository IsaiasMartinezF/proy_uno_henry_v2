from fastapi import FastAPI
import pandas as pd
df = pd.read_csv('data_trans')
df['Release Date'] = pd.to_datetime(df['release_date'])
app =FastAPI()

#S.P.M.:
# @app.get('/cantidad_filmaciones_mes/{mes}')
# def cantidad_filmaciones_mes(mes:str):
#     '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes historicamente'''
#     return {'mes':mes, 'cantidad':respuesta}

@app.get("/cantidad_filmaciones_mes/{Mes}")
def cantidad_filmaciones_mes(Mes):
    
    # Mapear los nombres de los meses en español a los números de mes
    meses = {
        'enero': '01',
        'febrero': '02',
        'marzo': '03',
        'abril': '04',
        'mayo': '05',
        'junio': '06',
        'julio': '07',
        'agosto': '08',
        'septiembre': '09',
        'octubre': '10',
        'noviembre': '11',
        'diciembre': '12'
    }
    
    # Convertir el mes consultado a minúsculas y obtener su equivalente en número de mes
    mes_numero = meses.get(Mes.lower())
    #print(mes_numero)
    # Filtrar el DataFrame por el mes consultado
    df_mes = df[df['release_date'].str.contains(f'-{mes_numero}-')]
    #print(df_mes)
    # Obtener la cantidad de películas estrenadas en el mes consultado
    cantidad_pelis = len(df_mes)
    # Devolver el resultado
    #return f"{cantidad_pelis} cantidad de películas fueron estrenadas en el mes de {Mes}"
    return {'mes':Mes, 'cantidad':cantidad_pelis}



# @app.get('/cantidad_filmaciones_dia{dia}')
# def cantidad_filmaciones_dia(dia:str):
#     '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrebaron ese dia historicamente'''
#     return {'dia':dia, 'cantidad':respuesta}

@app.get("/cantidad_filmaciones_dia/{Dia}")
def cantidad_filmaciones_dia(Dia):
    
    # Convertir la columna 'Release Date' a un tipo de dato de fecha
    #df['Release Date'] = pd.to_datetime(df['release_date'])
    
    # Mapear los nombres de los días en español a los números de día
    dias = {
        'lunes': 'Monday',
        'martes': 'Tuesday',
        'miércoles': 'Wednesday',
        'jueves': 'Thursday',
        'viernes': 'Friday',
        'sábado': 'Saturday',
        'domingo': 'Sunday'
    }
    
    # Convertir el día consultado a minúsculas y obtener su equivalente en nombre de día en inglés
    dia_ingles = dias.get(Dia.lower())
    
    # Filtrar el DataFrame por el día consultado
    df_dia = df[df['Release Date'].dt.day_name() == dia_ingles]
    
    # Obtener la cantidad de películas estrenadas en el día consultado
    cantidad_pelis = len(df_dia)
    
    # Devolver el resultado
    #return f"{cantidad_pelis} cantidad de películas fueron estrenadas en los días {Dia}"
    return {'dia':Dia, 'cantidad':cantidad_pelis}


# @app.get('/score_titulo/{titulo}')
# def score_titulo(titulo:str):
#     '''Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score'''
#     return {'titulo':titulo, 'anio':respuesta, 'popularidad':respuesta}

@app.get("/score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo_de_la_filmacion):
    
    # Filtrar el DataFrame por el título de la filmación
    df_filmacion = df[df['title'] == titulo_de_la_filmacion]
    
    # Verificar si se encontró la filmación
    if len(df_filmacion) == 0:
        return f"No se encontró la película {titulo_de_la_filmacion}"
    
    # Obtener los datos de la filmación (título, año de estreno y score)
    titulo = df_filmacion['title'].values[0]
    año_estreno = df_filmacion['release_year'].values[0]
    score = df_filmacion['popularity'].values[0]
    
    # Devolver el resultado
    #return f"La película {titulo} fue estrenada en el año {año_estreno} con un score/popularidad de {score}"
    return {'titulo':titulo, 'anio':año_estreno, 'popularidad':score}


# @app.get('/votos_titulo/{titulo}')
# def votos_titulo(titulo:str):
#     '''Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. 
#     La misma variable deberá de contar con al menos 2000 valoraciones, 
#     caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.'''
#     return {'titulo':titulo, 'anio':respuesta, 'voto_total':respuesta, 'voto_promedio':respuesta}

@app.get("/votos_titulo/{titulo_de_la_filmacion}")
def votos_titulo(titulo_de_la_filmacion):
    
    # Filtrar el DataFrame por el título de la filmación
    df_filmacion = df[df['title'] == titulo_de_la_filmacion]

    # Verificar si se encontró la filmación
    if len(df_filmacion) == 0:
        return f"No se encontró la película {titulo_de_la_filmacion}"  
     
    # Obtener los datos de la filmación (título, cantidad de votos y valor promedio de las votaciones)
    titulo = df_filmacion['title'].values[0]
    votos = df_filmacion['vote_count'].values[0]
    promedio_votos = df_filmacion['vote_average'].values[0]
    a_estreno = df_filmacion['release_year'].values[0]

    # Verificar si la cantidad de votos cumple con la condición mínima de 2000
    if votos < 2000:
        return f"La película {titulo} no cumple con la condición mínima de 2000 votos"
    # Devolver el resultado
    #return f"La película {titulo} fue estrenada en el año {a_estreno}.La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio_votos}"
    return {'titulo':titulo, 'anio':a_estreno, 'voto_total':votos, 'voto_promedio':promedio_votos}



# @app.get('/get_actor/{nombre_actor}')
# def get_actor(nombre_actor:str):
#     '''Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
#     Además, la cantidad de películas que en las que ha participado y el promedio de retorno'''
#     return {'actor':nombre_actor, 'cantidad_filmaciones':respuesta, 'retorno_total':respuesta, 'retorno_promedio':respuesta}
@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor):
    
    # Filtrar el DataFrame por el nombre del actor
    df_actor = df[df['cast'].apply(lambda x: nombre_actor in x)]
    
    # Verificar si se encontró el actor
    if len(df_actor) == 0:
        return f"No se encontró el actor {nombre_actor}"
    
    # Filtrar el DataFrame para excluir las filas correspondientes a directores
    #df_actor = df_actor[df_actor['Rol'] != 'Director']
    
    # Obtener los datos del actor (cantidad de filmaciones, éxito y promedio de retorno)
    cantidad_filmaciones = len(df_actor)
    exito = df_actor['return'].sum()
    promedio_retorno = df_actor['return'].mean()

    # Devolver el resultado
    #return f"El actor {nombre_actor} ha participado en {cantidad_filmaciones} cantidad de filmaciones. a conseguido un retorno de {exito} con un promedio de {promedio_retorno} por filmación."
    return {'actor':nombre_actor, 'cantidad_filmaciones':cantidad_filmaciones, 'retorno_total':exito, 'retorno_promedio':promedio_retorno}



# @app.get('/get_director/{nombre_director}')
# def get_director(nombre_director:str):
#     ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
#     Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.'''
#     return {'director':nombre_director, 'retorno_total_director':respuesta, 
#     'peliculas':respuesta, 'anio':respuesta,, 'retorno_pelicula':respuesta, 
#     'budget_pelicula':respuesta, 'revenue_pelicula':respuesta}
@app.get("/get_director/{nombre_director}")

def get_director(nombre_director):
    # Filtrar el DataFrame por el nombre del director
    df_director = df[df['crew'].apply(lambda x: nombre_director in x)]
    
    # Verificar si se encontró el director
    if len(df_director) == 0:
        return {"director": nombre_director, "retorno_total_director": "No se encontró el director",
                "peliculas": [], "anio": [], "retorno_pelicula": [], "budget_pelicula": [], "revenue_pelicula": []}
    
    # Obtener los datos del director (éxito y detalles de cada película)
    exito = df_director['return'].sum()
    detalles_peliculas = []
    for _, row in df_director.iterrows():
        titulo = row['title']
        fecha_lanzamiento = row['release_date']
        retorno = row['return']
        costo = row['budget']
        ganancia = row['revenue'] - row['budget']
        detalles_peliculas.append((titulo, fecha_lanzamiento, retorno, costo, ganancia))
    
    # Construir el diccionario de respuesta
    respuesta = {
        "director": nombre_director,
        "retorno_total_director": exito,
        "peliculas": [],
        "anio": [],
        "retorno_pelicula": [],
        "budget_pelicula": [],
        "revenue_pelicula": []
    }
    
    for detalle in detalles_peliculas:
        titulo, fecha_lanzamiento, retorno, costo, ganancia = detalle
        respuesta["peliculas"].append(titulo)
        respuesta["anio"].append(fecha_lanzamiento)
        respuesta["retorno_pelicula"].append(retorno)
        respuesta["budget_pelicula"].append(costo)
        respuesta["revenue_pelicula"].append(ganancia)
    
    return respuesta



#generemos el modelo para hacer el coseno de similitud:
#con la base un poco mas pequeña, por el computo y memoria corta generemos la ultyima funcion
df_ml = pd.read_excel('df_machler.xlsx')
df_ml = df_ml[:2000]

#vectorizacion
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(max_features=15)#con 100 y 50 en el otro jala
vectorized_data = tfidf.fit_transform(df_ml['tags'].values)

vectorized_dataframe = pd.DataFrame(vectorized_data.toarray(), index=df_ml['tags'].index.tolist())

#reduccion de dimensiones
from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components=5)

reduced_data = svd.fit_transform(vectorized_dataframe)

#importemos la libreria para el coseno
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(reduced_data)





# ML
@app.get('/recomendacion/{titulo}')
#la segnora funcion 

def recomendacion(titulo):
    id_of_movie = df_ml[df_ml['title']==titulo].index[0]
    distances = similarity[id_of_movie]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    recommended_movies = [df_ml.iloc[movie_id[0]].title for movie_id in movie_list]
    return {'lista recomendada': recommended_movies}