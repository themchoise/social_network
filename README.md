# 🎓 Red Social Institucional IFTS

![Django](https://img.shields.io/badge/Django-5.2.6-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.3.0-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

Una plataforma integral de red social diseñada específicamente para instituciones educativas, que facilita la interacción académica, el intercambio de conocimientos y la colaboración entre estudiantes y docentes.

## 📋 Tabla de Contenidos

- [🎯 Características Principales](#-características-principales)
- [🏗️ Arquitectura del Sistema](#️-arquitectura-del-sistema)
- [📊 Modelo de Datos](#-modelo-de-datos)
- [🚀 Tecnologías](#-tecnologías)
- [📦 Instalación](#-instalación)
- [🐳 Deployment con Docker](#-deployment-con-docker)
- [🔧 Configuración](#-configuración)
- [📱 Uso de la Aplicación](#-uso-de-la-aplicación)
- [🏆 Sistema de Gamificación](#-sistema-de-gamificación)
- [🛠️ API y Endpoints](#️-api-y-endpoints)
- [🤝 Contribución](#-contribución)
- [📄 Licencia](#-licencia)

## 🎯 Características Principales

### 🎓 **Sistema Académico Integrado**

- **Gestión de Carreras**: Múltiples programas académicos con duración, créditos y modalidades
- **Materias y Prerrequisitos**: Sistema completo de materias con dependencias académicas
- **Perfiles de Usuario**: Estudiantes con información académica completa
- **Seguimiento de Progreso**: Monitoreo del avance académico individual

### 🤝 **Red Social Educativa**

- **Timeline Académico**: Feed personalizado con contenido educativo relevante
- **Sistema de Amistad**: Conexiones entre estudiantes con diferentes niveles de privacidad
- **Seguimiento (Follow)**: Sistema asimétrico para seguir a usuarios sin reciprocidad
- **Grupos de Estudio**: Espacios colaborativos organizados por materias o temas

### 📚 **Gestión de Contenido Académico**

- **Publicaciones Educativas**: Posts con múltiples tipos (texto, imagen, video, enlaces)
- **Notas Académicas**: Sistema completo de apuntes con categorización por materia
- **Comentarios y Discusiones**: Interacciones threaded para debates académicos
- **Archivos Adjuntos**: Soporte para documentos PDF, imágenes y otros materiales

### 🏆 **Sistema de Gamificación**

- **Puntos y Niveles**: Progresión basada en participación y calidad de contenido
- **Logros (Achievements)**: Sistema de reconocimientos por hitos académicos y sociales
- **Reacciones Múltiples**: 8 tipos de reacciones emocionales para contenido
- **Sistema de "Me Gusta"**: Valoración de contenido por la comunidad

### 🔔 **Notificaciones Inteligentes**

- **Notificaciones en Tiempo Real**: Sistema completo de alertas personalizables
- **Preferencias Granulares**: Control detallado sobre tipos y frecuencia de notificaciones
- **Múltiples Canales**: Notificaciones in-app y por email

### 🛡️ **Seguridad y Privacidad**

- **Niveles de Privacidad**: Público, solo amigos, grupos específicos o privado
- **Sistema de Bloqueo**: Herramientas para gestionar interacciones no deseadas
- **Moderación de Contenido**: Herramientas para reportar y moderar contenido inapropiado

## 🏗️ Arquitectura del Sistema

### **Patrón MVT (Model-View-Template)**

```
socialnetwork_project/
├── 📁 apps/                    # Aplicaciones modulares
│   ├── 👤 user/               # Gestión de usuarios
│   ├── 🎓 career/             # Carreras académicas
│   ├── 📚 subject/            # Materias y cursos
│   ├── 📝 post/               # Publicaciones
│   ├── 💬 comment/            # Comentarios
│   ├── 📋 note/               # Notas académicas
│   ├── 👥 group/              # Grupos de estudio
│   ├── 🤝 friendship/         # Sistema de amistad
│   ├── 👍 like/               # Sistema de likes
│   ├── 😊 reaction/           # Reacciones emocionales
│   ├── 🔔 notification/       # Notificaciones
│   ├── 🏆 achievement/        # Logros y gamificación
│   └── 🏠 main/               # Vistas principales
├── 📁 templates/              # Templates HTML
├── 📁 static/                 # Archivos estáticos
├── 📁 media/                  # Archivos subidos
└── 📁 socialnetwork_project/  # Configuración principal
```

### **Sistema de Apps Modulares**

Cada funcionalidad está encapsulada en una app Django independiente, siguiendo el principio de **separación de responsabilidades** y facilitando el mantenimiento y escalabilidad.

## 📊 Modelo de Datos

### 👤 **User (Usuario)**

**Descripción**: Modelo central que extiende AbstractUser de Django para usuarios del sistema.

**Campos Principales**:

```python
# Información Personal
email = EmailField(unique=True)           # Email único
bio = TextField(max_length=500)           # Biografía
avatar = ImageField()                     # Foto de perfil
birth_date = DateField()                  # Fecha de nacimiento
location = CharField(max_length=100)      # Ubicación
website = URLField()                      # Sitio web personal

# Información Académica
career = ForeignKey('career.Career')      # Carrera inscrita
student_id = CharField(unique=True)       # Número de estudiante
current_semester = PositiveIntegerField() # Semestre actual
enrollment_year = PositiveIntegerField()  # Año de ingreso

# Gamificación
total_points = PositiveIntegerField()     # Puntos totales
level = PositiveIntegerField()            # Nivel actual
achievements = ManyToManyField()          # Logros obtenidos

# Configuración
profile_visibility = CharField()          # Privacidad del perfil
show_email = BooleanField()              # Mostrar email públicamente
```

**Relaciones**:

- **1:N** con Post (posts creados)
- **1:N** con Comment (comentarios realizados)
- **1:N** con Note (notas creadas)
- **M:N** con User (amistades bidireccionales)
- **M:N** con Achievement (logros obtenidos)
- **M:N** con Group (grupos unidos)

---

### 🎓 **Career (Carrera)**

**Descripción**: Representa los programas académicos disponibles en la institución.

**Campos Principales**:

```python
# Información Básica
name = CharField(max_length=200)          # Nombre completo
code = CharField(unique=True)             # Código único (ej: TSDS001)
acronym = CharField(max_length=10)        # Siglas (ej: TSDS)
description = TextField()                 # Descripción detallada

# Clasificación
career_type = CharField()                 # Tipo: undergraduate, graduate, etc.
modality = CharField()                    # Modalidad: presencial, virtual, híbrida
faculty = CharField(max_length=100)       # Facultad
department = CharField(max_length=100)    # Departamento

# Duración y Créditos
duration_semesters = PositiveIntegerField() # Duración en semestres
duration_years = PositiveIntegerField()     # Duración en años
total_credits = PositiveIntegerField()      # Créditos totales requeridos

# Configuración
is_active = BooleanField()                # Carrera activa
requires_admission_exam = BooleanField()   # Requiere examen de ingreso
max_students_per_semester = PositiveIntegerField() # Cupo máximo
```

**Relaciones**:

- **1:N** con User (estudiantes inscriptos)
- **M:N** con Subject (materias del plan de estudios)
- **1:N** con Group (grupos relacionados)

---

### 📚 **Subject (Materia)**

**Descripción**: Materias y cursos que componen los planes de estudio.

**Campos Principales**:

```python
# Información Básica
name = CharField(max_length=200)          # Nombre de la materia
code = CharField(unique=True)             # Código único
description = TextField()                 # Descripción del contenido

# Configuración Académica
semester = PositiveIntegerField()         # Semestre correspondiente
credits = PositiveIntegerField()          # Créditos que otorga
subject_type = CharField()                # Tipo: obligatoria, electiva, opcional

# Estado
is_active = BooleanField()                # Materia activa
```

**Relaciones**:

- **M:N** con Career (carreras que incluyen la materia)
- **M:N** con Subject (prerrequisitos - relación consigo misma)
- **1:N** con Note (notas relacionadas)
- **1:N** con Group (grupos de estudio)

---

### 📝 **Post (Publicación)**

**Descripción**: Contenido principal del feed social, incluyendo diferentes tipos de publicaciones.

**Campos Principales**:

```python
# Contenido
content = TextField()                     # Texto principal
post_type = CharField()                   # Tipo: text, image, video, link, etc.
title = CharField(max_length=200)         # Título (opcional)

# Archivos Multimedia
image = ImageField()                      # Imagen adjunta
video = FileField()                       # Video adjunto
link_url = URLField()                     # URL externa
link_title = CharField()                  # Título del enlace
link_description = TextField()            # Descripción del enlace

# Configuración
privacy_level = CharField()               # Privacidad: public, friends, group, private
is_featured = BooleanField()              # Publicación destacada
is_pinned = BooleanField()               # Publicación fijada
allow_comments = BooleanField()           # Permitir comentarios

# Estadísticas
views_count = PositiveIntegerField()      # Número de visualizaciones
shares_count = PositiveIntegerField()     # Número de compartidas
```

**Relaciones**:

- **N:1** con User (autor)
- **1:N** con Comment (comentarios recibidos)
- **M:N** con User (likes a través de Like)
- **1:N** con Reaction (reacciones recibidas)
- **N:1** con Group (grupo al que pertenece - opcional)

---

### 💬 **Comment (Comentario)**

**Descripción**: Sistema de comentarios para publicaciones y otros comentarios (threading).

**Campos Principales**:

```python
# Contenido
content = TextField()                     # Texto del comentario
edited = BooleanField()                   # Indica si fue editado
edit_reason = CharField()                 # Razón de la edición

# Jerarquía
parent_comment = ForeignKey('self')       # Comentario padre (threading)
depth_level = PositiveIntegerField()      # Nivel de profundidad

# Referencias Genéricas
content_type = ForeignKey(ContentType)    # Tipo de objeto comentado
object_id = PositiveIntegerField()        # ID del objeto comentado
content_object = GenericForeignKey()      # Objeto comentado
```

**Relaciones**:

- **N:1** con User (autor)
- **1:N** con Comment (respuestas - relación consigo mismo)
- **Generic** con cualquier modelo (Post, Note, etc.)
- **1:N** con Like (likes recibidos)
- **1:N** con Reaction (reacciones recibidas)

---

### 📋 **Note (Nota Académica)**

**Descripción**: Sistema de notas y apuntes académicos compartibles entre estudiantes.

**Campos Principales**:

```python
# Contenido
title = CharField(max_length=200)         # Título de la nota
content = TextField()                     # Contenido principal
note_type = CharField()                   # Tipo: class, summary, exercise, etc.
tags = CharField(max_length=500)          # Tags separados por comas

# Archivo Adjunto
file_attachment = FileField()             # Archivo adjunto (PDF, DOC, etc.)

# Configuración
privacy_level = CharField()               # Nivel de privacidad
is_featured = BooleanField()              # Nota destacada
is_active = BooleanField()                # Nota activa

# Estadísticas
views_count = PositiveIntegerField()      # Visualizaciones
downloads_count = PositiveIntegerField()   # Descargas
```

**Relaciones**:

- **N:1** con User (autor)
- **N:1** con Subject (materia relacionada)
- **M:N** con User (favoritos a través de NoteFavorite)
- **1:N** con Comment (comentarios recibidos)
- **1:N** con Like (likes recibidos)

---

### 👥 **Group (Grupo)**

**Descripción**: Espacios de colaboración para estudiantes con intereses académicos comunes.

**Campos Principales**:

```python
# Información Básica
name = CharField(max_length=100)          # Nombre del grupo
description = TextField()                 # Descripción y propósito
group_type = CharField()                  # Tipo: study, project, social, etc.
privacy_level = CharField()               # Privacidad: public, private, closed

# Configuración
max_members = PositiveIntegerField()      # Máximo de miembros
allow_member_posts = BooleanField()       # Permitir posts de miembros
allow_member_invites = BooleanField()     # Permitir invitaciones de miembros
require_admin_approval = BooleanField()   # Requiere aprobación para unirse

# Imagen
cover_image = ImageField()                # Imagen de portada
```

**Relaciones**:

- **N:1** con User (creador/administrador)
- **M:N** con User (miembros a través de GroupMembership)
- **N:1** con Subject (materia relacionada - opcional)
- **N:1** con Career (carrera relacionada - opcional)
- **1:N** con Post (publicaciones del grupo)

---

### 🤝 **Friendship (Amistad)**

**Descripción**: Sistema de amistad bidireccional con estados de solicitud.

**Campos Principales**:

```python
# Usuarios
sender = ForeignKey('user.User')          # Usuario que envía solicitud
receiver = ForeignKey('user.User')        # Usuario que recibe solicitud

# Estado
status = CharField()                      # Estado: pending, accepted, rejected, blocked
request_date = DateTimeField()            # Fecha de solicitud
response_date = DateTimeField()           # Fecha de respuesta
message = TextField(max_length=200)       # Mensaje de solicitud
```

**Estados**:

- **pending**: Solicitud enviada, esperando respuesta
- **accepted**: Amistad confirmada por ambas partes
- **rejected**: Solicitud rechazada
- **blocked**: Usuario bloqueado

**Relaciones**:

- **N:1** con User (remitente)
- **N:1** con User (receptor)

---

### 🔔 **Notification (Notificación)**

**Descripción**: Sistema completo de notificaciones para mantener a los usuarios informados.

**Campos Principales**:

```python
# Usuarios
recipient = ForeignKey('user.User')       # Usuario que recibe
sender = ForeignKey('user.User')          # Usuario que genera (opcional)

# Contenido
notification_type = CharField()           # Tipo de notificación
title = CharField(max_length=200)         # Título
message = TextField()                     # Mensaje detallado

# Estado
is_read = BooleanField()                  # Leída o no
read_at = DateTimeField()                 # Momento de lectura

# Referencias
action_url = URLField()                   # URL de acción
content_type = ForeignKey(ContentType)    # Tipo de objeto relacionado
object_id = PositiveIntegerField()        # ID del objeto relacionado
```

**Tipos de Notificación**:

- **like**: Me gusta recibido
- **comment**: Comentario en publicación
- **friendship_request**: Solicitud de amistad
- **follow**: Nuevo seguidor
- **mention**: Mención en publicación
- **achievement**: Logro desbloqueado
- **group_invite**: Invitación a grupo

---

### 🏆 **Achievement (Logro)**

**Descripción**: Sistema de gamificación con logros desbloqueables.

**Campos Principales**:

```python
# Información
name = CharField(max_length=200)          # Nombre del logro
description = TextField()                 # Descripción detallada
condition_description = TextField()       # Condiciones para desbloquear

# Clasificación
achievement_type = CharField()            # Tipo: academic, social, completion, etc.
level = CharField()                       # Nivel: bronze, silver, gold, platinum
points = PositiveIntegerField()           # Puntos que otorga
icon = CharField(max_length=100)          # Clase de icono

# Estado
is_active = BooleanField()                # Logro activo
```

**Tipos de Logro**:

- **academic**: Relacionados con rendimiento académico
- **social**: Interacciones y participación social
- **completion**: Finalización de tareas o cursos
- **milestone**: Hitos importantes
- **special**: Eventos especiales o únicos

**Relaciones**:

- **M:N** con User (usuarios que lo han obtenido a través de UserAchievement)

---

### 👍 **Like (Me Gusta)**

**Descripción**: Sistema genérico de "me gusta" aplicable a cualquier contenido.

**Campos Principales**:

```python
# Usuario
user = ForeignKey('user.User')            # Usuario que da like

# Referencia Genérica
content_type = ForeignKey(ContentType)    # Tipo de objeto
object_id = PositiveIntegerField()        # ID del objeto
content_object = GenericForeignKey()      # Objeto al que se da like

# Timestamp
created_at = DateTimeField()              # Momento del like
```

**Aplicable a**:

- Posts
- Comments
- Notes
- Cualquier modelo que implemente GenericRelation

---

### 😊 **Reaction (Reacción)**

**Descripción**: Sistema avanzado de reacciones emocionales para expresar diferentes sentimientos.

**Campos Principales**:

```python
# Usuario
user = ForeignKey('user.User')            # Usuario que reacciona

# Tipo de Reacción
reaction_type = CharField()               # Tipo de reacción

# Referencia Genérica
content_type = ForeignKey(ContentType)    # Tipo de objeto
object_id = PositiveIntegerField()        # ID del objeto
content_object = GenericForeignKey()      # Objeto al que se reacciona
```

**Tipos de Reacción**:

- 👍 **like**: Me gusta
- ❤️ **love**: Me encanta
- 😂 **laugh**: Divertido
- 😮 **wow**: Sorpresa
- 😢 **sad**: Triste
- 😠 **angry**: Enojado
- 🎉 **celebrate**: Celebrar
- 💪 **support**: Apoyo

---

## 🚀 Tecnologías

### **Backend**

- **Framework**: Django 5.2.6
- **Lenguaje**: Python 3.11
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Servidor Web**: Gunicorn
- **Archivos Estáticos**: WhiteNoise

### **Frontend**

- **CSS Framework**: Tailwind CSS 3.3.0
- **JavaScript**: Vanilla JS con componentes interactivos
- **Build Tool**: Node.js + npm
- **Iconos**: Heroicons (SVG)

### **Deployment**

- **Containerización**: Docker
- **Orquestación**: CapRover
- **Servidor Web**: Nginx (reverse proxy)
- **SSL**: Let's Encrypt

### **Herramientas de Desarrollo**

- **Control de Versiones**: Git
- **Linting**: flake8, ESLint
- **Formateo**: Black, Prettier
- **Testing**: Django TestCase, Jest

## 📦 Instalación

### **Prerrequisitos**

- Python 3.11+
- Node.js 18+
- Git

### **Instalación Local**

1. **Clonar el repositorio**

```bash
git clone https://github.com/tuusuario/social-network-ifts.git
cd social-network-ifts
```

2. **Crear entorno virtual**

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows
```

3. **Instalar dependencias Python**

```bash
pip install -r requirements.txt
```

4. **Instalar dependencias Node.js**

```bash
npm install
```

5. **Compilar CSS**

```bash
npm run build
```

6. **Configurar base de datos**

```bash
python manage.py migrate
```

7. **Crear superusuario**

```bash
python manage.py createsuperuser
```

8. **Cargar datos de ejemplo**

```bash
python crear_datos_ejemplo.py
```

9. **Ejecutar servidor de desarrollo**

```bash
python manage.py runserver
```

La aplicación estará disponible en `http://127.0.0.1:8000/`

## 🐳 Deployment con Docker

### **Para CapRover**

1. **Clonar y configurar**

```bash
git clone https://github.com/tuusuario/social-network-ifts.git
cd social-network-ifts
```

2. **Configurar variables de entorno en CapRover**

```bash
DEBUG=False
SECRET_KEY=tu-clave-secreta-aqui
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@ifts.edu.ar
DJANGO_SUPERUSER_PASSWORD=password-seguro
```

3. **Deployment automático**
   CapRover detectará automáticamente el `captain-definition` y realizará el deployment.

Para más detalles, consulta [CAPROVER_DEPLOYMENT.md](CAPROVER_DEPLOYMENT.md)

## 🔧 Configuración

### **Configuración de Desarrollo**

```python
# settings.py
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Base de datos SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### **Configuración de Producción**

```python
# production_settings.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com']

# Base de datos PostgreSQL
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

# Archivos estáticos con WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
```

### **Variables de Entorno**

```bash
# Seguridad
SECRET_KEY=clave-secreta-muy-larga
DEBUG=False

# Base de datos
DATABASE_URL=postgres://user:pass@host:5432/dbname

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password

# Superusuario inicial
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@ifts.edu.ar
DJANGO_SUPERUSER_PASSWORD=password-seguro
```

## 📱 Uso de la Aplicación

### **Panel de Administración**

Accede a `/admin/` con credenciales de superusuario para:

- Gestionar usuarios y permisos
- Configurar carreras y materias
- Moderar contenido
- Ver estadísticas de uso

### **Timeline Principal**

La página principal (`/main/`) muestra:

- Feed personalizado de publicaciones
- Sidebar con navegación rápida
- Widget de progreso académico
- Usuarios sugeridos para conectar

### **Gestión de Perfil**

Los usuarios pueden:

- Actualizar información personal y académica
- Configurar privacidad del perfil
- Gestionar notificaciones
- Ver historial de puntos y logros

### **Grupos de Estudio**

Funcionalidades incluyen:

- Crear grupos por materia o tema
- Invitar estudiantes específicos
- Compartir notas y recursos
- Organizar discusiones temáticas

### **Sistema de Notas**

Los estudiantes pueden:

- Subir apuntes de clase
- Categorizar por materia y tipo
- Compartir con diferentes niveles de privacidad
- Descargar notas de otros estudiantes

## 🏆 Sistema de Gamificación

### **Puntos**

Los usuarios ganan puntos por:

- **Crear publicación**: 5 puntos
- **Recibir like**: 2 puntos
- **Comentar**: 3 puntos
- **Compartir nota**: 10 puntos
- **Hacer amistad**: 10 puntos
- **Unirse a grupo**: 5 puntos

### **Niveles**

La progresión de niveles se basa en puntos totales:

- **Nivel 1**: 0-100 puntos (Novato)
- **Nivel 2**: 101-250 puntos (Estudiante)
- **Nivel 3**: 251-500 puntos (Colaborador)
- **Nivel 4**: 501-1000 puntos (Mentor)
- **Nivel 5**: 1000+ puntos (Experto)

### **Logros**

Ejemplos de logros disponibles:

#### **Académicos** 🎓

- **Primera Nota**: Subir tu primera nota de estudio
- **Maestro del Apunte**: Tener 10 notas con más de 50 visualizaciones
- **Estudiante Destacado**: Obtener 100 likes en contenido académico

#### **Sociales** 🤝

- **Sociable**: Tener 25 amigos
- **Influencer**: Tener 100 seguidores
- **Comentarista Activo**: Realizar 100 comentarios

#### **Especiales** ⭐

- **Usuario Fundador**: Estar entre los primeros 100 usuarios
- **Madrugador**: Publicar contenido antes de las 7:00 AM
- **Nocturno**: Estar activo después de las 11:00 PM

## 🛠️ API y Endpoints

### **Endpoints Principales**

#### **Autenticación**

```
POST /api/auth/login/          # Iniciar sesión
POST /api/auth/logout/         # Cerrar sesión
POST /api/auth/register/       # Registrarse
```

#### **Usuarios**

```
GET  /api/users/               # Listar usuarios
GET  /api/users/{id}/          # Detalle de usuario
PUT  /api/users/{id}/          # Actualizar perfil
```

#### **Publicaciones**

```
GET  /api/posts/               # Feed de publicaciones
POST /api/posts/               # Crear publicación
GET  /api/posts/{id}/          # Detalle de publicación
PUT  /api/posts/{id}/          # Editar publicación
DEL  /api/posts/{id}/          # Eliminar publicación
```

#### **Notas**

```
GET  /api/notes/               # Listar notas
POST /api/notes/               # Crear nota
GET  /api/notes/{id}/          # Descargar nota
PUT  /api/notes/{id}/favorite/ # Marcar como favorita
```

#### **Grupos**

```
GET  /api/groups/              # Listar grupos
POST /api/groups/              # Crear grupo
POST /api/groups/{id}/join/    # Unirse a grupo
DEL  /api/groups/{id}/leave/   # Salir de grupo
```

### **Formato de Respuesta**

```json
{
  "status": "success",
  "data": {
    // Datos solicitados
  },
  "message": "Operación exitosa",
  "timestamp": "2025-09-30T12:00:00Z"
}
```

## 🤝 Contribución

### **Proceso de Contribución**

1. **Fork del repositorio**
2. **Crear rama para feature**

```bash
git checkout -b feature/nueva-funcionalidad
```

3. **Realizar cambios y commits**

```bash
git commit -m "feat: agregar nueva funcionalidad"
```

4. **Push a tu fork**

```bash
git push origin feature/nueva-funcionalidad
```

5. **Crear Pull Request**

### **Estándares de Código**

#### **Python**

- Seguir PEP 8
- Usar Black para formateo
- Máximo 88 caracteres por línea
- Docstrings para todas las funciones

#### **JavaScript**

- Usar ESLint
- Preferir const/let sobre var
- Comentarios para lógica compleja

#### **CSS**

- Usar Tailwind CSS classes
- Evitar CSS custom cuando sea posible
- Nomenclatura BEM para componentes custom

### **Testing**

```bash
# Ejecutar tests
python manage.py test

# Con cobertura
coverage run --source='.' manage.py test
coverage report
```

### **Commit Messages**

Usar formato conventional commits:

```
feat: nueva funcionalidad
fix: corrección de bug
docs: actualización de documentación
style: cambios de formato
refactor: refactorización de código
test: agregar o actualizar tests
```

## 📄 Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).

```
MIT License

Copyright (c) 2025 IFTS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Soporte y Contacto

- **Email**: soporte@ifts.edu.ar
- **Issues**: [GitHub Issues](https://github.com/tuusuario/social-network-ifts/issues)
- **Documentación**: [Wiki del Proyecto](https://github.com/tuusuario/social-network-ifts/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/tuusuario/social-network-ifts/discussions)

---

## 🙏 Agradecimientos

- **Equipo de Desarrollo IFTS**
- **Comunidad Django**
- **Tailwind CSS Team**
- **Todos los contribuidores** que han hecho posible este proyecto

---

<div align="center">

**Desarrollado con ❤️ para la comunidad educativa**

[⬆ Volver al inicio](#-red-social-institucional-ifts)

</div>
