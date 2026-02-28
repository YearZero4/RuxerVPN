from bs4 import BeautifulSoup as b
import requests, re, json, random, os, subprocess, threading, queue, sys


vpn_process = None
folder_saved_vpn = os.path.join(os.environ.get('APPDATA', ''), 'RuxerVPN', 'saved_vpn')
fullPath = os.path.join(folder_saved_vpn, "vpn.ovpn")
nameFileCredentials = "auth.txt"
pathCredentials = os.path.join(folder_saved_vpn, nameFileCredentials)


def get_openvpn_path():
 if getattr(sys, 'frozen', False):
  base_path = os.path.dirname(sys.executable)
  return os.path.join(base_path, "_internal", "src", "openvpn64", "openvpn.exe")
 else:
  return os.path.join("src", "openvpn64", "openvpn.exe")

openvpn64 = get_openvpn_path()

if not os.path.exists(folder_saved_vpn):
 os.makedirs(folder_saved_vpn)

def reqLink():
 link = "https://www.vpnbook.com/es/freevpn/openvpn"
 req = requests.get(link)
 data = req.text
 return data

def obtenerData():
 data = reqLink()
 soup = b(data, 'html.parser')
 script = soup.find_all('script')
 code = soup.find_all('code')
 found = []
 nameArray = []
 hostnameArray = []
 ipAddressArray = []
 allDataDict = {}

 for c in code:
  if len(c.text) < 12:
   found.append(c.text)
 allDataDict["password"] = found[-1]
 dataDict = {}
 
 for c in script:
  if c.string and 'ipAddress' in c.string:
   script = str(c)
   sc = script.split(r'servers\":[')[1].replace(",", "\n").replace(r'\\"', "").replace(
       '\\"', '').replace('{', '').replace('}', '').replace(":", " : ")
   lines = sc.split("\n")
   for line in lines:
    if line.strip().startswith(("name", "hostname", "ipAddress")):
     line = line.strip()
     if line.startswith("name :"):
      nameArray.append(line.split(":")[-1].strip())
     elif line.startswith("hostname :"):
      hostnameArray.append(line.split(":")[-1].strip())
     elif line.startswith("ipAddress :"):
      ipAddressArray.append(line.split(":")[-1].strip())
 
 for name, hostname, ip in zip(nameArray, hostnameArray, ipAddressArray):
  dataDict[name] = {"hostname": hostname, "ip": ip}
 allDataDict["data"] = dataDict
 return allDataDict

try:
 data = obtenerData()["data"]
 password = obtenerData()["password"]
except exceptions.ConnectionError:
 print("Error de conexion...")

def servers():
 availableServers = []
 for server in data.keys():
  availableServers.append(server)
 return availableServers

def linkVPN(nameServer, protocol):
 if protocol == 443 or protocol == 80:
  protocol = f"tcp{protocol}"
 else:
  protocol = f"udp{protocol}"
 dictServer = data[nameServer]
 link = f"https://www.vpnbook.com/api/openvpn?hostname={dictServer["hostname"]}&protocol={protocol}&ip={dictServer["ip"]}"
 return link

def linkRandom():
 rangeServers = len(servers()) - 1
 numberRandom = random.randint(0, rangeServers)
 serverRandom = servers()[numberRandom]
 link = linkVPN(serverRandom, 443)
 return link

def saveFile(content):
 with open(fullPath, "wb") as f:
  f.write(content)
  f.close()

def addCredentials():
 with open(fullPath, 'r') as f:
  lineas = f.readlines()
 lineas = [l for l in lineas if 'auth-user-pass' not in l]
 with open(fullPath, 'w') as f:
  for l in lineas:
   f.write(l)
   if 'remote' in l:
    f.write(f'auth-user-pass {os.path.join(folder_saved_vpn, nameFileCredentials).replace(os.sep, "/")}\n')

def save_credentials():
 with open(pathCredentials, "w") as f:
  f.write(f"vpnbook\n{password}")
  f.close()

def disconnect():
 global vpn_process
 if vpn_process:
  try:
   vpn_process.terminate()
  except:
   pass
  vpn_process = None


def connect(link, callback=None):
 print(f"Buscando openvpn en: {openvpn64}")
 print(f"Existe?: {os.path.exists(openvpn64)}")
 global vpn_process
 vpn_process = None

 if not os.path.exists(folder_saved_vpn):
  os.makedirs(folder_saved_vpn)
 try:
  file = requests.get(link).content
  saveFile(file)
  save_credentials()
  addCredentials()
 except:
  print("Error al descargar...")
  return

 # process = subprocess.Popen([openvpn64, fullPath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
 process = subprocess.Popen(
    [openvpn64, fullPath],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    creationflags=subprocess.CREATE_NO_WINDOW 
)
 vpn_process = process

 for line in process.stdout:
  print(line.strip())
  if "Initialization Sequence Completed" in line:
   print("VPN CONNECTED")
   if callback:
    callback()

 process.wait()
