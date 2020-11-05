import pygame
from pygame_widgets import Button, Slider, TextBox

pygame.init()
win = pygame.display.set_mode((1000, 600))

def write():
    x = slider.getValue()
    print(x)

slider = Slider(win, 50, 30, 300, 30, min=10, max=50, step=1)
output = TextBox(win, 380, 30, 30, 30, fontSize=18)
button = Button(
            win, 450, 30, 100, 30, text='Generate',
            fontSize=18, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=write
         )

run = True

while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((255, 255, 255))

    slider.listen(events)
    slider.draw()
    button.listen(events)
    button.draw()

    output.setText(slider.getValue())

    output.draw()

    pygame.display.update()