import os
import shutil
import sys
from PyInstaller.__main__ import run as pyinstaller_run

def safe_move(src, dst):
    """Безопасно перемещает файл/папку с проверками и backup"""
    try:
        if not os.path.exists(src):
            print(f"⚠️ Файл для перемещения не найден: {src}")
            return False
            
        if os.path.exists(dst):
            # Создаем backup
            backup = dst + ".bak"
            if os.path.exists(backup):
                if os.path.isdir(backup):
                    shutil.rmtree(backup)
                else:
                    os.remove(backup)
            shutil.move(dst, backup)
            print(f"🔁 Создан backup: {backup}")
            
        # Создаем целевую директорию если нужно
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        
        shutil.move(src, dst)
        return True
    except Exception as e:
        print(f"❌ Ошибка при перемещении {src} -> {dst}: {str(e)}")
        return False

def build_main_app():
    """Сборка основного приложения с проверкой всех этапов"""
    print("🔧 Собираем основное приложение...")
    
    # Проверка существования необходимых файлов
    required_files = [
        'start_app.py',
        'settings.yaml',
        '.env',
        'static/',
        'assets/',
        'ffmpeg/'
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print("❌ Отсутствуют необходимые файлы:")
        for f in missing_files:
            print(f"- {f}")
        return False

    try:
        pyinstaller_run([
            'start_app.py',
            '--name=start_app',
            '--onedir',
            '--add-data=templates/*:templates',
            '--add-data=settings.yaml:.',
            '--add-data=.env:.',
            '--add-data=static;static',
            '--add-data=assets;assets',
            '--add-data=ffmpeg;ffmpeg',
            '--clean',
            '--noconfirm',
            '--log-level=ERROR'
        ])

        # Перенос файлов из _internal в корень
        dist_dir = 'dist/start_app'
        internal_dir = os.path.join(dist_dir, '_internal')

        # 1. Переносим settings.yaml
        settings_src = os.path.join(internal_dir, 'settings.yaml')
        settings_dst = os.path.join(dist_dir, 'settings.yaml')
        if not safe_move(settings_src, settings_dst):
            print("❌ Не удалось переместить settings.yaml")

        # 2. Переносим папку assets
        assets_src = os.path.join(internal_dir, 'assets')
        assets_dst = os.path.join(dist_dir, 'assets')
        if not safe_move(assets_src, assets_dst):
            print("❌ Не удалось переместить assets")

        print("✅ Основное приложение успешно собрано")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при сборке основного приложения: {str(e)}")
        return False

def build_test_system():
    """Сборка тестовой системы"""
    print("\n🔧 Собираем тестовую систему...")
    
    if not os.path.exists('test_system.py'):
        print("❌ Файл test_system.py не найден")
        return False

    try:
        pyinstaller_run([
            'test_system.py',
            '--name=test_system',
            '--onedir',
            '--clean',
            '--noconfirm',
            '--log-level=ERROR'
        ])
        
        # Переносим test_system.exe
        src_exe = os.path.join('dist', 'test_system', 'test_system.exe')
        dst_exe = os.path.join('dist', 'start_app', 'test_system.exe')
        
        if not safe_move(src_exe, dst_exe):
            print("❌ Не удалось переместить test_system.exe")
            return False
        
        # Удаляем временную папку
        test_system_dir = os.path.join('dist', 'test_system')
        if os.path.exists(test_system_dir):
            shutil.rmtree(test_system_dir, ignore_errors=True)
            
        print("✅ Тестовая система успешно собрана")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при сборке тестовой системы: {str(e)}")
        return False

if __name__ == '__main__':
    # Очистка предыдущих сборок
    if os.path.exists('dist'):
        shutil.rmtree('dist', ignore_errors=True)
    if os.path.exists('build'):
        shutil.rmtree('build', ignore_errors=True)
    
    # Сначала собираем основное приложение
    success = build_main_app()
    
    # Если основное приложение собралось, собираем тестовую систему
    if success:
        success &= build_test_system()
    
    # Итоговый статус
    if success:
        print("\n🎉 Оба приложения успешно собраны!")
        print(f"Итоговая папка: {os.path.abspath('dist/start_app')}")
    else:
        print("\n❌ Сборка завершена с ошибками")
        sys.exit(1)