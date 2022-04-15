import requests
import wget
import json
import re
import os
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument("package", nargs="+")
parser.add_argument("-d", "--download", action="store_true")
parser.add_argument("-q", "--quiet", action="store_true")
args = parser.parse_args()
folder_name = "cache/"

with open("config.json", "r") as f:
  data = json.load(f)

def download_link(arg):
  url = requests.get("https://filehippo.com/download_{}/post_download/".format(arg)).text
  soup = BeautifulSoup(url, "lxml")
  download_link = soup.find("script", {"type": "text/javascript", "data-qa-download-url": True})["data-qa-download-url"]
  if arg == "spotify":
    download_link = "https://download.spotify.com/SpotifyFullSetup.exe"
  return download_link

def version(arg):
  url = requests.get("https://filehippo.com/download_{}/post_download/".format(arg)).text
  soup = BeautifulSoup(url, "lxml")
  version = "".join(re.findall("\d|[.]", soup.find("p", class_="program-header-inline__version").text))
  return version

def download(arg):
  if args.quiet:
    wget.download(download_link(arg), folder_name, bar=None)
  else:
    print("\nDownloading {}...".format(arg))
    wget.download(download_link(arg), folder_name)

def install(arg):
  if not args.quiet:
    print("\nInstalling {}...".format(arg))
  if data[arg]["installer"] == "custom":
    os.system("cmd /c start cache/{} {}".format(file_name(arg), data[arg]["arguments"]))
  if data[arg]["installer"] == "msi":
    os.system("cmd /c msiexec /i cache/{} /qn /norestart".format(file_name(arg)))
  if data[arg]["installer"] == "innosetup":
    os.system("cmd /c start cache/{} /VERYSILENT /NORESTART".format(file_name(arg)))
  if data[arg]["installer"] == "installshield":
    os.system("cmd /c start cache/{} /s".format(file_name(arg)))
  if data[arg]["installer"] == "nsis":
    os.system("cmd /c start cache/{} /S".format(file_name(arg)))
  if data[arg]["installer"] == "squirrel":
    os.system("cmd /c start cache/{} -s".format(file_name(arg)))

def file_name(arg):
  return os.path.basename(urlparse(download_link(arg)).path)

def file_path(arg):
  return folder_name + file_name(arg)

def deploy():
  for package in data and args.package:
    if package not in data:
      if not args.quiet:
        print("\n{} not found.".format(package))
    elif args.download:
      if data[package]["version"] == version(package) and os.path.exists(file_path(package)):
        download(package)
    else:
      if data[package]["version"] == version(package) and os.path.exists(file_path(package)):
        install(package)
      else:
        data[package]["version"] = version(package)
        json.dump(data, open("config.json", "w"), indent = 4)
        if os.path.exists(file_path(package)):
          os.remove(file_path(package))
        download(package)
        install(package)

if __name__ == "__main__":
  deploy()
