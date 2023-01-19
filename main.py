import pyttsx3

#Inicializamos el asistente

s = pyttsx3.init()
data = "Hola que tal "

#Aqui seteamos la velocidad del asistente
rate = s.getProperty('rate')
s.setProperty('rate', 120)
s.say(data)
s.runAndWait()

