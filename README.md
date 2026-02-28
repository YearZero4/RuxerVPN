# Ruxer VPN 🔒

![Ruxer VPN](icon.ico)

A lightweight, free VPN client with a modern GUI built with Python and PySide6, utilizing VPNBook's free servers.

## ✨ Features

- **Simple & Clean Interface** - Easy-to-use graphical interface with dark theme
- **Quick Connect** - One-click connection to a random VPN server
- **Server Selection** - Browse and choose from multiple VPN servers
- **Geolocation Display** - Shows your current IP and country after connection
- **Auto-disconnect** - Automatically disconnects previous connection before new one
- **OpenVPN Integration** - Uses OpenVPN for reliable connections
- **Cross-platform** - Windows support (with admin privileges for OpenVPN)

## 🚀 How It Works

1. **Connect** - Click the big green "Connect" button to connect to a random VPN server
2. **Other VPN** - Browse available servers and choose your preferred one
3. **Disconnect** - Click "Disconnect" to terminate the VPN connection
4. **Geolocation** - Your IP and country are displayed automatically after connection

## 🛠️ Technical Details

- **Frontend**: PySide6 (Qt for Python)
- **VPN Service**: VPNBook free servers
- **VPN Protocol**: OpenVPN
- **Connection Method**: TCP 443 (default)
- **Language**: Python 3.x

## 📦 Installation

### Prerequisites
- Windows 10/11 (64-bit)
- Administrator privileges
- [TAP Driver](https://github.com/YearZero4/RuxerVPN/releases/download/tap-openvpn/tap-openvpn.msi) (required for OpenVPN)

# Download the TAP driver
# Direct link: https://github.com/YearZero4/RuxerVPN/releases/download/tap-openvpn/tap-openvpn.msi

# Run the installer as administrator
# Right-click the downloaded file and select "Run as administrator"

### From Source
```bash

# Clone the repository
git clone https://github.com/yourusername/RuxerVPN.git
cd ruxer-vpn

# Install dependencies
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Run the application
python gui.pyw

```

<img width="632" height="505" alt="Screenshot-260228 12_44_51" src="https://github.com/user-attachments/assets/d6a9660e-c55e-4938-9297-653b930d06f4" />
<img width="636" height="463" alt="Screenshot-260228 12_46_10" src="https://github.com/user-attachments/assets/d48e0b00-bfe9-4d9c-aba6-09bc3bc19946" />
