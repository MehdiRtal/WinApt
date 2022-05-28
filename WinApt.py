import requests
import wget
import json
import os
import argparse
import zipfile
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("package", nargs="*", help="Download and install a package.")
parser.add_argument("-all", action="store_true", help="Download and install all packages.")
parser.add_argument("-l", "--list", action="store_true", help="List available packages.")
parser.add_argument("-q", "--quiet", action="store_false", help="Quiet mode.")
parser.add_argument("-s", "--schedule", nargs="?", metavar="", help="Schedule packages as a task.")
args = parser.parse_args()
folder_name = os.path.expandvars("%temp%/WinApt/")

if not os.path.exists(folder_name):
  os.makedirs(folder_name)
if not os.path.exists(folder_name + "packages.json"):
  wget.download("https://raw.githubusercontent.com/MehdiRtal/WinApt/main/packages.json", folder_name, bar=None)
with open(folder_name + "packages.json", "r") as f:
  data = json.load(f)

def soup(arg, arg2 = ""):
  if arg["downloader"] == "filehippo":
    response = requests.get(f"https://filehippo.com/download_{arg["id"]}/{arg2}"
  return BeautifulSoup(response.text, "lxml")

def download_link(arg):
  if data[arg]["downloader"] == "filehippo":
    return soup(data[arg], "post_download/").find("script", {"type": "text/javascript", "data-qa-download-url": True})["data-qa-download-url"]
  else:
    return data[arg]["url"]

def version(arg):
  if data[arg]["downloader"] == "filehippo":
    return soup(data[arg]).find("p", class_="program-header__version").text
  else:
    return "Latest"

def download(arg):
  if args.quiet:
    print(f"\nDownloading {arg} v{version(arg)}"
    wget.download(download_link(arg), folder_name)
  else:
    wget.download(download_link(arg), folder_name, bar=None)

def install(arg):
  if args.quiet:
    print(f"\nInstalling {arg} v{version(arg)}.."
  if data[arg]["installer"] == "custom":
    os.system(f"cmd /c start {file_path(arg)} {data[arg]["arguments"]}"
  if data[arg]["installer"] == "zip":
    if not os.path.exists(folder_name + arg):
      os.makedirs(folder_name + arg)
    with zipfile.ZipFile(file_path(arg), "r") as zip:
      zip.extractall(folder_name + arg)
    os.system(f"cmd /c start {folder_name} {data[arg]["filename"]}"
  if data[arg]["installer"] == "as-is":
    os.system(f"cmd /c start {file_path(arg)}"
  if data[arg]["installer"] == "msi":
    os.system(f"cmd /c msiexec /i {file_path(arg)} /qn /norestart"
  if data[arg]["installer"] == "innosetup":
    os.system(f"cmd /c start {file_path(arg)} /VERYSILENT /NORESTART"
  if data[arg]["installer"] == "installshield":
    os.system(f"cmd /c start {file_path(arg)} /s"
  if data[arg]["installer"] == "nsis":
    os.system(f"cmd /c start {file_path(arg)} /S"
  if data[arg]["installer"] == "squirrel":
    os.system(f"cmd /c start {file_path(arg)} -s"

def file_path(arg):
  return folder_name + wget.filename_from_url(download_link(arg))

def schedule():
  if args.schedule == "start":
    print("Starting the task schedulling..")
    os.system("cmd /c schtasks /run /tn WinApt")
  elif args.schedule == "stop":
    print("Stopping the task schedulling..")
    os.system("cmd /c schtasks /end /tn WinApt")
  else:
    print("\nSchedulling packages as a task..")
    if args.schedule.endswith("h"):
      sc = "HOURLY"
      mo = args.schedule.split("h")[0]
    if args.schedule.endswith("mn"):
      sc = "MINUTE"
      mo = args.schedule.split("mn")[0]
    if args.schedule.endswith("d"):
      sc = "DAILY"
      mo = args.schedule.split("d")[0]
    if args.schedule.endswith("w"):
      sc = "WEEKLY"
      mo = args.schedule.split("w")[0]
    if args.schedule == "onstart":
      sc = "ONSTART"
    if args.schedule == "onidle":
      sc = "ONIDLE"
    os.system(f"cmd /c schtasks /create /sc {sc} /mo {mo} /tn WinApt /tr start {folder_name}WinApt.exe {" ".join(args.package)}"

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
          if "version" not in data[package] or data[package]["version"] == version(package):
            install(package)
        else:
          if os.path.exists(file_path(package)):
            os.remove(file_path(package))
          download(package)
          install(package)
    except AttributeError:
      if args.quiet:
        print(f"\n{package} not found."
      else: pass

if __name__ == "__main__":
  if args.schedule:
    schedule()
  else:
    deploy()
