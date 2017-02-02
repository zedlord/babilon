# Zelda Zeegers
# 11397705

from PIL import Image
import os
import csv
import json

images = []
years = []

# folder is the name of the painting folder. Also it is the artist
folder = "Dali"
old_year = 0
# loop over all files in folder and get the rgb value of all pixels
for filename in os.listdir(folder):
    im = Image.open(folder + '\\' + filename)
    pix = im.load()
    values = []
    [width, length] = im.size
    for i in range (0,width-1):
        for j in range (0,length-1):
            values.append(pix[i,j])
    # get the sum of all the pixels
    avg = [float(sum(col))/len(col) for col in zip(*values)]

    # get the year from the filename whene there are more paintings in one
    # year the values should also be combined
    if len(filename) > 8:
        split = filename.split(' ')
    else:
        split = filename.split('.')
    year = split[0]
    if year == old_year:
        images.append([avg, filename])
        avg = [avg, old_avg]
        old_avg = [float(sum(col))/len(col) for col in zip(*avg)]
        years.pop()
    else:
        images.append([avg,filename])
        old_avg = avg
        old_year = year
    tot = sum(old_avg)
    years.append([old_avg, tot, year])

# write the data for each year to the jsonfile
length = len(years)
jsonfiley = open(folder + '_year_data.json', 'w')
i = 0
jsonfiley.write("[\n")
for list in years:
    red = (100 * list[0][0])/list[1]
    green = (100 * list[0][1])/list[1]
    blue = (100 * list[0][2])/list[1]
    i += 1
    json.dump(({"year": list[2], "red": red, "green": green, "blue": blue, "total": list[1]}), jsonfiley, indent = 4)
    if i < length:
        jsonfiley.write(",\n")
jsonfiley.write("\n]")

# write the data for each painting to the other jsonfile
length2 = len(images)
jsonfilei = open(folder + '_images_data.json', 'w')
i = 0
jsonfilei.write('[')
for list in images:
        jsonfilei.write('{"name":"' + list[1] + '",\n')
        jsonfilei.write('"values":[\n')
        red = (100 * list[0][0])/sum(list[0])
        green = (100 * list[0][1])/sum(list[0])
        blue = (100 * list[0][2])/sum(list[0])
        i += 1
        json.dump(({"color":"red", "ratio": red}),jsonfilei)
        jsonfilei.write(',\n')
        json.dump(({"color":"green", "ratio": green}),jsonfilei)
        jsonfilei.write(',\n')
        json.dump(({"color":"blue", "ratio": blue}),jsonfilei)
        jsonfilei.write(']')
        jsonfilei.write("\n}")
        if i < length2:
            jsonfilei.write(",\n")
jsonfilei.write(']')
