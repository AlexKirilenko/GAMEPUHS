import pygame
import random
import customtkinter
import os
import tkinter as tk
from tkinter import messagebox

# --- Настройки игры ---
SCREEN_WIDTH = 960
SCREEN_HEIGTH = 640

# --- Цвета ---
COLOR_BACKGROUND = (100, 150, 200)

# --- Файлы ---
RECORDS_FILE = os.path.join(os.path.expanduser("~"), "Documents", "megapush_records.txt")

# --- Игровые переменные ---
running = False
hits = 0
player_name = ""
target_x = 0
target_y = 0
target_width = 82
target_height = 70

target_image = None
screen = None
icon = None

last_hit_time = 0  # Время последнего попадания (в миллисекундах)
show_target_duration = 2000 # Длительность показа цели
misses = 0  # Счетчик промахов
MAX_MISSES = 3 # Максимальное количество промахов


# --- Функции Pygame ---
def init_game():
    """Инициализация Pygame и игровых объектов."""
    global screen, target_image, target_x, target_y, running, hits, icon, last_hit_time
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
    pygame.display.set_caption("megapush")
    icon = pygame.image.load("image/rm.png")
    pygame.display.set_icon(icon)
    target_image = pygame.image.load("image/klip.png")

    target_width = 70  # Initialize target_width here
    target_height = 80  # Initialize target_height here

    target_x = random.randint(0, SCREEN_WIDTH - target_width)
    target_y = random.randint(0, SCREEN_HEIGTH - target_height)
    hits = 0  # Reset hits to 0
    running = True
    last_hit_time = pygame.time.get_ticks()  # Инициализируем время последнего попадания
    game_loop()  # Start the game loop

def game_loop():

    """Основной игровой цикл."""
    global running, target_x, target_y, hits, last_hit_time, show_target_duration, misses,screen, icon, target_image

    clock = pygame.time.Clock() # Добавлено для контроля FPS
    misses = 0 # Обнуляем счетчик промахов

    while running:
        screen.fill(COLOR_BACKGROUND) # Отрисовка фона

        current_time = pygame.time.get_ticks() # Текущее время

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if target_x < mouse_x < target_x + target_width and target_y < mouse_y < target_y + target_height:
                    target_x = random.randint(0, SCREEN_WIDTH - target_width)
                    target_y = random.randint(0, SCREEN_HEIGTH - target_height)
                    hits += 1  # Увеличиваем счетчик попаданий
                    print(f"Попал! Счет: {hits}")
                    last_hit_time = current_time # Обновляем время последнего попадания
                    misses = 0 # Обнуляем счетчик промахов
                else:
                   misses += 1
                   print(f"Мимо! Промахов: {misses}")
                   if misses >= MAX_MISSES:
                       print("Игра окончена! Слишком много промахов.")
                       running = False

        # Отрисовываем цели при соблюдении всех условий
        if misses < MAX_MISSES and current_time - last_hit_time <= show_target_duration:
            screen.blit(target_image, (target_x, target_y))

        # Обновляем видимость цели по времени (в миллисекундах)
        if hits < 20:
            show_target_duration = 2000
        else:
            show_target_duration = 1000

        pygame.display.flip()  # Используйте flip вместо update
        clock.tick(60) # Ограничение FPS до 60 (или любое другое значение)

    pygame.quit()

def save_record():
    """Сохранение рекорда в файл."""
    try:
        with open(RECORDS_FILE, "a") as f:
            f.write(f"{player_name}:{hits}\n")
        print("Рекорд сохранен!")
    except Exception as e:
        print(f"Ошибка сохранения рекорда: {e}")

def load_records():
    """Загрузка рекордов из файла."""
    records = []
    try:
        with open(RECORDS_FILE, "r") as f:
            for line in f:
                name, score = line.strip().split(":")
                records.append((name, int(score)))
    except FileNotFoundError:
        print("Файл рекордов не найден.")
    except Exception as e:
        print(f"Ошибка загрузки рекордов: {e}")
    return records

def show_records():
    """Отображение рекордов в диалоговом окне."""
    records = load_records()
    if not records:
        messagebox.showinfo("Рекорды", "Нет рекордов для отображения.")
        return

    record_text = "Рекорды:\n"
    for name, score in sorted(records, key=lambda x: x[1], reverse=True):
        record_text += f"{name}: {score}\n"

    messagebox.showinfo("Рекорды", record_text)

# --- Функции CustomTkinter ---
def start_game_command():
    """Запуск игры."""
    global player_name, running
    if not player_name:
        messagebox.showerror("Ошибка", "Пожалуйста, введите имя игрока.")
        return

    init_game()
    show_main_menu()  # Показываем главное меню после ввода имени

def show_records_command():
    """Показ рекордов."""
    show_records()

def exit_command():
    """Выход из программы."""
    if running:
        pygame.quit()
    app.destroy()

def on_name_entry_return(event):
    """Обработчик нажатия Enter в строке ввода имени."""
    global player_name

    name = name_entry.get()
    if name:
        player_name = name
        save_player_name(player_name)  # Сохраняем имя игрока
    name_entry.destroy()  # Удаляем строку ввода имени
    label_welcome.destroy()  # Удаляем приветствие
    show_main_menu()  # Показываем основное меню


def save_player_name(player_name):
    """Сохраняет имя игрока в файл, обновляя список."""
    # Файл для хранения имен игроков
    PLAYER_NAMES_FILE = os.path.join(os.path.expanduser("~"), "Documents", "megapush_player_names.txt")

    try:
        # Загружаем существующие имена
        existing_names = []
        if os.path.exists(PLAYER_NAMES_FILE):
            with open(PLAYER_NAMES_FILE, "r") as f:
                existing_names = [line.strip() for line in f]

        # Добавляем новое имя, если его еще нет
        if player_name not in existing_names:
            existing_names.append(player_name)

        # Записываем все имена обратно в файл
        with open(PLAYER_NAMES_FILE, "w") as f: # Открываем файл для записи (перезаписи)
            for name in existing_names:
                f.write(name + "\n")

        print(f"Имя игрока '{player_name}' сохранено/обновлено в файле.")
    except Exception as e:
        print(f"Ошибка при сохранении имени игрока: {e}")

def show_main_menu():
    """Отображает основное меню с кнопками."""
    global start_button, records_button, exit_button
    # Добавляем отступы
    for _ in range(3):  # Три пустых строки
        empty_label = customtkinter.CTkLabel(master=app, text="")
        empty_label.pack(pady=2, padx=10)
    # Создаем кнопки только один раз при первом вызове
    start_button = customtkinter.CTkButton(master=app, text="Начать игру", command=start_game_command)
    start_button.pack(pady=2, padx=10)

    records_button = customtkinter.CTkButton(master=app, text="Рекорды", command=show_records_command)
    records_button.pack(pady=2, padx=10)

    exit_button = customtkinter.CTkButton(master=app, text="Выход", command=exit_command)
    exit_button.pack(pady=2, padx=10)


# --- Создание окна CustomTkinter ---
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("400x300")
app.title("MegaPush")

# --- Ввод имени в начале ---
label_welcome = customtkinter.CTkLabel(master=app, text="Введите имя игрока:")
label_welcome.pack(pady=2, padx=10)

name_entry = customtkinter.CTkEntry(master=app)
name_entry.pack(pady=2, padx=10)
name_entry.bind("<Return>", on_name_entry_return) # Обработчик Enter

# --- Глобальные переменные для кнопок ---
start_button = None
records_button = None
exit_button = None

# --- Запуск окна CustomTkinter ---
app.mainloop()