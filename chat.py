from flask import Flask, render_template
from flask_socketio import SocketIO
import difflib
from time import sleep

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

respuestas = {
    "¿qué es el folio de una solicitud?": "El folio es la combinación de las primeras 3 letras de su empresa y la fecha de hoy sin guiones o barras. Ejemplo: emp121123 (emp=empresa y 121123=12/11/2023).",
    "¿qué son los servicios?": "Los servicios son elementos adicionales que puede contratar para su proyecto, como agua, energía, andamios, herramientas, máquinas de construcción, etc.",
    "¿cuántos servicios podré contratar?": "Puede contratar tantos servicios como necesite y considere útiles para su proyecto.",
    "¿quien sera el supervisor de mi proyecto?": "El equipo de trabajo le asignará un supervisor que será seleccionado considerando lo mejor para su proyecto.",
    "¿qué debo incluir en la descripción de mi solicitud?": "Debe incluir detalles sobre lo que se construirá o reparará, así como cualquier otra información relevante para su solicitud.",
    "Explícame qué significa el término 'folio' en una solicitud.": "El folio es una combinación única de las primeras 3 letras de su empresa y la fecha actual. Ejemplo: emp121123 (emp=empresa y 121123=12/11/2023).",
    "¿Puedes definir qué es un 'servicio' en el contexto de un proyecto?": "En el contexto de un proyecto, un 'servicio' se refiere a elementos adicionales que se pueden contratar, como agua, energía, herramientas, etc.",
    "¿Existe un límite en la cantidad de servicios que puedo incluir en mi proyecto?": "No hay un límite específico en la cantidad de servicios que puede incluir en su proyecto. Puede contratar tantos como necesite.",
    "¿Cómo se elige al supervisor para un proyecto específico?": "El supervisor se elige considerando lo mejor para su proyecto. El equipo de trabajo evaluará las necesidades y asignará un supervisor adecuado.",
    "¿Cuáles son los elementos esenciales que debo mencionar al describir mi solicitud?": "Al describir su solicitud, incluya detalles sobre lo que se construirá o reparará y cualquier información relevante para comprender su proyecto.",
    "¿Cuál es la importancia de incluir detalles específicos al solicitar un folio?": "Incluir detalles específicos al solicitar un folio ayuda a garantizar que el folio generado sea único y se ajuste a las características de su proyecto.",
    "Dame más información sobre la asignación de supervisores en los proyectos.": "La asignación de supervisores se realiza considerando las necesidades específicas de su proyecto. Se seleccionará un supervisor cualificado para supervisar el progreso.",
    "¿Puedo agregar servicios adicionales a mi proyecto después de presentar la solicitud inicial?": "Sí, puede agregar servicios adicionales a su proyecto después de presentar la solicitud inicial. Comuníquese con el equipo de trabajo para hacer modificaciones.",
    "¿Qué criterios se utilizan para seleccionar al supervisor de un proyecto?": "Los criterios para seleccionar al supervisor incluyen la experiencia, las habilidades y la adecuación a las necesidades específicas de su proyecto.",
    "¿Cómo afecta la combinación de letras de la empresa y la fecha al folio de la solicitud?": "La combinación de letras de la empresa y la fecha se utiliza para generar un folio único que identifica su solicitud de manera exclusiva. Ejemplo: emp121123."
}

@socketio.on('message')
def handle_message(message):
    pregunta_similar = encontrar_pregunta_similar(message)
    if pregunta_similar:
        respuesta = respuestas[pregunta_similar]
        enviar_respuesta_pregunta_separada(respuesta)
    else:
        mensaje_respuesta = "Por favor, envía una de las siguientes preguntas:\n" + "\n".join(respuestas.keys())
        enviar_respuesta_pregunta_separada(mensaje_respuesta)

def enviar_respuesta_pregunta_separada(respuesta):
    for linea in respuesta.splitlines():
        sleep(0.3)  # Retraso de 1 segundo entre preguntas (ajusta según sea necesario)
        socketio.emit('message', linea)

@socketio.on('connect')
def handle_connect():
    # No envíes el saludo aquí, manejarás el saludo desde el cliente
    pass

def encontrar_pregunta_similar(pregunta):
    preguntas = respuestas.keys()
    pregunta_similar = difflib.get_close_matches(pregunta, preguntas, n=1, cutoff=0.4)
    return pregunta_similar[0] if pregunta_similar else None

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=3000)


