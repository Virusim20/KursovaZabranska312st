import os
import cv2
import numpy as np

def process_photo_or_video(file_path, operation, params, is_video=False, show_preview=True):
    if is_video:
        process_video(file_path, operation, params)  # Обробляємо відео
    else:
        image = load_photo(file_path)  # Завантажуємо фото
        if image is None:
            return  # Виходимо з функції, якщо фото не завантажено правильно

        if show_preview:
            cv2.imshow('Original Photo', image)  # Показуємо оригінальне фото
            cv2.waitKey(0)  # Чекаємо на натискання будь-якої клавіші перед застосуванням трансформації

        processed_image = apply_operations(image, operation, params)  # Застосовуємо обрані операції до фото
        cv2.imshow('Processed Photo', processed_image)  # Показуємо оброблене фото
        cv2.waitKey(0)  # Чекаємо на натискання будь-якої клавіші

        save_option = input("Зберегти оброблене фото? (так/ні): ").lower()  # Запитуємо про збереження
        if save_option == 'так':
            save_path = input("Введіть шлях для збереження обробленого фото: ")
            save_photo(processed_image, save_path)
            print("Оброблене фото успішно збережено.")

        cv2.destroyAllWindows()  # Закриваємо всі вікна OpenCV


def capture_video(output_path='output_video.mp4', operation=None, params=None):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 20.0  # Можете налаштувати кадрову частоту за потребою
    frame_size = (640, 480)  # Можете налаштувати розмір кадру за потребою
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Помилка: Неможливо відкрити камеру.")
        return

    print("Натисніть 'q' для завершення запису та збереження відео.")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Помилка: Не вдалося захопити кадр.")
            break

        if operation is not None:
            frame = apply_operations(frame, operation, params)

        out.write(frame)

        cv2.imshow('Запис відео', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Відео збережено за шляхом {output_path}")
    return output_path

def process_video(video_path, operation, params, output_path='output_video.mp4'):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Помилка: Неможливо відкрити відеофайл {video_path}")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not out.isOpened():
        print(f"Помилка: Неможливо створити вихідний відеофайл {output_path}")
        cap.release()
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = apply_operations(frame, operation, params)

        out.write(processed_frame)

        cv2.imshow('Оригінальне відео', frame)
        cv2.imshow('Оброблене відео', processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Оброблене відео збережено за шляхом {output_path}")
    return output_path

def capture_photo():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Зняте фото', frame)
        cv2.waitKey(0)
        save_option = input("Зберегти це фото? (так/ні): ").lower()
        if save_option == 'так':
            file_path = input("Введіть шлях для збереження фото: ")
            cv2.imwrite(file_path, frame)
            print("Фото успішно збережено.")
    else:
        print("Не вдалося захопити фото з камери.")
    cap.release()
    cv2.destroyAllWindows()

def load_photo(file_path):
    image = cv2.imread(file_path)
    if image is None:
        print(f"Помилка: Неможливо прочитати файл зображення {file_path}")
    return image

def choose_operation(file_type):
    print("\nОберіть операцію:")
    if file_type == 1:
        print("1. Дзеркальне відображення")
        print("2. Розтягнення зображення")
        print("3. Конвертація до простору кольорів LAB")
        print("4. Високочастотний фільтр")
    elif file_type == 2:
        print("1. Дзеркальне відображення відео")
        print("2. Розтягнення відео")
        print("3. Конвертація до простору кольорів LAB")
        print("4. Високочастотний фільтр")
    operation = int(input("Введіть номер операції: "))
    params = None
    if operation == 2:
        horizontal_factor = float(input("Введіть горизонтальний коефіцієнт розтягування: "))
        vertical_factor = float(input("Введіть вертикальний коефіцієнт розтягування: "))
        params = (horizontal_factor, vertical_factor)
    elif operation == 4:
        kernel_size = int(input("Введіть розмір ядра для високочастотного фільтру (непарне число): "))
        if kernel_size % 2 == 0:
            print("Розмір ядра повинен бути непарним числом. Використовуємо наступне найменше непарне число.")
            kernel_size += 1
        params = kernel_size
    return operation, params


def apply_operations(image, operation, params):
    if operation == 1:
        return mirror_image(image)
    elif operation == 2:
        horizontal_factor, vertical_factor = params
        return stretch_image(image, horizontal_factor, vertical_factor)
    elif operation == 3:
        return convert_to_lab(image)
    elif operation == 4:
        kernel_size = params
        return high_pass_filter(image, kernel_size)

def mirror_image(image):
    return cv2.flip(image, 1)

def stretch_image(image, horizontal_factor, vertical_factor):
    height, width = image.shape[:2]
    new_width = int(width * horizontal_factor)
    new_height = int(height * vertical_factor)
    return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

def convert_to_lab(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

def high_pass_filter(image, kernel_size):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
    kernel[kernel_size // 2, kernel_size // 2] = 0
    kernel -= np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
    return cv2.filter2D(gray_image, -1, kernel)
