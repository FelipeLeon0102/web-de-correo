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

app = Flask(__name__)
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

def enviar_email(request: EmailRequest):
    servidor_smtp = "mail.idicol.com"
    puerto_smtp = 465  # Cambiado para SSL
    usuario_smtp = "solicitudes@idicol.com"
    contraseña_smtp = "Sol2578/*/"

    msg = MIMEMultipart()
    msg['From'] = usuario_smtp
    msg['To'] = request.destinatario
    msg['Subject'] = request.asunto
    msg.attach(MIMEText(request.mensaje, 'plain'))

    try:
        server = smtplib.SMTP_SSL(servidor_smtp, puerto_smtp)
        server.login(usuario_smtp, contraseña_smtp)
        text = msg.as_string()
        server.sendmail(usuario_smtp, request.destinatario, text)
        server.quit()
        return {"mensaje": "Correo enviado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar el correo: {e}")

# bloque de prueba
if __name__ == "__main__":
    app.run(debug=True)






    

