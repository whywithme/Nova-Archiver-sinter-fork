# 📦 Nova Archiver

<div align="center">

**Universal archiver with support for all formats and beautiful interface**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.5+-green.svg)](https://pypi.org/project/PyQt6/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## 🎯 Main Features

### 📁 Support for all formats
- Native formats: .zip, .sntr, .nv (full support)
- Standard archives: .rar, .7z (via additional libraries)
- Unix archives: .tar, .tar.gz, .tar.bz2, .tar.xz
- Protected archives: ZIP with passwords (AES-256 and ZIP encryption)

### 🖥️ Smart file associations (Windows)
- Automatic registration as default archiver
- Unique Nova icon for all archive files
- Opening archives with double click
- Context menu "Open with Nova"

### 🔐 Security and encryption
- Setting/removing passwords for ZIP archives
- AES-256 (recommended) and ZIP encryption support
- Password prompt when opening protected archives
- Password storage in encrypted form

### 🎨 Modern interface
- Dark theme with gradients
- Detailed file information table
- Progress bar for long operations
- Context menu for quick actions
- Recent files history

---

## 📂 Project Structure

```text
nova-archiver/                                          # The root folder of the project
├── 📁 icons/                                          # Folder with icons (created automatically)
│ └── nova_temp.ico                             # Temporary icon (if nova.ico is not found)
│
├── 📄 nova_archiver.py                      # MAIN PROGRAM
├── 🎨 nova.ico                                     # MAIN ICON (your file is here)
│
├── ⚙️ setup_associations.py             # File Association Installer
├── 🎯 check_icon.py                           # Checking/creating an icon
├── 🚀 install.bat                                   # Automatic Installer (Windows)
├── ⚡ nova.bat                                     # Shortcut to launch
├── 🔨 build.py                                      # Build the project .exe
├── ▶️ run.py                                         # Easy launch for development
│
├── 📋 requirements.txt                       # Python Dependencies
├── 📦 setup.py                                     # Installation as a Python package
├── ⚙️ pyproject.toml                           # Assembly configuration
├── 📖 README.md                              # the Documentation in Russian
```

---

## 🚀 Quick Start

### Option 1: Automatic installation (recommended for Windows)
1. Download all files to one folder
2. Run the install.bat file
3. Follow the on-screen instructions
4. Ready! Nova Archiver is installed and registered as the default archiver

### Option 2: Manual installation
- Install Python dependencies: pip install -r requirements.txt
- Check and create icon: python check_icon.py
- Register file associations (requires administrator rights in Windows): python setup_associations.py
- Run the program: python nova_archiver.py

### Option 3: Run without installation
- python run.py

---

## 📖 Detailed File Description

### nova_archiver.py
This is the main program file containing the following key components:

- PasswordDialog Class: Dialog window for entering a password when opening protected archives
- SetPasswordDialog Class: Dialog window for setting a password on an archive
- ArchiveHandler Class: Main archive handler providing format detection and operations
- NovaArchiver Class: Main application window with modern interface
- ArchiveAssociation Class: Responsible for registering file associations in Windows

### nova.ico
Main program icon in ICO format (256x256). This icon will be displayed for all associated files in Windows.

### setup_associations.py
Utility for registering file associations in Windows. Registers Nova Archiver as the default program for all supported archive formats.

### check_icon.py
Utility for checking and creating icons. If the nova.ico file is missing, it creates a temporary icon.

### install.bat
Batch file for automatic installation on Windows. Installs dependencies, creates icons and registers associations.

### nova.bat
Shortcut for quick program launch from command line.

### run.py
Simple script to run the program without installing dependencies in the system.

### build.py
Script for building the program into an executable file (.exe) using PyInstaller.

### setup.py
Script for installing the program as a Python package via pip.

### pyproject.toml
Modern configuration file for package building.

### requirements.txt
List of Python dependencies required for the program:
- PyQt6>=6.5.0: for graphical interface
- py7zr>=0.20.5: for .7z archive support
- rarfile>=4.0: for reading .rar archives
- pyzipper>=0.3.6: for working with passwords in ZIP archives
- Pillow>=10.0.0: for icon processing

---

## 🛠️ Installation and Usage

### Installing dependencies
The program requires installation of several Python libraries. You can install them all at once:

```bash
pip install PyQt6 py7zr rarfile pyzipper Pillow
```

Or use the requirements.txt file:

```bash
pip install -r requirements.txt
```

### Registering file associations in Windows
To register Nova Archiver as the default archiver, run:

```bash
python setup_associations.py
```

This utility will perform the following actions:
- Check for the presence of nova.ico file
- Register all supported formats in Windows registry
- Set Nova icon for all archive files
- Configure opening archives with double click

Note: Administrator rights are required to register associations.

### Creating an icon
If you don't have the nova.ico file, you can create it using:

```bash
python check_icon.py
```

This utility will check for the icon and create a new one if the file is missing or damaged.

---

## 📁 Supported Formats

### Full support (read and write)
- .zip - Standard ZIP archives
- .sntr - Sinter archives (technically these are ZIP archives)
- .nv - Native Nova Archiver format (ZIP with different extension)

### Partial support (require library installation)
- .7z - 7-Zip format (requires py7zr)
- .rar - WinRAR archives (read-only, requires rarfile)

### Unix/Linux archives
- .tar - TAR archives without compression
- .tar.gz - TAR archives with GZIP compression
- .tar.bz2 - TAR archives with BZIP2 compression
- .tar.xz - TAR archives with XZ compression

### Protected archives
- ZIP with passwords - Full support via pyzipper
- AES-256 encryption - Recommended protection method
- ZIP encryption - Old compatibility method

---

## 🔐 Working with Passwords

### Setting a password on an archive
1. Open the archive in Nova Archiver
2. Click the "Password" button on the toolbar
3. Enter password and confirmation
4. Select encryption method (AES-256 recommended)
5. Click "OK" to apply password

### Removing password from an archive
1. Open the protected archive
2. Select "Archive" → "Remove Password..."
3. Enter current password
4. Confirm protection removal

### Opening protected archives
When opening a protected archive, the program will automatically request a password. You can:
- Enter password in dialog window
- Check "Remember password" for current session
- Use saved passwords from settings

---

## 🖥️ Program Interface

### Main window
The main window of Nova Archiver consists of the following elements:

1. Menu - Contains all available commands, grouped by categories
2. Toolbar - Quick access to main functions
3. Information panel - Displays information about current archive
4. File table - Shows archive contents with detailed information
5. Progress panel - Shows progress of long operations
6. Status bar - Shows current status and statistics

### Context menu
Right-clicking on a file in the table opens a context menu with options:
- Extract selected
- Remove from archive
- View file properties

---

## ⚙️ Settings and Configuration

### Settings file
The program saves settings to the file:

```text
C:\Users\your_name\.nova_archiver.json (Windows)
```

```text
~/.nova_archiver.json (Linux/macOS)
```

Settings save:
- List of recently opened files
- Saved passwords (in encrypted form)
- Window size and position
- Other user preferences

### Command line
Nova Archiver supports launching with command line parameters:

nova_archiver.py archive.zip (Open specified archive)
nova_archiver.py --help (Show help)
nova_archiver.py --version (Show version)

---

## 🔧 For Developers

### Building into executable file
To create an executable file (.exe), use:

```bash
python build.py
```

Or directly via PyInstaller:

pyinstaller --onefile --windowed --name="NovaArchiver" --icon=nova.ico nova_archiver.py

### Installing as a Python package
You can install Nova Archiver as a Python package:

```bash
pip install
```

Or in development mode:

```bash
pip install -e
```

---

## ❓ Frequently Asked Questions

### Question: Why won't .rar files open?
Answer: To work with .rar files, the rarfile library is required. Install it with the command: pip install rarfile

### Question: How to make Nova Archiver the default archiver?
Answer: Run setup_associations.py with administrator rights. The program will register all formats and set the Nova icon

### Question: Can I open protected archives from other programs?
Answer: Yes, Nova Archiver supports ZIP archives with passwords created in other programs (WinRAR, 7-Zip, etc.).

### Question: Are Linux and macOS supported?
Answer: Yes, the program is cross-platform. However, file associations only work in Windows

### Question: How to uninstall the program?
Answer:
1. Delete program files
2. Run setup_associations.py and select "Remove all associations"
3. Delete the settings file (if needed)

---

## 🐛 Bug Reports and Support

If you find a bug or have suggestions for improvement:

1. Check if all dependencies are installed
2. Make sure you're using the latest version of the program
3. Describe the problem in as much detail as possible
4. Specify your operating system and Python version

### Known limitations
- .rar archives are read-only
- .7z archives require py7zr installation
- File associations only work in Windows
- Encryption is only supported for ZIP archives

---

<div align="center">

### ⭐ If you like Nova Archiver, share it with friends!

**Made with ❤️ for the community**

</div>