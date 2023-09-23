import pytesseract
from PIL import Image
import cv2
import numpy as np
from pytesseract import Output

# selected_area = Image.open('/Users/noppanan/Desktop/orc-proj/orc-proj-ddata/screenshots/test.png')
img = cv2.imread('/Users/noppanan/Desktop/orc-proj/orc-proj-ddata/screenshots/selected_area_screenshot.png')
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(img, -1, sharpen_kernel)
cv2.imwrite('screenshots/shapened.png', sharpen)
extracted_text = pytesseract.image_to_string(sharpen, lang='tha+eng')
print(extracted_text)