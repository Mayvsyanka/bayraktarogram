import os

folder_name = "bayraktarogram"

# Получаем текущую директорию (текущую папку)
current_directory = os.getcwd()

# Объединяем текущую директорию с именем папки для получения полного пути
folder_path = os.path.join(current_directory, folder_name)

# Получаем абсолютный путь к папке
absolute_folder_path = os.path.abspath(folder_path)

print("Путь к папке:", absolute_folder_path)