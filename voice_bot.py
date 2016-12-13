# -*-coding:utf-8-*-
import telebot, requests, os, subprocess, time, json
## secret tokens
from settings import TOKEN, key_google

def convertor(name, codic):
    PIPE = subprocess.PIPE
    cmd = 'ffmpeg -i ' + name + ' ' + name + '.' + codic

    p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE,
            stderr=subprocess.STDOUT, close_fds=True)
    s = p.stdout.readline()

url_google = "https://www.google.com/speech-api/v2/recognize?output=json&lang=ru-ru&key="+key_google

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, u"Привет, Я бот, ты можешь общаться со мной голосом, как и с другими людьми")


def analyse(words):
    words = words.split()
    hello_w = {
        'приветики солнышко': 'приветики',
        'привет, как дела?': 'привет',
        'здравтвуйте': 'добрый день',
        'добрый день': 'здравтвуйте',
        'здорова братан': 'здорова'
    } 
    for word in words:
        i = 0
        for x in hello_w:
            if word.islower() in x.value():
                return x.key()
    return 'было весело, задайте ещё один вопрос'


@bot.message_handler(content_types=['voice'])
def handle_docs_audio(message):
    chat_id = message.chat.id

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src='/Users/ghost/serv/voice/'+file_info.file_path;
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(chat_id, u"Так, сейчас подумаю")

    convertor(file_info.file_path, 'flac')
    time.sleep(3)
    bot.send_message(chat_id, u"Хмм надо по раскинуть мозгами")
    audio = open(file_info.file_path+'.flac', 'rb').read()

    headers={'Content-Type': 'audio/x-flac; rate=44100'}

    response = requests.post(url_google, data=audio, headers=headers).text.split('\n')[1]

    bot.send_message(chat_id, u"Речь шла о")

    msg = json.loads(response)['result'][0]['alternative'][0]['transcript']
    
    # msg = analyse(msg)
    bot.send_message(chat_id, msg)


bot.polling()
