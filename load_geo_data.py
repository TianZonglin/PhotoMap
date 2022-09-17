import exifread
import os
import json

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)
 
list_name=[]
path='D:\Huawei Share\Backup\HuaweiPhotos\myphone_6EB4698362B9\Camera'   #文件夹路径
listdir(path,list_name)

write = []


for item in list_name:
    if is_number(item.split("\Camera\\")[1][:1]) is False:
        with open(item, 'rb') as f:
            exif_dict = exifread.process_file(f)
            try:
                
                lon_ref = exif_dict["GPS GPSLongitudeRef"].printable
                lon = exif_dict["GPS GPSLongitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
                lon = float(lon[0]) + float(lon[1]) / 60 + float(lon[2]) / float(lon[3]) / 3600
                if lon_ref != "E":
                    lon = lon * (-1)

                # 纬度
                lat_ref = exif_dict["GPS GPSLatitudeRef"].printable
                lat = exif_dict["GPS GPSLatitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
                lat = float(lat[0]) + float(lat[1]) / 60 + float(lat[2]) / float(lat[3]) / 3600
                if lat_ref != "N":
                    lat = lat * (-1)
                #print(str(exif_dict['EXIF DateTimeOriginal'])+";"+exif_dict['Image Make'].printable + "-" + exif_dict['Image Model'].printable + ";" + (str(lat) + "," + str(lon)))
                write.append(str(exif_dict['EXIF DateTimeOriginal']) + "," 
                    + exif_dict['Image Make'].printable + "-" + exif_dict['Image Model'].printable + "," 
                    + (str(lat) + "@" + str(lon)))
                #print(str(exif_dict['EXIF DateTimeOriginal']), exif_dict['Image Make'].printable + "-" + exif_dict['Image Model'].printable + " " + (str(lat) + "," + str(lon))+'\n')

            except:
                print("error -> this picture has no geo records")

#print(json.dumps(write))              
with open('./list.json','w') as iof:     #要存入的txt             
    
    iof.write(json.dumps(write))
    iof.close()