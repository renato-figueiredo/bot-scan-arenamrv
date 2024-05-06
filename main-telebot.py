# main.py

import telebot
from bs4 import BeautifulSoup
import requests
import datetime
import config

bot = telebot.TeleBot(config.BOT_TOKEN)  # Inicializa o bot

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

@bot.message_handler(commands=["hoje"])
def handle_hoje(message):
    """Envia eventos de hoje."""
    today = datetime.date.today()
    events = get_events()
    message_text = "Eventos de hoje na Arena MRV:\n\n"
    for date, title in events:
        if date == today:
            message_text += format_event(date, title) + "\n"
    bot.send_message(message.chat.id, message_text)

@bot.message_handler(commands=["arena"])
def handle_arena(message):
    """Envia eventos dos próximos 7 dias."""
    today = datetime.date.today()
    week_from_now = today + datetime.timedelta(days=7)
    events = get_events()
    message_text = "Próximos eventos na Arena MRV:\n\n"
    for date, title in events:
        if today <= date < week_from_now:
            message_text += format_event(date, title) + "\n"
    bot.send_message(message.chat.id, message_text)

@bot.message_handler(commands=["teste"])
def handle_teste(message):
    """Responde com mensagem de sucesso."""
    bot.send_message(message.chat.id, "Teste bem-sucedido!")

bot.polling()  # Inicia o bot e o mantém escutando por mensagens