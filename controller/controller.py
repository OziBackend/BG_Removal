import rembg
from PIL import Image
from flask import jsonify, url_for

import configuration.environment as config

def remove_background(app, file_path, filename_with_time, return_data):
    with app.app_context():
        try:
            print('Try Statement')

            filename = filename_with_time.split('.')[0] + '.png'
            input_image = Image.open(file_path)

            #path for an output image
            output_path = f'static/output/{filename}'
            #removing background of the image
            output_image = rembg.remove(input_image)

            output_image.save(output_path, 'PNG')

            image_url = f'http://{config.IP}:{config.PORT}/{output_path}'
            # image_url = url_for('static', filename= f'output/{filename}', _external=True)
            return_data['image_url'] = image_url

        except BaseException as e:
            print(f'1........... in function remove_background error is {e}')
            return_data['image_url'] = ''