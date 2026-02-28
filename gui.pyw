import pyuac, win32security, sys, threading, requests, subprocess, os
from PySide6.QtWidgets import QApplication, QPushButton, QLabel, QWidget, QVBoxLayout, QScrollArea
from PySide6.QtCore import Qt, QMetaObject, Q_ARG
import src.vpn as vpn

if not pyuac.isUserAdmin():
 print("Re-running as administrator...")
 pyuac.runAsAdmin()
 sys.exit()


msgGeoWait = "Geolocating, please wait..."
def geo():
 try:
  response = requests.get("http://ip-api.com/json/")
  data = response.json()
  ip = data.get("query")
  country = data.get("country")
  QMetaObject.invokeMethod(info_geo, "setText", Qt.ConnectionType.QueuedConnection, Q_ARG(str, f"IP address: <span style='color:#03FF07;'>{ip}</span>\nCountry: <span style='color:#03FF07;'>{country}</span>"))
 except:
  QMetaObject.invokeMethod(info_geo, "setText", Qt.ConnectionType.QueuedConnection, Q_ARG(str, f"Geolocation Error"))


def on_vpn_connected():
 btn_connect.setText("VPN Connected")
 info_geo.setText(msgGeoWait)
 geo()

def killProcess():
 vpn.disconnect()
 if os.name == "nt":
  subprocess.run("taskkill /f /im openvpn.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def kill_and_geo():
 info_geo.setText(msgGeoWait)
 killProcess()
 geo()


def clickDisconnectVPN():
 btn_connect.setText("Disconnected")
 threading.Thread(target=kill_and_geo).start()


def threadDisconnectVPN():
 hilo1 = threading.Thread(target=killProcess)
 hilo1.start()


def connectToSelected(serverName):
 hilo1 = threading.Thread(target=killProcess)
 hilo1.start()
 btn_connect.setText("Connecting...")
 hilo = threading.Thread(target=vpn.connect, args=(vpn.linkVPN(serverName, 443), on_vpn_connected))
 hilo.daemon = True
 hilo.start()
 back()


def connect():
 hilo1 = threading.Thread(target=killProcess)
 hilo1.start()
 btn_connect.setText("Connecting...")
 hilo = threading.Thread(target=vpn.connect, args=(vpn.linkRandom(), on_vpn_connected))
 hilo.daemon = True
 hilo.start()

def back():
 if hasattr(window, 'scroll'):
  window.scroll.hide()

 for widget in window.findChildren(QPushButton):
  if widget.objectName() == "btnNameServer":
   widget.hide()
   widget.deleteLater()
 btn_connect.show()
 btn_disconnect.show()
 info_geo.show()
 btn_other_vpn.setText("Other VPN")
 btn_other_vpn.clicked.disconnect()
 btn_other_vpn.clicked.connect(otherVPNs)


def otherVPNs():
 btn_other_vpn.setText("Back")
 btn_other_vpn.clicked.disconnect()
 btn_other_vpn.clicked.connect(back)
 btn_connect.hide()
 btn_disconnect.hide()
 info_geo.hide()
 
 scroll = QScrollArea(window)
 scroll.setWidgetResizable(True)
 scroll.setGeometry(10, 40, 280, 215)
 scroll_widget = QWidget()
 scroll_layout = QVBoxLayout(scroll_widget)
 for nameServer in vpn.servers():
  btnNameServer = QPushButton(nameServer)
  btnNameServer.setObjectName("btnNameServer")
  btnNameServer.clicked.connect(lambda checked, n=nameServer: connectToSelected(n))
  scroll_layout.addWidget(btnNameServer)
 scroll.setWidget(scroll_widget)
 scroll.show()
 window.scroll = scroll


app = QApplication(sys.argv)
app.setStyleSheet("""

QWidget{
 background:#000;
 color:#fff;
}

#btn_connect{
 background:#00CC0B;
 color:#000;
 font-weight:bold;
 border:1px solid #fff;
 border-radius: 85px;
 font-size:20px;
}

#btn_connect:hover{
 background: #00990A;
 border: 2px solid #fff;
}

#info_geo{
 font-weight:bold;
}

#author{
 font-size:10px;
 font-style: italic;
 color:#888;
 font-weight:bold;
}

#btn_other_vpn{
 font-weight:bold;
 background:#333;
}

#btn_other_vpn:hover{
 color: #00CC0B;
}

#btnNameServer{
 background:#127D00;
}

#btnNameServer:hover{
 font-weight:bold;
 background: #0E5C00;
 border:1px solid #fff;

}

#btn_disconnect{
 font-weight:bold;

}

#btn_disconnect:hover{
 background:#111;
 color: #ff0;
}

QScrollArea{
 border: none;
}

 """)

window = QWidget()
window.resize(300, 300)
window.setWindowTitle("Ruxer VPN v1.0")

layout = QVBoxLayout(window)
layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

btn_connect = QPushButton("Connect")
btn_connect.setFixedSize(170, 170)
btn_connect.setObjectName("btn_connect")
btn_connect.clicked.connect(connect)

info_geo = QLabel(msgGeoWait)
info_geo.setObjectName("info_geo")
info_geo.setAlignment(Qt.AlignmentFlag.AlignCenter)
info_geo.setWordWrap(True)

layout.addWidget(btn_connect)
layout.addWidget(info_geo)


author = QLabel("PGX <span style='color:#00CC0B;'>Creator</span>", window)
author.setGeometry(5, 265, 80, 40)
author.setObjectName("author")


btn_disconnect = QPushButton("Disconnect", window)
btn_disconnect.setGeometry(215, 265, 80, 30)
btn_disconnect.clicked.connect(clickDisconnectVPN)
btn_disconnect.setObjectName("btn_disconnect")

btn_other_vpn = QPushButton("Other VPN", window)
btn_other_vpn.setGeometry(220, 5, 70, 30)
btn_other_vpn.setObjectName("btn_other_vpn")
btn_other_vpn.clicked.connect(otherVPNs)

window.show()
hilo = threading.Thread(target=geo)
hilo.daemon = True
hilo.start()
threadDisconnectVPN()

sys.exit(app.exec())
