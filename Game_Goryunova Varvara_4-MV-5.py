import pygame
import sys

pygame.init()

width = 405
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ИГРА")

#Загрузка фона для стартового окна
background_image = pygame.image.load("Background.png")
background_image = pygame.transform.scale(background_image, (width, height))

#Класс для кнопок
class Button:
    def __init__(self, text, x, y, width, height, text_color, button_color, font):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.text_color = text_color
        self.button_color = button_color
        self.font = font
        self.rendered_text = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.rendered_text.get_rect()
        self.text_rect.center = self.rect.center  # Центрирование текста в кнопке

    def draw(self, screen):
        pygame.draw.rect(screen, self.button_color, self.rect, 0, 10)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 3)  # Черная обводка
        screen.blit(self.rendered_text, self.text_rect)


button_width = 300
button_height = 100
text_color = (0, 0, 0)
button_color = (255, 255, 255)
font_kino = pygame.font.Font("Kino-Regular.otf", 20)

title_text = "КосмоРейв"
title_button = pygame.font.Font(None, 36).render(title_text, True, (0, 0, 0))
title_button_rect = title_button.get_rect(center=(width // 2, height // 5 - 50))

start_button = Button("Начать игру", width // 2 - button_width // 2, height // 3 - 50, button_width, button_height, (255, 0, 0), button_color, font_kino)
results_button = Button("Посмотреть результаты", width // 2 - button_width // 2, height // 2 - 50, button_width, button_height, text_color, button_color, font_kino)
exit_button = Button("Выйти из игры", width // 2 - button_width // 2, height // 1.5 - 50, button_width, button_height, text_color, button_color, font_kino)










#Управление работой игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if exit_button.rect.collidepoint(event.pos):
                running = False


#Отображение созданных объектов
    screen.blit(background_image, (0, 0))
    screen.blit(title_button, title_button_rect)
    start_button.draw(screen)
    results_button.draw(screen)
    exit_button.draw(screen)
    pygame.display.flip()


pygame.quit()
sys.exit()  # Выход из программы