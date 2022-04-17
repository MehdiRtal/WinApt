import requests
import wget
import json
import re
import os
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument("package", nargs="*", help="Download and Install a package")
parser.add_argument("-d", "--download", action="store_true", help="Install a package only")
parser.add_argument("-q", "--quiet", action="store_false", help="Execute silently")
parser.add_argument("-l", "--list", action="store_true", help="List Available Packages")
args = parser.parse_args()

if not os.path.exists("packages.json"):
  wget.download("https://raw.githubusercontent.com/MehdiRtal/WinApt/main/packages.json", bar=None)
data = json.load(open("packages.json", "r"))

folder_name = "cache/"

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
    print("\nDownloading {}...".format(arg))
    wget.download(download_link(arg), folder_name)
  else:
    wget.download(download_link(arg), folder_name, bar=None)

def install(arg):
  if args.quiet:
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
  for package in data if "".join(args.package) == "all" or args.list else data and args.package:
    try:
      if not os.path.exists(folder_name):
         os.makedirs(folder_name)
      if "version" not in data:
        data[package]["version"] = version(package)
        json.dump(data, open("packages.json", "w"), indent = 2)
      if args.list:
        print(package + " v" + version(package))
      elif args.download:
        if data[package]["version"] != version(package) and os.path.exists(file_path(package)):
          os.remove(file_path(package))
        if not os.path.exists(file_path(package)):
          download(package)
      elif data[package]["version"] == version(package) and os.path.exists(file_path(package)):
        install(package)
      else:
        if os.path.exists(file_path(package)):
          os.remove(file_path(package))
        download(package)
        install(package)
    except:
      if args.quiet:
        print("\n{} not found.".format(package))
      else:
        pass

if __name__ == "__main__":
  deploy()
