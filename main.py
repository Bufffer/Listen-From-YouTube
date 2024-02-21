from flask import Flask, request, render_template, send_from_directory
from pytube import YouTube
import os
import shutil

app = Flask(__name__)

TEMP_FOLDER = 'temp'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    yt_url = request.form['text']
    yt = YouTube(yt_url)
    video = yt.streams.filter(only_audio=True).first()
    
    if not os.path.exists(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)
    else:
        shutil.rmtree(TEMP_FOLDER)
        os.makedirs(TEMP_FOLDER)

    out_file = video.download(output_path=TEMP_FOLDER)
    base, _ = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    file_name = os.path.basename(new_file)
    return render_template('results.html', file_name=file_name)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(TEMP_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
