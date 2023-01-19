import pyttsx3
import speech_recognition as sr
import pywhatkit
import wikipedia
import webbrowser
from datetime import datetime

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

hablar = talk("¿Hola, que deseas hacer?")
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

elif 'dia' or 'día' in opcion:
    # Usamos el metodo de arriba, porque la variable diaSemana si no nos devuelve un numero
    # Asi la convertimos para que nos devuelva el dia de la semana de la siguiente forma:
    # lunes, martes, miercoles...
    date = datetime.now().date()
    diaSemana = datetime.now().weekday()
    weekdayString = getWeekDay(diaSemana)
    talk("Hoy es " + weekdayString.__str__() + ", " + date.__str__())
