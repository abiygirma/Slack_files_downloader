# Slack files downloader

Author: abiysemail@gmail.com
Created date: 2022-10-05

On slack the option for Export Data is limisted by giving you only the json files with a lot of links to your files. It is difficult to find those links and download the file manually. There must be a mechanisem to look for file links in json files and download them automatically. 

This program search for every files links in each json documents downloaded from slack (Slack Export Data), and download them under a folder name with respected channel name.

   - Extract the zip file that is downloaded from slack export and put them under one folder. 
   - Create new folder under the folder you put the extracted files.
   - Put this python file under the new folder you created.
   - The new folder must have all permission enabled, because this code will create files and folders under it.
   - Run 
