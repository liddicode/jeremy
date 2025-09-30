from PIL import Image

import pytesseract
import os
print(os.getcwd())
print(pytesseract.image_to_string(Image.open('./../../Pictures/Testrecipt.jpeg')))