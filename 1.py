import logging
import sqlite3
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логгера
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Логика БД
def init_db():
    conn = sqlite3.connect('birthdays.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS birthdays (
            user_id INTEGER,
            name TEXT,
            date TEXT,
            PRIMARY KEY (user_id, name)
        )
    ''')
    conn.commit()
    conn.close()
def add_birthday(user_id, name, date):
    conn = sqlite3.connect('birthdays.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO birthdays VALUES (?, ?, ?)', (user_id, name, date))
    conn.commit()
    conn.close()
def remove_birthday(user_id, name):
    conn = sqlite3.connect('birthdays.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM birthdays WHERE user_id = ? AND name = ?', (user_id, name))
    conn.commit()
    conn.close()
def get_birthdays(user_id):
    conn = sqlite3.connect('birthdays.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, date FROM birthdays WHERE user_id = ?', (user_id,))
    birthdays = cursor.fetchall()
    conn.close()
    return birthdays

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False

# Команды 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Привет! Я бот для отслеживания дней рождения.\n'
        'Команды:\n'
        '/add <имя> <дата> - добавить день рождения (формат: ДД.ММ.ГГГГ)\n'
        '/remove <имя> - удалить день рождения\n'
        '/list - показать все дни рождения\n'
        '/help - справка'
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if len(context.args) < 2:
        await update.message.reply_text('Использование: /add <имя> <дата>')
        return

    name = context.args[0]
    date = context.args[1]

    if not validate_date(date):
        await update.message.reply_text('Неверный формат даты. Используйте: ДД.ММ.ГГГГ')
        return

    add_birthday(user_id, name, date)
    await update.message.reply_text(f'День рождения {name} добавлен!')

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if not context.args:
        await update.message.reply_text('Использование: /remove <имя>')
        return

    name = context.args[0]
    remove_birthday(user_id, name)
    await update.message.reply_text(f'День рождения {name} удален!')

async def list_birthdays(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    birthdays = get_birthdays(user_id)

    if not birthdays:
        await update.message.reply_text('У вас нет сохраненных дней рождения.')
        return

    text = 'Ваши дни рождения:\n'
    for name, date in birthdays:
        text += f'{name}: {date}\n'
    
    await update.message.reply_text(text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Доступные команды:\n'
        '/add <имя> <дата> - добавить день рождения\n'
        '/remove <имя> - удалить день рождения\n'
        '/list - показать все дни рождения\n'
        '/help - справка'
    )

async def check_reminders(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now()
    three_days_later = now + timedelta(days=3)  
    conn = sqlite3.connect('birthdays.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT user_id FROM birthdays')
    users = cursor.fetchall()    
    for (user_id,) in users:
        birthdays = get_birthdays(user_id)
        for name, date_str in birthdays:
            birth_date = datetime.strptime(date_str, '%d.%m.%Y')
            birth_date_this_year = birth_date.replace(year=now.year)
            
            if now <= birth_date_this_year <= three_days_later:
                days_left = (birth_date_this_year - now).days
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f'Напоминание: через {days_left} дней день рождения у {name} ({date_str})'
                )

def main():
    init_db() 
    # ТОКЕН ВСТАВЛЯТЬ ТУТА ->
    application = Application.builder().token("").build()
    #
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("remove", remove))
    application.add_handler(CommandHandler("list", list_birthdays))
    application.add_handler(CommandHandler("help", help_command))
    job_queue = application.job_queue
    job_queue.run_repeating(check_reminders, interval=86400, first=10)  # Проверка каждые 24 часа    
    application.run_polling()

if __name__ == '__main__':
    main()