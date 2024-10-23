from flask import Flask, render_template, request, Response, jsonify
import cv2
import numpy as np
import requests
import json
import ia

app = Flask(__name__)

# Inicializa a câmera
camera = cv2.VideoCapture(1)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html', result='XXXXXXX')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/confirmar', methods=['POST'])
def confirmar():
    success, frame = camera.read()
    if success:
        # Codifica a imagem em formato JPEG
        #_, buffer = cv2.imencode('.jpg', frame)
        #image_data = buffer.tobytes()

        # Aqui você chamaria sua função de IA
        # Exemplo: response = ia.confirmar(image_data)
        # Para a demonstração, vamos simular uma resposta
        response = ia.leitura(frame)
        
        # Supondo que a resposta seja um JSON com um campo 'message'
        json_response = response
        return render_template('index.html', result=json_response)

    return render_template('index.html', result='Falha ao capturar a imagem.')

if __name__ == '__main__':
    app.run(debug=True)
