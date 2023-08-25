import pyttsx3
import speech_recognition as sr
import pywhatkit
import pyjokes
import webbrowser
import datetime
import wikipedia

# Idiomas de voz
id_spanish = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id_english = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'


# Escuchar nuestro micrófono y devolver el audio como texto
def transformar_audio_en_texto():
    # Almaenar recognizer en variable
    r = sr.Recognizer()

    # Configurar el micrófono
    with sr.Microphone() as microfono:
        # Tiempo de espera
        r.pause_threshold = 0.8

        # Informar que comenzó la grabación
        print("Ya puedes hablar")

        # Guardar lo que escuche como audio
        audio = r.listen(microfono)

        try:
            # Buscar en google
            pedido = r.recognize_google(audio, language="es-es")

            # Prueba de que pudo ingresar
            print("Dijiste: " + pedido)

            # Devolver pedido
            return pedido

        # En caso de que no comprenda el audio
        except sr.UnknownValueError:
            print("No te he entendido")

            # Devolver error
            return "sigo esperando"

        # En caso de no resolver el pedido
        except sr.RequestError:
            print("Conexión fuera de servicio. :(")

            # Devolver error
            return "sigo esperando"

        # Error inesperado
        except:
            print("Algo ha salido mal")

            # Devolver error
            return "sigo esperando"


# Funcion para que el asistente sea escuchado
def hablar(mensaje):
    # Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id_spanish)

    # Pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# Informar del dia de la semana
def pedir_dia():
    # Crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # Crear variable para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # Diccionario con nombre de los dias
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}

    # Decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


# Informar de que hora es
def pedir_hora():
    # Crear una variable con datos de la hora
    hora = datetime.datetime.now()
    print(hora)
    hora = f'Son las {hora.hour} y {hora.minute}.'

    # Decir la hora
    hablar(hora)


# Saludar
def saludo():
    # Crear variable con datos de hora
    hora = datetime.datetime.now()

    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour <= 12:
        momento = 'Buenos días'
    else:
        momento = 'Buenas tardes'

    # Decir el saludo
    hablar(f"{momento}, soy el churumbel Assistant, ¿En qué puedo ayudarte?")


# Funcion central de asistente
def pedir_tareas():
    # Saludar
    saludo()

    # Variable de finalizacion
    comenzar = True

    # Loop central
    while comenzar:

        # Activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir gmail' in pedido:
            hablar('Abriendo yimeil.')
            webbrowser.open('https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox')
            continue
        elif 'abrir el navegador' in pedido:
            hablar('Abriendo el navegador')
            webbrowser.open('https://www.google.com')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando eso en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Según wikipedia: ')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Buscando en internet: ')
            pedido = pedido.replace('busca en internet', '')
            print(pedido)
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'adiós' in pedido:
            hablar("Hasta luego")
            comenzar = False
            continue
        else:
            hablar('No te entendí. ¿Puedes repetírmelo?')
            continue


pedir_tareas()
