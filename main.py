import pygame
import sys

pygame.init()

# Налаштування екрану
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Вікторина")

font = pygame.font.SysFont("Arial", 30)

# Звуки
win_sound = pygame.mixer.Sound("mellstroy-raduet.mp3")
lose_sound = pygame.mixer.Sound("mellstroi-otkazano (mp3cut (mp3cut.net).mp3")

# Питання
questions = [
    ("Столиця України?", ["Київ", "Львів", "Харків", "Одеса"], 0),
    ("5 + 7 = ?", ["10", "12", "13", "14"], 1),
    ("Найближча планета до Сонця?", ["Венера", "Земля", "Меркурій", "Марс"], 2),
    ("Автор Кобзаря?", ["Франко", "Шевченко", "Леся", "Котляревський"], 1),
    ("Колір неба?", ["Червоний", "Синій", "Зелений", "Жовтий"], 1),
    ("Днів у тижні?", ["5", "6", "7", "8"], 2),
    ("Найбільша тварина?", ["Слон", "Кит", "Жираф", "Акула"], 1),
    ("Мова на P?", ["Java", "Python", "C++", "Ruby"], 1),
    ("9 * 3 = ?", ["27", "21", "18", "24"], 0),
    ("Найбільший океан?", ["Атлантичний", "Індійський", "Тихий", "Арктичний"], 2)
]

current_q = 0
score = 0

def draw_text(text, x, y):
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (x, y))

def draw_question():
    screen.fill((30, 30, 30))
    q, options, _ = questions[current_q]

    draw_text(q, 50, 50)

    buttons = []
    for i, option in enumerate(options):
        rect = pygame.Rect(100, 150 + i*80, 600, 50)
        pygame.draw.rect(screen, (70, 70, 200), rect)
        draw_text(option, rect.x + 10, rect.y + 10)
        buttons.append(rect)

    return buttons

def show_result():
    screen.fill((0, 0, 0))
    draw_text(f"Результат: {score}/10", 300, 200)

    if score >= 7:
        draw_text("Ти виграв!", 320, 300)
        win_sound.play()
    else:
        draw_text("Ти програв!", 320, 300)
        lose_sound.play()

    pygame.display.flip()
    pygame.time.delay(3000)

# Головний цикл
running = True
while running:
    if current_q < len(questions):
        buttons = draw_question()
    else:
        show_result()
        break

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            _, _, correct = questions[current_q]

            for i, btn in enumerate(buttons):
                if btn.collidepoint(mouse_pos):
                    if i == correct:
                        score += 1
                    current_q += 1

pygame.quit()
sys.exit()