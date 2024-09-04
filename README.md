# TP0: Docker + Comunicaciones + Concurrencia

En el presente repositorio se provee un ejemplo de cliente-servidor el cual corre en containers con la ayuda de [docker-compose](https://docs.docker.com/compose/). El mismo es un ejemplo práctico brindado por la cátedra para que los alumnos tengan un esqueleto básico de cómo armar un proyecto de cero en donde todas las dependencias del mismo se encuentren encapsuladas en containers. El cliente (Golang) y el servidor (Python) fueron desarrollados en diferentes lenguajes simplemente para mostrar cómo dos lenguajes de programación pueden convivir en el mismo proyecto con la ayuda de containers.

Por otro lado, se presenta una guía de ejercicios que los alumnos deberán resolver teniendo en cuenta las consideraciones generales descriptas al pie de este archivo.

## Instrucciones de uso
El repositorio cuenta con un **Makefile** que posee encapsulado diferentes comandos utilizados recurrentemente en el proyecto en forma de targets. Los targets se ejecutan mediante la invocación de:

* **make \<target\>**:
Los target imprescindibles para iniciar y detener el sistema son **docker-compose-up** y **docker-compose-down**, siendo los restantes targets de utilidad para el proceso de _debugging_ y _troubleshooting_.

Los targets disponibles son:
* **docker-compose-up**: Inicializa el ambiente de desarrollo (buildear docker images del servidor y cliente, inicializar la red a utilizar por docker, etc.) y arranca los containers de las aplicaciones que componen el proyecto.
* **docker-compose-down**: Realiza un `docker-compose stop` para detener los containers asociados al compose y luego realiza un `docker-compose down` para destruir todos los recursos asociados al proyecto que fueron inicializados. Se recomienda ejecutar este comando al finalizar cada ejecución para evitar que el disco de la máquina host se llene.
* **docker-compose-logs**: Permite ver los logs actuales del proyecto. Acompañar con `grep` para lograr ver mensajes de una aplicación específica dentro del compose.
* **docker-image**: Buildea las imágenes a ser utilizadas tanto en el servidor como en el cliente. Este target es utilizado por **docker-compose-up**, por lo cual se lo puede utilizar para testear nuevos cambios en las imágenes antes de arrancar el proyecto.
* **build**: Compila la aplicación cliente para ejecución en el _host_ en lugar de en docker. La compilación de esta forma es mucho más rápida pero requiere tener el entorno de Golang instalado en la máquina _host_.

### Servidor
El servidor del presente ejemplo es un EchoServer: los mensajes recibidos por el cliente son devueltos inmediatamente. El servidor actual funciona de la siguiente forma:
1. Servidor acepta una nueva conexión.
2. Servidor recibe mensaje del cliente y procede a responder el mismo.
3. Servidor desconecta al cliente.
4. Servidor procede a recibir una conexión nuevamente.

### Cliente
El cliente del presente ejemplo se conecta reiteradas veces al servidor y envía mensajes de la siguiente forma.
1. Cliente se conecta al servidor.
2. Cliente genera mensaje incremental.
recibe mensaje del cliente y procede a responder el mismo.
3. Cliente envía mensaje al servidor y espera mensaje de respuesta.
Servidor desconecta al cliente.
4. Cliente verifica si aún debe enviar un mensaje y si es así, vuelve al paso 2.

Al ejecutar el comando `make docker-compose-up` para comenzar la ejecución del ejemplo y luego el comando `make docker-compose-logs`, se observan los siguientes logs:

```
client1  | 2024-08-21 22:11:15 INFO     action: config | result: success | client_id: 1 | server_address: server:12345 | loop_amount: 5 | loop_period: 5s | log_level: DEBUG
client1  | 2024-08-21 22:11:15 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°1
server   | 2024-08-21 22:11:14 DEBUG    action: config | result: success | port: 12345 | listen_backlog: 5 | logging_level: DEBUG
server   | 2024-08-21 22:11:14 INFO     action: accept_connections | result: in_progress
server   | 2024-08-21 22:11:15 INFO     action: accept_connections | result: success | ip: 172.25.125.3
server   | 2024-08-21 22:11:15 INFO     action: receive_message | result: success | ip: 172.25.125.3 | msg: [CLIENT 1] Message N°1
server   | 2024-08-21 22:11:15 INFO     action: accept_connections | result: in_progress
server   | 2024-08-21 22:11:20 INFO     action: accept_connections | result: success | ip: 172.25.125.3
server   | 2024-08-21 22:11:20 INFO     action: receive_message | result: success | ip: 172.25.125.3 | msg: [CLIENT 1] Message N°2
server   | 2024-08-21 22:11:20 INFO     action: accept_connections | result: in_progress
client1  | 2024-08-21 22:11:20 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°2
server   | 2024-08-21 22:11:25 INFO     action: accept_connections | result: success | ip: 172.25.125.3
server   | 2024-08-21 22:11:25 INFO     action: receive_message | result: success | ip: 172.25.125.3 | msg: [CLIENT 1] Message N°3
client1  | 2024-08-21 22:11:25 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°3
server   | 2024-08-21 22:11:25 INFO     action: accept_connections | result: in_progress
server   | 2024-08-21 22:11:30 INFO     action: accept_connections | result: success | ip: 172.25.125.3
server   | 2024-08-21 22:11:30 INFO     action: receive_message | result: success | ip: 172.25.125.3 | msg: [CLIENT 1] Message N°4
server   | 2024-08-21 22:11:30 INFO     action: accept_connections | result: in_progress
client1  | 2024-08-21 22:11:30 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°4
server   | 2024-08-21 22:11:35 INFO     action: accept_connections | result: success | ip: 172.25.125.3
server   | 2024-08-21 22:11:35 INFO     action: receive_message | result: success | ip: 172.25.125.3 | msg: [CLIENT 1] Message N°5
client1  | 2024-08-21 22:11:35 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°5
server   | 2024-08-21 22:11:35 INFO     action: accept_connections | result: in_progress
client1  | 2024-08-21 22:11:40 INFO     action: loop_finished | result: success | client_id: 1
client1 exited with code 0
```

## Parte 1: Introducción a Docker
En esta primera parte del trabajo práctico se plantean una serie de ejercicios que sirven para introducir las herramientas básicas de Docker que se utilizarán a lo largo de la materia. El entendimiento de las mismas será crucial para el desarrollo de los próximos TPs.

### Ejercicio N°1:
Además, definir un script de bash `generar-compose.sh` que permita crear una definición de DockerCompose con una cantidad configurable de clientes.  El nombre de los containers deberá seguir el formato propuesto: client1, client2, client3, etc. 

El script deberá ubicarse en la raíz del proyecto y recibirá por parámetro el nombre del archivo de salida y la cantidad de clientes esperados:

`./generar-compose.sh docker-compose-dev.yaml 5`

Considerar que en el contenido del script pueden invocar un subscript de Go o Python:

```
#!/bin/bash
echo "Nombre del archivo de salida: $1"
echo "Cantidad de clientes: $2"
python3 mi-generador.py $1 $2
```



### Ejercicio N°2:
Modificar el cliente y el servidor para lograr que realizar cambios en el archivo de configuración no requiera un nuevo build de las imágenes de Docker para que los mismos sean efectivos. La configuración a través del archivo correspondiente (`config.ini` y `config.yaml`, dependiendo de la aplicación) debe ser inyectada en el container y persistida afuera de la imagen (hint: `docker volumes`).



### Ejercicio N°3:
Crear un script de bash `validar-echo-server.sh` que permita verificar el correcto funcionamiento del servidor utilizando el comando `netcat` para interactuar con el mismo. Dado que el servidor es un EchoServer, se debe enviar un mensaje al servidor y esperar recibir el mismo mensaje enviado.

En caso de que la validación sea exitosa imprimir: `action: test_echo_server | result: success`, de lo contrario imprimir:`action: test_echo_server | result: fail`.

El script deberá ubicarse en la raíz del proyecto. Netcat no debe ser instalado en la máquina _host_ y no se puede exponer puertos del servidor para realizar la comunicación (hint: `docker network`). `



### Ejercicio N°4:
Modificar servidor y cliente para que ambos sistemas terminen de forma _graceful_ al recibir la signal SIGTERM. Terminar la aplicación de forma _graceful_ implica que todos los _file descriptors_ (entre los que se encuentran archivos, sockets, threads y procesos) deben cerrarse correctamente antes que el thread de la aplicación principal muera. Loguear mensajes en el cierre de cada recurso (hint: Verificar que hace el flag `-t` utilizado en el comando `docker compose down`).



## Parte 2: Repaso de Comunicaciones

Las secciones de repaso del trabajo práctico plantean un caso de uso denominado **Lotería Nacional**. Para la resolución de las mismas deberá utilizarse como base al código fuente provisto en la primera parte, con las modificaciones agregadas en el ejercicio 4.



### Ejercicio N°5:
Modificar la lógica de negocio tanto de los clientes como del servidor para nuestro nuevo caso de uso.

#### Cliente
Emulará a una _agencia de quiniela_ que participa del proyecto. Existen 5 agencias. Deberán recibir como variables de entorno los campos que representan la apuesta de una persona: nombre, apellido, DNI, nacimiento, numero apostado (en adelante 'número'). Ej.: `NOMBRE=Santiago Lionel`, `APELLIDO=Lorca`, `DOCUMENTO=30904465`, `NACIMIENTO=1999-03-17` y `NUMERO=7574` respectivamente.

Los campos deben enviarse al servidor para dejar registro de la apuesta. Al recibir la confirmación del servidor se debe imprimir por log: `action: apuesta_enviada | result: success | dni: ${DNI} | numero: ${NUMERO}`.



#### Servidor
Emulará a la _central de Lotería Nacional_. Deberá recibir los campos de la cada apuesta desde los clientes y almacenar la información mediante la función `store_bet(...)` para control futuro de ganadores. La función `store_bet(...)` es provista por la cátedra y no podrá ser modificada por el alumno.
Al persistir se debe imprimir por log: `action: apuesta_almacenada | result: success | dni: ${DNI} | numero: ${NUMERO}`.

#### Comunicación:
Se deberá implementar un módulo de comunicación entre el cliente y el servidor donde se maneje el envío y la recepción de los paquetes, el cual se espera que contemple:
* Definición de un protocolo para el envío de los mensajes.
* Serialización de los datos.
* Correcta separación de responsabilidades entre modelo de dominio y capa de comunicación.
* Correcto empleo de sockets, incluyendo manejo de errores y evitando los fenómenos conocidos como [_short read y short write_](https://cs61.seas.harvard.edu/site/2018/FileDescriptors/).



### Ejercicio N°6:
Modificar los clientes para que envíen varias apuestas a la vez (modalidad conocida como procesamiento por _chunks_ o _batchs_). La información de cada agencia será simulada por la ingesta de su archivo numerado correspondiente, provisto por la cátedra dentro de `.data/datasets.zip`.
Los _batchs_ permiten que el cliente registre varias apuestas en una misma consulta, acortando tiempos de transmisión y procesamiento.

En el servidor, si todas las apuestas del *batch* fueron procesadas correctamente, imprimir por log: `action: apuesta_recibida | result: success | cantidad: ${CANTIDAD_DE_APUESTAS}`. En caso de detectar un error con alguna de las apuestas, debe responder con un código de error a elección e imprimir: `action: apuesta_recibida | result: fail | cantidad: ${CANTIDAD_DE_APUESTAS}`.

La cantidad máxima de apuestas dentro de cada _batch_ debe ser configurable desde config.yaml. Respetar la clave `batch: maxAmount`, pero modificar el valor por defecto de modo tal que los paquetes no excedan los 8kB. 

El servidor, por otro lado, deberá responder con éxito solamente si todas las apuestas del _batch_ fueron procesadas correctamente.



### Ejercicio N°7:
Modificar los clientes para que notifiquen al servidor al finalizar con el envío de todas las apuestas y así proceder con el sorteo.
Inmediatamente después de la notificacion, los clientes consultarán la lista de ganadores del sorteo correspondientes a su agencia.
Una vez el cliente obtenga los resultados, deberá imprimir por log: `action: consulta_ganadores | result: success | cant_ganadores: ${CANT}`.

El servidor deberá esperar la notificación de las 5 agencias para considerar que se realizó el sorteo e imprimir por log: `action: sorteo | result: success`.
Luego de este evento, podrá verificar cada apuesta con las funciones `load_bets(...)` y `has_won(...)` y retornar los DNI de los ganadores de la agencia en cuestión. Antes del sorteo, no podrá responder consultas por la lista de ganadores.
Las funciones `load_bets(...)` y `has_won(...)` son provistas por la cátedra y no podrán ser modificadas por el alumno.



## Parte 3: Repaso de Concurrencia

### Ejercicio N°8:
Modificar el servidor para que permita aceptar conexiones y procesar mensajes en paralelo.
En este ejercicio es importante considerar los mecanismos de sincronización a utilizar para el correcto funcionamiento de la persistencia.

En caso de que el alumno implemente el servidor Python utilizando _multithreading_,  deberán tenerse en cuenta las [limitaciones propias del lenguaje](https://wiki.python.org/moin/GlobalInterpreterLock).



## Consideraciones Generales
Se espera que los alumnos realicen un _fork_ del presente repositorio para el desarrollo de los ejercicios.El _fork_ deberá contar con una sección de README que indique como ejecutar cada ejercicio.

La Parte 2 requiere una sección donde se explique el protocolo de comunicación implementado.
La Parte 3 requiere una sección que expliquen los mecanismos de sincronización utilizados.

Cada ejercicio deberá resolverse en una rama independiente con nombres siguiendo el formato `ej${Nro de ejercicio}`. Se permite agregar commits en cualquier órden, así como crear una rama a partir de otra, pero al momento de la entrega deben existir 8 ramas llamadas: ej1, ej2, ..., ej7, ej8.

(hint: verificar listado de ramas y últimos commits con `git ls-remote`)

Puden obtener un listado del último commit de cada rama ejecutando `git ls-remote`.

Finalmente, se pide a los alumnos leer atentamente y **tener en cuenta** los criterios de corrección provistos [en el campus](https://campusgrado.fi.uba.ar/mod/page/view.php?id=73393).

# Resolución - TP 0 Ramos Federico Cuatrimestre 2 2024
# Ejercicio 1

Se escribio el código necesario para la creación de un `yaml` con N clientes, siendo la cantidad de clientes
y el nombre del archivo `yaml` configurable por cli. Para ejecutar el script se debe:

```console
bash scripts/docker_generator.sh
```

<details>
<summary>Ejemplo de ejecución</summary>

```console
bash scripts/docker_generator.sh                                    
Ingrese el nombre del archivo a crear: example.yaml
Ingrese el número de clientes: 12
```

</details>

<details>
<summary>Archivo generado</summary>

```yaml
name: tp0
services:
  server:
    container_name: server
    image: server:latest
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
      - LOGGING_LEVEL=DEBUG
    networks:
      - testing_net

  client1:
    container_name: client1
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID=1
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    depends_on:
      - server

  client2:
    container_name: client2
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID=2
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    depends_on:
      - server

  client3:
    container_name: client3
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID=3
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    depends_on:
      - server

  client4:
    container_name: client4
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID=4
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    depends_on:
      - server

  client5:
    container_name: client5
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID=5
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    depends_on:
      - server

  client6:
    container_name: client6
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID=6
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    depends_on:
      - server

  client7:
    container_name: client7
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID=7
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    depends_on:
      - server

  client8:
    container_name: client8
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID=8
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    depends_on:
      - server

  client9:
    container_name: client9
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID=9
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    depends_on:
      - server

  client10:
    container_name: client10
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID=10
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    depends_on:
      - server

  client11:
    container_name: client11
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID=11
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    depends_on:
      - server

  client12:
    container_name: client12
    image: client:latest
    entrypoint: /client
    environment:
      - CLI_ID=12
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    depends_on:
      - server


networks:
  testing_net:
    ipam:
      driver: default
      config:
        - subnet: 172.25.125.0/24


```
</details>

<details>
<summary>Uso de docker compose con el archivo generado</summary>

```console
 docker compose -f example.yaml up                          02:56:14 PM
[+] Running 14/14
 ✔ Network tp0_testing_net  Created                                                                                0.0s
 ✔ Container server         Created                                                                                0.0s
 ✔ Container client5        Created                                                                                0.1s
 ✔ Container client12       Created                                                                                0.1s
 ✔ Container client6        Created                                                                                0.1s
 ✔ Container client7        Created                                                                                0.1s
 ✔ Container client3        Created                                                                                0.0s
 ✔ Container client2        Created                                                                                0.1s
 ✔ Container client1        Created                                                                                0.1s
 ✔ Container client10       Created                                                                                0.1s
 ✔ Container client8        Created                                                                                0.1s
 ✔ Container client9        Created                                                                                0.1s
 ✔ Container client11       Created                                                                                0.1s
 ✔ Container client4        Created                                                                                0.1s
Attaching to client1, client10, client11, client12, client2, client3, client4, client5, client6, client7, client8, client9, server
server    | 2024-09-01 17:56:16 DEBUG    action: config | result: success | port: 12345 | listen_backlog: 5 | logging_level: DEBUG
server    | 2024-09-01 17:56:16 INFO     action: accept_connections | result: in_progress
client6   | 2024-09-01 17:56:17 INFO     action: config | result: success | client_id: 6 | server_address: server:12345 | loop_amount: 5 | loop_period: 5s | log_level: DEBUG
client5   | 2024-09-01 17:56:17 INFO     action: config | result: success | client_id: 5 | server_address: server:12345 | loop_amount: 5 | loop_period: 5s | log_level: DEBUG
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: success | ip: 172.25.125.4
server    | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | ip: 172.25.125.4 | msg: [CLIENT 5] Message N°1
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: in_progress
client5   | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | client_id: 5 | msg: [CLIENT 5] Message N°1
client1   | 2024-09-01 17:56:17 INFO     action: config | result: success | client_id: 1 | server_address: server:12345 | loop_amount: 5 | loop_period: 5s | log_level: DEBUG
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: success | ip: 172.25.125.5
server    | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | ip: 172.25.125.5 | msg: [CLIENT 1] Message N°1
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: in_progress
client1   | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°1
client7   | 2024-09-01 17:56:17 INFO     action: config | result: success | client_id: 7 | server_address: server:12345 | loop_amount: 5 | loop_period: 5s | log_level: DEBUG
client7   | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | client_id: 7 | msg: [CLIENT 7] Message N°1
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: success | ip: 172.25.125.6
server    | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | ip: 172.25.125.6 | msg: [CLIENT 7] Message N°1
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: in_progress
client3   | 2024-09-01 17:56:17 INFO     action: config | result: success | client_id: 3 | server_address: server:12345 | loop_amount: 5 | loop_period: 5s | log_level: DEBUG
client3   | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | client_id: 3 | msg: [CLIENT 3] Message N°1
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: success | ip: 172.25.125.7
server    | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | ip: 172.25.125.7 | msg: [CLIENT 3] Message N°1
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: in_progress
client9   | 2024-09-01 17:56:17 INFO     action: config | result: success | client_id: 9 | server_address: server:12345 | loop_amount: 5 | loop_period: 5s | log_level: DEBUG
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: success | ip: 172.25.125.8
server    | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | ip: 172.25.125.8 | msg: [CLIENT 9] Message N°1
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: in_progress
client9   | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | client_id: 9 | msg: [CLIENT 9] Message N°1
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: success | ip: 172.25.125.9
client11  | 2024-09-01 17:56:17 INFO     action: config | result: success | client_id: 11 | server_address: server:12345 | loop_amount: 5 | loop_period: 5s | log_level: DEBUG
server    | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | ip: 172.25.125.9 | msg: [CLIENT 11] Message N°1
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: in_progress
client11  | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | client_id: 11 | msg: [CLIENT 11] Message N°1
client12  | 2024-09-01 17:56:17 INFO     action: config | result: success | client_id: 12 | server_address: server:12345 | loop_amount: 5 | loop_period: 5s | log_level: DEBUG
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: success | ip: 172.25.125.10
server    | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | ip: 172.25.125.10 | msg: [CLIENT 12] Message N°1
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: in_progress
client12  | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | client_id: 12 | msg: [CLIENT 12] Message N°1
client2   | 2024-09-01 17:56:17 INFO     action: config | result: success | client_id: 2 | server_address: server:12345 | loop_amount: 5 | loop_period: 5s | log_level: DEBUG
client2   | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | client_id: 2 | msg: [CLIENT 2] Message N°1
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: success | ip: 172.25.125.11
server    | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | ip: 172.25.125.11 | msg: [CLIENT 2] Message N°1
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: in_progress
client10  | 2024-09-01 17:56:17 INFO     action: config | result: success | client_id: 10 | server_address: server:12345 | loop_amount: 5 | loop_period: 5s | log_level: DEBUG
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: success | ip: 172.25.125.12
server    | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | ip: 172.25.125.12 | msg: [CLIENT 10] Message N°1
client10  | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | client_id: 10 | msg: [CLIENT 10] Message N°1
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: in_progress
client4   | 2024-09-01 17:56:17 INFO     action: config | result: success | client_id: 4 | server_address: server:12345 | loop_amount: 5 | loop_period: 5s | log_level: DEBUG
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: success | ip: 172.25.125.13
server    | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | ip: 172.25.125.13 | msg: [CLIENT 4] Message N°1
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: in_progress
client4   | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | client_id: 4 | msg: [CLIENT 4] Message N°1
client8   | 2024-09-01 17:56:17 INFO     action: config | result: success | client_id: 8 | server_address: server:12345 | loop_amount: 5 | loop_period: 5s | log_level: DEBUG
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: success | ip: 172.25.125.14
server    | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | ip: 172.25.125.14 | msg: [CLIENT 8] Message N°1
server    | 2024-09-01 17:56:17 INFO     action: accept_connections | result: in_progress
client8   | 2024-09-01 17:56:17 INFO     action: receive_message | result: success | client_id: 8 | msg: [CLIENT 8] Message N°1
server    | 2024-09-01 17:56:18 INFO     action: accept_connections | result: success | ip: 172.25.125.3
server    | 2024-09-01 17:56:18 INFO     action: receive_message | result: success | ip: 172.25.125.3 | msg: [CLIENT 6] Message N°1
client6   | 2024-09-01 17:56:18 INFO     action: receive_message | result: success | client_id: 6 | msg: [CLIENT 6] Message N°1
server    | 2024-09-01 17:56:18 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: success | ip: 172.25.125.4
client5   | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | client_id: 5 | msg: [CLIENT 5] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | ip: 172.25.125.4 | msg: [CLIENT 5] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: success | ip: 172.25.125.5
client1   | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | ip: 172.25.125.5 | msg: [CLIENT 1] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: success | ip: 172.25.125.6
server    | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | ip: 172.25.125.6 | msg: [CLIENT 7] Message N°2
client7   | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | client_id: 7 | msg: [CLIENT 7] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: success | ip: 172.25.125.7
client3   | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | client_id: 3 | msg: [CLIENT 3] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | ip: 172.25.125.7 | msg: [CLIENT 3] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: in_progress
client9   | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | client_id: 9 | msg: [CLIENT 9] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: success | ip: 172.25.125.9
client11  | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | client_id: 11 | msg: [CLIENT 11] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | ip: 172.25.125.9 | msg: [CLIENT 11] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: success | ip: 172.25.125.8
server    | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | ip: 172.25.125.8 | msg: [CLIENT 9] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: success | ip: 172.25.125.10
server    | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | ip: 172.25.125.10 | msg: [CLIENT 12] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: in_progress
client12  | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | client_id: 12 | msg: [CLIENT 12] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: success | ip: 172.25.125.11
server    | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | ip: 172.25.125.11 | msg: [CLIENT 2] Message N°2
client2   | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | client_id: 2 | msg: [CLIENT 2] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: success | ip: 172.25.125.12
server    | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | ip: 172.25.125.12 | msg: [CLIENT 10] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: in_progress
client10  | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | client_id: 10 | msg: [CLIENT 10] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: success | ip: 172.25.125.13
server    | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | ip: 172.25.125.13 | msg: [CLIENT 4] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: in_progress
client4   | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | client_id: 4 | msg: [CLIENT 4] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: success | ip: 172.25.125.14
server    | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | ip: 172.25.125.14 | msg: [CLIENT 8] Message N°2
client8   | 2024-09-01 17:56:22 INFO     action: receive_message | result: success | client_id: 8 | msg: [CLIENT 8] Message N°2
server    | 2024-09-01 17:56:22 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:23 INFO     action: accept_connections | result: success | ip: 172.25.125.3
server    | 2024-09-01 17:56:23 INFO     action: receive_message | result: success | ip: 172.25.125.3 | msg: [CLIENT 6] Message N°2
client6   | 2024-09-01 17:56:23 INFO     action: receive_message | result: success | client_id: 6 | msg: [CLIENT 6] Message N°2
server    | 2024-09-01 17:56:23 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: success | ip: 172.25.125.4
server    | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | ip: 172.25.125.4 | msg: [CLIENT 5] Message N°3
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: in_progress
client5   | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | client_id: 5 | msg: [CLIENT 5] Message N°3
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: success | ip: 172.25.125.5
server    | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | ip: 172.25.125.5 | msg: [CLIENT 1] Message N°3
client1   | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°3
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: success | ip: 172.25.125.6
server    | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | ip: 172.25.125.6 | msg: [CLIENT 7] Message N°3
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: in_progress
client7   | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | client_id: 7 | msg: [CLIENT 7] Message N°3
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: success | ip: 172.25.125.7
server    | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | ip: 172.25.125.7 | msg: [CLIENT 3] Message N°3
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: in_progress
client3   | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | client_id: 3 | msg: [CLIENT 3] Message N°3
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: success | ip: 172.25.125.8
server    | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | ip: 172.25.125.8 | msg: [CLIENT 9] Message N°3
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: success | ip: 172.25.125.9
server    | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | ip: 172.25.125.9 | msg: [CLIENT 11] Message N°3
client11  | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | client_id: 11 | msg: [CLIENT 11] Message N°3
client9   | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | client_id: 9 | msg: [CLIENT 9] Message N°3
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: success | ip: 172.25.125.10
server    | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | ip: 172.25.125.10 | msg: [CLIENT 12] Message N°3
client12  | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | client_id: 12 | msg: [CLIENT 12] Message N°3
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: success | ip: 172.25.125.11
server    | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | ip: 172.25.125.11 | msg: [CLIENT 2] Message N°3
client2   | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | client_id: 2 | msg: [CLIENT 2] Message N°3
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: success | ip: 172.25.125.12
client10  | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | client_id: 10 | msg: [CLIENT 10] Message N°3
server    | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | ip: 172.25.125.12 | msg: [CLIENT 10] Message N°3
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: in_progress
client4   | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | client_id: 4 | msg: [CLIENT 4] Message N°3
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: success | ip: 172.25.125.13
server    | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | ip: 172.25.125.13 | msg: [CLIENT 4] Message N°3
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: success | ip: 172.25.125.14
server    | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | ip: 172.25.125.14 | msg: [CLIENT 8] Message N°3
server    | 2024-09-01 17:56:27 INFO     action: accept_connections | result: in_progress
client8   | 2024-09-01 17:56:27 INFO     action: receive_message | result: success | client_id: 8 | msg: [CLIENT 8] Message N°3
server    | 2024-09-01 17:56:28 INFO     action: accept_connections | result: success | ip: 172.25.125.3
server    | 2024-09-01 17:56:28 INFO     action: receive_message | result: success | ip: 172.25.125.3 | msg: [CLIENT 6] Message N°3
server    | 2024-09-01 17:56:28 INFO     action: accept_connections | result: in_progress
client6   | 2024-09-01 17:56:28 INFO     action: receive_message | result: success | client_id: 6 | msg: [CLIENT 6] Message N°3
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: success | ip: 172.25.125.4
server    | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | ip: 172.25.125.4 | msg: [CLIENT 5] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: in_progress
client5   | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | client_id: 5 | msg: [CLIENT 5] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: success | ip: 172.25.125.5
server    | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | ip: 172.25.125.5 | msg: [CLIENT 1] Message N°4
client1   | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: success | ip: 172.25.125.6
server    | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | ip: 172.25.125.6 | msg: [CLIENT 7] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: in_progress
client7   | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | client_id: 7 | msg: [CLIENT 7] Message N°4
client3   | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | client_id: 3 | msg: [CLIENT 3] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: success | ip: 172.25.125.7
server    | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | ip: 172.25.125.7 | msg: [CLIENT 3] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: in_progress
client11  | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | client_id: 11 | msg: [CLIENT 11] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: success | ip: 172.25.125.9
server    | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | ip: 172.25.125.9 | msg: [CLIENT 11] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: success | ip: 172.25.125.8
server    | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | ip: 172.25.125.8 | msg: [CLIENT 9] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: in_progress
client9   | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | client_id: 9 | msg: [CLIENT 9] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: success | ip: 172.25.125.10
server    | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | ip: 172.25.125.10 | msg: [CLIENT 12] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: in_progress
client12  | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | client_id: 12 | msg: [CLIENT 12] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: success | ip: 172.25.125.11
server    | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | ip: 172.25.125.11 | msg: [CLIENT 2] Message N°4
client2   | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | client_id: 2 | msg: [CLIENT 2] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: success | ip: 172.25.125.12
server    | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | ip: 172.25.125.12 | msg: [CLIENT 10] Message N°4
client10  | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | client_id: 10 | msg: [CLIENT 10] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: in_progress
client4   | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | client_id: 4 | msg: [CLIENT 4] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: success | ip: 172.25.125.13
server    | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | ip: 172.25.125.13 | msg: [CLIENT 4] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: success | ip: 172.25.125.14
server    | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | ip: 172.25.125.14 | msg: [CLIENT 8] Message N°4
client8   | 2024-09-01 17:56:32 INFO     action: receive_message | result: success | client_id: 8 | msg: [CLIENT 8] Message N°4
server    | 2024-09-01 17:56:32 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:33 INFO     action: accept_connections | result: success | ip: 172.25.125.3
server    | 2024-09-01 17:56:33 INFO     action: receive_message | result: success | ip: 172.25.125.3 | msg: [CLIENT 6] Message N°4
client6   | 2024-09-01 17:56:33 INFO     action: receive_message | result: success | client_id: 6 | msg: [CLIENT 6] Message N°4
server    | 2024-09-01 17:56:33 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: success | ip: 172.25.125.4
server    | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | ip: 172.25.125.4 | msg: [CLIENT 5] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: in_progress
client5   | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | client_id: 5 | msg: [CLIENT 5] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: success | ip: 172.25.125.5
server    | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | ip: 172.25.125.5 | msg: [CLIENT 1] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: in_progress
client1   | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: success | ip: 172.25.125.6
server    | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | ip: 172.25.125.6 | msg: [CLIENT 7] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: in_progress
client7   | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | client_id: 7 | msg: [CLIENT 7] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: success | ip: 172.25.125.7
client3   | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | client_id: 3 | msg: [CLIENT 3] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | ip: 172.25.125.7 | msg: [CLIENT 3] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: success | ip: 172.25.125.9
server    | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | ip: 172.25.125.9 | msg: [CLIENT 11] Message N°5
client11  | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | client_id: 11 | msg: [CLIENT 11] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: success | ip: 172.25.125.8
server    | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | ip: 172.25.125.8 | msg: [CLIENT 9] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: in_progress
client9   | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | client_id: 9 | msg: [CLIENT 9] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: success | ip: 172.25.125.10
server    | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | ip: 172.25.125.10 | msg: [CLIENT 12] Message N°5
client12  | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | client_id: 12 | msg: [CLIENT 12] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: success | ip: 172.25.125.11
server    | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | ip: 172.25.125.11 | msg: [CLIENT 2] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: in_progress
client2   | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | client_id: 2 | msg: [CLIENT 2] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: success | ip: 172.25.125.12
server    | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | ip: 172.25.125.12 | msg: [CLIENT 10] Message N°5
client10  | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | client_id: 10 | msg: [CLIENT 10] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: in_progress
client4   | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | client_id: 4 | msg: [CLIENT 4] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: success | ip: 172.25.125.13
server    | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | ip: 172.25.125.13 | msg: [CLIENT 4] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: in_progress
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: success | ip: 172.25.125.14
server    | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | ip: 172.25.125.14 | msg: [CLIENT 8] Message N°5
server    | 2024-09-01 17:56:37 INFO     action: accept_connections | result: in_progress
client8   | 2024-09-01 17:56:37 INFO     action: receive_message | result: success | client_id: 8 | msg: [CLIENT 8] Message N°5
client6   | 2024-09-01 17:56:38 INFO     action: receive_message | result: success | client_id: 6 | msg: [CLIENT 6] Message N°5
server    | 2024-09-01 17:56:38 INFO     action: accept_connections | result: success | ip: 172.25.125.3
server    | 2024-09-01 17:56:38 INFO     action: receive_message | result: success | ip: 172.25.125.3 | msg: [CLIENT 6] Message N°5
server    | 2024-09-01 17:56:38 INFO     action: accept_connections | result: in_progress
client5   | 2024-09-01 17:56:42 INFO     action: loop_finished | result: success | client_id: 5
client1   | 2024-09-01 17:56:42 INFO     action: loop_finished | result: success | client_id: 1
client7   | 2024-09-01 17:56:42 INFO     action: loop_finished | result: success | client_id: 7
client5 exited with code 0
client3   | 2024-09-01 17:56:42 INFO     action: loop_finished | result: success | client_id: 3
client1 exited with code 0
client11  | 2024-09-01 17:56:42 INFO     action: loop_finished | result: success | client_id: 11
client9   | 2024-09-01 17:56:42 INFO     action: loop_finished | result: success | client_id: 9
client7 exited with code 0
client3 exited with code 0
client12  | 2024-09-01 17:56:42 INFO     action: loop_finished | result: success | client_id: 12
client9 exited with code 0
client11 exited with code 0
client2   | 2024-09-01 17:56:42 INFO     action: loop_finished | result: success | client_id: 2
client10  | 2024-09-01 17:56:42 INFO     action: loop_finished | result: success | client_id: 10
client12 exited with code 0
client4   | 2024-09-01 17:56:42 INFO     action: loop_finished | result: success | client_id: 4
client8   | 2024-09-01 17:56:42 INFO     action: loop_finished | result: success | client_id: 8
client2 exited with code 0
client10 exited with code 0
client8 exited with code 0
client4 exited with code 0
client6   | 2024-09-01 17:56:43 INFO     action: loop_finished | result: success | client_id: 6
client6 exited with code 0
```

</details>

# Ejercicio 2
Para el segundo ejercicio se agregaron volumenes y mount binds para mapear la configuración dentro del host con
los contenidos dentro del container de la siguiente manera:

```yaml
  server:
    container_name: server
    ...
    volumes:
      - ./config/server/config.ini:/config.ini

  client2:
    container_name: client1
    ...
    volumes:
      - ./config/client/config.yaml:/config.yaml
```

El mount bind nos permite inyectar la configuración de cada uno de los containers sin la necesidad
de rebuildear la imagen, al igual que nos permite hacer la aplicación más segura debido a que la configuración
no queda persistida en la imagen a la hora de buildearla.


# Ejercicio 3
Para el ejercicio 3 se creo el script `validar-echo-server.sh`:

```bash
TEST_MESSAGE="Test Message"

RESPONSE=$(echo "$TEST_MESSAGE" | nc "server:12345")

if [ "$RESPONSE" = "$TEST_MESSAGE" ]; then
    echo "action: test_echo_server | result: success"
else
    echo "action: test_echo_server | result: fail"
fi

```

El script se encarga de enviar un mensaje al servidor e imprimir el resultado que devuelve el servidor. Para ejecutar
este script dentro de la red que levanta `docker` se agrego un nuevo servicio a la definición del `docker-compose`:

```yaml
  netcat:
    container_name: netcat
    image: alpine:latest
    entrypoint: [ "/bin/sh", "./validar-echo-server.sh" ]
    networks:
      - testing_net
    depends_on:
      - server
    volumes:
      - ./validar-echo-server.sh:/validar-echo-server.sh
```

Este servicio usa como imagen base `alpine:latest`. Se utilizo esta imagen debido a que tiene todas
las funcionalidades necesarias y solo pesa `5MB`, haciendola ideal para la ejecución de scripts de este
estilo. Además se utilizo un mount bind para mappear el script en la maquina host con el container y asi
poder probar el script sin necesidad de rebuildear la imagen.


<details>
<summary>Ejemplo de ejecución</summary>

```console
docker compose -f docker-compose-dev.yaml logs -f
client1  | 2024-09-01 20:27:40 INFO     action: config | result: success | client_id: 1 | server_address: server:12345 | loop_amount: 5 | loop_period: 1s | log_level: DEBUG
client1  | 2024-09-01 20:27:40 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°1
client1  | 2024-09-01 20:27:41 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°2
client1  | 2024-09-01 20:27:42 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°3
client1  | 2024-09-01 20:27:43 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°4
netcat   | action: test_echo_server | result: success
server   | 2024-09-01 20:27:40 DEBUG    action: config | result: success | port: 12345 | listen_backlog: 5 | logging_level: DEBUG
server   | 2024-09-01 20:27:40 INFO     action: accept_connections | result: in_progress
server   | 2024-09-01 20:27:40 INFO     action: accept_connections | result: success | ip: 172.25.125.3
server   | 2024-09-01 20:27:40 INFO     action: receive_message | result: success | ip: 172.25.125.3 | msg: Test Message
server   | 2024-09-01 20:27:40 INFO     action: accept_connections | result: in_progress
server   | 2024-09-01 20:27:40 INFO     action: accept_connections | result: success | ip: 172.25.125.4
server   | 2024-09-01 20:27:40 INFO     action: receive_message | result: success | ip: 172.25.125.4 | msg: [CLIENT 1] Message N°1
server   | 2024-09-01 20:27:40 INFO     action: accept_connections | result: in_progress
server   | 2024-09-01 20:27:41 INFO     action: accept_connections | result: success | ip: 172.25.125.4
server   | 2024-09-01 20:27:41 INFO     action: receive_message | result: success | ip: 172.25.125.4 | msg: [CLIENT 1] Message N°2
server   | 2024-09-01 20:27:41 INFO     action: accept_connections | result: in_progress
server   | 2024-09-01 20:27:42 INFO     action: accept_connections | result: success | ip: 172.25.125.4
server   | 2024-09-01 20:27:42 INFO     action: receive_message | result: success | ip: 172.25.125.4 | msg: [CLIENT 1] Message N°3
server   | 2024-09-01 20:27:42 INFO     action: accept_connections | result: in_progress
server   | 2024-09-01 20:27:43 INFO     action: accept_connections | result: success | ip: 172.25.125.4
server   | 2024-09-01 20:27:43 INFO     action: receive_message | result: success | ip: 172.25.125.4 | msg: [CLIENT 1] Message N°4
server   | 2024-09-01 20:27:43 INFO     action: accept_connections | result: in_progress
client1  | 2024-09-01 20:27:44 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°5
server   | 2024-09-01 20:27:44 INFO     action: accept_connections | result: success | ip: 172.25.125.4
server   | 2024-09-01 20:27:44 INFO     action: receive_message | result: success | ip: 172.25.125.4 | msg: [CLIENT 1] Message N°5
server   | 2024-09-01 20:27:44 INFO     action: accept_connections | result: in_progress
client1  | 2024-09-01 20:27:45 INFO     action: loop_finished | result: success | client_id: 1
client1 exited with code 0
```

</details>

# Ejercicio 4

## Cliente
Para el caso del cliente se agrego un `channel` encargado de recibir un mensaje cuando se triggerea un `SIGTERM`:

```go
// Channel that is notified on SIGTERM
sigTermChannel := make(chan os.Signal, 1)
signal.Notify(sigTermChannel, syscall.SIGTERM)
```

Una vez seteado el channel, se le pasa a la función StartClientLoop donde se utiliza un select para responder al primer "evento" que ocurra primero. Hay 2 posibles eventos:

- signalChan: El segundo evento es triggereado cuando se recibe la notificación del `SIGTERM`.
- Timeout LoopPeriod: El tercer evento es triggereado cuando se pasa el tiempo configurado en 
`loop.period` que determina el periodo de tiempo a esperar entre cada mensaje.

```go
select {
case <-terminateChan:
	log.Infof("action: sigterm_signal | result: success | client_id: %v", c.config.ID)
	return
	
case <-time.After(c.config.LoopPeriod):
	continue	
}
```

## Servidor
En el caso del server se agregaron las siguientes lineas:

```python
# Define signal handlers
signal.signal(signal.SIGINT, self._handle_signal)
signal.signal(signal.SIGTERM, self._handle_signal)
```

Esto define `handlers` para cuando llegue las `signals` `SIGINT` y `SIGTERM`. El método `_handle_signal`
se encarga de cerrar todos los sockets activos de clientes, luego el socket del servidor y finalmente dar
de baja el mismo.

Tambien se agrego la property `self._shutdown` para identificar cuando se
obtuvo una signal. Si bien no es de gran utilidad en este momento y solo nos sirve
para catchear errores en el main loop causados por el cierre del server socket, en el futuro
este propiedad se puede reemplazar por un `multiprocessing.Event` como metodo de
sincronización entre los múltiples procesos.

<details>
<summary>Ejemplo de ejecución</summary>

```console
docker compose -f docker-compose-dev.yaml up -d           06:15:20 PM
[+] Running 3/4
 ⠼ Network tp0_testing_net  Created                                                                                0.4s
 ✔ Container server         Started                                                                                0.2s
 ✔ Container netcat         Started                                                                                0.4s
 ✔ Container client1        Started                                                                                0.4s
docker compose -f docker-compose-dev.yaml stop            06:15:23 PM
[+] Stopping 3/3
 ✔ Container netcat   Stopped                                                                                      0.0s
 ✔ Container client1  Stopped                                                                                      0.1s
 ✔ Container server   Stopped                                                                                      0.1s
docker compose -f docker-compose-dev.yaml logs            06:15:28 PM
netcat  | action: test_echo_server | result: success
server  | 2024-09-01 21:15:23 DEBUG    action: config | result: success | port: 12345 | listen_backlog: 5 | logging_level: DEBUG
server  | 2024-09-01 21:15:23 INFO     action: accept_connections | result: in_progress
server  | 2024-09-01 21:15:23 INFO     action: accept_connections | result: success | ip: 172.25.125.3
server  | 2024-09-01 21:15:23 INFO     action: receive_message | result: success | ip: 172.25.125.3 | msg: Test Message
server  | 2024-09-01 21:15:23 INFO     action: accept_connections | result: in_progress
server  | 2024-09-01 21:15:24 INFO     action: accept_connections | result: success | ip: 172.25.125.4
server   | 2024-09-01 21:15:24 INFO     action: receive_message | result: success | ip: 172.25.125.4 | msg: [CLIENT 1] Message N°1
client1  | 2024-09-01 21:15:23 INFO     action: config | result: success | client_id: 1 | server_address: server:12345 | loop_amount: 5 | loop_period: 1s | log_level: DEBUG
client1  | 2024-09-01 21:15:24 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°1
client1  | 2024-09-01 21:15:26 INFO     action: receive_message | result: success | client_id: 1 | msg: [CLIENT 1] Message N°2
client1  | 2024-09-01 21:15:28 INFO     action: sigterm_signal | result: success | client_id: 1
server   | 2024-09-01 21:15:24 INFO     action: accept_connections | result: in_progress
server   | 2024-09-01 21:15:26 INFO     action: accept_connections | result: success | ip: 172.25.125.4
server   | 2024-09-01 21:15:26 INFO     action: receive_message | result: success | ip: 172.25.125.4 | msg: [CLIENT 1] Message N°2
server   | 2024-09-01 21:15:26 INFO     action: accept_connections | result: in_progress
server   | 2024-09-01 21:15:28 INFO     action: signal_handler | result: success | signal: 15
server   | 2024-09-01 21:15:28 DEBUG    action: close server socket | result: success
server   | 2024-09-01 21:15:28 INFO     action: receive_sigterm | result: success | msg: breaking server loop

```


</details>

# Ejercicio 5

Para el protocolo se utilizan 2 tipos de mensaje:
- Message
- ResponseFlag

> Si bien voy a ir mostrando cada uno de los tipos de mensaje en código Python, la implementación
> se hizo en ambos lenguajes

### Message

El `Message` es un mensaje que esta compuesto por:
- MsgType: El tipo del mensaje. Este tipo especifica que contiene en el `payload` del mismo. En este ejercicio el único tipo es `SEND_BET`. Tiene tamaño de 1 byte
- Size: Un header utilizado para especificar el tamaño del payload. Tiene el tamaño de 2 bytes. Este tamaño fue elegido por el siguiente ejercicio. Ya que el batcheo puede tener un tamaño no mayor a 8KB, 2 bytes pueden representar payloads de tamaño de 65,536 bytes.
- Payload: El contenido del mensaje.

```python
class MessageType(int, enum.Enum):
    SEND_BET = 0

class Message:
    MSG_TYPE_SIZE = 1
    HEADER_SIZE = 2
    ENDIAN: Literal["little", "big"] = "big"

    def __init__(self, msg_type: MessageType, size: int, payload: bytes):
        self.msg_type = msg_type
        self.size = size
        self.payload = payload

    def to_bytes(self) -> bytes:
        msg_type_bytes = struct.pack('>B', self.msg_type.value)
        header_bytes = struct.pack('>H', self.size)
        return msg_type_bytes + header_bytes + self.payload

    @classmethod
    def from_socket(cls, socket: socket.socket):
        msg_type = read_from_socket(socket, Message.MSG_TYPE_SIZE)
        payload_size = read_from_socket(socket, Message.HEADER_SIZE)
        payload_size_int = int.from_bytes(payload_size, Message.ENDIAN)
        payload = read_from_socket(socket, payload_size_int)

        return cls(MessageType(msg_type[0]), payload_size_int, payload)
```

### ResponseFlag

El `ResponseFlag` es un mensaje utilizado para denotar un evento. Principalmente es usado para hacer acknowledge de operaciones
y devolver si hubo o no un error. Para este ejercicio solo se tienen 2 tipos de flag:
- `OK`: Señaliza que la operación de recepción y guardado de bet no tuvo errores.
- `ERROR`: Señaliza que la operación de recepción y guardado de bet tuvo errores.

```python
class FlagType(int, enum.Enum):
    OK = 0
    ERROR = 1


class ResponseFlag:
    FLAG_TYPE_SIZE = 1

    def __init__(self, flag_type: FlagType):
        self.flag_type = flag_type

    def to_bytes(self) -> bytes:
        flag_type_bytes = struct.pack('>B', self.flag_type)
        return flag_type_bytes

    @classmethod
    def from_socket(cls, socket: socket.socket):
        flag_type = read_from_socket(socket, ResponseFlag.FLAG_TYPE_SIZE)

        return cls(FlagType(flag_type[0]))

    @classmethod
    def ok(cls):
        return cls(FlagType.OK)

    @classmethod
    def error(cls):
        return cls(FlagType.ERROR)
```

# Ejercicio 6

Para este ejercicio se agrego la estructura `Batcher` para todo lo relacionado al manejo
de batchs de datos:

```go
type Batcher struct {
	MaxLimit int
	Counter  int
	buffer   bytes.Buffer
}

func NewBatcher(maxBytesLimit int) *Batcher {
	return &Batcher{
		maxBytesLimit,
		0,
		bytes.Buffer{},
	}
}

func (b *Batcher) IsFull() bool {
	if b.Counter > b.MaxLimit {
		return true
	}

	return false
}

func (b *Batcher) IsEmpty() bool {
	return b.Counter == 0 && b.buffer.Len() == 0
}

func (b *Batcher) IsFullWithNewItem(message []byte) bool {
	if b.buffer.Len()+len(message) > MaxBytesLimit || b.Counter+1 > b.MaxLimit {
		return true
	}
	return false
}

func (b *Batcher) Add(message []byte) error {
	if b.IsFullWithNewItem(message) {
		return FullBatcherError
	}

	b.buffer.Write(message)
	b.buffer.WriteByte('\n')
	b.Counter += 1
	return nil
}

func (b *Batcher) ToBytes() []byte {
	return b.buffer.Bytes()[:b.buffer.Len()-1]
}

func (b *Batcher) Reset() {
	b.Counter = 0
	b.buffer.Reset()
}
```

Se agrego otro campo en el header del protocolo, el `Identifier` utilizado para distinguir cual de los 2 tipos de mensaje es (representado con 1 byte):
- `IdentifierTypeMessage`: Mensaje con payload. Este es el mismo que se menciona para el Ej5 `Message`.
- `IdentifierTypeFlag`: Mensaje con 1 byte que señaliza un evento. Este es el mismo que se menciona para el Ej5 `ResponseFlag`.

Tambien se agrego el `ResponseFlag` del tipoe `END` para señalizar
en el protocolo cuando el cliente deja de enviar mensajes. El cliente sigue
la siguiente lógica:
- Lee cada línea del CSV.
- Si el batch no esta lleno y no supera el límite de 8Kb con el nuevo elemento, se agrega el bet al batch.
- Si el batch esta lleno o supera el límite de 8Kb con el nuevo elemento, se envía todos los bets dentro del batch, se resetea el mismo y se agrega el nuevo bet.
- Una vez que se termina de leer todo el archivo, se envía todo lo que quedo en el batch.
- Finalmente se envía el mensaje de `END` al servidor para señalizar que no se va a mandar más información.

Desde el servidor la lógica es más sencilla:
- Recibe conección del cliente.
- Si el mensaje es del tipo `IdentifierTypeMessage`, parsea el payload con los bets y lo agrega con `store_bets` y responde con OK o ERROR dependiendo del resultado de la operación.
- Si el mensaje es del tipo `IdentifierTypeFlag` y es un `END`, deja de esperar bets del cliente.

# Ejecricio 7

Se agregaron 2 modelos para manejar todo lo relacionado a los ganadores del sorteo.
El primero de estos modelos es `Winners` y es utilizado para mandar la cantidad de ganadores para una agencia y los
documentos de cada uno de los ganadores. Se pasa la cantidad de ganadores para manejar los casos en el que la agencia no tiene
ningun ganador.

```python
class Winners:
    def __init__(self, documents: List[str]):
        """Initialize the Winners with a list of document strings.

        Args:
            documents (List[str]): List of document strings.
        """
        self._documents = documents

    def to_bytes(self) -> bytes:
        """Convert the Winners instance to a bytes representation.

        Returns:
            bytes: Byte representation of the Winners, including the count and documents.
        """
        size = len(self._documents)
        joined = f'{size}' + ','.join(self._documents)
        return joined.encode('utf-8')

```

El segundo es `AskWinner` que representa el request del cliente pidiendo los ganadores. En el mismo se adjunta
el id de la agencia.

```python
class AskWinner:
    AGENCY_ID_SIZE = 1

    def __init__(self, agency_id: int):
        """Initialize the AskWinner with an agency ID.

        Args:
            agency_id (int): The ID of the agency.
        """
        self.agency_id = agency_id

    @classmethod
    def from_bytes(cls, data: bytes):
        """Create an AskWinner instance from bytes data.

        Args:
            data (bytes): Byte data to decode into an AskWinner instance.

        Returns:
            AskWinner: An instance of AskWinner.

        Raises:
            ValueError: If the data length is invalid.
        """
        if len(data) != 1:
            raise ValueError("Invalid data length for AskWinner")
        agency_id = data[0]
        return cls(agency_id)
```


Finalmente, el cliente utiliza  una lógica de re-intentos para pedir los winners. Se hizo de esta manera para no bloquear
el server al igual que para permitir que el cliente no se quede bloqueado esperando los resultados.

```go
	for i := 0; i < maxNumberOfRetries; i++ {
		select {
		case <-terminateChan:
			log.Infof("action: sigterm_signal | result: success | client_id: %v", c.config.ID)
			return nil
		default:
			{
				conn, err := net.Dial("tcp", c.config.ServerAddress)
				if err != nil {
					c.LogError("connect", err)
					return err
				}

				askWinners := models.AskWinner{AgencyId: c.agency}
				msg := protocol.Message{
					Identifier: protocol.Identifier{Type: protocol.IdentifierTypeMessage},
					MsgType:    protocol.MsgTypeAskWinners,
					Size:       len(askWinners.ToBytes()),
					Payload:    askWinners.ToBytes(),
				}
				if err := utils.WriteToSocket(conn, msg.ToBytes()); err != nil {
					c.LogError("ask_winners", err)
					conn.Close()
					return err
				}

				identifier := protocol.Identifier{}
				if er := identifier.FromSocket(&conn); er != nil {
					c.LogError("recv_winners", err)
					conn.Close()
					return err
				}

				if identifier.Type == protocol.IdentifierTypeMessage {
					response := protocol.Message{}
					if err := response.FromSocket(&conn); err != nil {
						c.LogError("recv_winners", err)
						conn.Close()
						return err
					}
					winners := models.Winners{}
					if err := winners.FromBytes(response.Payload); err != nil {
						c.LogError("recv_winners", err)
						conn.Close()
						return err
					}

					log.Infof("action: consulta_ganadores | result: success | cant_ganadores: %v}",
						len(winners.Documents),
					)
					conn.Close()
					return nil
				} else if identifier.Type == protocol.IdentifierTypeFlag {
					response := protocol.ResponseFlag{}
					if err := response.FromSocket(&conn); err != nil {
						c.LogError("recv_winners", err)
						conn.Close()
						return err
					}
					log.Infof("action: recv_winners | result: not-available | msg: waiting %v seconds for retry",
						timeBetweenRestries,
					)
					conn.Close()
					time.Sleep(time.Duration(timeBetweenRestries) * time.Second)
				}
			}
		}
	}
```