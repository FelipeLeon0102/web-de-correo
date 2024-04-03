from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pydantic import BaseModel
from werkzeug.exceptions import HTTPException

class EmailRequest(BaseModel):
    destinatario: str
    asunto: str
    mensaje: str
    cc: list = None

app = Flask(__name__)

# Ruta para enviar correos electrónicos
@app.route('/enviar-correo', methods=['POST'])
def enviar_correo():
    request_data = request.get_json()
    try:
        email_request = EmailRequest(**request_data)
        enviar_email(email_request)
        return jsonify({"mensaje": "Correo enviado exitosamente."})
    except Exception as e:
        raise HTTPException(status_code=500, description=f"Error al enviar el correo: {e}")  # Utiliza HTTPException para manejar el error HTTP

def enviar_email(request: EmailRequest):
    servidor_smtp = "mail.idicol.com"
    puerto_smtp = 465  # Cambiado para SSL
    usuario_smtp = "solicitudes@idicol.com"
    contraseña_smtp = "Sol2578/*/"

    msg = MIMEMultipart()
    msg['From'] = usuario_smtp
    msg['To'] = request.destinatario
    msg['Subject'] = request.asunto
    
    
    msg.attach(MIMEText(request.mensaje, 'html'))

    
    if request.cc:
        msg['Cc'] = ', '.join(request.cc)

    try:
        server = smtplib.SMTP_SSL(servidor_smtp, puerto_smtp)
        server.login(usuario_smtp, contraseña_smtp)
        text = msg.as_string()
        destinatarios = [request.destinatario]
        if request.cc:
            destinatarios.extend(request.cc)
        server.sendmail(usuario_smtp, destinatarios, text)
        server.quit()
    except Exception as e:
        raise HTTPException(status_code=500, description=f"Error al enviar el correo: {e}")  # Utiliza HTTPException para manejar el error HTTP


# rutas
@app.route('/')
def raiz():
    titulo = "pagina inicio"
    return render_template('inicio.html', titulo=titulo)

# ruta para nosotros
@app.route('/nosotros')
def nosotros():
    titulo = "nosotros"
    return render_template('nosotros.html', titulo=titulo)


# bloque de prueba
if __name__ == "__main__":
    app.run(debug=True)
