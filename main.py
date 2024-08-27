import telebot
import requests

from api import TELEGRAM_TOKEN, WEATHER_API_KEY

bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(
      message.chat.id,
      "Hello, I am a weather forecasting bot. Give me a city name and I will tell you the weather.\nUsage : /weather city .\n--Created, Managed by Harshil Patel."
  )


@bot.message_handler(commands=['weather'])
def weather(message):
  userinput = message.text.split()
  if len(userinput) == 2:
    city = userinput[1]
    bot.reply_to(message, f'Fetching weather for {city}')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city_name = data['name']
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        message_text = f'Weather in {city_name}:\nTemperature: {temp}°C\nDescription: {description.capitalize()}'
        bot.reply_to(message, message_text)
    else:
        bot.reply_to(message, 'City not found. Please try again.')
    
    

  else:
    bot.reply_to(message, "Please enter a valid city name.")


@bot.message_handler(commands=['exit'])
def exit(message):
  bot.send_message(message.chat.id,
                   "Hope it helped you. Thanks.\n---Exited---")
  bot.stop_polling()


bot.polling()
