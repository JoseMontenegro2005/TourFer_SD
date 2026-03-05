# PARTE 1 – Exploración de Imágenes

## ✅ Actividad 1: Ver imágenes locales

Ejecutar:

```
docker images
```

![Docker-image](imagenes/Docker-image.png)

Respondan en equipo:

- ¿Qué es el IMAGE ID?

El **IMAGE ID** es un identificador único que Docker asigna a cada imagen. Sirve para distinguir una imagen de otra dentro del sistema y permite referenciarla cuando se ejecutan comandos como `docker run` o `docker rmi`.
- ¿Qué significa TAG?

El **TAG** es la etiqueta o versión de una imagen de Docker. Permite identificar diferentes versiones de la misma imagen. Por ejemplo, `latest` indica la versión más reciente disponible.
- ¿Qué representa SIZE?

El **SIZE** representa el tamaño que ocupa la imagen en el disco del sistema. Esto incluye todas las capas que componen la imagen.

- ¿Una imagen se está ejecutando?

No. Una imagen no se ejecuta por sí sola. Una imagen es solo una plantilla o modelo. Lo que realmente se ejecuta es un **contenedor**, que es una instancia creada a partir de una imagen.

## ✅ Actividad 2: Descargar nuevas imágenes

Cada equipo debe descargar una imagen diferente:

```
docker pull redis
```
![docker-pull-redis](imagenes/docker-pull-redis.png)
O también pueden usar:

```
docker pull mongo
docker pull httpd
docker pull postgres
```

Luego, ejecuten nuevamente:

```
docker images
```
![docker-image-2](imagenes/docker-image-2.png)
Reflexionar:

- ¿Qué cambió?

Después de ejecutar el comando `docker pull redis`, al usar nuevamente `docker images` se observa que aparece una nueva imagen llamada **redis** en la lista de imágenes locales. Esto significa que la imagen fue descargada correctamente desde Docker Hub y ahora está disponible en el equipo.

- ¿El servicio ya está funcionando?

No. El servicio aún no está funcionando. El comando `docker pull` solo descarga la imagen, pero no la ejecuta. Para que el servicio funcione es necesario crear y ejecutar un contenedor usando el comando `docker run`.

# PARTE 2 – Gestión de Contenedores

## ✅ Actividad 3: Crear un contenedor

Ejemplo con nginx:

```
docker run-d--name servidor-web-p8081:80 nginx
```
![docker-run](imagenes/docker-run.png)
Verificar:

```
dockerps
```
![docker-ps](imagenes/docker-ps.png)
Abrir el navegador:
```
http://localhost:8081
```
![local](imagenes/local.png)

## ✅ Actividad 4: Administrar el contenedor

Detener:

```
dockerstop servidor-web
```
![docker-stop](imagenes/docker-stop.png)

Ver todos los contenedores:

```
dockerps-a
```
![docker-ps-a](imagenes/docker-ps-a.png)
Reiniciar:

```
dockerstart servidor-web
```
![docker-start](imagenes/docker-start.png)
Eliminar:
```
dockerrm-f servidor-web
```
![docker-rm](imagenes/docker-rm.png)

# PARTE 3 – Análisis Conceptual

| Concepto                      | Imagen                                   | Contenedor                                      |
|--------------------------------|-------------------------------------------|--------------------------------------------------|
| ¿Es ejecutable?               | No, es una plantilla                      | Sí, es una instancia en ejecución de una imagen |
| ¿Ocupa recursos en ejecución? | No                                        | Sí, usa CPU, RAM y red                          |
| ¿Puede modificarse?           | No, es inmutable                          | Sí, puede cambiar durante su ejecución          |
| ¿Puede eliminarse?            | Sí, puede borrarse del sistema            | Sí, puede detenerse y eliminarse                |

# PARTE 4 – Reto en Equipo

Cada grupo debe:

1. Ejecutar un contenedor diferente.
2. Mostrar que está activo.
![redis](imagenes/redis.png)
3. Explicar:
    - ¿Qué tipo de servicio es?

    Redis es una base de datos NoSQL en memoria que se utiliza principalmente para almacenar datos de forma muy rápida. Se usa comúnmente como sistema de caché, almacenamiento de sesiones o cola de mensajes en aplicaciones.

    - ¿En qué tipo de sistema distribuido podría usarse?

    Redis puede utilizarse en sistemas distribuidos como arquitecturas de microservicios, aplicaciones web de gran escala o plataformas que necesitan acceso rápido a datos compartidos entre varios servicios.

    - ¿Qué pasaría si ese servicio falla?

    Si el servicio Redis falla, las aplicaciones que dependen de él podrían perder acceso a datos temporales como sesiones o caché, lo que puede causar lentitud en el sistema o errores en algunas funcionalidades.


# PARTE 5 – Análisis Crítico

### 1. ¿Cuál es la diferencia real entre imagen y contenedor?
Una imagen es una plantilla o modelo que contiene todo lo necesario para ejecutar una aplicación, como el sistema base, librerías y configuraciones. Un contenedor es una instancia en ejecución de esa imagen, es decir, un entorno aislado donde la aplicación se ejecuta.

### 2. ¿Por qué Docker facilita la escalabilidad?
Docker facilita la escalabilidad porque permite crear y ejecutar múltiples contenedores de manera rápida y eficiente. Esto hace posible replicar servicios fácilmente cuando aumenta la demanda, distribuyendo la carga entre varios contenedores.

### 3. ¿Cómo se relaciona esto con microservicios?
Docker es muy útil para arquitecturas de microservicios porque cada servicio puede ejecutarse en su propio contenedor de forma independiente. Esto permite desarrollar, desplegar y escalar cada microservicio sin afectar a los demás.

### 4. ¿Qué ventajas ofrece frente a instalar software directamente?
Docker ofrece varias ventajas como la portabilidad, ya que las aplicaciones pueden ejecutarse igual en diferentes sistemas. También facilita la instalación y configuración, evita conflictos entre dependencias y permite aislar cada aplicación en su propio entorno.

## Conclusión

Durante esta práctica se aprendió a trabajar con Docker para gestionar imágenes y contenedores, entendiendo cómo descargar imágenes, crear contenedores y administrarlos mediante comandos desde la terminal. También se comprendió la diferencia entre una imagen y un contenedor, así como la importancia de estos en el despliegue de aplicaciones. Además, se observó cómo Docker facilita la portabilidad, el aislamiento de aplicaciones y la escalabilidad en sistemas distribuidos. Estas características lo hacen una herramienta muy útil en el desarrollo moderno, especialmente en arquitecturas basadas en microservicios. En general, la práctica permitió comprender de forma práctica cómo funcionan los contenedores y su utilidad en entornos reales de desarrollo y despliegue de software.

