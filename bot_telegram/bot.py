import telebot
import sqlite3
from config import token


bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def cmd_start(message):
    
    bot.send_chat_action(message.chat.id,"typing")
    bot.reply_to(message, "Hola, soy ecaibot, mi trabajo aquí es ayudarte con lo que tengas que hacer, si quieres saber en lo que te puedo ayudar, escribe /help.")
    print(message.chat.id)

#↓↓↓↓↓↓↓↓↓↓↓↓↓↓"Lista comandos"↓↓↓↓↓↓↓↓↓↓↓↓↓↓#

@bot.message_handler(commands=["help"])
def cmd_start(message):
    
    bot.send_chat_action(message.chat.id,"typing")
    bot.reply_to(message, "/start, /help, /registrarse,/web,/donar")
    print(message.chat.id)

#↓↓↓↓↓↓↓↓↓↓↓↓↓↓"Comandos utiles"↓↓↓↓↓↓↓↓↓↓↓↓↓↓#

@bot.message_handler(commands=["registrarse"])
def cmd_start(message):
    
    bot.send_chat_action(message.chat.id,"typing")
    bot.reply_to(message, "Para registrarte dirigete aqui→→→→ https://graduacionpoblenou.000webhostapp.com/ ")
    print(message.chat.id)

#↓↓↓↓↓↓↓↓↓↓↓↓↓↓

@bot.message_handler(commands=["web"])
def cmd_start(message):
    
    bot.send_chat_action(message.chat.id,"typing")
    bot.reply_to(message, "Nuestra web es esta→→→→ https://graduacionpoblenou.000webhostapp.com/ ")
    print(message.chat.id)

#↓↓↓↓↓↓↓↓↓↓↓↓↓↓

@bot.message_handler(commands=["donar"])
def cmd_start(message):
    
    bot.send_chat_action(message.chat.id,"typing")
    bot.reply_to(message, "Muchas gracias!! Puedes donar aqui→→→→https://graduacionpoblenoudonativos.000webhostapp.com/")
    print(message.chat.id)

#↓↓↓↓↓↓↓↓↓↓↓↓↓↓

@bot.message_handler(commands=["reservar"])
def cmd_start(message):
    
    bot.send_chat_action(message.chat.id,"typing")
    bot.reservar_producto()
    print(message.chat.id)

    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓

@bot.message_handler(commands=[""])
def cmd_start(message):
    
    bot.send_chat_action(message.chat.id,"typing")
    bot.reply_to(message, "")
    print(message.chat.id)

#↓↓↓↓↓↓↓↓↓↓↓↓↓↓"txt"↓↓↓↓↓↓↓↓↓↓↓↓↓↓#
@bot.message_handler(content_types=["text"])
def bot_mensajes_texto(message):
    if message.text.startswith("/") and (message, "/start, /help, /registrarse,/web,/donar,/reservar"):
        bot.send_chat_action(message.chat.id,"typing")
        bot.send_message(message.chat.id, "Comando no existente, lo siento, tienes que comunicarte con nuestros comandos, puedes utilizar /help para ver que comandos puedes utilizar ")
    else:    
        bot.send_chat_action(message.chat.id,"typing")
        bot.reply_to(message, "Lo siento, tienes que comunicarte con comados, puedes utilizar /help para ver que comandos puedes utilizar")

#↓↓↓↓↓↓↓↓↓↓↓↓↓↓"Bucle infinito"↓↓↓↓↓↓↓↓↓↓↓↓↓↓#

if __name__ == '__main__':
    print('INICIADO')
    bot.infinity_polling()



conn = sqlite3.connect('productos_db.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        precio REAL,
        reservado INTEGER,
        contacto TEXT
    )
''')

productos = [
    ('Cuadro_1', 20.0, 0, '123-456-789'),
    ('Cuadro_2', 30.0, 1, '987-654-321'),
    ('Cuadro_3', 25.0, 0, '456-789-012')
]

cursor.executemany('INSERT INTO productos (nombre, precio, reservado, contacto) VALUES (?, ?, ?, ?)', productos)
conn.commit()

@bot.message_handler(commands=["start"])
def cmd_start(message):
    
    bot.send_chat_action(message.chat.id,"typing")
    bot.reply_to(message, "Hola, soy ecaibot, soy un bot hecho para ayudarte a vender o comprar productos de nuestra tienda del metaverso, si lo que quieres es comprar productos de nuestra tienda, tendras que decirme el nombre del producto, para saber los nombres, podras verlos en nuestra pagina web, pero si quieres una experiencia mas inmersiva,te recomiendo entrar en nuestra sala virtual de la plataforma vrchat y entrar en la sala ''Nombre de la sala'', ahi vereas una exposicion de arte digital y los nombres de cada cuadro.")
    print(message.chat.id)

@bot.message_handler(func=lambda message: True)
def consultar_producto(message):
    conn = sqlite3.connect('productos_db.db')
    cursor = conn.cursor()

    producto_nombre = message.text

    cursor.execute('SELECT nombre, precio, reservado, contacto FROM productos WHERE nombre LIKE ?', (f'%{producto_nombre}%',))
    producto = cursor.fetchone()

    if producto:
        nombre, precio, reservado, contacto = producto
        if reservado == 0:
            estado_reserva = "Disponible"
        else:
            estado_reserva = "Reservado"
        response = f"Nombre: {nombre}\nPrecio: {precio}\nEstado: {estado_reserva}\nContacto: {contacto}\n\n"\
                   f"Puedes usar /reservar_{nombre} para reservar este producto."
    else:
        response = "Producto no encontrado."

    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(message, response)

    conn.close()


@bot.message_handler(commands=['reservar'])
def reservar_producto(message):
    producto_nombre = message.text.split('_')[-1]  
    conn = sqlite3.connect('productos_db.db')
    cursor = conn.cursor()

    cursor.execute('SELECT reservado FROM productos WHERE nombre LIKE ?', (f'%{producto_nombre}%',))
    producto = cursor.fetchone()

    if producto:
        reservado = producto[0]
        if reservado == 0:
            cursor.execute('UPDATE productos SET reservado = 1 WHERE nombre LIKE ?', (f'%{producto_nombre}%',))
            conn.commit()
            bot.send_chat_action(message.chat.id, "typing")
            bot.reply_to(message, f"¡Producto {producto_nombre} reservado con éxito!")
        else:
            bot.send_chat_action(message.chat.id, "typing")
            bot.reply_to(message, f"Lo siento, {producto_nombre} ya está reservado.")
    else:
        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, "Producto no encontrado.")

    conn.close()



@bot.message_handler(commands=['agregar'])

def agregar_producto(message):
    bot.send_chat_action(message.chat.id, "typing")
    producto_nombre = message.text.split(' ', 1)[1] 
    conn = sqlite3.connect('productos_db.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM productos WHERE nombre = ?', (producto_nombre,))
    existe_producto = cursor.fetchone()

    if existe_producto:
        bot.reply_to(message, f"El producto '{producto_nombre}' ya está en la base de datos.")
    else:
        cursor.execute('INSERT INTO productos (nombre, precio, reservado, contacto) VALUES (?, ?, ?, ?)',
                       (producto_nombre, 0, 0, ''))
        conn.commit()
        bot.reply_to(message, f"¡Producto '{producto_nombre}' agregado con éxito!")

    conn.close()



if __name__ == '__main__':
    print('INICIADO')
    bot.infinity_polling()
