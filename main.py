# main.py

# Importar bibliotecas e configurações
from bs4 import BeautifulSoup
from queue import Queue 

import requests
import datetime
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler
import config

def get_events():
    """Extrai eventos da página de pesquisa do Google."""
    url = "https://www.google.com/search?q=arena+mrv+próximos+eventos"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    events = []
    for result in soup.find_all("div", class_="g"):
        try:
            date_str = result.find("div", class_="slp f").text.strip()
            date = datetime.datetime.strptime(date_str, "%a, %d de %b").date()
            title = result.find("div", class_="BNeawe vvjwJb AP7Wnd").text.strip()
            events.append((date, title))
        except:
            pass
    return events

def format_event(date, title):
    """Formata a informação do evento."""
    weekday = date.strftime("%a")
    month_day = date.strftime("%d/%b")
    return f"{weekday}, {month_day} - {title}"

def send_message(message):
    """Envia mensagem pelo Telegram."""
    bot = Bot(token=config.BOT_TOKEN)
    bot.send_message(chat_id=config.CHAT_ID, text=message)

def handle_hoje(update: Update, context):
    """Envia eventos de hoje."""
    today = datetime.date.today()
    events = get_events()
    message = "Eventos de hoje na Arena MRV:\n\n"
    for date, title in events:
        if date == today:
            message += format_event(date, title) + "\n"
    send_message(message)

def handle_arena(update: Update, context):
    """Envia eventos dos próximos 7 dias."""
    today = datetime.date.today()
    week_from_now = today + datetime.timedelta(days=7)
    events = get_events()
    message = "Próximos eventos na Arena MRV:\n\n"
    for date, title in events:
        if today <= date < week_from_now:
            message += format_event(date, title) + "\n"
    send_message(message)

def handle_teste(update: Update, context):
    """Responde com mensagem de sucesso."""
    update.message.reply_text("Teste bem-sucedido!")

def main():
    """Inicializa o bot e configura os handlers."""
    bot = Bot(token=config.BOT_TOKEN)  # Crie um objeto Bot
    update_queue = Queue()  # Crie uma fila para atualizações
    updater = Updater(bot=bot, update_queue=update_queue)  # Passe a fila para o Updater

    dispatcher = updater.dispatcher

    # Adicionar handlers para comandos
    dispatcher.add_handler(CommandHandler("hoje", handle_hoje))
    dispatcher.add_handler(CommandHandler("arena", handle_arena))
    dispatcher.add_handler(CommandHandler("teste", handle_teste))

    # Executar handlers de forma assíncrona 
    dispatcher.run_async
    
    # Iniciar o bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()