import telebot
import sqlite3
from config import token

bot = telebot.TeleBot(token)


@bot.message_handler(func=lambda message: True)
def manejar_seleccion(message):
    conn = sqlite3.connect('agenda_db.db')
    cursor = conn.cursor()

    # Si el mensaje es uno de los días de la semana
    if message.text in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]:
        dia_seleccionado = message.text

        cursor.execute('SELECT hora FROM agenda WHERE dia_semana = ? AND reservado = 0', (dia_seleccionado,))
        horas_disponibles = cursor.fetchall()

        if horas_disponibles:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add(*[hora[0] for hora in horas_disponibles])
            bot.send_message(message.chat.id, f"Horas disponibles para {dia_seleccionado}:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f"No hay horas disponibles para {dia_seleccionado}.")

    # Si el mensaje es una hora disponible
    else:
        hora_seleccionada = message.text

        cursor.execute('SELECT reservado FROM agenda WHERE hora = ?', (hora_seleccionada,))
        reserva = cursor.fetchone()

        if reserva and reserva[0] == 0:
            cursor.execute('UPDATE agenda SET reservado = 1, contacto = ? WHERE hora = ?', (message.chat.id, hora_seleccionada))
            conn.commit()
            bot.send_message(message.chat.id, f"Hora '{hora_seleccionada}' reservada con éxito.")
        else:
            bot.send_message(message.chat.id, f"La hora '{hora_seleccionada}' ya está reservada.")
import sqlite3

# Conectar a la base de datos o crearla si no existe
conn = sqlite3.connect('agenda_db.db')
cursor = conn.cursor()

# Crear la tabla 'agenda' si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS agenda (
        id INTEGER PRIMARY KEY,
        dia_semana TEXT,
        hora TEXT,
        reservado INTEGER DEFAULT 0,
        contacto TEXT DEFAULT NULL
    )
''')

# Agenda/Resevas
agenda = [
    ('Lunes', '09:00', 0, None),
    ('Lunes', '10:00', 0, None),
    ('Lunes', '11:00', 1, 'Usuario 1'),
    ('Martes', '09:00', 0, None),
    ('Martes', '10:00', 0, None),
    ('Martes', '11:00', 0, None),
    ('Miercoles', '09:00', 0, None),
    ('Miercoles', '10:00', 0, None),
    ('Miercoles', '11:00', 0, None),
    ('Jueves', '09:00', 0, None),
    ('Jueves', '10:00', 0, None),
    ('Jueves', '11:00', 0, None),
    ('Viernes', '10:00', 0, None),
    ('Viernes', '11:00', 0, None),
]

cursor.executemany('INSERT INTO agenda (dia_semana, hora, reservado, contacto) VALUES (?, ?, ?, ?)', agenda)
conn.commit()


conn.close()

if __name__ == '__main__':
    print('INICIADO')
    bot.infinity_polling()