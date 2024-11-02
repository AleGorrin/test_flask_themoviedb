##FLASK CON IMPLEMENTACION DE THEMOBIESDB

###OVERVIEW
El proyecto desarrolla una API RESTful en Flask que se conecta a The Movie Database (TMDB) siguiendo una arquitectura hexagonal para una clara separación de responsabilidades.

####Endpoints disponibles:

/populars
- Salida: JSON con las películas populares de TMDB.

/add_favorite/(media_id)
- Entrada: ID de la película para agregar a favoritos, ID USER/ADMIN
- Salida: JSON con el estado de la operación.

/delete_favorite_movie/(media_id)
- Entrada: ID de la película, ID USER/ADMIN
- Salida: JSON con el estado de la operación.

/rate_movie/(movie_id)/(rating)
- Entrada: ID de la película, valoración (0-5), ID USER/ADMIN
- Salida: JSON con el estado de la operación.

/get_rated_movies_from_favorites
- Entrada: ID USER/ADMIN
- Salida: JSON con las peliculas favoritas ordenadas por rating

/get_favorite_movies_by_release_date
- Entrada: ID USER/ADMIN
- Salida: JSON con las peliculas favoritas ordenadas fecha de salida

/get_favorite_movies
- Entrada: ID USER/ADMIN
- Salida: JSON con las películas favoritas del usuario.

/delete_favorite_movies
- Entrada: ID ADMIN
- Salida: JSON con el estado de la operación.

###Instalación
####Requerimientos
Instalar docker y docker-compose

####Setup
clona este repositorio y construye el contenedor docker con docker-compose

    git clone git@github.com:AleGorrin/test_flask_themoviedb.git
    cd test_flask_themoviedb
    docker-compose up -d

###Estructura del proyecto
- **Controllers**: Manejan las solicitudes HTTP y devuelven respuestas JSON. Son responsables de interactuar con los servicios de aplicación.
  
- **Application Services**: Contienen la lógica del negocio y se comunican con los adaptadores para obtener datos de la API externa o de otras fuentes.

- **Adapters**: Proporcionan una interfaz para interactuar con APIs externas y pueden incluir lógica de caché para mejorar el rendimiento.

- **Settings**: Configuraciones del proyecto, como claves de API y configuraciones de Redis.

- **Auth**: Maneja la autenticación y autorización de los usuarios.
- **Tests**: Posee los tests para cada seccion del proyecto.




