from flask import Flask, render_template, request, url_for
import qrcode
import os
import base64
import io
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_img = None
    if request.method == 'POST':
        qr_data = ""
        if request.form.get('text'):
            qr_data = request.form['text']
        elif request.form.get('url'):
            qr_data = request.form['url']
        elif request.form.get('image'):
            qr_data = request.form['image']
        elif request.form.get('name') or request.form.get('phone') or request.form.get('email'):
            name = request.form.get('name', '')
            phone = request.form.get('phone', '')
            email = request.form.get('email', '')
            qr_data = f"MECARD:N:{name};TEL:{phone};EMAIL:{email};;"
        elif request.form.get('ssid'):
            ssid = request.form['ssid']
            password = request.form.get('password', '')
            encryption = request.form.get('encryption', 'WPA')
            qr_data = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
        
        if qr_data:
            # Generate QR code as base64 instead of saving file
            img = qrcode.make(qr_data)
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            qr_img = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

    return render_template('index.html', qr_img=qr_img)

if __name__ == '__main__':
    app.run(debug=True)