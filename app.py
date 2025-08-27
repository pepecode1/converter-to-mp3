from flask import Flask, render_template, request, send_file, jsonify
import os
import yt_dlp
import threading
import logging

app = Flask(__name__)

# Configurar logging para depuración
logging.basicConfig(level=logging.DEBUG)

# Carpeta para guardar los archivos descargados
DOWNLOAD_FOLDER = os.path.join('static', 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Variable global para almacenar el progreso
download_progress = {'progress': 0, 'filename': None, 'status': 'idle'}

def progress_hook(d):
    global download_progress
    if d['status'] == 'downloading':
        # Calcular el porcentaje de progreso
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        if total_bytes and 'downloaded_bytes' in d:
            download_progress['progress'] = (d['downloaded_bytes'] / total_bytes) * 100
            app.logger.debug(f"Progreso: {download_progress['progress']:.2f}%")
        else:
            download_progress['progress'] = 0  # En caso de que no haya datos de tamaño
    elif d['status'] == 'finished':
        download_progress['progress'] = 100
        # Asegurarse de que el nombre del archivo sea el del MP3
        filename = d.get('filename', '').replace('.webm', '.mp3').replace('.m4a', '.mp3')
        download_progress['filename'] = os.path.basename(filename)
        download_progress['status'] = 'finished'
        app.logger.debug(f"Descarga completa: {download_progress['filename']}")
    else:
        app.logger.debug(f"Estado desconocido: {d['status']}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    global download_progress
    download_progress = {'progress': 0, 'filename': None, 'status': 'downloading'}
    url = request.form['url']
    app.logger.debug(f"Iniciando descarga para URL: {url}")

    def download_task():
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            download_progress['status'] = f'error: {str(e)}'
            app.logger.error(f"Error en la descarga: {str(e)}")

    # Ejecutar la descarga en un hilo separado
    threading.Thread(target=download_task).start()
    return jsonify({'status': 'started'})

@app.route('/progress')
def progress():
    global download_progress
    app.logger.debug(f"Progreso actual: {download_progress}")
    return jsonify(download_progress)

@app.route('/get_file/<filename>')
def get_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    app.logger.debug(f"Intentando enviar archivo: {file_path}")
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    app.logger.error(f"Archivo no encontrado: {file_path}")
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)