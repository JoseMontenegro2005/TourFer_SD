# Taller Práctico – Sistemas Distribuidos  
## Diseño e Integración con Docker Compose

## Descripción del sistema

El presente proyecto consiste en la implementación de un sistema distribuido básico para una aplicación de domicilios. La arquitectura se construye utilizando Docker Compose, permitiendo la ejecución y comunicación de múltiples servicios de manera aislada pero interconectada.

El sistema está diseñado bajo un enfoque de separación de responsabilidades, donde cada servicio cumple una función específica dentro de la aplicación.

---

## 4. Análisis

### 4.1 Rol de cada servicio

El sistema se compone de los siguientes servicios principales:

- **Frontend**:  
  Encargado de la interfaz de usuario. Permite la interacción con el sistema, mostrando información como restaurantes, productos y pedidos.

- **Backend**:  
  Gestiona la lógica de negocio. Procesa las solicitudes provenientes del frontend, maneja la información de pedidos y actúa como intermediario entre la interfaz y la base de datos.

- **Base de datos**:  
  Responsable del almacenamiento persistente de la información. Contiene los datos relacionados con usuarios, pedidos y productos.

---

### 4.2 Ventajas de dividir el sistema

La arquitectura basada en múltiples servicios ofrece diversas ventajas:

- **Escalabilidad**: cada servicio puede escalar de manera independiente según la demanda.
- **Mantenibilidad**: facilita la actualización o modificación de componentes sin afectar el sistema completo.
- **Aislamiento de fallos**: un error en un servicio no necesariamente afecta a los demás.
- **Flexibilidad tecnológica**: permite utilizar diferentes tecnologías según las necesidades de cada servicio.
- **Despliegue independiente**: cada componente puede desplegarse de forma autónoma.

---

### 4.3 Comunicación entre contenedores

Los contenedores se comunican mediante una red interna generada automáticamente por Docker Compose.

Cada servicio puede acceder a otro utilizando el nombre del servicio como identificador de red. Por ejemplo, el backend se conecta a la base de datos utilizando el nombre del servicio `db` como host.

Ejemplo de configuración de conexión:

```

host: db
puerto: 5432
usuario: fooddash
contraseña: fooddash_secret_2024

````

Este mecanismo elimina la necesidad de configuraciones externas complejas y facilita la integración entre servicios.

---

## 5. Exploración para la siguiente clase

### 5.1 Definición del servicio de base de datos

El servicio de base de datos se define en el archivo `docker-compose.yml` de la siguiente manera:

```yaml
db:
  image: postgres:16-alpine
  environment:
    POSTGRES_USER: fooddash
    POSTGRES_PASSWORD: fooddash_secret_2024
    POSTGRES_DB: fooddash
  ports:
    - "5432:5432"
````

---

### 5.2 Variables de entorno

Las variables de entorno permiten configurar los servicios sin necesidad de modificar el código fuente. En Docker Compose se definen mediante la sección `environment`.

Ejemplo:

```yaml
environment:
  POSTGRES_USER: fooddash
  POSTGRES_PASSWORD: fooddash_secret_2024
```

Adicionalmente, es posible utilizar archivos `.env` para centralizar la configuración y mejorar la seguridad.

---

### 5.3 Conexión del backend con la base de datos

El backend se conecta a la base de datos mediante una cadena de conexión que incluye los parámetros necesarios para establecer la comunicación.

Ejemplo:

```
DATABASE_URL=postgresql://fooddash:fooddash_secret_2024@db:5432/fooddash
```

Elementos principales de la conexión:

* Usuario
* Contraseña
* Host (nombre del servicio)
* Puerto
* Nombre de la base de datos

---

### 5.4 Posibles errores de conexión

Durante la implementación de sistemas distribuidos pueden presentarse los siguientes errores:

* **Base de datos no disponible**: el backend intenta conectarse antes de que la base de datos esté lista.
* **Credenciales incorrectas**: errores en usuario o contraseña.
* **Host incorrecto**: no utilizar el nombre del servicio definido en Docker Compose.
* **Conflictos de puertos**: otro servicio está utilizando el mismo puerto.
* **Problemas de red interna**: los contenedores no se encuentran en la misma red.

---

## Conclusión

El uso de Docker Compose permite implementar una arquitectura distribuida de forma eficiente, facilitando la comunicación entre servicios y mejorando la organización del sistema. Este enfoque es fundamental en el desarrollo de aplicaciones modernas, ya que promueve la escalabilidad, el mantenimiento y la resiliencia del sistema.

```
