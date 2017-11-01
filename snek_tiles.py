from random import random
from time import sleep

import pygame

size = width, height = 600, 900
black = 0, 0, 0
yellow = 230, 214, 23
blue = 22, 96, 165
light_blue = 73, 185, 249
pink = 251, 117, 228
grey = 140, 147, 149
red = 242, 59, 76
green = 19, 232, 174
orange = 226, 115, 45
white = 227, 231, 234


def process_tracks(screen, tracks, pressed):
    health_delta = 0
    score_delta = 0
    for i, track in enumerate(tracks):
        x = 100 * i
        for j, y in enumerate(track):
            if j == 0:
                if pressed[i] and 750 <= y <= 800:
                    score_delta += 1
                    tracks[i].pop(0)
                    continue
                elif y > 800:
                    health_delta -= 1
                    tracks[i].pop(0)
                    continue
            rect = [x + 20, y, 60, 50]
            pygame.draw.ellipse(screen, light_blue, rect, 5)
            tracks[i][j] += 1
        if (not track or track[-1] > 50) and random() < 0.0005:
            tracks[i].append(0)
    return health_delta, score_delta


def draw_lines(screen):
    keys = pygame.key.get_pressed()
    pressed = [keys[pygame.K_h], keys[pygame.K_j],
               keys[pygame.K_k], keys[pygame.K_l]]
    for i, x in enumerate((0, 100, 200, 300, 400)):
        colour = pink if x in (0, 400) else blue
        pygame.draw.line(screen, colour, [x, 0], [x, 900])
        if x != 400:
            line_colour = yellow if pressed[i] else grey
            pygame.draw.line(screen, line_colour, [x, 800], [x + 100, 800])


def render_text(screen, font, score, health):
    score_text = font.render(f'Score: {score}', 1, green)
    health_text = font.render(f'Health: {health}', 1, red)
    screen.blit(health_text, (420, 10))
    screen.blit(score_text, (420, 30))


def game_over(screen, score):
    score_font = pygame.font.Font(None, 30)
    prompt_font = pygame.font.Font(None, 25)
    score_text = f'Game Over, your score is {score}'
    prompt_text = 'Press Enter to restart, press any other key to quit.'

    score_text = score_font.render(score_text, 1, orange)
    prompt_text = prompt_font.render(prompt_text, 1, grey)

    score_rect = score_text.get_rect(center=(width / 2, 200))
    prompt_rect = prompt_text.get_rect(center=(width / 2, 220))
    screen.blit(score_text, score_rect)
    screen.blit(prompt_text, prompt_rect)


def show_help(screen):
    help_msg = (
        'Try to catch the notes falling down from the four tracks.',
        'Press H, J, K, L keys when the notes arrive at the grey line.',
        'You lose one health per missed notes, good luck.',
        'Press Enter to start, press any other keys to quit.'
    )
    font = pygame.font.Font(None, 30)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                else:
                    exit(0)
        screen.fill(black)
        y = 300
        for i, s in enumerate(help_msg):
            text = font.render(s, 1, white)
            rect = text.get_rect(center=(width / 2, y))
            screen.blit(text, rect)
            y += 20
            if i == 2:
                y += 20
        pygame.display.flip()


def main(display_help=True):
    screen = pygame.display.set_mode(size)
    pygame.init()
    font = pygame.font.Font(None, 30)
    tracks = [[], [], [], []]
    health = 15
    score = 0
    if display_help:
        show_help(screen)
    while True:
        pressed = [False, False, False, False]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_h:
                    pressed[0] = True
                elif key == pygame.K_j:
                    pressed[1] = True
                elif key == pygame.K_k:
                    pressed[2] = True
                elif key == pygame.K_l:
                    pressed[3] = True
                elif health <= 0:
                    if key == pygame.K_RETURN:
                        main(False)
                    else:
                        exit(0)
        screen.fill(black)
        if health > 0:
            health_delta, score_delta = process_tracks(screen, tracks, pressed)
            score += score_delta
            health += health_delta
            render_text(screen, font, score, health)
            draw_lines(screen)
        if health <= 0:
            game_over(screen, score)
        pygame.display.flip()
        sleep(0.001)


if __name__ == '__main__':
    main()
