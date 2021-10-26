import requests
import json
from googletrans import Translator

botCode = open("bot.py").read()

cmd = ["Inspire: ngirim quote\n",
       "Aku mau kode: ngirim source code\n",
       "Translate: translasi kalimat setelah kata translate, contoh: translate aku dan kamu -> me and you\n",
       "Alltranslate: translasi kalimat dari bahasa apa aja menjadi inggris\n",
       "Hai @bot: Hai\n",
       "Halo @bot: Halo\n",
       "Ls: nge list command\n"]

cmdEng = ["Inspire: send quote\n",
           "I want code: send source code\n",
           "Translate: translate sentence from Indonesian to English: translate aku dan kamu -> me and you\n",
           "Alltranslate: translate sentence from any language to English\n",
           "Hai @bot: Hai\n",
           "Halo @bot: Halo\n",
           "Ls: list command\n"]

def translasi(kata, *args):
    print(kata)
    translator = Translator()
    result = translator.translate(kata, *args)
    return result.text

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

def jawab(message, mention = False):
    if message.content.lower().startswith("inspire"):
        return get_quote()
    elif message.content.lower().startswith("aku mau kode") or message.content.lower().startswith("i want code"):
        return botCode
    elif message.content.lower().startswith("jangan bacot!"):
        return "Maaf, developerku belum ngode buat command ini..."
    elif message.content.lower().startswith("translate "):
        return translasi(message.content[10:], 'en', 'id')
    elif message.content.lower().startswith("alltranslate "):
        return translasi(message.content[13:])
    elif message.content.lower() == "ls":
        ret = ""
        for _ in cmd:
            ret += _
        ret += "\n\n"
        for _ in cmdEng:
            ret += _
        return ret
    elif message.content.lower().startswith("hai") and mention:
        return("Hai %s, aku adalah bot....\n"%(message.author)+
            "Kalau kamu mau dapat source code untuk bot ini, silahkan kirim pesan 'aku mau kode'\n"+
            "Untuk list command lengkap, silahkan kirim pesan 'ls'")
    elif message.content.lower().startswith("halo") and mention:
        return("Halo %s, aku adalah bot....\n"%(message.author)+
            "Kalau kamu mau dapat source code untuk bot ini, silahkan kirim pesan 'aku mau kode'\n"+
            "Untuk list command lengkap, silahkan kirim pesan 'ls'")
    elif message.content.lower().startswith("perkenalan") and mention:
        return("Hai %s, aku adalah bot....\n"%(message.author)+
            "Saat ini, aku bisa melakukan dua hal, yaitu memberi kalian quote, dan mentranslate kalimat\n"+
            "Untuk informasi lebih lanjutnya silahkan kirim pesan 'ls' 😁✌️")
    elif message.content.lower().startswith("introduction") and mention:
        return("Hello %s, I'm a bot....\n"%(message.author)+
            "Currently, I've been programmed to do two things, giving quote and translating sentences to English\n"+
            "For more information, please send 'ls' 😁✌️")
    return None



# +"Kalau bot ini terlalu berisik, silahkan kirim pesan 'jangan bacot!'"