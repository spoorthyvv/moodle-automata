#!/usr/bin/python3








import base64
import cv2
import sys
import os





dir = sys.argv[1]

files = os.listdir(dir)

questions, descriptions = [], []

for file in files:
    if 'Q' in file:
        questions.append(file)
    elif 'A' in file:
        descriptions.append(file)


questions.sort()
descriptions.sort()



print(questions)
print(descriptions)




answers = {}

with  open( os.path.join(dir, 'answers.txt')) as answers_processor:
    format  = answers_processor.readline()
    for line in answers_processor.readlines():
        question, answer = line.strip().split(',')
        answers[question] = int(answer)

# print(answers)





template = '''
::{0}::[html]<p><img src\="data\:image/png;base64,{1}" alt\="" role\="presentation" class\="img-responsive atto_image_button_text-bottom" width\="{2}" height\="{3}"><br></p>{{
    {4}<p>1<br></p>
    {5}<p>2<br></p>
    {6}<p>3<br></p>
    {7}<p>4<br></p>
    ####<p><img src\="data\:image/png;base64,{8}" alt\="" role\="presentation" class\="img-responsive atto_image_button_text-bottom" width\="{9}" height\="{10}"><br></p>
}}

'''


with open(sys.argv[2], 'w') as out_file:
    for question, description in zip(questions, descriptions):

        num = question.strip('Q').strip('.png')
        
        question, description = os.path.join(dir, question), os.path.join(dir, description) 
        height1, width1, _ = cv2.imread(question).shape
        height2, width2, _ = cv2.imread(description).shape


        initial = ['~' for  _  in range(4) ]
        initial[ answers[num] ] = '='
        one, two, three, four = initial

        with open(question, "rb") as image_file:
           encoded_string1 = base64.b64encode(image_file.read()).decode()

        with open(description, "rb") as image_file:
           encoded_string2 = base64.b64encode(image_file.read()).decode()

        out_file.write(template.format(num, encoded_string1, width1, height1, one, two, three, four, encoded_string2, width2, height2  ) )



