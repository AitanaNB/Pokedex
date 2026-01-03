# Pokedex Web Application
#### Autores: Sofia, Diego, Ibai, Aitana, Ziyan, Adrian y Mateo

## Descripción
Aplicación web Pokedex desarrollada con Flask que permite a los usuarios:
- Iniciar sesión y registrarse
- Explorar la Pokedex completa con Pokemon obtenidos de la API de PokeAPI
- Visualizar información detallada de cada Pokemon

## Características
- **Autenticación de usuarios**: Sistema de login y registro
- **Integración con PokeAPI**: Los datos de Pokemon se obtienen dinámicamente de la API oficial
- **Interfaz moderna**: Diseño con tema morado consistente en todas las páginas
- **Base de datos SQLite**: Almacenamiento local de Pokemon para acceso rápido

## Instalación

1. Clonar el proyecto en tu entorno local:
```bash
git clone https://github.com/AitanaNB/Pokedex.git
cd Pokedex
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar las dependencias:
```bash
pip install -r req.txt
```

4. Inicializar la base de datos (opcional, se hace automáticamente al iniciar la app):
```bash
python dbManager.py
```

5. Ejecutar la aplicación:
```bash
python main.py
```

6. Abrir el navegador en `http://127.0.0.1:5000`

## Credenciales de prueba
- **Usuario**: ash
- **Contraseña**: pikachu

## Estructura del proyecto
```
Pokedex/
├── main.py              # Aplicación principal Flask
├── dbManager.py         # Script de inicialización de base de datos
├── pokemon.db           # Base de datos SQLite
├── req.txt              # Dependencias del proyecto
├── templates/           # Plantillas HTML
│   ├── login.html
│   ├── register.html
│   └── index.html
├── static/              # Archivos estáticos
│   ├── style.css
│   └── images/
├── Documentación/       # Documentación del proyecto
└── README.md
```

## Tecnologías utilizadas
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Base de datos**: SQLite
- **API externa**: PokeAPI (https://pokeapi.co/)

## Nota de seguridad
⚠️ Esta aplicación es un proyecto educativo. NO utilices contraseñas reales o personales.
