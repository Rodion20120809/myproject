import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Вікторина з режимами")

font = pygame.font.SysFont("Arial", 30)

pygame.mixer.music.load("sounds/da-da-net-net.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

correct_sound = pygame.mixer.Sound("sounds/mellstroy-raduet (mp3cut.net).mp3")
correct_sound.set_volume(.3)
wrong_sound = pygame.mixer.Sound("sounds/otkazano.mp3")
wrong_sound.set_volume(.8)

win_sound = pygame.mixer.Sound("sounds/mellstroy-raduet (mp3cut.net).mp3")
lose_sound = pygame.mixer.Sound("sounds/otkazano.mp3")

modes_questions = {
    "Загальний": [
        ("Столиця України?", ["Київ", "Львів", "Харків", "Одеса"], 0),
        ("Автор Кобзаря?", ["Франко", "Шевченко", "Леся", "Котляревський"], 1),
        ("Колір неба?", ["Червоний", "Синій", "Зелений", "Жовтий"], 1),
        ("Днів у тижні?", ["5", "6", "7", "8"], 2),
        ("Найбільша тварина?", ["Слон", "Кит", "Жираф", "Акула"], 1),
        ("Мова на P?", ["Java", "Python", "C++", "Ruby"], 1),
        ("Який метал рідкий за кімнатної температури?", ["Залізо", "Ртуть", "Мідь", "Свинець"], 1),
        ("Яка планета найбільша в Сонячній системі?", ["Марс", "Сатурн", "Юпітер", "Нептун"], 2),
        ("Скільки зубів у дорослої людини (в нормі)?", ["28", "30", "32", "36"], 2),
        ("Супутник Землі?", ["Марс", "Місяць", "Сонце", "Фобос"], 1)
    ],
    "Математика": [
        ("5 + 7 = ?", ["10", "12", "13", "14"], 1),
        ("9 * 3 = ?", ["27", "21", "18", "24"], 0),
        ("Корінь з 64?", ["6", "7", "8", "9"], 2),
        ("2 ^ 5 = ?", ["16", "32", "64", "10"], 1),
        ("Скільки градусів у прямому куті?", ["45", "90", "180", "360"], 1),
        ("150 - 65 = ?", ["75", "85", "95", "65"], 1),
        ("Яке число йде за числом Пі (перші два знаки)?", ["3.14", "3.15", "3.12", "3.16"], 0),
        ("Скільки指揮 у гексагона (шестикутника)?", ["5", "6", "7", "8"], 1),
        ("7 * 8 = ?", ["54", "56", "62", "48"], 1),
        ("100 / 4 = ?", ["20", "25", "30", "15"], 1)
    ],
    "Географія": [
        ("Найближча планета до Сонця?", ["Венера", "Земля", "Меркурій", "Марс"], 2),
        ("Найбільший океан?", ["Атлантичний", "Індійський", "Тихий", "Арктичний"], 2),
        ("Найдовша річка у світі?", ["Амазонка", "Ніл", "Міссісіпі", "Дніпро"], 1),
        ("Яка країна найбільша за площею в Європі?", ["Франція", "Україна", "Німеччина", "Іспанія"], 1),
        ("Столиця Франції?", ["Лондон", "Берлін", "Рим", "Париж"], 3),
        ("Який континент найхолодніший?", ["Азія", "Антарктида", "Африка", "Австралія"], 1),
        ("В якій країні знаходяться піраміди Гізи?", ["Греція", "Єгипет", "Італія", "Мексика"], 1),
        ("Яке море омиває південь України?", ["Чорне", "Балтійське", "Середземне", "Червоне"], 0),
        ("Найвища гора у світі?", ["Кіліманджаро", "Ельбрус", "Еверест", "Говерла"], 2),
        ("Столиця Японії?", ["Pekін", "Сеул", "Токіо", "Кіото"], 2)
    ]
}

questions = []
current_q = 0
score = 0
game_state = "MENU"
current_mode = ""
sound_played = False


def draw_text_centered(text, y, color=(255, 255, 255)):
    text_width, _ = font.size(text)
    x = (WIDTH - text_width) // 2
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_exit_button():
    btn_width = 250
    btn_height = 55
    btn_x = (WIDTH - btn_width) // 2
    btn_y = 710
    exit_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
    pygame.draw.rect(screen, (180, 40, 40), exit_rect, border_radius=10)

    tw, th = font.size("Вихід")
    screen.blit(font.render("Вихід", True, (255, 255, 255)),
                (exit_rect.x + (btn_width - tw) // 2, exit_rect.y + (btn_height - th) // 2))
    return exit_rect


def draw_menu():
    screen.fill((20, 20, 40))
    draw_text_centered("ОБЕРИ СВІЙ РЕЖИМ ГРИ", 120, (255, 215, 0))

    modes = ["Загальний", "Математика", "Географія"]
    menu_buttons = []

    btn_width = 500
    btn_height = 70
    btn_x = (WIDTH - btn_width) // 2

    for i, mode_name in enumerate(modes):
        btn_y = 250 + i * 105
        rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
        pygame.draw.rect(screen, (50, 120, 100), rect, border_radius=15)

        tw, th = font.size(mode_name)
        screen.blit(font.render(mode_name, True, (255, 255, 255)),
                    (rect.x + (btn_width - tw) // 2, rect.y + (btn_height - th) // 2))
        menu_buttons.append((rect, mode_name))

    return menu_buttons


def draw_question():
    screen.fill((30, 30, 30))
    q, options, _ = questions[current_q]

    draw_text_centered(f"Режим: {current_mode} | Питання {current_q + 1} з {len(questions)}", 40, (150, 150, 150))
    draw_text_centered(q, 120)

    buttons = []
    btn_width = 800
    btn_height = 60
    btn_x = (WIDTH - btn_width) // 2

    for i, option in enumerate(options):
        btn_y = 220 + i * 85
        rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
        pygame.draw.rect(screen, (70, 70, 200), rect, border_radius=10)

        opt_width, opt_height = font.size(option)
        text_x = rect.x + (btn_width - opt_width) // 2
        text_y = rect.y + (btn_height - opt_height) // 2

        img = font.render(option, True, (255, 255, 255))
        screen.blit(img, (text_x, text_y))
        buttons.append(rect)

    return buttons


def draw_result():
    global sound_played
    screen.fill((15, 15, 15))

    if not sound_played:
        pygame.mixer.music.stop()
        if score >= 7:
            win_sound.play()
        else:
            lose_sound.play()
        sound_played = True

    draw_text_centered(f"Твій результат: {score} з {len(questions)}", 200, (255, 255, 255))
    if score >= 7:
        draw_text_centered("Ти виграв!", 280, (100, 255, 100))
    else:
        draw_text_centered("Ти програв!", 280, (255, 100, 100))

    btn_width = 400
    btn_height = 70

    retry_rect = pygame.Rect(WIDTH // 2 - 450, 420, btn_width, btn_height)
    pygame.draw.rect(screen, (50, 150, 50), retry_rect, border_radius=12)
    tw1, th1 = font.size("Грати знову")
    screen.blit(font.render("Грати знову", True, (255, 255, 255)),
                (retry_rect.x + (btn_width - tw1) // 2, retry_rect.y + (btn_height - th1) // 2))

    menu_rect = pygame.Rect(WIDTH // 2 + 50, 420, btn_width, btn_height)
    pygame.draw.rect(screen, (150, 50, 50), menu_rect, border_radius=12)
    tw2, th2 = font.size("В головне меню")
    screen.blit(font.render("В головне меню", True, (255, 255, 255)),
                (menu_rect.x + (btn_width - tw2) // 2, menu_rect.y + (btn_height - th2) // 2))

    return retry_rect, menu_rect


running = True
menu_buttons = []
game_buttons = []

while running:
    if game_state == "MENU":
        menu_buttons = draw_menu()
        exit_btn = draw_exit_button()
    elif game_state == "GAME":
        if current_q < len(questions):
            game_buttons = draw_question()
            exit_btn = draw_exit_button()
        else:
            game_state = "RESULT"
    elif game_state == "RESULT":
        retry_btn, lobby_btn = draw_result()
        exit_btn = draw_exit_button()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if exit_btn.collidepoint(mouse_pos):
                running = False
                break

            if game_state == "MENU":
                for rect, mode_name in menu_buttons:
                    if rect.collidepoint(mouse_pos):
                        current_mode = mode_name
                        questions = modes_questions[mode_name]
                        current_q = 0
                        score = 0
                        sound_played = False
                        game_state = "GAME"
                        break

            elif game_state == "GAME":
                _, _, correct = questions[current_q]
                for i, btn in enumerate(game_buttons):
                    if btn.collidepoint(mouse_pos):
                        if i == correct:
                            score += 1
                            correct_sound.play()
                        else:
                            wrong_sound.play()

                        current_q += 1
                        break

            elif game_state == "RESULT":
                if retry_btn.collidepoint(mouse_pos):
                    questions = modes_questions[current_mode]
                    current_q = 0
                    score = 0
                    sound_played = False
                    pygame.mixer.music.play(-1)
                    game_state = "GAME"

                elif lobby_btn.collidepoint(mouse_pos):
                    sound_played = False
                    pygame.mixer.music.play(-1)
                    game_state = "MENU"

pygame.quit()
sys.exit()
