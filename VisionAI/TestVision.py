import VisionConfig as config

import VisionAI as vi

FILE_NAME = config.TEST_IMAGE_NAME
FOLDER_PATH = config.INPUT_PATH
vision = vi.VisionAI()
resp = vision.extractTextFromImage(FOLDER_PATH, FILE_NAME)
print(resp)
