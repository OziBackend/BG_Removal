from flask import Flask, request, jsonify, send_from_directory, send_file
import threading
import os
from datetime import datetime

app = Flask(__name__, static_folder='static')

# Define the uploads directory
app.config['UPLOAD_FOLDER'] = 'uploads'

semaphores = threading.Semaphore(50)

#server environment
import configuration.environment as config

# Configure Flask app
# app.config['SERVER_NAME'] = f'{config.IP}:{config.PORT}'
# app.config['APPLICATION_ROOT'] = '/'
# app.config['PREFERRED_URL_SCHEME'] = 'http'

#importing the controller
from controller.controller import remove_background

input_folder = "static/input"

@app.route('/remove_bg', methods=['POST'])
def remove_bg():
    print('Function Remove_BG called')
    if 'file' not in request.files:
        return jsonify({"error": "No File Part"}), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename_with_timestamp = f"{file.filename.split('.')[0]}_{timestamp}.{file.filename.split('.')[1]}"
    file_path = os.path.join(input_folder, filename_with_timestamp)
    file.save(file_path)

    return_data = {}

    print('Acquiring a Semaphore')
    semaphores.acquire()

    t = threading.Thread(target=remove_background, args=(app, file_path, filename_with_timestamp, return_data))

    t.start()
    t.join()

    print(return_data)
    print('Releasing Semaphore')
    semaphores.release()

    if not return_data:
        return jsonify({"error": "No data returned"}), 400

    return jsonify(return_data)

if __name__ == "__main__":
    app.run(host=config.IP, port=config.PORT, debug=True)