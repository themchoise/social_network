# Social Network API Documentation

## Base URL

```
http://localhost:8000/api
```

## Documentación Interactiva

- **Swagger UI**: http://localhost:8000/api/docs
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## Autenticación

### JWT (JSON Web Token)

#### Obtener Token

```http
POST /api/token/pair
Content-Type: application/json

{
  "username": "usuario",
  "password": "contraseña"
}
```

**Respuesta exitosa (200):**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Usar Token en Requests

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Renovar Token

```http
POST /api/token/refresh
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Verificar Token

```http
POST /api/token/verify
Content-Type: application/json

{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Endpoints

### Users

#### Listar Usuarios (paginado)

```http
GET /api/users/?page=1&size=20&search=juan
```

**Parámetros de consulta:**

- `page` (int, default: 1): Número de página
- `size` (int, default: 20, max: 100): Elementos por página
- `search` (string, opcional): Buscar por username

**Respuesta (200):**

```json
{
  "total": 150,
  "page": 1,
  "size": 20,
  "items": [
    {
      "id": 1,
      "username": "juan_perez",
      "email": "juan@example.com",
      "first_name": "Juan",
      "last_name": "Pérez",
      "bio": "Estudiante de informática",
      "total_points": 1250,
      "level": 2,
      "is_verified": true,
      "achievements": [
        {
          "id": 1,
          "name": "First Post",
          "points": 10
        }
      ]
    }
  ]
}
```

#### Obtener Usuario

```http
GET /api/users/{user_id}
```

**Respuesta (200):** Objeto `UserOut` con achievements

**Respuesta (404):** Usuario no encontrado

#### Crear Usuario

```http
POST /api/users/
Content-Type: application/json

{
  "username": "nuevo_usuario",
  "email": "nuevo@example.com",
  "password": "contraseña_segura",
  "first_name": "Nombre",
  "last_name": "Apellido"
}
```

**Respuesta (200):** Objeto `UserOut` creado

#### Actualizar Usuario (requiere JWT)

```http
PUT /api/users/{user_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "email": "nuevo_email@example.com",
  "first_name": "Nuevo Nombre",
  "bio": "Nueva biografía"
}
```

**Restricción:** Solo el propio usuario puede actualizarse

**Respuesta (200):** Objeto `UserOut` actualizado

**Respuesta (401):** No autenticado

**Respuesta (404):** No autorizado o no encontrado

#### Eliminar Usuario (requiere JWT)

```http
DELETE /api/users/{user_id}
Authorization: Bearer {token}
```

**Restricción:** Solo el propio usuario puede eliminarse

**Respuesta (200):**

```json
{
  "success": true
}
```

---

### Posts

#### Listar Posts (paginado, con búsqueda y ordenamiento)

```http
GET /api/posts/?page=1&size=20&search=django&ordering=-views_count
```

**Parámetros:**

- `page` (int): Número de página
- `size` (int): Elementos por página
- `search` (string): Buscar en contenido
- `ordering` (string): `created_at`, `-created_at`, `views_count`, `-views_count`

**Respuesta (200):**

```json
{
  "total": 350,
  "page": 1,
  "size": 20,
  "items": [
    {
      "id": 42,
      "author_id": 5,
      "author_username": "maria_dev",
      "author": {
        "id": 5,
        "username": "maria_dev",
        "level": 3,
        "total_points": 2400,
        "is_verified": true
      },
      "content": "Aprendiendo Django Ninja para crear APIs RESTful",
      "views_count": 125,
      "like_count": 18,
      "comment_count": 7,
      "created_at": "2025-11-30T14:23:15.123456"
    }
  ]
}
```

#### Obtener Post

```http
GET /api/posts/{post_id}
```

**Respuesta (200):** Objeto `PostOut` con datos anidados del autor

#### Crear Post (requiere JWT)

```http
POST /api/posts/
Authorization: Bearer {token}
Content-Type: application/json

{
  "content": "Mi primer post desde la API"
}
```

**Respuesta (200):** Objeto `PostOut` creado

#### Actualizar Post (requiere JWT)

```http
PUT /api/posts/{post_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "content": "Contenido actualizado"
}
```

**Restricción:** Solo el autor puede editar

**Respuesta (200):** Objeto `PostOut` actualizado

#### Eliminar Post (requiere JWT)

```http
DELETE /api/posts/{post_id}
Authorization: Bearer {token}
```

**Restricción:** Solo el autor puede eliminar

**Respuesta (200):**

```json
{
  "success": true
}
```

#### Toggle Like en Post (requiere JWT)

```http
POST /api/posts/{post_id}/like
Authorization: Bearer {token}
```

**Respuesta (200):**

```json
{
  "success": true,
  "liked": true,
  "like_count": 19
}
```

---

### Comments

#### Listar Comentarios (paginado, filtro por post)

```http
GET /api/comments/?page=1&size=20&post_id=42
```

**Parámetros:**

- `page` (int): Número de página
- `size` (int): Elementos por página
- `post_id` (int, opcional): Filtrar por post

**Respuesta (200):**

```json
{
  "total": 45,
  "page": 1,
  "size": 20,
  "items": [
    {
      "id": 15,
      "author_id": 8,
      "author_username": "carlos_2025",
      "post_id": 42,
      "content": "Excelente explicación, gracias!",
      "parent_id": null,
      "like_count": 3,
      "is_edited": false,
      "created_at": "2025-11-30T15:10:30.123456"
    }
  ]
}
```

#### Obtener Comentario

```http
GET /api/comments/{comment_id}
```

#### Crear Comentario (requiere JWT)

```http
POST /api/comments/
Authorization: Bearer {token}
Content-Type: application/json

{
  "post_id": 42,
  "content": "Muy útil este tutorial",
  "parent_id": null
}
```

**Para responder a otro comentario:** usa `parent_id` con el ID del comentario padre

#### Actualizar Comentario (requiere JWT)

```http
PUT /api/comments/{comment_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "content": "Contenido corregido"
}
```

**Restricción:** Solo el autor puede editar

**Nota:** Se marca automáticamente como `is_edited: true`

#### Eliminar Comentario (requiere JWT)

```http
DELETE /api/comments/{comment_id}
Authorization: Bearer {token}
```

---

### Notes

#### Listar Notas (paginado, con filtros)

```http
GET /api/notes/?page=1&size=20&author_id=5&subject_id=3&search=algoritmos
```

**Parámetros:**

- `page` (int): Número de página
- `size` (int): Elementos por página
- `author_id` (int, opcional): Filtrar por autor
- `subject_id` (int, opcional): Filtrar por materia
- `search` (string, opcional): Buscar en título

**Respuesta (200):**

```json
{
  "total": 28,
  "page": 1,
  "size": 20,
  "items": [
    {
      "id": 10,
      "title": "Algoritmos de Ordenamiento",
      "content": "Resumen de los principales algoritmos...",
      "author_id": 5,
      "author_username": "maria_dev",
      "subject_id": 3,
      "note_type": "summary",
      "privacy_level": "public",
      "views_count": 89,
      "downloads_count": 12,
      "is_featured": false,
      "created_at": "2025-11-28T10:15:00.123456"
    }
  ]
}
```

#### Obtener Nota

```http
GET /api/notes/{note_id}
```

#### Crear Nota (requiere JWT)

```http
POST /api/notes/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Introducción a Python",
  "content": "Contenido de la nota...",
  "subject_id": 5,
  "note_type": "class",
  "privacy_level": "public",
  "tags": "python, programación, básico"
}
```

**note_type:** `class`, `summary`, `exercise`, `project`, `exam`, `reference`

**privacy_level:** `public`, `friends`, `private`

#### Actualizar Nota (requiere JWT)

```http
PUT /api/notes/{note_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Nuevo título",
  "content": "Contenido actualizado"
}
```

#### Eliminar Nota (requiere JWT)

```http
DELETE /api/notes/{note_id}
Authorization: Bearer {token}
```

---

### Gamification

#### Estadísticas de Usuario

```http
GET /api/users/{user_id}/stats
```

**Respuesta (200):**

```json
{
  "user_id": 5,
  "username": "maria_dev",
  "total_points": 2400,
  "level": 3,
  "experience_points": 2400,
  "achievements_count": 8,
  "posts_count": 34,
  "comments_count": 127
}
```

#### Logros de Usuario

```http
GET /api/users/{user_id}/achievements
```

**Respuesta (200):**

```json
[
  {
    "id": 1,
    "name": "First Post",
    "description": "Crear tu primer post",
    "points": 10,
    "earned_at": "2025-11-15T08:30:00.123456"
  },
  {
    "id": 5,
    "name": "Helpful",
    "description": "Recibir 50 likes",
    "points": 50,
    "earned_at": "2025-11-28T14:20:00.123456"
  }
]
```

#### Tabla de Clasificación

```http
GET /api/users/leaderboard?limit=50
```

**Parámetros:**

- `limit` (int, default: 50, max: 100): Número de usuarios

**Respuesta (200):**

```json
{
  "entries": [
    {
      "rank": 1,
      "user_id": 12,
      "username": "super_estudiante",
      "total_points": 8500,
      "level": 9,
      "is_verified": true
    },
    {
      "rank": 2,
      "user_id": 5,
      "username": "maria_dev",
      "total_points": 2400,
      "level": 3,
      "is_verified": true
    }
  ]
}
```

#### Historial de Puntos

```http
GET /api/users/{user_id}/points-history?limit=50
```

**Respuesta (200):**

```json
[
  {
    "points": 10,
    "source": "post",
    "description": "Created a new post",
    "created_at": "2025-11-30T14:00:00.123456"
  },
  {
    "points": 5,
    "source": "comment",
    "description": "Created a comment",
    "created_at": "2025-11-30T13:45:00.123456"
  }
]
```

#### Otorgar Puntos (requiere JWT + staff)

```http
POST /api/users/award-points
Authorization: Bearer {token}
Content-Type: application/json

{
  "user_id": 5,
  "points": 100,
  "source": "admin_bonus",
  "description": "Reconocimiento por contribución destacada"
}
```

**Restricción:** Solo usuarios staff/admin

**Respuesta (200):**

```json
{
  "success": true,
  "new_total": 2500,
  "new_level": 3
}
```

**Respuesta (401):** No autorizado (no staff)

---

## Códigos de Respuesta HTTP

- **200 OK**: Solicitud exitosa
- **201 Created**: Recurso creado exitosamente
- **400 Bad Request**: Datos de entrada inválidos
- **401 Unauthorized**: No autenticado o token inválido
- **403 Forbidden**: Autenticado pero sin permisos
- **404 Not Found**: Recurso no encontrado
- **500 Internal Server Error**: Error del servidor

---

## Ejemplos de Uso

### Flujo completo: Crear usuario, login y crear post

```bash
# 1. Crear usuario
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "email": "test@example.com",
    "password": "secure_password123"
  }'

# 2. Obtener token JWT
curl -X POST http://localhost:8000/api/token/pair \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "password": "secure_password123"
  }'

# Respuesta:
# {
#   "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
# }

# 3. Crear post con el token
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -d '{
    "content": "Mi primer post desde la API!"
  }'

# 4. Listar posts con búsqueda
curl "http://localhost:8000/api/posts/?search=API&page=1&size=10"

# 5. Dar like a un post
curl -X POST http://localhost:8000/api/posts/1/like \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## Paginación

Todos los endpoints de listado soportan paginación:

```http
GET /api/posts/?page=2&size=25
```

**Respuesta:**

```json
{
  "total": 350,
  "page": 2,
  "size": 25,
  "items": [...]
}
```

**Calcular páginas totales:**

```javascript
const totalPages = Math.ceil(response.total / response.size);
```

---

## Filtros y Ordenamiento

### Posts

- **search**: Buscar en contenido
- **ordering**: `created_at`, `-created_at`, `views_count`, `-views_count`

### Comments

- **post_id**: Filtrar por post específico

### Notes

- **author_id**: Filtrar por autor
- **subject_id**: Filtrar por materia
- **search**: Buscar en título

### Users

- **search**: Buscar por username

---

## Schemas Anidados

Los endpoints incluyen relaciones anidadas para reducir requests:

**PostOut incluye:**

- `author`: Objeto completo con `username`, `level`, `total_points`, `is_verified`
- `comment_count`: Total de comentarios
- `like_count`: Total de likes

**UserOut incluye:**

- `achievements`: Lista de logros (máximo 5 más recientes)

---

## Notas Técnicas

- **Rate Limiting**: No implementado (considerar para producción)
- **CORS**: Configurar en settings para frontend separado
- **Autenticación Session**: También disponible para navegador
- **Timezone**: Todas las fechas en UTC (ISO 8601)
- **Validaciones**: Pydantic schemas validan datos automáticamente
- **N+1 Queries**: Optimizado con `select_related` y `prefetch_related`

---

## Testing

Ejecutar tests de la API:

```bash
python manage.py test apps.post.tests apps.user.tests apps.comment.tests
```

---

## Contacto y Soporte

- **Documentación Interactiva**: http://localhost:8000/api/docs
- **Repositorio**: https://github.com/themchoise/social_network
