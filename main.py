import pyttsx3
import speech_recognition as sr
import pywhatkit
import wikipedia
import webbrowser
from datetime import datetime
import pyjokes
import requests
import json
import openai
import os

# Creamos una variable listener, para reconocer la voz
listener = sr.Recognizer()
# Inicializamos el asistente

engine = pyttsx3.init()

voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('rate', 150)


# Cambimos de velocidad al asistente

# Sacar el dia de la semana
def getWeekDay(dia):
    if dia == 0:
        return "lunes"
    elif dia == 1:
        return "martes"
    elif dia == 2:
        return "miercoles"
    elif dia == 3:
        return "jueves"
    elif dia == 4:
        return "viernes"
    elif dia == 5:
        return "sabado"
    elif dia == 6:
        return "domingo"


def chat():
    openai.api_key = "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"
    prompt = "Era una noche oscura y tormentosa, y"
    model = "text-davinci-003"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=0.5,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1,
    )
    text = response.choices[0].text
    print(text)


def getTemperatura(ciudad):
    api_key = "e6c9e5c846f8325be631e26e53bfb034"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + ciudad
    response = requests.get(complete_url)
    # Obtenemos la respuesta en formato JSON
    x = response.json()
    y = x["main"]
    temperatura = y["temp"]
    temperaturaConverted = kelvinToC(temperatura)
    # Sacamos la temperatura de la ciudad que queramos y la transformamos a grados centigrados
    return temperaturaConverted


# Para que nos de la temperatura en grados centigrados
def kelvinToC(grados):
    centigrado = grados - 273, 15
    return centigrado


def talk(text):
    engine.say(text)
    engine.runAndWait()


# Lo metemos en un try-catch por si el microfono falla
# Funcion para que el asistente nos escuche
def escuchar():
    try:
        with sr.Microphone() as source:
            voice = listener.listen(source)
            # Para que nos lo detecte en castellano
            rec = listener.recognize_google(voice, language='es-ES')
            return rec
    except:
        pass


# Variable que comprueba si el asistente si ha inicializado ya

talk("¿Hola, que deseas hacer?")
opcion = escuchar()
print(opcion)

"""Vamos a hacer un switch case para las diferentes opciones, aunque lo vamos a hacer con ifs"""

# Nos va a abrir una ventana en youtube y nos reproducira la music que le digamos
if 'reproduce' in opcion:
    music = opcion.replace('reproduce', '')
    talk('Reproduciendo ' + music)
    pywhatkit.playonyt(music)

# Para buscar en wikipedia
elif 'busca' in opcion:
    busqueda = opcion.replace('busca', '')
    talk('Buscando ' + busqueda + 'en wikipedia')
    talk("¿Quieres que te lo lea o lo haces tu?")
    # Si le dices que quieres hacerlo tu, hara una busqueda en wikipedia y te abre el navegador
    elegir = escuchar()
    if 'yo' in elegir:
        webbrowser.open_new_tab("https://es.wikipedia.org/wiki/" + busqueda)
    else:
        # Si no le dices que quieres hacerlo tu, el programa nos leera la entrada de wikipedia
        info = wikipedia.summary(busqueda, 1)
        talk(info)
# Metodos para obtener la hora actual o la fecha a dia de hoy
elif 'hora' in opcion:
    hora = datetime.now().hour
    minutos = datetime.now().minute
    talk("Son las " + hora.__str__() + " " + minutos.__str__())

elif 'día' in opcion:
    # Usamos el metodo de arriba, porque la variable diaSemana si no nos devuelve un numero
    # Asi la convertimos para que nos devuelva el dia de la semana de la siguiente forma:
    # lunes, martes, miercoles...
    date = datetime.now().date()
    diaSemana = datetime.now().weekday()
    weekdayString = getWeekDay(diaSemana)
    talk("Hoy es " + weekdayString.__str__() + ", " + date.__str__())

elif 'broma' in opcion:
    # Metodo para contar bromas aleatorias
    broma = pyjokes.get_joke(language='es', category='all')
    talk(broma)

elif 'temperatura' in opcion:
    # Metodo que usa la api de https://home.openweathermap.org para darnos la temperatura de la ciudad que le digamos
    talk("¿Que ciudad quieres comprobar?")
    ciudad = escuchar()
    temp = getTemperatura(ciudad).__str__()
    talk("La temperatura en " + ciudad + " es de " + temp[0:2] + " grados centigrados")

elif 'historia' in opcion:
    chat()

elif 'salir' in opcion:
    talk('Siento no haberte sido de utilidad, hasta la próxima')
