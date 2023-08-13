import os
import piexif
from PIL import Image
import json
from datetime import datetime

directory = "./"


for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.json'):

            print(os.path.join(root, file))

            image_path = os.path.join(root, file)[:-5]
            json_path = os.path.join(root, file)
            
            with open(json_path, 'r', encoding='utf-8') as json_file:
                info = json.load(json_file)

            try:
                title = info['title']
                image_path = os.path.join(root, title)

                create_time = int(info['creationTime']['timestamp'])
                taken_time = int(info['photoTakenTime']['timestamp'])
            
                try:
                    exif_dict = piexif.load(image_path)

                    exif_dict['Exif'][36867] = datetime.utcfromtimestamp(create_time).strftime('%Y:%m:%d %H:%M:%S')
                    exif_dict['Exif'][36868] = datetime.utcfromtimestamp(create_time).strftime('%Y:%m:%d %H:%M:%S')
                    exif_dict['0th'][306] = datetime.utcfromtimestamp(taken_time).strftime('%Y:%m:%d %H:%M:%S')

                    exif_bytes = piexif.dump(exif_dict)
                    piexif.insert(exif_bytes, image_path, image_path)
                except:
                    print("exif error "+os.path.join(root, file))
                
                os.utime(image_path,(taken_time,taken_time))
                os.utime(json_path,(taken_time,taken_time))

                if image_path[-4:] == "HEIC":
                    video_path = image_path[:-4]+"MP4"
                    print(video_path)
                    os.utime(video_path,(taken_time,taken_time))
                
            except:
                print("json error "+os.path.join(root, file))

            