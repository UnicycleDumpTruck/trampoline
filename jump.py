#!/usr/bin/env python3
import sys
from pygame.locals import (
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)
import time
from jsession import Session
import automationhat
import pygame

import requests
import json

from loguru import logger
import telemetry

logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("main.log", rotation="1024 MB")

beam_was_broken = 0
beam_brake = 0
session = Session()

automationhat.enable_auto_lights(False)

pygame.init()

pygame.mouse.set_visible(False)

display_width = 1280
display_height = 800

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
grey = (128, 128, 128)

counterDisplay = pygame.display.set_mode((display_width, display_height))

red_background_image = pygame.image.load(
    "/home/exhibits/Trampoline/red.png").convert()
blue_background_image = pygame.image.load(
    "/home/exhibits/Trampoline/blue.png").convert()
black_background_image = pygame.image.load(
    "/home/exhibits/Trampoline/black.png").convert()

gilroy_location = '/home/exhibits/Trampoline/Gilroy-Bold.ttf'
gilsans_location = '/home/exhibits/Trampoline/GillSans-Bold.ttf'

current_background = red_background_image
text_color = white
current_font = gilroy_location

counterDisplay.blit(current_background, [0, 0])
pygame.display.set_caption('Trampoline Counter')
clock = pygame.time.Clock()


def text_objects(text, font):
    textSurface = font.render(text, True, text_color)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font(current_font, 400)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    counterDisplay.blit(current_background, [0, 0])
    counterDisplay.blit(TextSurf, TextRect)
    pygame.display.update()


def count_display(number):
    text = f"{number}"
    if len(text) < 4:
        largeText = pygame.font.Font(current_font, 600)
    elif len(text) == 4:
        largeText = pygame.font.Font(current_font, 500)
    elif len(text) == 5:
        largeText = pygame.font.Font(current_font, 400)
    elif len(text) == 6:
        largeText = pygame.font.Font(current_font, 330)
    elif len(text) == 7:
        largeText = pygame.font.Font(current_font, 300)
    elif len(text) == 8:
        largeText = pygame.font.Font(current_font, 250)
    elif len(text) == 9:
        largeText = pygame.font.Font(current_font, 220)
    elif len(text) == 10:
        largeText = pygame.font.Font(current_font, 200)
    elif len(text) == 11:
        largeText = pygame.font.Font(current_font, 180)
    elif len(text) == 12:
        largeText = pygame.font.Font(current_font, 150)

    else:
        largeText = pygame.font.Font(current_font, 100)

    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), ((display_height/2) + 70))
    counterDisplay.blit(current_background, [0, 0])
    counterDisplay.blit(TextSurf, TextRect)
    pygame.display.update()


if automationhat.is_automation_hat():
    automationhat.light.power.write(1)


#test_count = 1
message_display("Jump!")

running = True

logger.info("Trampoline code commencing.")

while running:
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            if event.key == K_1:
                current_background = black_background_image
                message_display("Jump!")
            if event.key == K_2:
                current_background = blue_background_image
                message_display("Jump!")
            if event.key == K_3:
                current_background = red_background_image
                message_display("Jump!")
            if event.key == K_4:
                text_color = white
                message_display("Jump!")
            if event.key == K_5:
                text_color = black
                message_display("Jump!")
            if event.key == K_6:
                text_color = red
                message_display("Jump!")
            if event.key == K_7:
                current_font = gilroy_location
                message_display("Jump!")
            if event.key == K_8:
                current_font = gilsans_location
                message_display("Jump!")

            # if event.key == K_SPACE:
            #    count_display(test_count)
            #    test_count = test_count * 10

            # Was it the Escape key? If so, stop the loop.
            elif event.key == K_ESCAPE:
                running = False

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running = False

    beam_brake = automationhat.input.one.read()
    if beam_brake:
        if beam_was_broken:
            continue
        beam_was_broken = 1
        if not session.active:
            session.start()
        session.add_jump()
        temperature = automationhat.analog.four.read()
        temperature = round(((((temperature - 0.5) * 100) * 1.8) + 32), 1)
        #print(f"Jump: {session.jump_count}, Temperature: {temperature}")
        count_display(session.jump_count)

    else:
        beam_was_broken = 0
        if (session.active and ((time.time() - session.time_of_last_jump) > 15)):
            session.log_stop_clear()
            message_display("Jump!")

    time.sleep(0.1)
