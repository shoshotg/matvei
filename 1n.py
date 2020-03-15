import pyowm
import telebot
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from telebot import types
admins = [412422372]
users_id_file = 'users.txt'
bot = telebot.TeleBot("") # Создание объекта бота
owm = pyowm.OWM('bbc3649126d17d7bb4111c44c6a562d5', language = "ru") # Объект owm

print("Бот запущен")


def keyboard():
        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
        button1 = types.KeyboardButton('Вк') # как кнопка занывается
        button2 = types.KeyboardButton('Погода') # как кнопка называется
        button3 = types.KeyboardButton('Админ')
        markup.add(button1) # добавляем 1 кнопку
        markup.add(button2) # добавляем 2 кнопку
        markup.add(button3)
        return markup
        
@bot.message_handler(commands=['start']) # Декоратор на команды start и хелп. Срабатывает когда пишут их
def send_welcome(message):                                                                       #вот тут подключаем клаву(с команды старт)
    bot.reply_to(message, "Привет! Ты тут можешь узнать погоду и все... \nно я буду развиваться) , как то так.", reply_markup = keyboard())
    id_of_user = message.from_user.id
    print(id_of_user)
    save_chat_id(id_of_user)

@bot.message_handler(commands=['s'])
def cit(message):
    citata = bot.send_message(message.from_user.id, 'напиши цитату')
    bot.register_next_step_handler(citata, cici)

def cici(message):
    image = Image.open("cit.jpg")
    font = ImageFont.truetype("18928.ttf", size=32)
    text = message.text
    text_color = (255, 255, 255) # белый
    text_position = (150, 450) #второе горизонт

    draw = ImageDraw.Draw(image)
    draw.text(text_position, text, text_color, font)
    image.save("quote_out.png")
    try:
        bot.send_photo(message.chat.id, open('quote_out.png', 'rb'))
    except:
        print('/n')
def save_chat_id(id_of_user):
    id_of_user = str(id_of_user)                
    with open(users_id_file,"a+") as users_id:
        users_id.seek(0)
        users = [line.split('\n')[0] for line in users_id]
        if id_of_user not in users:
            users_id.write(f'{id_of_user}\n')
            users.append(id_of_user)
            print( f'New id_of_user saved: {id_of_user}')
        else:
            print( f'id_of_user {id_of_user} is already saved')
         
@bot.message_handler(commands=['spam'])
def helper(message):
    if message.from_user.id in admins:
        msag = bot.send_message(message.from_user.id, "Напиши нужный текст") # Получие объекта отправки
        bot.register_next_step_handler(msag, spam)
    else:
        bot.send_message(message.from_user.id, "ты не адмен")
       
@bot.message_handler(commands=['spams'])
def inl(message):
        if message.from_user.id in admins:
            smg = bot.send_message(message.from_user.id, "Напиши нужную сылку") # Получие объекта отправки
            bot.register_next_step_handler(smg, spamss)
        else:
            bot.send_message(message.from_user.id, "ты не адмен")
        
def spamss(message):
    with open(users_id_file, "r") as users_id:
        for line in users_id:
            try:
                bot.send_message(line, spams)
            except telebot.apihelper.ApiException:
                print('есть крыса')
                
def spams(message): # это инлайновая клава - то есть привязана к сообщению от бота
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="тык", url=message.text)
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "сообщение от адмена", reply_markup=keyboard)

                
def spam(message):
    with open(users_id_file, "r") as users_id:
        for line in users_id:
            try:
                bot.send_message(line, message.text)
            except telebot.apihelper.ApiException:
                print('есть крыса')
            
    
@bot.message_handler(content_types=['text']) # Хедлер на текстовые сообщения
def pogoda(message):
    if message.text == 'Погода': # Проверяет, является ли таким сообщие
        msg = bot.send_message(message.from_user.id, "Напиши нужный город.") # Получие объекта отправки
        bot.register_next_step_handler(msg, answer_city) # Ожидание названия города
    elif message.text == 'Вк':
        vk(message)
    elif message.text == 'Админ':
    	admin(message)
    elif message.text == 'Взлом':
    	zlom(message)
    elif message.text == 'citat':
        print('dsa')
        
def answer_city(message):
	try:
	    observation = owm.weather_at_place(message.text)
	    w = observation.get_weather()
	    temp = w.get_temperature('celsius')["temp"]
	    otv = "В городе " + message.text + " сейчас " + w.get_detailed_status() + "\n" 
	    otv += "Температура на улице равна " + str(temp) + "\n"

	    if temp < 10:
	        otv += "На улице дубак, советую брать шубу и валенки."
	    elif temp < 15:
	        otv += "на улцие неплохая погода, можете одеться как хотите."
	    else:
	        otv += "на улцие неплохая погода, можете одеться как хотите."
	    bot.send_message(message.chat.id, otv) 

	except:
		bot.send_message(message.chat.id, "Вы ввели неправильный город") 

def vk(message): # это инлайновая клава - то есть привязана к сообщению от бота
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="тык тыгыдык", url="https://vk.com")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Это вк разраба", reply_markup=keyboard)
    
def admin(message):
	if message.from_user.id in admins:
		bot.send_message(message.from_user.id, 'welcome')
	else:
		bot.send_message(message.from_user.id, 'Only for admins')
        
def zlom(message): # это инлайновая клава - то есть привязана к сообщению от бота
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="ссылка", url="https://google.com")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "база кредитных карт", reply_markup=keyboard)

try:
    bot.infinity_polling(none_stop = True)
except:
    print('\n')
