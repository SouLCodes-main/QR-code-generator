from flask import Flask, render_template, request, url_for
import qrcode
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/qr_codes'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
            file_name = f"qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            img = qrcode.make(qr_data)
            img.save(file_path)
            qr_img = url_for('static', filename=f'qr_codes/{file_name}')

    return render_template('index.html', qr_img=qr_img)

if __name__ == '__main__':
    app.run(debug=True)