from .basic import Button

class NewGameButton(Button):

    def __init__(self, parent, image, position = (300,300)):
        Button.__init__(self, parent, 'New Game', image, position)

    def on_click(self):
        self.parent.reset()

