from . import Button

class ExitButton(Button):
    def __init__(self, parent, position = (800-81,1)):
        Button.__init__(self, parent,'EXIT', None, position)

    def on_click(self):
        pygame.event.post(pygame.event.Event(QUIT))
