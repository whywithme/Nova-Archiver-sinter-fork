# [file name]: setup_associations.py
"""
Установщик ассоциаций файлов для Nova Archiver
"""

import sys
import os
import ctypes
import subprocess
from pathlib import Path

def is_admin():
    """Проверяет, запущена ли программа с правами администратора"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Перезапускает скрипт с правами администратора"""
    if hasattr(sys, 'frozen'):
        # Для исполняемого файла
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
    else:
        # Для скрипта Python
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{__file__}"', None, 1
        )
    sys.exit()

def check_requirements():
    """Проверяет необходимые файлы"""
    required_files = ['nova_archiver.py', 'nova.ico']
    
    print("="*50)
    print("ПРОВЕРКА ТРЕБОВАНИЙ")
    print("="*50)
    
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - НЕ НАЙДЕН")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Отсутствуют файлы: {', '.join(missing_files)}")
        print("Поместите файл nova.ico в ту же папку, что и программу")
        return False
    
    return True

def show_menu():
    """Показывает меню установки"""
    print("\n" + "="*50)
    print("NOVA ARCHIVER - УСТАНОВКА АССОЦИАЦИЙ ФАЙЛОВ")
    print("="*50)
    print("\nЭта программа зарегистрирует Nova Archiver как архиватор по умолчанию")
    print("для следующих форматов:")
    print("  • .zip, .sntr, .nv (нативные форматы)")
    print("  • .rar, .7z (если установлены библиотеки)")
    print("  • .tar, .tar.gz, .tar.bz2, .tar.xz")
    print("\nВсе файлы будут иметь иконку Nova и открываться двойным кликом")
    
    if not is_admin():
        print("\n⚠️  Для регистрации форматов требуются права администратора")
        print("\nВыберите действие:")
        print("1. Запустить с правами администратора и установить")
        print("2. Выйти")
    else:
        print("\n✓ Запущено с правами администратора")
        print("\nВыберите действие:")
        print("1. Установить ассоциации файлов")
        print("2. Удалить все ассоциации Nova")
        print("3. Проверить установленные ассоциации")
        print("4. Выйти")
    
    return input("\nВаш выбор (1-4): ").strip()

def install_associations():
    """Устанавливает ассоциации файлов"""
    try:
        print("\n" + "="*50)
        print("УСТАНОВКА АССОЦИАЦИЙ")
        print("="*50)
        
        # Импортируем класс ассоциаций
        from nova_archiver import ArchiveAssociation
        
        success = ArchiveAssociation.register_all_formats()
        
        if success:
            print("\n" + "="*50)
            print("✅ АССОЦИАЦИИ УСПЕШНО УСТАНОВЛЕНЫ!")
            print("="*50)
            print("\nТеперь вы можете:")
            print("1. Открывать архивы двойным кликом")
            print("2. Все архивы будут иметь иконку Nova")
            print("3. Nova будет архиватором по умолчанию")
        else:
            print("\n❌ Ошибка при установке ассоциаций")
            
        input("\nНажмите Enter для продолжения...")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        input("\nНажмите Enter для продолжения...")

def uninstall_associations():
    """Удаляет ассоциации файлов"""
    try:
        print("\n" + "="*50)
        print("УДАЛЕНИЕ АССОЦИАЦИЙ")
        print("="*50)
        
        confirm = input("Вы уверены, что хотите удалить все ассоциации Nova? (y/N): ")
        if confirm.lower() != 'y':
            print("Отменено")
            return
        
        from nova_archiver import ArchiveAssociation
        success = ArchiveAssociation.unregister_all_formats()
        
        if success:
            print("\n✅ Ассоциации успешно удалены")
        else:
            print("\n❌ Ошибка при удалении ассоциаций")
            
        input("\nНажмите Enter для продолжения...")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        input("\nНажмите Enter для продолжения...")

def check_associations():
    """Проверяет текущие ассоциации"""
    try:
        import winreg
        
        print("\n" + "="*50)
        print("ПРОВЕРКА АССОЦИАЦИЙ")
        print("="*50)
        
        formats = [
            ('.zip', 'Nova.ZipArchive'),
            ('.sntr', 'Nova.SinterArchive'),
            ('.nv', 'Nova.NovaArchive'),
            ('.tar', 'Nova.TarArchive'),
            ('.rar', 'Nova.RarArchive'),
            ('.7z', 'Nova.SevenZipArchive'),
        ]
        
        for ext, expected_type in formats:
            try:
                with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, ext) as key:
                    actual_type, _ = winreg.QueryValueEx(key, "")
                    status = "✅" if actual_type == expected_type else "❌"
                    print(f"{status} {ext:15} -> {actual_type}")
            except:
                print(f"❌ {ext:15} -> НЕ ЗАРЕГИСТРИРОВАН")
                
        input("\nНажмите Enter для продолжения...")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        input("\nНажмите Enter для продолжения...")

def main():
    """Главная функция установщика"""
    
    if not check_requirements():
        input("\nНажмите Enter для выхода...")
        return
    
    while True:
        choice = show_menu()
        
        if not is_admin():
            if choice == "1":
                run_as_admin()
            elif choice == "2":
                break
            else:
                print("Неверный выбор")
        else:
            if choice == "1":
                install_associations()
            elif choice == "2":
                uninstall_associations()
            elif choice == "3":
                check_associations()
            elif choice == "4":
                break
            else:
                print("Неверный выбор")

if __name__ == "__main__":
    main()