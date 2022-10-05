####################################################################
#
#   Slack files downloader
#   Author: abiysemail @g mail .com
#   Created date: 2022-10-05
#
#   This program search for every files in each json documents 
#   downlaoded from slack (Slack Export Data), and download 
#   them under a folder name with respected channel name.
#
#   - Extract the zip file that is downloaded from slack export
#     and put them under one folder. 
#   - Create new folder under the folder you put the extracted 
#     files.
#   - Put this python file under the new folder you created.
#   - The new folder must have all permission enabled, because
#     this code will create files and folders under it.
#   - Run 
#   
#############################################################

from genericpath import exists, isdir
import json
import os
import requests


print("I will search for every files in each json documents and download them. Wish me luck :) ")

def is_json_file(file_name: str):
    token = file_name.split(".")
    
    if token[len(token)-1] == "json":
        return True
    return False

def get_file_name_from_url(url):
    token = url.split("/")
    return token[len(token)-1]
    

def finde_all_json(slack_export_dir):
    dir_list = os.listdir(slack_export_dir)
    json_file_list = []
    
    for dir_name in dir_list:
        if isdir(slack_export_dir + dir_name) and dir_name != "_download_files":
            file_list = os.listdir(slack_export_dir + dir_name + "/")
            for file_name in file_list:
                if is_json_file(file_name=file_name):
                    json_file_list.append({"root_dir": slack_export_dir,"dir_name": dir_name,"json_file_name": file_name})
    
    return json_file_list

def read_json_text(json_file_path):
    json_file = open(json_file_path, "r")
    
    json_text = json_file.read()
    
    json_file.close()
    
    return json_text

def populate_file_list_from_json(json_file_list):
    json_decoder = json.JSONDecoder()
    downloadeable_file_list = []
    
    for json_file in json_file_list:
        root_dir = json_file["root_dir"]
        dir_name = json_file["dir_name"]
        json_file_name = json_file["json_file_name"]
        
        json_file_path =  root_dir + dir_name + "/" + json_file_name
        
        json_text = read_json_text(json_file_path=json_file_path)
        json_object = json_decoder.decode(json_text)
        
        for _object in json_object:
            #print(_object)
            #print("\n\n--\n\n")
            if "files" in _object:
                for file in _object["files"]:
                    downloadeable_file_list.append({"root_dir": root_dir,"dir_name": dir_name,"json_file_name": json_file_name, "permalink": file["permalink"], "url_private_download" : file["url_private_download"]})
    
    return downloadeable_file_list

def download_file(url, folder_path, file_name, retry=1):
    timeout = 300 * retry
    print(url)
    try:
        rs = requests.get(url=url, timeout=timeout)
        out_put_file = open(folder_path + "/" + file_name, "wb")
        out_put_file.write(rs.content)
        out_put_file.close()
    except Exception as e:
        print("ERROR: Faild to download.")
        print(str(e))
        return False
    
    return True    

def download_each_files(downloadeable_file_list, retry=1):
    faild_to_download = []
    cnt = 1
    for file_detail in downloadeable_file_list:
        folder_path = f"./{file_detail['dir_name']}"
        url = file_detail["url_private_download"]
        file_name = get_file_name_from_url(file_detail["permalink"])
        
        if not isdir(folder_path):
            os.mkdir(folder_path)
        
        i = 2
        while exists(folder_path + "/" + file_name):
            if not exists(f"{folder_path}/{i}_{file_name}"):
                file_name = f"{i}_{file_name}"
            i += 1
        
        print(f"\n{cnt} of {len(downloadeable_file_list)}\t{file_name}")
        cnt += 1
        if not download_file(url=url, folder_path=folder_path, file_name=file_name, retry=retry):
            faild_to_download.append(file_detail)
    
    if len(faild_to_download) > 0:
        print("\nThere are some files faild to download. Do you want to retry")
        x = input("Y/N : ")
        if x == "Y" or x == "y":
            download_each_files(downloadeable_file_list=faild_to_download, retry=retry+1)
    else:
        print("\nAll files are downloaded successfully.")
        
        

def main():
    slack_export_dir = "../"
    
    json_file_list = finde_all_json(slack_export_dir)
    
    downloadeable_file_list = populate_file_list_from_json(json_file_list=json_file_list)
    
    print (f"\n{len(downloadeable_file_list)} files are found.")
    
    print("\nDownloading files...")
    download_each_files(downloadeable_file_list=downloadeable_file_list)
    print("\nFinished")
    

main()