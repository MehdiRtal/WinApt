import requests
import wget
import json
import re
import os
from bs4 import BeautifulSoup

with open("config.json", "r") as f:
  data = json.load(f)

def download_link(arg):
  url = requests.get("https://filehippo.com/download_{}/post_download/".format(arg)).text
  soup = BeautifulSoup(url, "lxml")
  download_link = soup.find("script", {"type": "text/javascript", "data-qa-download-url": True})["data-qa-download-url"]
  return download_link

def version(arg):
  url = requests.get("https://filehippo.com/download_{}/post_download/".format(arg)).text
  soup = BeautifulSoup(url, "lxml")
  version = "".join(re.findall("\d|[.]", soup.find("p", class_="program-header-inline__version").text))
  return version

def file_name(arg):
  file_name = download_link(arg).split("&Filename=", 1)[1]
  return file_name

def installer(arg):
  if data[arg]["installer"] == "custom":
    os.system("cmd /c start cache/{} {}".format(file_name(arg), data[arg]["arguments"]))
  if data[arg]["installer"] == "msi":
    os.system("cmd /c msiexec /i cache/{} /qn /norestart".format(file_name(arg)))

for id in data:
  if data[id]["version"] == version(id):
    installer(id)
  else:
    data[id]["version"] = version(id)
    open("config.json", "w").json.dump(data, f, indent = 4)
    if os.path.exists("cache/" + file_name(id)):
        os.remove("cache/" + file_name(id))
    wget.download(download_link(id), "cache/")
    installer(id)
    