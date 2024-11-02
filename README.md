## FLASK CON IMPLEMENTACION DE THEMOBIESDB

### OVERVIEW
El proyecto desarrolla una API RESTful en Flask que se conecta a The Movie Database (TMDB) siguiendo una arquitectura hexagonal para una clara separación de responsabilidades.

### Instalación
#### Requerimientos
Instalar docker y docker-compose

#### Setup
clona este repositorio y construye el contenedor docker con docker-compose

    git clone git@github.com:AleGorrin/test_flask_themoviedb.git
    cd test_flask_themoviedb
    docker-compose up -d

#### Uso 

La forma recomendable de usar es mediante Postman, ya que la mayoria de solicitudes y peticiones requieren de una autorizacion, primero, se especificaran los Endpoints siendo localhost:5000 la base de cada uno.
Al enviar la peticion, en la seccion de header, se debe agregar 

key:Authorization, Value: numero
dondel el value para realizar pruebas son 
1 para admin
2 para consumidor
NOTA: Estos se encuentran hardcodeados en el proyecto, ya que el enfoque no es creacion y manejo de usuarios. 

#### Endpoints disponibles:

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

#### NOTA: Este desarrollo implementa redis para guardar en la cache las listas obtenidas con GET y para aplicar se ajustaron 30 segundos antes de eliminar la cache.Por lo que, si se realiza una peticion get_favorite y luego add_favorite, no se vera reflejado al realizar la peticion nueva mente de get_favorite hasta pasar los 30 segundos.
#### NOTA: Si bien el desarrollo posee un docker-compose, el aplicativo corre por su cuenta sin depender de redis, realizando las acciones de no encontrara a redis conectado.

### Estructura del proyecto
El proyecto esta estructurado usando arquitectura hexagonal, por lo que cada capa cumple un rol en especifico y mantiene aislamiento. Las capas son las siguientes:

- **Controllers**: Manejan las solicitudes HTTP y devuelven respuestas JSON. Son responsables de interactuar con los servicios de aplicación.
  
- **Application Services**: Contienen la lógica del negocio y se comunican con los adaptadores para obtener datos de la API externa o de otras fuentes.

- **Adapters**: Proporcionan una interfaz para interactuar con APIs externas y pueden incluir lógica de caché para mejorar el rendimiento.

- **Settings**: Configuraciones del proyecto, como claves de API y configuraciones de Redis.

- **Auth**: Maneja la autenticación y autorización de los usuarios.
- **Tests**: Posee los tests para cada seccion del proyecto.

#### Testing
Para ejecutar los tests se debe tener la libreria pytest. En la siguiente seccion, se muestra el cmd esperado para correr las pruebas en un virtualenv, de tal forma que no se instale pytest de forma principal.

    git clone git@github.com:AleGorrin/test_flask_themoviedb.git
    cd test_flask_themoviedb
    pip install virutalenv 
    virtualenv -p python env
    .\env\Scripts\activate
    pip install pytest==8.3.3
    pytest tests -v

    .\env\Scripts\deactivate
