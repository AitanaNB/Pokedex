# 🔴 Pokédex - Proyecto ADSI

**Autores:** Sofia, Diego, Ibai, Aitana, Ziyan, Adrian y Mateo  
**Tecnologías:** Flask 3.1.2, SQLite3, PokeAPI, Python 3.13, bcrypt  

Aplicación web de Pokédex con arquitectura MVC
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

# 2. Iniciar venv
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r req.txt

# 4. Iniciar servidor (auto-crea DB con 151 Pokémon)
python run.py
```

Acceder a: **http://localhost:5000**

### Credenciales por defecto
- **Username:** admin
- **Password:** admin123
- **Rol:** Administrador


- **Username:** user1
- **Password:** 123456
- **Rol:** Usuario Normal
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
├── db.sqlite3
├── README.md
├── req.txt
├── run.py
├── VERIFICACION_MVC_Y_ARQUITECTURA.md
├── app/
│   ├── __init__.py
│   ├── chatbot/
│   │   ├── __init__.py
│   │   └── chatbot_controller.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── admin_controller.py
│   │   ├── auth_controller.py
│   │   ├── changelog_controller.py
│   │   ├── pokedex_controller.py
│   │   ├── Pokedex.py
+│   │   ├── pokedle_controller.py
│   │   ├── telegram_controller.py
│   │   └── TelegramAPI.py
│   ├── models/
│   │   └── __init__.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── equipo_repository.py
│   │   ├── GestorEquipo.py
│   │   ├── GestorUsuario.py
│   │   ├── pokemon_repository.py
│   │   └── SGBD.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chatbot_service.py
│   │   ├── pokeapi_service.py
│   │   └── pokedex_service.py
│   └── utils/
│       ├── __init__.py
	├── decorators.py
	└── security.py
│
├── config/
│   ├── __init__.py
│   └── database.py
├── data/
│   └── pokemon.sqbpro
├── Documentación/
│   ├── BD.drawio
│   └── log de cambios
├── static/
│   ├── capture.js
│   ├── dashboard.css
│   ├── perfil.css
│   ├── style.css
│   └── images/
├── templates/
│   ├── dashboard.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── admin/
│   │   └── usuarios.html
│   ├── changelog/
│   │   └── index.html
│   ├── chatbot/
│   │   └── index.html
│   ├── pokedex/
│   │   ├── capture.html
│   │   ├── equipos.html
│   │   ├── especie_detail.html
│   │   └── index.html
│   ├── pokedle/
│   │   └── game.html
│   ├── telegram/
│   │   └── share.html
│   └── user/
│       └── perfil.html
├── tests/
│   ├── __init__.py
│   ├── func1GestionUsuarios.py
│   ├── func2CrearEquipos.py
│   ├── func3ChangeLog.py
│   ├── funciones_TelegramAPI.py
│   └── test_chatbot.py
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
- **Sofia:** Pokedle
- **Diego:** Bot de Telegram
- **Ibai:** Lista Pokemon y busquedas con filtros
- **Aitana:** Changelog
- **Ziyan:** Gestion usuarios
- **Adrian:** Crear equipos
- **Mateo:** ChatBot

---

## 📝 Notas Técnicas

### Para regenerar la BD
```bash
# Eliminar DB actual
rm data/pokemon.db

# Iniciar app (auto-crea con los 151 Pokémon)
python run.py
```

## 👥 Créditos

**Equipo ADSI 2026:**
- Sofia, Diego, Ibai, Aitana, Ziyan, Adrian, Mateo

**Tecnologías:** Flask 3.1.2, SQLite3, Python 3.13, bcrypt, PokeAPI

---

**Estado:** ✅ Funcional - Última actualización: Enero 2026
