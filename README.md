# 🔴 Pokédex - Proyecto ADSI

**Autores:** Sofia, Diego, Ibai, Aitana, Ziyan, Adrian y Mateo  
**Tecnologías:** Flask 3.1.2, SQLite3, PokeAPI, Python 3.13, bcrypt  
**Estado:** ✅ ChatBot completamente operativo (v1.0)

Aplicación web de Pokédex con arquitectura MVC, autenticación con bcrypt, gestión de equipos, búsqueda por tipos, integración con PokeAPI y ChatBot con 3 comandos funcionales.

---

## 🚀 Inicio Rápido

### Requisitos
- Python 3.13+
- pip

### Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/AitanaNB/Pokedex.git
cd Pokedex

# 2. Instalar dependencias
pip install -r req.txt

# 3. Iniciar servidor (auto-crea DB con 151 Pokémon)
python app.py
```

Acceder a: **http://localhost:5000**

### Credenciales por defecto
- **Username:** admin
- **Password:** admin123
- **Rol:** Administrador

---

## 📋 Funcionalidades Completadas ✅

### Autenticación
- ✅ Registro con validación de email
- ✅ Login/Logout con bcrypt seguro
- ✅ Sistema de aprobación de usuarios por admin
- ✅ Roles: Usuario normal y Administrador
- ✅ Decoradores para proteger rutas

### Pokédex
- ✅ Catálogo de 151 Pokémon Gen 1
- ✅ Búsqueda por nombre (real-time)
- ✅ Filtro por tipos (17 tipos)
- ✅ Imágenes PNG desde PokeAPI
- ✅ Estadísticas detalladas por Pokémon

### ChatBot (3 Comandos Funcionales)
- ✅ **/stats <pokémon>** - Muestra estadísticas completas
- ✅ **/evolucion <pokémon>** - Cadena de evolución desde PokeAPI
- ✅ **/tipo <tipo>** - Lista todos los Pokémon de un tipo
- ✅ Interface con selector visual de Pokémon
- ✅ Resultados formateados y claros

### Equipos
- ✅ Crear equipos (máx 10 por usuario)
- ✅ Agregar Pokémon (máx 6 por equipo)
- ✅ Gestión completa (ver/eliminar)

### Base de Datos
- ✅ 13 tablas SQLite con relaciones N:M
- ✅ 151 Pokémon precargados
- ✅ 218 asociaciones tipo-especie
- ✅ Integridad referencial con FK

### Administración
- ✅ Panel de gestión de usuarios
- ✅ Aprobación de cuentas
- ✅ Decoradores para protección de rutas

---

## 🗄️ Base de Datos

**Estructura (13 tablas):**
- `usuario` - Usuarios con roles y aprobación
- `tipo` - Tipos de Pokémon (17 tipos Gen 1)
- `especie` - Especies con estadísticas (151 Pokémon)
- `especie_tipo` - Relación N:M (218 asociaciones)
- `ataque` - Movimientos/ataques
- `equipo` - Equipos personalizados
- `pokemon` - Instancias de Pokémon capturados
- `equipo_pokemon` - Relación N:M
- `especie_ataque` - Relación N:M
- `notificaciones` - Sistema de alertas
- `seguidores` - Sistema de amigos
- `pokemon_ataque` - Relación N:M
- `afectado` - Efectividad de tipos

---

## 📂 Estructura del Proyecto

```
Pokedex/
├── app/
│   ├── __init__.py
│   ├── models/                 # Modelos de datos
│   ├── repositories/           # Acceso a BD
│   │   └── pokemon_repository.py
│   ├── services/               # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── pokedex_service.py
│   │   ├── chatbot_service.py
│   │   └── pokeapi_service.py
│   ├── controllers/            # Rutas Flask
│   │   ├── auth_controller.py
│   │   ├── pokedex_controller.py
│   │   ├── chatbot_controller.py
│   │   ├── admin_controller.py
│   │   └── ...más 3 blueprints
│   ├── utils/
│   │   ├── security.py         # Bcrypt
│   │   └── decorators.py       # @login_required, etc
│
├── config/
│   ├── database.py             # Conexiones SQLite
│   └── __init__.py
│
├── templates/
│   ├── base.html
│   ├── login.html & register.html
│   ├── dashboard.html          # Panel principal
│   ├── pokedex/                # Pokédex páginas
│   ├── chatbot/                # ChatBot interfaz
│   ├── admin/                  # Admin panel
│   ├── changelog/              # Actividades
│   ├── telegram/               # Compartir
│   └── pokedle/                # Juego
│
├── static/
│   ├── style.css               # Gradiente morado unificado
│   └── images/
│
├── data/
│   └── pokemon.db              # SQLite (151 Pokémon + 13 tablas)
│
├── app.py                      # Punto de entrada
├── req.txt                     # Dependencias
├── .gitignore
└── README.md
```

---

## 🎨 Diseño Visual

**Tema:** Gradiente púrpura (#667eea → #764ba2)  
**Responsive:** Mobile first, compatible con todos los dispositivos  
**UI:** Cards con sombras, botones con hover, animaciones suaves

---

## 🔧 Configuración

| Parámetro | Valor |
|-----------|-------|
| **Puerto** | 5000 |
| **BD** | data/pokemon.db (SQLite3) |
| **Debug** | Activado en desarrollo |
| **Hot-reload** | Enabled |

---

## 📋 Pendientes por Implementar

### Por Equipo
- **Sofia:** Mejoras UI en Pokédex (filtros avanzados)
- **Diego:** Selector de equipos en ChatBot
- **Ibai:** Integración Telegram Bot
- **Aitana:** Juego Pokedle (mini-juego diario)
- **Ziyan:** Panel Admin (aprobar usuarios)
- **Adrian:** Changelog de actividades
- **Mateo:** ✅ ChatBot v1.0 (COMPLETADO)

---

## 🚀 Próximos Pasos

1. Integrar Telegram Bot para compartir equipos
2. Implementar Pokedle (guessing game)
3. Mejorar UI del admin panel
4. Agregar más Pokémon (Gen 2+)
5. Implementar combates simples

---

## 📝 Notas Técnicas

### Para regenerar la BD
```bash
# Eliminar DB actual
rm data/pokemon.db

# Iniciar app (auto-crea con los 151 Pokémon)
python app.py
```

### Problemas Comunes Resueltos

**Error:** `idEspecie` column not found  
**Solución:** ✅ Corregido - Usar `nombreEspecie` como PRIMARY KEY

**Error:** Método fuera de clase  
**Solución:** ✅ Corregido - `get_all_pokemon()` dentro de PokedexService

**Error:** `pb` (pokebase) no definido  
**Solución:** ✅ Reemplazado con `requests` library

---

## 👥 Créditos

**Equipo ADSI 2026:**
- Sofia, Diego, Ibai, Aitana, Ziyan, Adrian, Mateo

**Tecnologías:** Flask 3.1.2, SQLite3, Python 3.13, bcrypt, PokeAPI

---

**Estado:** ✅ Funcional - Última actualización: Enero 2026
