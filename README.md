# TwitterFilter MongoDB

## Autora: Almudena García Jurado-Centurión

## Objetivo del proyecto

Llevar a la práctica, mediante una aplicación informática, los conocimientos adquiridos durante el desarrollo de la  asignatura, en la parte  correspondiente a las bases de datos NoSQL

Este proyecto consistirá en la realización de una aplicación (escritorio, web, etc.) cuya funcionalidad
esté basada, fundamentalmente, en la gestión de un Sistema de Información NoSQL.
La fuente de datos seleccionada para esta práctica serán los tweets extraídos de la red social Twitter
a través de su API.

## Pasos previos

Pasos previos
Para poder extraer tweets es necesario crear una cuenta de desarrollador en la API de Twitter.
Previamente debemos tener una cuenta en la red social Twitter.
Los pasos a seguir son:

- Crear una cuenta en apps.twitter.com
- Crear una nueva APP (es necesario completar los campos obligatorios del formulario y aceptar los términos y condiciones de Twitter)
- Una vez que el proyecto ha sido creado, es necesario obtener los accesos correspondientes
pulsando "Keys and Access Tokens"
- Al final del proceso, debemos tener los siguientes códigos necesarios para conectarnos a
Twitter mediante su API:

	- Customer Secret
	- Consumer Key
	- Access Token
	- Access Secret Token
	
## Diseño del proyecto

El proyecto tendrá dos partes diferenciadas:

1. Un script Python cuya funcionalidad será la de extraer tweets y almacenarlos en la base de datos.
La aplicación podrá ejecutarse desde la línea de comandos o se podrá diseñar una interfaz gráfica
para que el usuario pueda introducir los argumentos (por ejemplo, la/s palabra/s de búsqueda, el
número de tweets que desea almacenar, etc.). En esta parte no se debe establecer ningún filtro
para la búsqueda aunque podéis almacenar solo los campos que consideréis necesarios para
implementar la funcionalidad de la aplicación.

2. Una aplicación informática (escritorio, web, etc.) para gestionar la información de los tweets
almacenados. La aplicación tendrá dos secciones diferenciadas:

	- Estadísticas de las colecciones de tuits
	- Filtrado de un subconjunto de tuits
	

## Planteamiento

### Descarga de los tuits

Para la descarga de los tuits, se ha utilizado un cursor que descarga los tuits desde el histórico de Twitter. Dado que usamos la API gratuita, la búsqueda se limita a los últimos 15 días.

La búsqueda se puede filtrar por fecha inicial y/o fecha final (si usamos únicamente la fecha final, estaremos limitados a los últimos 7 días) y por palabras clave. Para que el texto de los tuits se descargue completo, utilizamos el modo "extended" de la API. También se le debe indicar la cantidad de tuits a descargar.

La API de Twitter permite la descarga de una cantidad limitada de tuits en una única operación. Para que la descarga no se detenga en caso de superarla, activamos la opción de esperar en caso de superar la ratio de descarga. Esto esperará el tiempo indicado por la API, y reanudará la descarga automáticamente al terminar la espera.

Los tuits se descargan en ficheros de texto en formato json, en forma de array de documentos. Estos se almacenarán en el directorio del proyecto, o en la ruta indicada por el usuario.

### Carga de los tuits en la base de datos

Una vez descargados las colecciones de tuits en nuestro directorio, toca cargarlos en MongoDB. 
La colección está en un único JSON, en forma de array de documentos, por lo que, si la cargamos tal cual, se creará un único documento con todo el array.

Para resolverlo, nos creamos una función que lee el fichero json documento a documento, y lo va cargando en la colección indicada de la base de datos. A su vez, el formato de fecha utilizado por los tuits no es interpretable por MongoDB, por lo que, antes de cargar el documento, realizamos una conversión del campo `created_at` a un formato de fecha adecuado. Una vez hecho esto, el documento se carga con todos sus campos dentro de la colección.

### Filtrado de subconjuntos de tuits desde la base de datos

Para filtrar subconjuntos de tuits, se han implementado una serie de funciones primitivas con varios criterios de filtrado:

- **Palabras clave:** Filtra los tuits que tengan al menos una de las palabras indicadas en la lista
- **Fecha exacta:** Filtra los tuits publicados en una fecha exacta (dia, mes y año)
- **Rango de fechas:** Filtra los tuits que fueron publicados entre dos fechas (dia, mes y año)
- **Hashtag:** Filtra los tuits que contienen el hashtag indicado
- **Usuario:** Filtra los tuits publicados por un determinado usuario
- **Descartar retuits:** Filtra únicamente los tuits originales, descartando los retuits

De estos criterios, el único obligatorio es el de las palabras clave. Por razones obvias, los criterios de fecha exacta y rango de fechas son excluyentes, y solo se puede aplicar uno a la vez.

Las funciones devuelven un cursor al conjunto de tuits obtenido.

#### Filtrado con múltiples criterios

Para poder realizar un filtrado según múltiples criterios, seguimos una estrategia de filtrado iterativo: vamos aplicando criterio a criterio, y almacenando en colecciones temporales. Filtramos por el primer criterio, almacenamos los resultados en una colección temporal, sobre la cual aplicaremos el segundo criterio, y generaremos otra nueva colección temporal. Y así sucesivamente hasta completar todos los criterios de filtrado.

Una vez completamos el filtrado, almacenamos los resultados en una colección final, y borramos todas las colecciones temporales.

### Obtención de estadísticas en una colección

Para obtener las estadísticas de una colección, implementamos una serie de funciones primitivas, que realizan la consulta de cada dato que queremos obtener. Estas devuelven diferentes tipos de datos: diccionarios, listas o variables, según el resultado de cada consulta.

Para mostrarlas en la interfaz, nos creamos una nueva función, que va llamando a cada una de las primitivas, almacenando el resultado en una cadena de caracteres.

## Implementación

### Tecnologías utilizadas

La implementación se ha realizado íntegramente en Python, tanto en la parte de descarga de los tuits, como en la parte de la aplicación informática. 

Para la descarga de los tuits, se ha utilizado tweepy y la librería json. 
Para la aplicación se ha utilizado pymongo para la gestión de la base de datos y las colecciones, y PyQt5 para la interfaz. 

### Descarga de los tuits

La descarga de los tuits está implementada en el fichero `download_tweets.py`. Esta se compone de dos clases: `TwitterLogin`, para establecer la conexión; y 	`TwitterQuery` para realizar las consultas en la API de Twitter y descargar los tuits.

- **TwitterLogin**

	La clase TwitterLogin se encarga de iniciar sesión en la API de Twitter, y obtener el objeto de acceso a la API. 
	Para el inicio de sesión, se utilizan las claves *consumer_key*, *consumer_secret*, *access_token* y *access_token_secret*, las cuales se obtienen a partir del fichero `twitter_keys.py`.
	
	En la llamada a la API, se utilizan los parámetros `wait_on_rate_limit=True` y `wait_on_rate_limit_notify=True`, para que la aplicación espere en caso de superar la ratio de descarga permitida por la API, y notifique al usuario en dicho caso.
	
- **TwitterQuery**

	La clase TwitterQuery se encarga de realizar las consultas a la API de Twitter y descargar los resultados en formato JSON.
	
	Se compone de los siguientes métodos:
	
	- `get_user_timeline(username: str)`: Obtiene los últimos n tuits del timeline de un determinado usuario.
	
	- `search_tweets_by_wordlist(wordlist: str, limit: int)`: Descarga los últimos n tuits que coinciden con una lista de palabras clave. Las palabras clave se escriben en una cadena de caracteres separados por espacios.  El número de tuits a descargar viene delimitado por el parámetro `limit`. **Para descargar los tuits con el texto completo, aplicamos el parámetro `tweet_mode='extended'`. **
	
	- `search_tweets_by_wordlist_and_date_range(wordlist: str, date_start: str, date_end: str, limit: int)`: Descarga los últimos n tuits, filtrando por palabras clave, y rango de fechas. Las fechas se escriben en una cadena de caracteres, en formato "AAAA-MM-DD". 
	
	- `search_tweets_by_wordlist_and_date_start(wordlist: str, date_start: str, limit: int)`: Descarga los últimos n tuits, filtrando por palabras clave y fecha inicial. 
	
	- `search_tweets_by_wordlist_and_date_end(self, wordlist: str, date_end: str, limit: int)`: Descarga los últimos n tuits, filtrando por palabras clave y fecha final. La fecha final no puede ser superior a los últimos 7 días.
	
	- `export_tweets_json(tweets: tw.Cursor)`: exporta los tuits obtenidos a una estructura JSON almacenada en memoria. La estructura está formada por un array de documentos. Recibe por parámetro el cursor devuelto por Tweepy con los resultados de la consulta. Dado que los tuits utilizan codificación UTF-8, en lugar de ASCII, aplicamos el parámetro `ensure_ascii=False` a la función `json.dump()`, para asegurar que se respete el formato de texto utilizado en los tuits.
	
	- `export_tweets_to_file(self, tweets: tw.Cursor, filename: str)`: exporta los tuits obtenidos a un fichero en formato JSON. Para poder exportarlos "en directo" mientras se descarga, se utiliza una lista por compresión, dentro de la función `json.dump()`. Recibe por parámetro el cursor obtenido de Tweepy y el nombre del fichero donde queremos almacenar los resultados.
	
Para la descarga de los tuits se requiere la escritura de un pequeño script, en el que se invoquen a los métodos con los parámetros necesarios para la descarga y almacenamiento de los resultados. En el propio fichero se disponen de algunos ejemplos de descarga y exportación a ficheros.

### Gestión de la instancia de MongoDB

Para la gestión de la instancia de MongoDB disponemos de la clase `MongoManager`, almacenada en el fichero `mongodb_manager.py`. Esta se encarga de la conexión a la instancia de MongoDB, y el listado y conexión de las bases de datos.

Esta se compone de los siguientes métodos:  

- `__init__(domain: str)`: Constructor. Recibe por parámetro el dominio de la instancia a la que nos queremos conectar, y establece la conexión con la misma.

- `connect(domain: str)`: Establece la conexión con la instancia indicada. Este método es invocado por el constructor para conectar a la instancia. 

- `get_db_list()`: Devuelve la lista de bases de datos existentes en la instancia

- `get_db_manager(db_name: str)`: Devuelve el gestor de la base de datos indicada por parámetro. El gestor es un objeto de la clase `DBManager`. Asume que la base de datos está almacenada sin contraseña.

- `disconnect()`: Cierra la conexión actual con la instancia

- `reconnect()`: Reinicia la conexión actual con la instancia, cerrando la conexión y volviéndola a abrir.

### Gestión de la base de datos en MongoDB

Para la gestión de la base de datos disponemos de la clase `DBManager`, almacenada en el fichero `mongodb_manager.py`, que se encarga del acceso a la base de datos y la carga, acceso y borrado de las colecciones. 

La gestión de las colecciones se realiza en la clase `CollectionManager` en el fichero `collection_manager.py`. Al crear o acceder a una colección, se nos devolverá un objeto de dicha clase. 

La clase `DBManager` se compone de los siguientes métodos:

- `__init__(db: pymongo.database)`: Constructor. Recibe por parámetro el objeto de Tweepy correspondiente a dicha base de datos.

- `load_collection_from_file(filename: str, collection_name: str)`: Crea y carga una nueva colección, a partir de un fichero en formato JSON en formato de array de documentos. Adapta la fecha del formato de Twitter, a un formato de fecha interpretable por MongoDB, e inserta cada documento dentro de la colección. Devuelve un objeto `CollectionManager` asociado a dicha colección.

- `load_collection_from_cursor(docs, collection_name: str)`: Crea y carga una nueva colección, a partir de un cursor de PyMongo. Esto permite cargar en una nueva colección los resultados del filtrado en una colección anterior. Devuelve un objeto `CollectionManager` asociado a dicha colección.

- `get_collection_manager(collection_name: str)`: Devuelve el objeto `CollectionManager` asociado a una colección ya existente

- `get_collection_list()`: Devuelve la lista de colecciones existentes en la base de datos

- `remove_collection(collection_name: str)`: Borra la colección indicada por parámetro de la base de datos

- `clone_collection_to_another(collection_src: str, collection_dest: str)`: Permite clonar los contenidos de una colección a otra. Devuelve el objeto `CollectionManager` de la colección destino.

### Gestión de las colecciones de MongoDB

La gestión de las colecciones se realiza en la clase `CollectionManager()`. Esta implementa métodos para crear, borrar y buscar índices de texto, obtener la longitud de la colección, y obtener las clases para consultas y estadísticas.

Esta clase se compone de los siguientes métodos:

- `__init__(self, collection: pymongo.collection)`: Constructor. Recibe por parámetro la colección de PyMongo sobre la que queremos operar.

- `create_text_index(field: str)`: Crea un índice de texto sobre el campo indicado por parámetro  

- `check_text_index(field: str)`: Comprueba si existe un índice de texto sobre el campo indicado por parámetro.  

- `remove_all_index()`: Borra todos los índices de la colección

- `get_query()`: Devuelve un objeto `CollectionQuery`, que permite realizar consultas sobre la colección  

- `get_stats()`: Devuelve un objeto `CollectionStatistics`, que permite consultar las estadísticas de la colección

- `get_lenght()`: Devuelve el número de documentos de la colección

#### Realización de consultas sobre la colección

Para realizar consultas de filtrado sobre la colección, disponemos de la clase `CollectionQuery`, almacenada en el fichero `collection_query.py`. Esta permite realizar consultas de filtrado bajo diferentes criterios, y devuelve un cursor con el subconjunto obtenido. Está compuesta por varios métodos con primitivas de consulta, y algunos métodos combinando diferentes criterios. 

La clase se compone de los siguientes métodos:

- ` __init__(collection: pymongo.collection)`: Constructor. Recibe por parámetro el objeto `collection` devuelto por PyMongo. 

- `find_docs_by_keywords(keywords: str)`: Filtra el conjunto de documentos que coincidan con alguna de las palabras clave indicadas. Las palabras clave deben pasarse en una única cadena de caracteres, separadas por espacios.

- `find_docs_by_date_range(date_start: str, date_end: str)`: Filtra los tuits cuyo campo `create_at` esté dentro del intervalo de fechas indicado. Las fechas deben indicarse en forma de cadena de caracteres, con formato "dd-MM-AAAA"

- `find_docs_by_date(date: str)`: Filtra los tuits cuyo campo `create_at` esté dentro del día indicado. 

- `find_docs_by_keywords_and_date(keywords: str, date: str)`: Mezcla de los dos anteriores. Filtra los documentos cuyo campo `create_at` esté dentro de la fecha indicada, y que coincidan con alguna de las palabras clave indicadas.

- `find_docs_by_keywords_and_date_range(keywords: str, date_start: str, date_end: str)`: Similar al anterior, pero usando un rango de fechas.

- `find_docs_by_user(self, username: str)`: Filtra los tuits de un determinado usuario. El usuario se indica mediante su alias (su @), sin incluir la @ en sí. 

- `find_docs_by_hashtag(self, hashtag: str)`: Filtra los tuits según un determinado hashtag. El hashtag debe introducirse sin el #

- `find_docs_no_retweet(self)`: Filtra los tuits que no son retuits de otros.

#### Estadísticas de la colección

Para realizar consultas estadísticas sobre la colección, disponemos de la clase `CollectionStatistics`. 
Esta clase implementa varios métodos con primitivas de consulta, y un método para obtener todas las estadísticas en una única cadena de caracteres.

Esta clase se compone de los siguientes métodos:

- ` __init__(collection: pymongo.collection)`: Constructor. Recibe por parámetro el objeto `collection` devuelto por PyMongo. 

- `get_docs_number()`: Obtiene el número de documentos de la colección

- `get_download_period()`: Devuelve el periodo de descarga de la colección, obtenido como la fecha mas antigua y mas nueva del campo `create_at` del conjunto de tuits.

- `get_most_retweeted_text()`: Devuelve el texto del tuit mas retuiteado

- `get_most_published_users()`: Devuelve el nombre de los 5 usuarios con mas publicaciones, junto al número de publicaciones realizadas por cada uno de ellos.

- `get_most_appears_urls()`: Devuelve las 5 URL mas mencionadas en las publicaciones, junto al número total de menciones de cada una de ellas.

- `get_most_appears_hashtags()`: Devuelve los 5 hashtag mas mencionados en las publicaciones, junto al número total de menciones de cada uno de ellos.

- `get_most_mentioned_users()`: Devuelve los 5 usuarios mas mencionados, junto al número de menciones de cada uno de ellos.

- `get_hottest_minute()`: Devuelve el minuto mas caliente, en el que mas publicaciones se han realizado, junto al número total de publicaciones realizadas en dicho minuto.

- `show_all_stats()`: Devuelve una cadena de caracteres con todas las estadísticas agrupadas con sus textos descriptores.

### Aplicación

La interfaz de la aplicación es una ventana tipo formulario, implementada en PyQt5. El diseño de la interfaz se ha realizado con Qt Designer, y posteriormente se ha utilizado pyuic5 para exportarlo a PyQt5. El fichero obtenido se llama `app.py`. Sobre el código obtenido, posteriormente se han realizado algunas modificaciones, para cambiar algunos widget por otros, establecer algunas restricciones, modificar tamaños, o añadir nuevos widgets. La clase generada se llama `Ui_MainWindow`.

La interfaz resultante es la siguiente:

![](interfaz_app.png)

La implementación de las acciones se ha realizado también con PyQt5, asociando eventos de los widgets a funciones. Se ha implementado una función para realizar el filtrado, otra para obtener estadísticas, y varias funciones auxiliares para actualizar diferentes elementos de la interfaz. Para esto se ha creado una nueva clase, que conecta con la anterior, llamada `MainWindow`. 

Entre los métodos destacados de esta última se encuentran:

- `_filter_tweets()`: Asociada al botón de buscar, recoge el contenido de los cuadros de texto y de las casillas de la interfaz, y realiza el filtrado de los tuits en la colección indicada por el menú desplegable.

- ` __remove_temporary_collections(collection_name: str)`: Método auxiliar asociado al anterior, borra las colecciones temporales generadas durante el filtrado. Los nombres de las colecciones temporales se obtienen mediante el nombre de la colección final, asociándolo a unos patrones conocidos.

- `__update_query_collection(collection_name: str, docs)`: Método auxiliar asociado al primero, copia los documentos en una nueva colección, crea un índice de texto sobre el campo `full_text`, y devuelve el objeto `CollectionQuery` para realizar las consultas.

- `` _get_collection_stats()`: Acción asociada al botón "Obtener estadísticas", muestra en el campo de texto (situado en la parte inferior de la pantalla) las estadísticas de la colección seleccionada en el menú desplegable.

## Instalación de la aplicación

Antes de probar la aplicación, hemos de preparar el entorno de ejecución apropiado

### Instalación de dependencias

Nuestro programa requiere varias librerías para funcionar. Estas son:

- Python 3
	- PyMongo
	- Tweepy
	- PyQt5

Para instalar las dependencias, se ofrece un fichero requirements.txt, el cual podemos utilizarlo desde pip de la siguiente manera:

	pip install -r requeriments.txt

La instalación durará unos minutos

El programa también requiere de una instancia de MongoDB instalada en el sistema. Esta debe estar instalada en local, en la misma máquina donde se ejecuta el programa, y configurada en el puerto 27017.

### Ejecución del programa

Para ejecutar la aplicación, debemos ejecutar el fichero `app.py`. Podemos hacerlo desde consola, con este comando:

	python3 app.py

Esto nos abrirá la interfaz, que se verá de la siguiente manera:

![](interfaz_vacia.png)

En el siguiente capítulo explicaremos su funcionamiento

## Funcionamiento de la aplicación

Una vez abierta la aplicación, esta se conectará a nuestra instancia de MongoDB, y cargará en el menú desplegable "Base de Datos" las bases de datos que encuentre.

### Conexión a la base de datos

Para empezar, debemos seleccionar una base de datos del desplegable, y pulsar en "Acceder". Esto conectará la aplicación a la base de datos indicada, y cargará su lista de colecciones en el desplegable inferior. Además, activará los botones de "Obtener estadísticas" y los de la sección "Filtrado de tuits"

![](interfaz_conectada.png)

### Operando sobre una colección

Para seleccionar una colección, debemos desplegar el menú "Colecciones" y pulsar en la colección de nuestro interés. Esto cargará la colección dentro de nuestra aplicación

#### Obtención de estadísticas

Para mostrar las estadísticas, simplemente debemos pulsar en el botón "Obtener estadísticas". Esto nos mostrará un resumen de las estadísticas obtenidas en el campo de texto de la parte inferior de la ventana.

![](mostrar_estadisticas_app.png)

Este campo dispone de un pequeño scroll, mediante el cual podremos avanzar en el texto para ver todas las estadísticas.

#### Filtrando subconjuntos de la colección actual

Para filtrar tuits, debemos fijarnos en la sección "Filtrado de tuits". En esa disponemos de varios campos para establecer filtros.

El campo "Palabras clave" es obligatorio, y siempre se busca. Si no introducimos nada, se buscará una cadena vacía, y no se obtendrá ningún resultado. Si indicamos una lista de palabras, estas deben introducirse separadas por espacios.

Los filtros "Rango de fechas" y "Fecha exacta" son excluyentes, y solo se podrá activar uno a la vez. Además, una vez seleccionado uno de los dos, no se podrán desactivar ambos. Cada uno de ellos tiene a su derecha los widget de fecha a través de los cuales se podrán introducir las fechas de búsqueda.

Los filtros "Usuario", "Hashtag" y "Descartar RT" son opcionales, y se activan con un check, pulsando sobre ellos. Estos se pueden activar o desactivar sin limitación. En los dos primeros, podremos introducir valores escribiendo en los campos de texto situados a su derecha. Este texto sólo será considerado una vez se active la opción dentro de la interfaz.

Si queremos borrar todos los filtros, podemos pulsar el botón "Borrar filtros" (antes de iniciar la búsqueda). Esto desmarcará todos los filtros (incluidos los de fecha) y borrará los valores de los campos de fecha y de texto.

**NOTA: La función de "Obtener estadísticas" no borra los filtros marcados en la interfaz, por lo que se puede utilizar para realizar una consulta mientras introducimos los valores de filtrado**

Una vez indicados los filtros a utilizar, pulsamos en el botón "Buscar" para iniciar la búsqueda. Esta puede tardar entre segundos o minutos, dependiendo del tamaño de la colección y el número de criterios a filtrar.

![](filtros_app.png)

Si no obtenemos ningún resultado, se nos mostrará el mensaje "Sin resultados" en el lado derecho, y se volverá a recargar la lista de colecciones.

![](sin_resultados (copia).png)

Si obtenemos algún resultado, se nos mostrará el mensaje "Éxito", y veremos una nueva colección en el menú desplegable.

![](nueva_coleccion.jpg)

La nueva colección tendrá el nombre de la anterior, añadiéndole el sufijo "fíltered" y la fecha y hora exacta en que se ha generado

Si pulsamos en la nueva colección, podemos ver sus estadísticas pulsando en "Obtener estadísticas"

![](estadisticas_nueva_coleccion.png)

En este caso, si comparamos los resultados con los de la colección original (capturada en una imagen anterior), vemos que el número de documentos se ha reducido, y que los filtros se han aplicado correctamente: el tuit mostrado no es un retuit, solo hay un único usuario (y su número de publicaciones coincide con el total), los hashtag se han filtrado correctamente, y la fecha coincide.

También notamos que, tras la consulta, la mayoría de los filtros se han borrado. También se actualizará la lista de colecciones, **por lo que la colección seleccionada puede cambiar.**

### Alternando entre varias colecciones

Este ciclo de trabajo se puede repetir alternando entre varias colecciones: simplemente tenemos que elegir una nueva colección en el menú desplegable, y trabajar sobre ella.



