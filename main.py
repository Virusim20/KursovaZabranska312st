import os
import cv2
from file import process_photo_or_video, choose_operation, capture_photo, capture_video  # Імпортуємо необхідні функції
from tkinter import Tk, filedialog

def main():
    while True:
        print("==== Оберіть тип файлу ====\n\n")  # Виводимо меню вибору типу файлу
        print("1. Фото\n")
        print("2. Відео\n")
        print("3. Вийти\n\n")
        user_input = input("Введіть номер типу: ")  # Запитуємо користувача про вибір
        try:
            file_type = int(user_input)  # Конвертуємо введене значення у ціле число
            if file_type == 3:
                break
            elif file_type in [1, 2]:
                process_file_type(file_type)  # Викликаємо функцію для обробки обраного типу файлу
        except ValueError:
            pass

def process_file_type(file_type):
    while True:
        print("==== Оберіть місце розташування файлу ====\n\n")  # Виводимо меню вибору місця розташування файлу
        print("1. Захоплення з камери\n")
        print("2. Вибір файлу\n")
        print("3. Вийти\n\n")
        user_input = input("Введіть номер місця: ")  # Запитуємо користувача про вибір
        try:
            location_type = int(user_input)  # Конвертуємо введене значення у ціле число
            if location_type == 3:
                break
            elif location_type == 1:
                if file_type == 1:
                    photo = capture_photo()  # Захоплюємо фото з камери
                    if photo is not None:
                        operation, params = choose_operation(file_type)  # Обираємо операцію для обробки
                        process_photo_or_video(photo, operation, params, is_video=False)  # Обробляємо фото
                elif file_type == 2:
                    output_path = capture_video()  # Захоплюємо відео з камери
                    if output_path:
                        operation, params = choose_operation(file_type)  # Обираємо операцію для обробки
                        process_photo_or_video(output_path, operation, params, is_video=True)  # Обробляємо відео
            elif location_type == 2:
                file_path = select_file()  # Вибираємо файл за допомогою діалогового вікна
                if file_path:
                    operation, params = choose_operation(file_type)  # Обираємо операцію для обробки
                    is_video = file_path.lower().endswith(('.mp4', '.avi', '.mov'))  # Визначаємо, чи є файл відео
                    process_photo_or_video(file_path, operation, params, is_video=is_video)  # Обробляємо фото або відео
        except ValueError:
            pass

def select_file():
    root = Tk()
    root.withdraw()  # Ховаємо головне вікно
    file_path = filedialog.askopenfilename()  # Відкриваємо діалогове вікно для вибору файлу
    root.destroy()  # Закриваємо Tk вікно
    return file_path

if __name__ == "__main__":
    main()  # Викликаємо головну функцію

if __name__ == "__main__":
    main()  # Викликаємо головну функцію