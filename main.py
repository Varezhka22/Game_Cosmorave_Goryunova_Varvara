import pygame
import sys
import random

pygame.init()
clock = pygame.time.Clock()

asteroid_timer = 0
asteroid_interval = 2000

running = True  # Установка флага для запуска игрового цикла
game_started = True  # Флаг, указывающий, что игра ещё не началась
displaying_lives_text = False  # Флаг, указывающий, что надпись с жизнями отображается

countdown = 4  # Начальное значение времени обратного отсчёта (4 секунды)
last_countdown_time = 0  # Время последнего события в отсчёте
game_start_time = 0 #Время для таймера

lives = 3  # Начальное количество жизней
collision_count = 0  # Счетчик столкновений
lives_text = ""  # Текст для отображения количества жизней
lives_text_display_time = 2000  # Время отображения надписи в миллисекундах (2 секунды)
lives_text_display_start = 0  # Время начала отображения надписи
best_results = []
game_start_time = 0


width = 405
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ИГРА")

background_image = pygame.image.load("Background.png")
background_image = pygame.transform.scale(background_image, (width, height))
stars_image = pygame.image.load("Stars.png")
stars_image = pygame.transform.scale(stars_image, (width, height))


#Настройки кнопок
button_width = 300
button_height = 100
text_color = (0, 0, 0)
button_color = (255, 255, 255)
hover_color = (200, 200, 200)
font_kino = pygame.font.Font("Kino-Regular.otf", 20)
title_font = pygame.font.Font("Kino-Regular.otf", 40)
title_text_color = (255, 255, 255)

# Словарь для хранения изображений астероидов
met_images = {}
# Загрузка изображений астероидов
met1_image = pygame.image.load("Met1.png")
met1_image = pygame.transform.scale(met1_image, (30, 30))
met_images["met1"] = met1_image  #Связь изображения с именем

met2_image = pygame.image.load("Met2.png")
met2_image = pygame.transform.scale(met2_image, (30, 30))
met_images["met2"] = met2_image

met3_image = pygame.image.load("Met3.png")
met3_image = pygame.transform.scale(met3_image, (30, 30))
met_images["met3"] = met3_image

met4_image = pygame.image.load("Met4.png")
met4_image = pygame.transform.scale(met4_image, (30, 30))
met_images["met4"] = met4_image

met5_image = pygame.image.load("Met5.png")
met5_image = pygame.transform.scale(met5_image, (30, 30))
met_images["met5"] = met5_image

met6_image = pygame.image.load("Met6.png")
met6_image = pygame.transform.scale(met6_image, (30, 30))
met_images["met6"] = met6_image

met7_image = pygame.image.load("Met7.png")
met7_image = pygame.transform.scale(met7_image, (30, 30))
met_images["met7"] = met7_image

met8_image = pygame.image.load("Met8.png")
met8_image = pygame.transform.scale(met8_image, (30, 30))
met_images["met8"] = met8_image

# Класс кнопок
class Button:
    def __init__(self, text, x, y, width, height, text_color, button_color, hover_color, font):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.font = font
        self.rendered_text = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.rendered_text.get_rect()
        self.text_rect.center = self.rect.center
        self.is_hovered = False

    def draw(self, screen):
        if self.is_hovered:
            pygame.draw.rect(screen, self.hover_color, self.rect, 0, 10)
        else:
            pygame.draw.rect(screen, self.button_color, self.rect, 0, 10)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 3)
        screen.blit(self.rendered_text, self.text_rect)

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
        else:
            self.is_hovered = False


# Класс Астеройдов
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, image, x, y, image_name):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(1, 5)
        self.rotation_angle = 0
        self.image_name = image_name

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.rotation_angle += 10

        self.image = pygame.transform.rotate(pygame.transform.scale(met_images[self.image_name], (30, 30)),
                                             self.rotation_angle)

        if self.rect.top > height:
            self.rect.y = random.randint(-100, -50)
            self.rect.x = random.randint(0, width - self.rect.width)
            self.speed_x = random.uniform(-1, 1)
            self.speed_y = random.uniform(1, 5)

    def create_new_asteroid(self):
        while True:
            x = random.randint(0, width)
            y = random.randint(-100, -50)
            random_asteroid = random.choice(
                [asteroid1, asteroid2, asteroid3, asteroid4, asteroid5, asteroid6, asteroid7, asteroid8])
            new_asteroid = Asteroid(random_asteroid.image, x, y, random_asteroid.image_name)
            new_asteroid.rotation_angle = random.uniform(0, 360)
            collisions = pygame.sprite.spritecollide(new_asteroid, asteroids, False)

            if not collisions:
                asteroids.add(new_asteroid)
                all_sprites.add(new_asteroid)
                break


# Класс Ракеты
class Rocket(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(image, (image.get_width() // 4, image.get_height() // 4))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 3

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.rect.left > 0:
                self.rect.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.rect.right < width:
                self.rect.x += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.rect.top > 0:
                self.rect.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if self.rect.bottom < height:
                self.rect.y += self.speed


title_text = "КосмоРейв"
title_button = title_font.render(title_text, True, title_text_color)
title_button_rect = title_button.get_rect(center=(width // 2, height // 3.5 - 50))

start_button = Button("Начать игру", width // 2 - button_width // 2, height // 2.5 - 50, button_width, button_height,
                      (255, 0, 0), button_color, hover_color, font_kino)
exit_button = Button("Выйти из игры", width // 2 - button_width // 2, height // 1.75 - 50, button_width, button_height,
                     text_color, button_color, hover_color, font_kino)

signature_text = "Работа Горюновой Варвары 4-МВ-5"
signature_font = pygame.font.Font("Kino-Regular.otf", 15)
signature_color = (255, 255, 255)
signature_text_rendered = signature_font.render(signature_text, True, signature_color)
signature_text_rect = signature_text_rendered.get_rect(center=(width // 2, height // 1 - 30))

font = pygame.font.Font("Kino-Regular.otf", 36)

# Создание объектов спрайтов для астероидов
asteroid1 = Asteroid(met1_image, random.randint(0, width), random.randint(-90, -50), "met1")
asteroid2 = Asteroid(met2_image, random.randint(0, width), random.randint(-150, -100), "met2")
asteroid3 = Asteroid(met3_image, random.randint(0, width), random.randint(-200, -150), "met3")
asteroid4 = Asteroid(met4_image, random.randint(0, width), random.randint(-250, -200), "met4")
asteroid5 = Asteroid(met5_image, random.randint(0, width), random.randint(-300, -250), "met5")
asteroid6 = Asteroid(met6_image, random.randint(0, width), random.randint(-350, -300), "met6")
asteroid7 = Asteroid(met7_image, random.randint(0, width), random.randint(-400, -350), "met7")
asteroid8 = Asteroid(met8_image, random.randint(0, width), random.randint(-450, -400), "met8")

rocket = Rocket(pygame.image.load("Rocket.png"), width // 2, height - 50)

all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
all_sprites.add(asteroid1, asteroid2, asteroid3, asteroid4, asteroid5, asteroid6, asteroid7, asteroid8, rocket)
asteroids.add(asteroid1, asteroid2, asteroid3, asteroid4, asteroid5, asteroid6, asteroid7, asteroid8)

countdown_font = pygame.font.Font("Kino-Regular.otf", 100)


#Функция вращения астеройдов
def rotate_image(image, angle):
    return pygame.transform.rotate(image, angle)

#Функция пересоздания астеройдов
def reset_asteroids():
    for asteroid in asteroids:
        asteroid.kill()

    # Создайте новые астероиды, как вы делали в начале
    asteroid1.create_new_asteroid()
    asteroid2.create_new_asteroid()
    asteroid3.create_new_asteroid()
    asteroid4.create_new_asteroid()
    asteroid5.create_new_asteroid()
    asteroid6.create_new_asteroid()
    asteroid7.create_new_asteroid()
    asteroid8.create_new_asteroid()

    for asteroid in asteroids:
        asteroid.rotation_angle = random.uniform(0, 360)

#Функция пересоздания игры
def reset_game():
    global game_started, collision_count, lives, game_start_time
    game_started = True
    collision_count = 0
    lives = 3
    game_start_time = pygame.time.get_ticks()  # Обновить глобальную переменную game_start_time
    reset_asteroids()



while running:  # Главный игровой цикл
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if exit_button.rect.collidepoint(event.pos):
                running = False
            elif start_button.rect.collidepoint(event.pos):
                reset_game()

    collisions = pygame.sprite.spritecollide(rocket, asteroids,
                                             False)  # Проверка столкновений между ракетой и астероидами

    mouse_pos = pygame.mouse.get_pos()  # Получение текущей позиции мыши
    start_button.check_hover(mouse_pos)  # Проверка наведения мыши на кнопку "Начать игру"
    exit_button.check_hover(mouse_pos)  # Проверка наведения мыши на кнопку "Выйти из игры"

    screen.blit(background_image, (0, 0))  # Отрисовка фонового изображения

    if game_started:  # Если игра уже началась
        screen.blit(stars_image, (0, 0))  # Отрисовка звёзд на фоне игрового экрана
        current_time = pygame.time.get_ticks() #Таймер
        time_elapsed = (current_time - game_start_time)

        # Время в минутах, секундах
        total_seconds = time_elapsed // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        # Отображение таймера
        timer_font = pygame.font.Font("Kino-Regular.otf", 20)
        timer_color = (255, 255, 255)
        timer_text = f"Время: {minutes:02}:{seconds:02}"
        timer_text_rendered = timer_font.render(timer_text, True, timer_color)
        timer_text_rect = timer_text_rendered.get_rect()
        timer_text_rect.topright = (width - 10, 10)
        screen.blit(timer_text_rendered, timer_text_rect)

        if collisions and not displaying_lives_text:  # Проверка, что надпись еще не отображалась
            displaying_lives_text = True  # флаг, что надпись нужно отобразить
            lives_text_display_start = pygame.time.get_ticks()  # Если произошло столкновение между ракетой и астероидами
            collision_count += 1  # Изменить счетчик столкновений
            lives -= 1  # Уменьшить количество жизней

            if lives > 0:
                lives_text = f"У Вас осталось {lives} жизни"
                reset_asteroids()  # Пересоздать астероиды
                game_start_time = pygame.time.get_ticks()  # Обновите таймер при восстановлении игры
            else:
                game_started = False  # Завершить игру
                lives_text = "Конец"
                message_text = "Вы проиграли"  # Вывести сообщение о проигрыше
                pygame.display.flip()  # Обновить экран
                pygame.time.delay(2000)  # Пауза перед выходом (2 секунды)

                displaying_lives_text = True  # флаг, что надпись нужно отобразить
                lives_text_display_start = pygame.time.get_ticks()  # Запомнить время начала отображения надписи

                # Теперь, после проигрыша, сравнить текущий результат с лучшими результатами
                current_time = pygame.time.get_ticks()
                time_elapsed = current_time - game_start_time

                # Добавить текущий результат в список лучших результатов и отсортировать его
                if not best_results:
                    best_results.append(time_elapsed)
                else:
                    best_results.append(time_elapsed)
                    best_results.sort()
                    if len(best_results) > 3:
                        best_results = best_results[:3]

            # Изменения для отображения лучших результатов
            if best_results:
                best_results_text = "Лучший результат:"
                y = height // 3
                for result in best_results:
                    minutes = result // 60000
                    seconds = (result % 60000) // 1000
                    result_str = f"{minutes:02}:{seconds:02}"
                    best_results_text += f"\n{result_str}"

                best_results_rendered = font_kino.render(best_results_text, True, (255, 0, 0))
                screen.blit(best_results_rendered, (width // 2 - best_results_rendered.get_width() // 2, y))

            displaying_lives_text = True  # Установить флаг, что надпись нужно отобразить
            lives_text_display_start = pygame.time.get_ticks()  # Запомнить время начала отображения надписи

            # Проверка, нужно ли отображать надпись
            if displaying_lives_text:
                current_time = pygame.time.get_ticks()

                if current_time - lives_text_display_start >= lives_text_display_time:
                    displaying_lives_text = False  # Закончить отображение надписи
                else:
                    lives_text_font = pygame.font.Font("Kino-Regular.otf", 20)
                    lives_text_color = (0, 0, 0)
                    background_color = (200, 200, 200)
                    lives_text_rendered = lives_text_font.render(lives_text, True, lives_text_color)
                    text_rect = lives_text_rendered.get_rect(center=(width // 2, height // 2))
                    background_rect = text_rect.inflate(10, 10)
                    background_rect.topleft = text_rect.topleft
                    pygame.draw.rect(screen, background_color, background_rect)
                    screen.blit(lives_text_rendered, text_rect)

        else:  # Если столкновения не произошло (игра продолжается)
            message_text = ""  # Сбросить текстовое сообщение
            all_sprites.update()  # Обновление всех спрайтов (астероидов и ракеты)
            all_sprites.draw(screen)  # Отрисовка всех спрайтов на экране
            displaying_lives_text = False

    else:  # Если игра ещё не началась (экран заголовка и кнопок)
        screen.blit(title_button, title_button_rect)  # Отрисовка заголовка игры и кнопок
        start_button.draw(screen)  # Отрисовка кнопки "Начать игру"
        exit_button.draw(screen)  # Отрисовка кнопки "Выйти из игры"
        screen.blit(signature_text_rendered, signature_text_rect)  # Отрисовка текста с подписью

    pygame.display.flip()  # Обновление экрана
    clock.tick(60)  # Ограничение скорости кадров до 60 кадров в секунду

pygame.quit()  # Завершение работы Pygame
sys.exit()  # Завершение программы