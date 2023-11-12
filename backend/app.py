from flask import Flask, request, jsonify, redirect, url_for, send_from_directory
import os
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from human import start_analyse

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/static/<filename>', methods=['GET'])
def get_video(filename):
    return send_from_directory(directory='static/', path=filename)

@app.route("/api/upload", methods=['POST', 'GET'])
@cross_origin()
def upload_file():
    if request.method == 'POST':
        # Проверяем, есть ли в запросе ключ 'file'
        if "file" not in request.files:
            return jsonify({"error": "No file found in request"}), 400

        # Получаем файл из запроса
        file = request.files["file"]
        trueName = secure_filename(file.filename)
        # Сохраняем файл на диск
        file.save("static/" + trueName)

@app.route("/api/analyse/<filename>")
@cross_origin()
def analyse(filename):
    passName = f'static/{filename}'
    result = start_analyse(filename)
    return result

if __name__ == "__main__":
    app.run(host='localhost')