# Traemos las herramientas FastAPI, BaseModel y sqlite3 a nuestro archivo
import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

# Declaramos el modelo de datos como una clase que hereda de BaseModel
class Item(BaseModel):
	name: str				# Dato obligatorio

# Creamos la aplicación y la guardamos en una variable llamada app. Es el camarero del restaurante, sin saber que pedidos atender
app = FastAPI()

# Abrir conexión; con row_factory las filas se pueden convertir a diccionario
def get_db():
	con = sqlite3.connect("habits.db")
	con.row_factory = sqlite3.Row		# Filas accesibles por nombre de columna
	return (con)

# -- Una sola vez al arrancar: Crear la tabla (el id se genera solo) --
def create_table():
	# Abrimos conexión y convertimos tuplas a diccionarios
	con = get_db()
	# Creamos la tabla
	con.execute("""CREATE TABLE IF NOT EXISTS habits (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	done INTEGER DEFAULT 0
	)""")
	# Hacemos commit a los cambios
	con.commit()
	# Cerramos la base de datos
	con.close()

# Llamamos a create_table antes de nada para crear la tabla
create_table()

# Le dice al camarero "cuando alguien haga un POST a la direccíon /habits (añadir un hábito) ejecuta la función de debajo"
@app.post("/habits")
async def add_habit(item: Item):
	# Abrimos conexión y convertimos tuplas a diccionarios
	con = get_db()
	# Ejecutamos un INSERT
	cur = con.execute("INSERT INTO habits (name) VALUES (?)", (item.name,))	# Recibimos el habito en item y su nombre en item.name
	# Hacemos commit a los cambios
	con.commit()
	# Recogemos el id que la base de datos acaba de asignar
	habit_id = cur.lastrowid
	# Cerramos la base de datos
	con.close()
	# Devolvemos el hábito con su id y su name
	return ({"id": habit_id, "name": item.name, "done": 0})

# Cada vez que alguien haga un GET a la dirección /habits se devolverá la lista con todos los hábitos
@app.get("/habits")
async def show_habits():
	# Abrimos conexión y convertimos tuplas a diccionarios
	con = get_db()
	# Ejecutamos un SELECT - 1. Leemos todo
	filas = con.execute("SELECT * FROM habits").fetchall()
	# 2. Convertimos las filas en diccionarios
	lista = [dict(fila) for fila in filas]
	# Cerramos la base de datos
	con.close()
	# Devolvemos la lista
	return (lista)

# Cada vez que alguien haga un DELETE a la dirección de un habito concreto (habits/id) se ejecuta la función delete_habit
@app.delete("/habits/{id}")
async def delete_habit(id : int):
	# Abrimos conexión y convertimos tuplas a diccionarios
	con = get_db()
	# Ejecutamos un DELETE
	cur = con.execute("DELETE FROM habits WHERE id = ?", (id,))
	# Hacemos commit a los cambios
	con.commit()
	# Cerramos la Base de Datos
	con.close()
	# Devolvemos el mensaje de éxito
	return ("Hábito eliminado correctamente")

# Montamos la aplicación index.html
# "app.mount(...)" - todo lo que llegue a un path concreto se entrega a una cosa externa para que lo maneje
#"/app" - Cualquier dirección que empiece por /app irá a esa otra cosa
# StaticFiles(...) Es la otra cosa que se monta: una carpeta de FastAPI que entrega archivos de una carpeta tal cual sin ejecutarlos
	# directory="static" - la carpeta de la que sirve los archivos.
	# html=True - cuando alguien pide una carpeta y no un archivo concreto (como /app/), entrega el index.html de dentro. Sin esto habría que escribir /app/index.html
# name="app" Es un nombre interno para esta "pieza montada". De momento solo lo usa Fast API, se puede ignorar.
# -- EN RESUMEN -- «todo lo que llegue a /app, atiéndelo sirviendo los archivos de la carpeta static, y si piden la carpeta en sí, entrega su index.html»
app.mount("/app", StaticFiles(directory="static", html=True), name="app")