# [file name]: run.py
"""
Простой скрипт для запуска Nova Archiver
"""

import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from nova_archiver import main
    print("="*50)
    print("Запускаю Nova Archiver...")
    print("="*50)
    main()
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("\nУстановите зависимости командой:")
    print("pip install PyQt6")
    input("\nНажмите Enter для выхода...")
except Exception as e:
    print(f"Неожиданная ошибка: {e}")
    import traceback
    traceback.print_exc()
    input("\nНажмите Enter для выхода...")