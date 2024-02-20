import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect('mi_base_de_datos.db')

# Crear un cursor
cursor = conn.cursor()

# Crear una tabla llamada "usuarios"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        email TEXT
    )
''')

# Insertar datos en la tabla "usuarios"
cursor.execute('INSERT INTO usuarios (pepe, email) VALUES (?, ?)', ('Hola', ''))

# Realizar una consulta para obtener todos los usuarios
cursor.execute('SELECT * FROM usuarios')
usuarios = cursor.fetchall()

# Mostrar los usuarios
for usuario in usuarios:
    print(usuario)

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()
