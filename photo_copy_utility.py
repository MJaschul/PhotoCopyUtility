import os
import regex
from shutil import copyfile

from exif import Image

inputpath = 'C:\\Users\\Matthias\\Pictures\\2019-MatthiasHandy'
output = 'C:\\Users\\Matthias\\Pictures\\automated'
if not os.path.exists(output):
    os.mkdir(output)

outputdict = {'2020-11': set()}

UnsortedImages = os.listdir(inputpath)
for image in UnsortedImages:
    with open(os.path.join(inputpath, image), 'rb') as image_file:
        my_image = Image(image_file)
        p = regex.match(r'(^\d{4}):(\d{2}):', my_image.datetime)
        folder = p.group(1) + '-' + p.group(2)

        print('Datei: ' + str(image) + '\t Aufnahme ' + my_image.datetime)
        print('year \t' + p.group(1))
        print('month \t' + p.group(2))
        print(folder)
        if (folder in outputdict):
            outputdict[folder].add(image)
        else:
            outputdict.update({folder: set([image])})

print('Anzahl an Bildern ' + str(len(UnsortedImages)))

for month in outputdict:
    print(month)
    for file in outputdict[month]:
        print('\t' + file)

copies = 0
for month in outputdict:
    monthpath = os.path.join(output, month)
    if not os.path.exists(monthpath):
        os.mkdir(monthpath)
        print('create folder' + monthpath)
    for file in outputdict[month]:
        print('\t' + file + ' copied to ' + monthpath)
        copyfile(os.path.join(inputpath, file), os.path.join(monthpath, file))
        copies = copies+1

print('Number of Copied Files: ' + str(copies))

if (copies != len(UnsortedImages)):
    print('ACHTUNG: Anzahl an kopierter Dateien' + str(copies) + 'ungleich Anzahl der Inputdateien ' + str(len(UnsortedImages)))
