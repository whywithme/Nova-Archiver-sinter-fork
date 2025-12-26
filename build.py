# [file name]: build.py
"""
Скрипт для сборки и установки Nova Archiver
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Выполнить команду с выводом в консоль"""
    print(f"\n{'='*50}")
    print(f"Выполняю: {description}")
    print(f"Команда: {cmd}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True)
        print(f"✓ Успешно: {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Ошибка при выполнении: {description}")
        print(f"Код ошибки: {e.returncode}")
        print(f"Вывод: {e.stdout}")
        return False

def build():
    """Собрать проект"""
    # Удаляем старые сборки
    for dir_name in ['build', 'dist', 'nova_archiver.egg-info']:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
    
    # Собираем wheel
    if run_command("python setup.py sdist bdist_wheel", "Сборка проекта"):
        print("\n✓ Сборка завершена успешно!")
        print("Файлы в папке 'dist':")
        for file in Path("dist").iterdir():
            print(f"  - {file.name}")
        return True
    return False

def install():
    """Установить проект"""
    # Ищем последний собранный wheel
    dist_files = list(Path("dist").glob("*.whl"))
    if not dist_files:
        print("Не найдены собранные файлы. Сначала выполните сборку.")
        return False
    
    latest_wheel = max(dist_files, key=lambda x: x.stat().st_mtime)
    
    if run_command(f"pip install {latest_wheel}", "Установка проекта"):
        print("\n✓ Установка завершена успешно!")
        print("Запустите программу командой: nova-archiver")
        return True
    return False

def create_exe():
    """Создать исполняемый файл с помощью PyInstaller"""
    if not Path("icons/nova_icon.ico").exists():
        print("Создаю иконку...")
        Path("icons").mkdir(exist_ok=True)
        # Простая заготовка для иконки
        ico_content = b""  # Здесь должны быть данные иконки
        with open("icons/nova_icon.ico", "wb") as f:
            f.write(ico_content)
    
    if run_command(
        'pyinstaller --onefile --windowed --name="NovaArchiver" --icon=icons/nova_icon.ico --add-data="icons;icons" nova_archiver.py',
        "Создание исполняемого файла"
    ):
        print("\n✓ Исполняемый файл создан!")
        print("Находится в: dist/NovaArchiver.exe")
        return True
    return False

def clean():
    """Очистить временные файлы"""
    folders_to_remove = ['build', 'dist', 'nova_archiver.egg-info', '__pycache__']
    files_to_remove = ['*.pyc', '*.spec']
    
    print("\nОчистка временных файлов...")
    
    for folder in folders_to_remove:
        if Path(folder).exists():
            shutil.rmtree(folder)
            print(f"✓ Удалено: {folder}")
    
    import glob
    for pattern in files_to_remove:
        for file in glob.glob(pattern):
            os.remove(file)
            print(f"✓ Удалено: {file}")
    
    print("\n✓ Очистка завершена!")

def main():
    """Главное меню"""
    print("\n" + "="*50)
    print("NOVA ARCHIVER - СИСТЕМА СБОРКИ")
    print("="*50)
    
    while True:
        print("\nВыберите действие:")
        print("1. Собрать проект (sdist + wheel)")
        print("2. Установить проект")
        print("3. Собрать и установить")
        print("4. Создать исполняемый файл (.exe)")
        print("5. Очистить временные файлы")
        print("6. Выйти")
        
        choice = input("\nВаш выбор (1-6): ").strip()
        
        if choice == "1":
            build()
        elif choice == "2":
            install()
        elif choice == "3":
            if build():
                install()
        elif choice == "4":
            create_exe()
        elif choice == "5":
            clean()
        elif choice == "6":
            print("\nДо свидания!")
            break
        else:
            print("\nНеверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    # Создаем необходимые папки
    Path("icons").mkdir(exist_ok=True)
    main()