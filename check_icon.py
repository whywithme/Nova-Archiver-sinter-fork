# [file name]: check_icon.py
"""
Проверка и создание иконки Nova
"""

from PIL import Image, ImageDraw, ImageFont
import tempfile
from pathlib import Path

def create_nova_icon(output_path="nova.ico"):
    """Создает иконку Nova Archiver"""
    try:
        # Размеры для иконки Windows
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        images = []
        
        for size in sizes:
            # Создаем изображение
            img = Image.new('RGBA', size, (59, 130, 246, 255))  # Синий фон Nova
            draw = ImageDraw.Draw(img)
            
            # Пробуем использовать шрифт, иначе рисуем простую N
            try:
                # Для больших размеров используем больший шрифт
                font_size = max(8, size[0] // 2)
                font = ImageFont.truetype("arial.ttf", font_size)
                
                # Рассчитываем позицию текста
                text = "N"
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (size[0] - text_width) // 2
                y = (size[1] - text_height) // 2
                
                draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
            except:
                # Простая буква N без шрифта
                margin = size[0] // 4
                points = [
                    (margin, margin),
                    (size[0] // 2, size[1] // 2),
                    (size[0] - margin, margin),
                    (size[0] - margin, size[1] - margin),
                    (size[0] // 2, size[1] // 2),
                    (margin, size[1] - margin),
                ]
                draw.line(points, fill=(255, 255, 255, 255), width=max(1, size[0] // 16))
            
            images.append(img)
        
        # Сохраняем как ICO
        images[0].save(output_path, format='ICO', save_all=True, append_images=images[1:])
        print(f"✅ Иконка создана: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания иконки: {e}")
        
        # Создаем простую иконку
        try:
            with open(output_path, 'wb') as f:
                # Минимальный корректный ICO файл
                f.write(b'\x00\x00\x01\x00\x01\x00\x01\x01\x00\x00\x01\x00\x08\x00(\x00\x00\x00\x16\x00\x00\x00(\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x01\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00\x00')
            print(f"⚠️  Создана простая иконка: {output_path}")
            return True
        except:
            return False

def check_icon_file():
    """Проверяет существование и корректность иконки"""
    icon_path = Path("nova.ico")
    
    if not icon_path.exists():
        print("❌ Файл nova.ico не найден")
        print("Создаю новую иконку...")
        return create_nova_icon()
    
    try:
        # Пробуем открыть как изображение
        with Image.open(icon_path) as img:
            if img.format == 'ICO':
                print(f"✅ Иконка найдена: {icon_path} ({img.size})")
                return True
            else:
                print(f"⚠️  Файл найден, но не ICO формат")
                return create_nova_icon()
    except:
        print("⚠️  Не могу прочитать иконку, создаю новую...")
        return create_nova_icon()

if __name__ == "__main__":
    print("="*50)
    print("ПРОВЕРКА ИКОНКИ NOVA ARCHIVER")
    print("="*50)
    
    success = check_icon_file()
    
    if success:
        print("\n✅ Иконка готова к использованию")
        print("\nДля регистрации ассоциаций файлов запустите:")
        print("python setup_associations.py")
    else:
        print("\n❌ Не удалось создать иконку")
        print("\nУстановите библиотеку Pillow:")
        print("pip install Pillow")
    
    input("\nНажмите Enter для выхода...")