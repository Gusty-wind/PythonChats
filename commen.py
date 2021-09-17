import re
import os,json, io
import base64
import datetime
from pathlib import Path
from PIL import Image
from pydantic.types import FilePath
#init create new dir and file

def get_user_file_name_path (username):
    date = datetime.datetime.now()
    format_dir_name = str(username) + str(date.year)
    file_name = str(username) + '_' + str(date.year) + str(date.month) + str(date.day)
    file_patch_list = {}
    file_patch_list["path"] =  format_dir_name
    file_patch_list["path_url"] = format_dir_name + '/' + file_name + '.txt'
    return file_patch_list

def created_file(filename):
    file_patch_list = get_user_file_name_path(filename)
    # return
    print(file_patch_list, '##')
    if not os.path.isdir(file_patch_list['path']):
        os.makedirs(file_patch_list['path'])
        image_path = file_patch_list['path'] + '/image'
        os.makedirs(image_path)
    if not os.path.isfile(file_patch_list['path_url']):
        fd = open(file_patch_list['path_url'], mode="w", encoding="utf-8")
        fd.close()
        return file_patch_list['path_url']
    else:
        return file_patch_list['path_url']
#append data to file
def file_write_message(filename, message, parentNode):
    file_path = created_file(filename)
    if os.path.isfile(file_path):
        with open(file_path, "a+") as file_object:
            file_object.seek(0)
            data = file_object.read(1000)
            if len(data) > 0:
                file_object.write("\n")
            file_object.write(str(message))
        # file_object.write(json.dumps(message))
#remove file
def file_remove(filenames, dirname):
    os.remove(filenames)
    os.rmdir(dirname)
#read file

def file_read_message(filenames):
    file_path = get_user_file_name_path(filenames)
    fileArry = []
    if os.path.isfile(file_path['path_url']):
        with open(file_path['path_url'], "r+") as file:
            for line in file.readlines():
                line = line.strip("\n")
                fileArry.append(json.dumps(line))
            file.close()
            return fileArry
    else:
        print ('No exist file')

def created_image_file():
    """
        save the images to the server
    """


    pass

def get_image_store_path(img_name, username):
    file_path = get_user_file_name_path(username)['path']
    path = file_path + '/image/' + img_name
    return path
def stroe_image_to_directory(img_name, img_base64, img_type, username):

    img_path = get_image_store_path(img_name, username)
    img_format_type = img_type[img_type.index('/') +1:]
    """
        change the front base64 to python standard by base64
    """                  
    img_base64 = re.sub('^data:image/.+;base64,', '', img_base64)
    """
        save image path
    """
    img = Image.open(io.BytesIO(base64.b64decode(img_base64)))
    img.save(img_path, img_format_type)