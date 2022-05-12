import requests
import wget
import json
import os
import argparse
import zipfile
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("package", nargs="*", help="Download and install a package")
parser.add_argument("-all", action="store_true", help="Download and install all packages")
parser.add_argument("-l", "--list", action="store_true", help="List available packages")
parser.add_argument("-q", "--quiet", action="store_false", help="Quiet mode")
args = parser.parse_args()

folder_name = os.path.expandvars("%temp%/WinApt/")

if not os.path.exists(folder_name):
  os.makedirs(folder_name)
if not os.path.exists(folder_name + "packages.json"):
  wget.download("https://raw.githubusercontent.com/MehdiRtal/WinApt/main/packages.json", folder_name, bar=None)

with open(folder_name + "packages.json", "r") as f:
  data = json.load(f)

def soup(arg, arg2):
  if arg["downloader"] == "filehippo":
    response = requests.get("https://filehippo.com/download_{}/{}".format(arg["id"], arg2))
  soup = BeautifulSoup(response.text, "lxml")
  return soup

def download_link(arg):
  if data[arg]["downloader"] == "filehippo":
    download_link = soup(data[arg], "post_download/").find("script", {"type": "text/javascript", "data-qa-download-url": True})["data-qa-download-url"]
  else:
    download_link = data[arg]["url"]
  return download_link

def version(arg):
  if data[arg]["downloader"] == "filehippo":
    version = soup(data[arg], "").find("p", class_="program-header__version").text
  else:
    version = "Latest"
  return version

def download(arg):
  if args.quiet:
    print("\nDownloading {} v{}".format(arg, version(arg)))
    wget.download(download_link(arg), folder_name)
  else:
    wget.download(download_link(arg), folder_name, bar=None)

def install(arg):
  if args.quiet:
    print("\nInstalling {} v{}".format(arg, version(arg)))
  if data[arg]["installer"] == "custom":
    os.system("cmd /c start {} {}".format(file_path(arg), data[arg]["arguments"]))
  if data[arg]["installer"] == "zip":
    with zipfile.ZipFile(file_path(arg), 'r') as zip:
      zip.extractall(folder_name)
    os.system("cmd /c start {} {}".format(folder_name, data[arg]["filename"]))
  if data[arg]["installer"] == "as-is":
    os.system("cmd /c start {}".format(file_path(arg)))
  if data[arg]["installer"] == "msi":
    os.system("cmd /c msiexec /i {} /qn /norestart".format(file_path(arg)))
  if data[arg]["installer"] == "innosetup":
    os.system("cmd /c start {} /VERYSILENT /NORESTART".format(file_path(arg)))
  if data[arg]["installer"] == "installshield":
    os.system("cmd /c start {} /s".format(file_path(arg)))
  if data[arg]["installer"] == "nsis":
    os.system("cmd /c start {} /S".format(file_path(arg)))
  if data[arg]["installer"] == "squirrel":
    os.system("cmd /c start {} -s".format(file_path(arg)))

def file_path(arg):
  file_name = wget.filename_from_url(download_link(arg))
  return folder_name + file_name

def deploy():
  for package in data if args.all or args.list else data and args.package:
    try:
      if "version" not in data or data[package]["version"] != version(package):
        if data[package]["downloader"] != "custom":
          data[package]["version"] = version(package)
          with open(folder_name + "packages.json", "w") as f:
            json.dump(data, f, indent = 2)
      if args.list:
        print(package + " v" + version(package))
      else:
        if os.path.exists(file_path(package)):
          if data[package]["version"] == version(package) or data[package]["version"] not in data:
            install(package)
        else:
          if os.path.exists(file_path(package)):
            os.remove(file_path(package))
          download(package)
          install(package)
    except AttributeError:
      if args.quiet:
        print("\n{} not found.".format(package))
      else: pass

if __name__ == "__main__":
	deploy()
