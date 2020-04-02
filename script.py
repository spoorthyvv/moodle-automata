#!/usr/bin/python3








import base64
#import cv2
import sys
import os
import time



print(
"""
    _    _                      __  __                 _ _      
   / \  | |_   ____ _ ___      |  \/  | ___   ___   __| | | ___ 
  / _ \ | \ \ / / _` / __|_____| |\/| |/ _ \ / _ \ / _` | |/ _ \\
 / ___ \| |\ V / (_| \__ \_____| |  | | (_) | (_) | (_| | |  __/
/_/   \_\_| \_/ \__,_|___/     |_|  |_|\___/ \___/ \__,_|_|\___|
                                                                
                                                               
""")


dir = input('Enter the folder/directory >>> ')

print()
print()

output_file = input('Output File  >>> ')


files = os.listdir(dir)

questions, descriptions = [], []

for file in files:
    if 'Q' in file:
        questions.append(file)
    elif 'A' in file:
        descriptions.append(file)


questions.sort(key=lambda x: int(x.strip('Q').strip('.png')) )
descriptions.sort(key=lambda x: int(x.strip('A').strip('.png')))



print(questions)
print(descriptions)




answers = {}

with  open( os.path.join(dir, 'answers.txt')) as answers_processor:
    paper_format  = answers_processor.readline()
    for line in answers_processor.readlines():
        question, answer = line.strip().split('=')
        answers[question] = int(answer) - 1

# print(answers)


def jpeg_res(filename):

    with open(filename,'rb') as img_file:

       # height of image (in 2 bytes) is at 164th position
       img_file.seek(163)

       # read the 2 bytes
       a = img_file.read(2)

       # calculate height
       height = (a[0] << 8) + a[1]

       # next 2 bytes is width
       a = img_file.read(2)

       # calculate width
       width = (a[0] << 8) + a[1]

    return width, height




template = '''
::{0}::[html]<p><img src\="data\:image/png;base64,{1}" alt\="" role\="presentation" class\="img-responsive atto_image_button_text-bottom" width\="{2}" height\="{3}"><br></p>{{
    {4}<p>1<br></p>
    {5}<p>2<br></p>
    {6}<p>3<br></p>
    {7}<p>4<br></p>
    ####<p><img src\="data\:image/png;base64,{8}" alt\="" role\="presentation" class\="img-responsive atto_image_button_text-bottom" width\="{9}" height\="{10}"><br></p>
}}

'''


with open(output_file, 'w') as out_file:
    for question, description in zip(questions, descriptions):

        num = question.strip('Q').strip('.png')
        
        question, description = os.path.join(dir, question), os.path.join(dir, description) 
        height1, width1 = jpeg_res(question)
        height2, width2 = jpeg_res(description)

        if paper_format == 'cet': 
             initial = ['~' for  _  in range(4) ]
        elif paper_format in {'neet', 'jee'} :
             initial = ['~%-25%' for  _  in range(4) ]        
               
        initial[ answers[num] ] = '='
        one, two, three, four = initial

        with open(question, "rb") as image_file:
           encoded_string1 = base64.b64encode(image_file.read()).decode()

        with open(description, "rb") as image_file:
           encoded_string2 = base64.b64encode(image_file.read()).decode()

        out_file.write(template.format(num, encoded_string1, width1, height1, one, two, three, four, encoded_string2, width2, height2  ) )



print('Process completed ........')
time.sleep(1)
sys.exit(0)
