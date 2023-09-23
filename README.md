# ORC-PROJECT
The python environemnt needed [3.11.5], with provided requirements.txt

pip install -r requirements.txt

### To run
python tha_ocr.py

09/23/2023

### Update list:
- paning canvas using up, down, right, left arrows
- next image function
### 2nd Updates:
- remove unused functions
- users don't need to choose the image everytime clicking on "Next image", it works automatically.
- Once program started, user just select the folder of image with {".png", ".jpg", ".jpeg", ".bmp} these file extensions, otherwise, they will be ignored (not load when use 'next image' function)
  
### Basic instruction:
1. load the initialize image folder
2. select lang need to extract
note -> we're are able to extract both Thai and Eng at the same time, but the performace doesn't quite well.
3. drag a curosr cover the desierd text
4. click on 'Extract and Copy' to Copy the text from image
5. now, we're able to paste the text anywhere


