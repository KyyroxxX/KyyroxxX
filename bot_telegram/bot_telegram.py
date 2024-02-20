import telebot
import sqlite3
from config import token

bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(message, "¡Hola! Soy ecaibot. Si necesitas ayuda, escribe /help.")

@bot.message_handler(commands=["help"])
def cmd_help(message):
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(message, "/start - Iniciar el bot\n/help - Mostrar comandos disponibles\n/productos - Mostrar productos disponibles\n/reservar - Reservar un producto")

@bot.message_handler(commands=["reservar"])
def cmd_reservar(message):
    conn = sqlite3.connect('productos_db.db')
    cursor = conn.cursor()

    cursor.execute('SELECT nombre, precio FROM productos WHERE reservado = 0')
    productos_disponibles = cursor.fetchall()

    if productos_disponibles:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        buttons = []
        for producto in productos_disponibles:
            nombre, precio = producto
            buttons.append(telebot.types.KeyboardButton(f"{nombre} - {precio}"))

        markup.add(*buttons)
        bot.send_message(message.chat.id, "Selecciona un producto para reservar:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "No hay productos disponibles para reservar en este momento.")

    conn.close()

@bot.message_handler(func=lambda message: True, content_types=['text'])
def reservar_producto_seleccionado(message):
    conn = sqlite3.connect('productos_db.db')
    cursor = conn.cursor()

    producto_seleccionado = message.text.split(' - ')[0]

    cursor.execute('SELECT reservado FROM productos WHERE nombre = ?', (producto_seleccionado,))
    producto = cursor.fetchone()

    if producto:
        reservado = producto[0]
        if reservado == 0:
            cursor.execute('UPDATE productos SET reservado = 1 WHERE nombre = ?', (producto_seleccionado,))
            conn.commit()
            bot.send_chat_action(message.chat.id, "typing")
            bot.reply_to(message, f"¡Producto '{producto_seleccionado}' reservado con éxito!")
        else:
            bot.send_chat_action(message.chat.id, "typing")
            bot.reply_to(message, f"Lo siento, '{producto_seleccionado}' ya está reservado.")
    else:
        bot.send_chat_action(message.chat.id, "typing")
        bot.reply_to(message, "Producto no encontrado.")

    conn.close()

@bot.message_handler(commands=["productos"])
def mostrar_productos(message):
    conn = sqlite3.connect('productos_db.db')
    cursor = conn.cursor()

    cursor.execute('SELECT nombre, precio FROM productos')
    productos = cursor.fetchall()

    if productos:
        response = "Lista de productos disponibles:\n"
        for producto in productos:
            nombre, precio = producto
            response += f"Producto: {nombre} - Precio: {precio}\n"
    else:
        response = "No hay productos disponibles en este momento."

    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(message, response)

    conn.close()

if __name__ == '__main__':
    print('INICIADO')
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
        ('Cuadro_3', 98.0, 0, '456-789-012'),
        ('Cuadro_4', 90.0, 0, '574-958-142'),
        ('Cuadro_5', 70.0, 0, '432-765-098')


    ]

    cursor.executemany('INSERT INTO productos (nombre, precio, reservado, contacto) VALUES (?, ?, ?, ?)', productos)
    conn.commit()

    bot.infinity_polling()
