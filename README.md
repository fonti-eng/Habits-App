# Habits-App

Aplicación web mínima para registrar hábitos: una página donde escribes un hábito, lo añades y lo ves en una lista que se guarda en una base de datos.

## Qué hace

- Permite añadir hábitos desde una página (cuadro de texto y botón «Añadir»).
- Muestra la lista de hábitos guardados.
- Los hábitos se guardan en una base de datos, así que siguen ahí al recargar la página o reiniciar el servidor.
- La página no envía nombres vacíos, recorta los espacios sobrantes al principio y al final, y admite tildes y emojis.

## Cómo funciona

Tiene tres piezas, cada una en un archivo distinto:

```
Página (static/index.html)  ──fetch──►  API (main.py, FastAPI)  ──SQL──►  Base de datos (habits.db, SQLite)
```

## Qué no hace todavía

- No se pueden borrar hábitos desde la página. Se hace en `http://127.0.0.1:8000/docs`, con la operación `DELETE /habits/{id}` y el `id` del hábito.
- No se pueden editar ni marcar como completados.
- La API acepta nombres vacíos si se le envían directamente (por ejemplo, desde `/docs`). Solo la página los filtra.

## Instalación

Requisitos: Python 3.10 o superior, con `venv` y `pip` disponibles. Los comandos son para Linux, macOS o WSL.

1. Obtén el proyecto y entra en su carpeta: `cd habits-app`
2. Crea el entorno virtual (solo la primera vez): `python3 -m venv .venv`
3. Actívalo: `source .venv/bin/activate`
   (en Windows PowerShell: `.\.venv\Scripts\Activate.ps1`). Deberías ver `(.venv)` al principio del prompt.
4. Instala las dependencias: `python -m pip install -r requirements.txt`
5. Arranca el servidor: `uvicorn main:app --reload`
6. Abre en el navegador:
   - La aplicación: `http://127.0.0.1:8000/app/`
   - La documentación de la API (donde se puede borrar): `http://127.0.0.1:8000/docs`

Para parar el servidor, pulsa `Ctrl+C`. Las veces siguientes solo hacen falta los pasos 3 y 5.

## Contenido del proyecto

- `main.py`: el servidor (la API). Define el modelo de datos, crea la tabla de la base de datos al arrancar, contiene las tres rutas (`POST /habits` para crear, `GET /habits` para listar y `DELETE /habits/{id}` para borrar) y sirve la carpeta `static` en la dirección `/app`.
- `static/index.html`: la página que ves en el navegador. Tiene el HTML (campo, botón y lista) y el JavaScript que pide la lista a la API y envía los hábitos nuevos a la misma.
- `habits.db`: la base de datos SQLite, con la tabla `habits` (columnas `id`, `name` y `done`). Se crea sola la primera vez que arrancas el servidor, así que no hace falta crearla a mano, y no se sube a Git.
- `requirements.txt`: la lista de paquetes de Python con sus versiones exactas (FastAPI, uvicorn y sus dependencias). `sqlite3` no aparece porque viene incluido en Python.
- `.venv/`: el entorno virtual, una copia aislada de Python con los paquetes del proyecto. No se sube a Git: se recrea con los pasos 2 a 4.