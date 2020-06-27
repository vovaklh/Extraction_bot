import telebot
import pytesseract as ps
from PIL import Image

token = ""
bot = telebot.TeleBot(token)
ps.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\tesseract.exe'


def extract_text_from_image():
    img = Image.open("image.jpg")
    text = ps.image_to_string(img)
    return text


def download_image(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    image = bot.download_file(file_info.file_path)

    with open("image.jpg", 'wb') as new_file:
        new_file.write(image)


@bot.message_handler(commands=['start'])
def handle_start(message):
    welcome = 'This bot is used to extract text from image'
    bot.send_message(message.from_user.id, welcome)


@bot.message_handler(commands=['help'])
def handle_help(message):
    our_help = 'Please send image to get text'
    bot.send_message(message.from_user.id, our_help)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    download_image(message)
    extracted_text = extract_text_from_image()
    bot.send_message(message.from_user.id, extracted_text )


bot.polling(none_stop=True, interval=0)
