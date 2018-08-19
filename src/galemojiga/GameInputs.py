import pygame
import galemojiga.globals as globals


def get_input_dict(events):
    event_dict = {'key_down': set(),
                  'key_up': set()}

    for event in events:
        if event.type == pygame.KEYDOWN:
            event_dict['key_down'].add(event.key)
        elif event.type == pygame.KEYUP:
            event_dict['key_up'].add(event.key)
    return event_dict

