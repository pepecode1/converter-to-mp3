from flask import Flask, render_template, request, send_file
import os
import yt_dlp
from pydub import AudioSegment

app = Flask(__name__)

# Carpeta para guardar los archivos descargados
DOWNLOAD_FOLDER = os.path.join('static', 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        # Opciones para yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        # Descargar y convertir a MP3
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', None)
            mp3_file = os.path.join(DOWNLOAD_FOLDER, f"{title}.mp3")

        # Enviar el archivo al usuario
        return send_file(mp3_file, as_attachment=True)

    except Exception as e:
        error_message = f"Error: {str(e)}"
        if "soundcloud" in url.lower():
            error_message += " Asegúrate de que la pista de SoundCloud esté habilitada para descarga."
        elif "youtube" in url.lower():
            error_message += " Verifica que el enlace de YouTube sea válido."
        return error_message

if __name__ == '__main__':
    app.run(debug=True)