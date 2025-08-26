from flask import Flask, request, render_template
import os
import qrcode
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/qr_codes'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_img_path = None
    if request.method == 'POST':
        data = request.form.get('data')

        if data:
            file_name = f"qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

            img = qrcode.make(data)
            img.save(file_path)

            qr_img_path = file_path  # To display on the page

    return render_template('index.html', qr_img=qr_img_path)

if __name__ == '__main__':
    app.run(debug=True)
            