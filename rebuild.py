import os
import shutil
import sys
from PyInstaller.__main__ import run as pyinstaller_run

def fast_exe_update(script_name):
    """Обновляет только EXE без пересборки зависимостей
    
    Args:
        script_name (str): Имя Python-скрипта для пересборки (например 'start_app.py')
    """
    print(f"⚡ Обновление EXE для {script_name} ")
    
    # Конфигурация
    app_name = os.path.splitext(script_name)[0]  # Убираем .py из имени
    temp_dir = "dist_temp"
    target_dir = f"dist/start_app"
    
    try:
        # Проверяем существование исходного файла
        if not os.path.exists(script_name):
            print(f"❌ Файл не найден: {script_name}")
            return False

        # 1. Минимальная сборка во временную папку
        pyinstaller_run([
            script_name,
            f'--name={app_name}',
            '--onedir',
            f'--distpath={temp_dir}',
            '--workpath=build_temp',
            '--noconfirm',
            '--log-level=ERROR',
            
            # Параметры для ускорения
            '--exclude-module=unused',
            '--disable-windowed-traceback',
        ])
        
        # 2. Переносим только EXE
        new_exe = os.path.join(temp_dir, app_name, f"{app_name}.exe")
        old_exe = os.path.join(target_dir, f"{app_name}.exe")
        
        if os.path.exists(new_exe):
            # Создаем backup
            if os.path.exists(old_exe):
                backup_name = old_exe + ".bak"
                if os.path.exists(backup_name):
                    os.remove(backup_name)
                os.rename(old_exe, backup_name)
                print(f"🔁 Создан backup: {backup_name}")
            
            # Заменяем EXE
            shutil.move(new_exe, old_exe)
            print(f"✅ EXE обновлён. Размер: {os.path.getsize(old_exe)/1024/1024:.1f} MB")
            return True
        
        print("❌ Новый EXE не найден")
        return False
        
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        return False
    finally:
        # Очистка
        shutil.rmtree(temp_dir, ignore_errors=True)
        shutil.rmtree('build_temp', ignore_errors=True)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Использование: rebuild.py <имя_скрипта.py>")
        print("Пример: python rebuild.py start_app.py")
        sys.exit(1)
    
    script_to_rebuild = sys.argv[1]
    if fast_exe_update(script_to_rebuild):
        print(f"\n🔄 Запустите обновлённый EXE: dist/{os.path.splitext(script_to_rebuild)[0]}/{os.path.splitext(script_to_rebuild)[0]}.exe")
    else:
        print("\n❌ Требуется полная пересборка ")