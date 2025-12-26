# [file name]: nova_archiver.py
"""
Nova Archiver - Универсальный архиватор с поддержкой всех форматов
"""

__version__ = "2.1.0"

import sys
import os
import json
import shutil
import zipfile
import tempfile
import hashlib
import tarfile
import threading
import winreg  # Для Windows
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# Проверяем и импортируем дополнительные библиотеки
LIBRARIES = {
    'py7zr': ('py7zr', 'Для .7z архивов'),
    'rarfile': ('rarfile', 'Для .rar архивов (чтение)'),
    'pyzipper': ('pyzipper', 'Для паролей в ZIP архивах'),
}

for lib_name, (module_name, description) in LIBRARIES.items():
    try:
        globals()[f"HAS_{lib_name.upper()}"] = True
        globals()[lib_name.upper()] = __import__(module_name)
    except ImportError:
        globals()[f"HAS_{lib_name.upper()}"] = False
        print(f"ℹ️  {lib_name} не установлен: {description}")

# Инициализация переменных для библиотек
HAS_7Z = globals().get('HAS_PY7ZR', False)
HAS_RAR = globals().get('HAS_RARFILE', False)
HAS_PYZIPPER = globals().get('HAS_PYZIPPER', False)

class ArchiveAssociation:
    """Класс для управления ассоциацией файлов в Windows"""
    
    @staticmethod
    def is_admin():
        """Проверяет, запущена ли программа с правами администратора"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    @staticmethod
    def get_icon_path():
        """Возвращает путь к иконке программы"""
        # Пробуем найти иконку рядом с исполняемым файлом
        base_dir = Path(sys.executable).parent if hasattr(sys, 'frozen') else Path(__file__).parent
        icon_paths = [
            base_dir / "nova.ico",
            base_dir / "icons" / "nova.ico",
            base_dir / "nova_icon.ico",
        ]
        
        for path in icon_paths:
            if path.exists():
                return str(path)
        
        # Если иконка не найдена, создадим временную
        return ArchiveAssociation.create_temp_icon()
    
    @staticmethod
    def create_temp_icon():
        """Создает временную иконку, если основная не найдена"""
        temp_dir = Path(tempfile.gettempdir()) / "nova_archiver"
        temp_dir.mkdir(exist_ok=True)
        icon_path = temp_dir / "nova_temp.ico"
        
        # Простая иконка Nova (синяя буква N)
        try:
            from PIL import Image, ImageDraw, ImageFont
            img = Image.new('RGBA', (256, 256), (59, 130, 246, 255))
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("arial.ttf", 150)
            except:
                font = ImageFont.load_default()
            
            draw.text((80, 50), "N", font=font, fill=(255, 255, 255, 255))
            img.save(icon_path, format='ICO', sizes=[(256, 256)])
            return str(icon_path)
        except:
            # Если PIL не установлен, просто возвращаем путь к пустому файлу
            with open(icon_path, 'wb') as f:
                pass
            return str(icon_path)
    
    @staticmethod
    def register_all_formats():
        """Регистрирует все форматы архива для Nova Archiver"""
        if not ArchiveAssociation.is_admin():
            print("Требуются права администратора для регистрации форматов")
            return False
        
        try:
            exe_path = sys.executable if hasattr(sys, 'frozen') else sys.argv[0]
            icon_path = ArchiveAssociation.get_icon_path()
            
            # Форматы для регистрации
            formats = [
                ('.zip', 'Nova.ZipArchive', 'ZIP Archive'),
                ('.sntr', 'Nova.SinterArchive', 'Sinter Archive'),
                ('.nv', 'Nova.NovaArchive', 'Nova Archive'),
                ('.tar', 'Nova.TarArchive', 'TAR Archive'),
                ('.tar.gz', 'Nova.TarGzArchive', 'TAR.GZ Archive'),
                ('.tar.bz2', 'Nova.TarBz2Archive', 'TAR.BZ2 Archive'),
                ('.tar.xz', 'Nova.TarXzArchive', 'TAR.XZ Archive'),
                ('.rar', 'Nova.RarArchive', 'RAR Archive'),
                ('.7z', 'Nova.SevenZipArchive', '7-Zip Archive'),
            ]
            
            for ext, file_type, description in formats:
                ArchiveAssociation.register_format(ext, file_type, description, exe_path, icon_path)
            
            # Обновляем кэш иконок Windows
            try:
                import ctypes
                ctypes.windll.shell32.SHChangeNotify(0x08000000, 0, 0, 0)
            except:
                pass
            
            return True
            
        except Exception as e:
            print(f"Ошибка при регистрации форматов: {e}")
            return False
    
    @staticmethod
    def register_format(extension, file_type, description, exe_path, icon_path):
        """Регистрирует один формат файла"""
        try:
            # Ассоциируем расширение с типом файла
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, extension) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, file_type)
            
            # Создаем описание типа файла
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, file_type) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, description)
            
            # Устанавливаем иконку
            icon_key_path = f"{file_type}\\DefaultIcon"
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, icon_key_path) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, f'"{icon_path}"')
            
            # Команда для открытия
            command_key_path = f"{file_type}\\shell\\open\\command"
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, command_key_path) as key:
                command = f'"{exe_path}" "%1"'
                winreg.SetValue(key, "", winreg.REG_SZ, command)
            
            # Добавляем в контекстное меню "Открыть с помощью Nova"
            shell_key_path = f"{file_type}\\shell\\open"
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, shell_key_path) as key:
                winreg.SetValue(key, "", winreg.REG_SZ, "&Открыть с помощью Nova")
            
            print(f"✅ Зарегистрирован формат: {extension} -> {description}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка регистрации {extension}: {e}")
            return False
    
    @staticmethod
    def unregister_all_formats():
        """Удаляет все ассоциации Nova Archiver"""
        if not ArchiveAssociation.is_admin():
            print("Требуются права администратора")
            return False
        
        try:
            formats = [
                '.zip', '.sntr', '.nv', '.tar', '.rar', '.7z',
                '.tar.gz', '.tar.bz2', '.tar.xz'
            ]
            
            for ext in formats:
                try:
                    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, ext)
                    print(f"✅ Удален формат: {ext}")
                except:
                    pass
            
            # Удаляем типы файлов
            file_types = [
                'Nova.ZipArchive', 'Nova.SinterArchive', 'Nova.NovaArchive',
                'Nova.TarArchive', 'Nova.RarArchive', 'Nova.SevenZipArchive',
                'Nova.TarGzArchive', 'Nova.TarBz2Archive', 'Nova.TarXzArchive'
            ]
            
            for file_type in file_types:
                try:
                    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, file_type)
                except:
                    pass
            
            return True
            
        except Exception as e:
            print(f"Ошибка при удалении форматов: {e}")
            return False

# ... (остальной код NovaArchiver остается таким же, как в предыдущем ответе)
# Добавьте все остальные классы: PasswordDialog, SetPasswordDialog, ArchiveHandler, NovaArchiver