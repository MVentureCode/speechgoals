# SpeechGoals
Aplicación web desarrollada con Django para la consulta, organización y planificación de objetivos terapéuticos utilizados en intervención logopédica.

SpeechGoals está diseñada como una herramienta de apoyo para profesionales de la logopedia. El proyecto utiliza datos de pacientes de forma anonimizada, sin almacenar nombres, datos de contacto ni otra información identificativa.

## Objetivo del proyecto
SpeechGoals permite consultar un catálogo estructurado de objetivos terapéuticos y encontrar aquellos que pueden ser adecuados según diferentes criterios, como el área de intervención y el rango de edad.

El proyecto contempla diferentes áreas de intervención:
* Habla
* Lenguaje
* Comunicación
* Deglución
La aplicación también incluye una estructura de pacientes y diagnósticos anonimizada que permite recomendar objetivos según el área afectada y la edad del paciente.


## Funcionalidades

### Catálogo de objetivos
* Consulta pública del catálogo de objetivos.
* Visualización del detalle de cada objetivo.
* Clasificación por área de intervención.
* Clasificación por nivel de dificultad.
* Rango de edad recomendado.

### Búsqueda y filtros
El listado de objetivos permite:
* Buscar objetivos mediante texto.
* Filtrar por área.
* Filtrar por edad.
* Combinar diferentes filtros.

### Ordenación
Los resultados pueden ordenarse mediante parámetros GET:
* Descripción
* Área
* Dificultad
* Edad mínima
* Edad máxima
Además se puede seleccionar la dirección:
* Ascendente
* Descendente

### Paginación
El catálogo utiliza `Paginator` de Django para mostrar:
* 10 objetivos por página.
* Página anterior y siguiente.
* Conservación de los parámetros de búsqueda, filtros y ordenación al cambiar de página.

### Usuarios y autenticación
La aplicación incluye:
* Registro de usuarios: /registro/
* Login: /accounts/login/
* Logout: /accounts/logout/
* Protección de las acciones de creación y edición.
* Listado y detalle de objetivos disponibles públicamente.

### Gestión de objetivos
Los usuarios autenticados pueden:
* Crear objetivos.
* Editar objetivos.
* Utilizar formularios basados en `ModelForm`.
* Recibir mensajes de confirmación después de realizar operaciones correctamente.

## Tecnologías utilizadas
* Python 3.13
* Django 6
* SQLite
* HTML
* Django Templates
* Git
* GitHub

## Estructura del proyecto
speechgoals/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── goals/
│   ├── migrations/
│   ├── fixtures/
│   ├── templates/
│   │   └── goals/
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md

## Instalación y ejecución

### 1. Clonar el repositorio
git clone URL_DEL_REPOSITORIO
Entrar en la carpeta del proyecto:
cd speechgoals

### 2. Crear y activar el entorno virtual
- En macOS/Linux:
python3 -m venv venv
source venv/bin/activate
- En Windows:
python -m venv venv
venv\Scripts\activate

### 3. Instalar las dependencias
pip install -r requirements.txt

### 4. Aplicar las migraciones
python manage.py migrate

### 5. Crear un superusuario
Para acceder al panel de administración:
python manage.py createsuperuser
Django solicitará:
* Username
* Email
* Password

### 6. Comprobar el proyecto
python manage.py check
Si todo está correcto, Django mostrará:
System check identified no issues

### 7. Iniciar el servidor
python manage.py runserver
La aplicación estará disponible en:
http://127.0.0.1:8000/

## Registro y usuarios
Los usuarios pueden registrarse desde: /registro/
También pueden iniciar sesión desde: /login/
Y cerrar sesión mediante: /logout/
Las acciones de creación y edición de objetivos requieren que el usuario haya iniciado sesión.

## Ejemplos de búsqueda, filtros y ordenación

### Buscar por texto
/objetivos/?q=lenguaje

### Filtrar por área
/objetivos/?area=habla

### Filtrar por edad
/objetivos/?edad=5

### Ordenar por dificultad
/objetivos/?order=dificultad&dir=asc

### Orden descendente
/objetivos/?order=dificultad&dir=desc

### Combinar búsqueda, filtros y ordenación
/objetivos/?q=lenguaje&area=lenguaje&edad=5&order=dificultad&dir=desc

### Utilizar paginación
/objetivos/?page=2
También es posible combinar la paginación con los demás parámetros:
/objetivos/?q=lenguaje&area=lenguaje&edad=5&order=dificultad&dir=desc&page=2

## Modelos principales
El proyecto utiliza los siguientes modelos:

### Diagnostico
Catálogo de diagnósticos asociados a un área principal de intervención.

### Paciente
Representa un caso anonimizado. Actualmente almacena únicamente:
* Edad
* Diagnóstico
No se almacenan datos identificativos.

### Objetivo
Es el modelo principal del catálogo. Incluye:
* Área
* Descripción
* Dificultad
* Edad mínima
* Edad máxima

### PlanTratamiento
Permite relacionar un paciente con diferentes objetivos terapéuticos mediante una relación `ManyToMany`.

## Consideraciones sobre privacidad
SpeechGoals se ha diseñado para trabajar con casos de ejemplo y datos anonimizados durante esta etapa del proyecto.
El modelo `Paciente` no almacena:
* Nombre
* Apellidos
* Teléfono
* Dirección
* Correo electrónico
* Otros datos identificativos
El proyecto no debe utilizarse con datos clínicos reales sin implementar previamente las medidas de seguridad, privacidad y protección de datos correspondientes.


## Estado del proyecto
**En desarrollo.**
Esta versión corresponde a la implementación de funcionalidades de navegación y organización de datos con Django, incluyendo:
* Modelos
* ModelForms
* Validación
* Autenticación
* Registro de usuarios
* Búsqueda
* Filtros
* Ordenación
* Paginación
* Templates con herencia
* Mensajes de Django

## Autora
**Maria Victoria Galzadet**
Logopeda y desarrolladora en formación.
Proyecto orientado a la aplicación de tecnologías web y herramientas digitales al ámbito de la logopedia.

## Fecha de creación
Junio 2026