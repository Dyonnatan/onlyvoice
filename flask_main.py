from flask import Flask, redirect, render_template, request, send_from_directory

from datetime import datetime
import logging
import os


app = Flask(__name__)

os.makedirs(os.path.join(app.instance_path, 'htmlfi'), exist_ok=True)

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = {'mp3'}
FILE_NAME = 'my_audio.mp3'

app.config['UPLOAD_FOLDER'] = app.instance_path

@app.route('/')
def page(audio_entities=[]):
    return render_template('homepage.html', audio_entities=audio_entities)
	


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/upload_sound', methods=['GET', 'POST'])
def upload_sound():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], FILE_NAME))
        
        separate()
        
        uploads = os.path.join(app.config['UPLOAD_FOLDER'], 'my_audio')
        print(uploads, FILE_NAME)
        return send_from_directory(directory=uploads, filename='vocals.wav', as_attachment=True)
    
    uploads = os.path.join(app.config['UPLOAD_FOLDER'])
    print(uploads, file.filename)
    return send_from_directory(directory=uploads, filename=FILE_NAME)
	
def separate():
    print('spleeter separate -i ' + os.path.join(app.config['UPLOAD_FOLDER'],FILE_NAME) + '  -o '+ os.path.join(app.config['UPLOAD_FOLDER']))
    os.system('spleeter separate -i ' + os.path.join(app.config['UPLOAD_FOLDER'],FILE_NAME) + ' -o '+ os.path.join(app.config['UPLOAD_FOLDER']))
	
@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """An internal error occurred: <pre>{}</pre>""".format(e), 500



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)