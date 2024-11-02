##FLASK CON IMPLEMENTACION DE THEMOBIESDB

###OVERVIEW
El proyecto desarrolla una API RESTful en Flask que se conecta a The Movie Database (TMDB) siguiendo una arquitectura hexagonal para una clara separación de responsabilidades.

####Endpoints disponibles:

/populars
- Salida: JSON con las películas populares de TMDB.

/add_favorite/(media_id)
- Entrada: ID de la película para agregar a favoritos.
- Salida: JSON con el estado de la operación.

/delete_favorite_movie/(media_id)
- Entrada: ID de la película .
- Salida: JSON con el estado de la operación.

/rate_movie/(movie_id)/(rating)
- Entrada: ID de la película y valoración (0-5).
- Salida: JSON con el estado de la operación.

/get_rated_movies_from_favorites
- Salida: JSON con las peliculas favoritas ordenadas por rating

/get_favorite_movies_by_release_date
- Salida: JSON con las peliculas favoritas ordenadas fecha de salida

/get_favorite_movies
- Salida: JSON con las películas favoritas del usuario.

/delete_favorite_movies
- Entrada: ID de admin
- Salida: JSON con el estado de la operación.

###Instalación

###Estructura del proyecto
- **Controllers**: Manejan las solicitudes HTTP y devuelven respuestas JSON. Son responsables de interactuar con los servicios de aplicación.
  
- **Application Services**: Contienen la lógica del negocio y se comunican con los adaptadores para obtener datos de la API externa o de otras fuentes.

- **Adapters**: Proporcionan una interfaz para interactuar con APIs externas y pueden incluir lógica de caché para mejorar el rendimiento.

- **Settings**: Configuraciones del proyecto, como claves de API y configuraciones de Redis.

- **Auth**: Maneja la autenticación y autorización de los usuarios.
- **Tests**: Posee los tests para cada seccion del proyecto.




