import io
import json
import os

from google.cloud import vision

import VisionAI.VisionConfig as config

# Setting credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.credentials_folder_path


class VisionAI:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def extractTextFromImage(self, folder_path, file_name):
        try:
            with io.open(os.path.join(folder_path, file_name), 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)
            response = self.client.text_detection(image=image)
            return response.full_text_annotation.text
        except Exception as e:
            print(e)
            return json.load('')
