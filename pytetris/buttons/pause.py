from .basic import Button

class PauseButton(Button):
    def __init__(self, parent, image, position = (300,300)):
        Button.__init__(self, parent, 'Start / Pause', image, position)
    def on_click(self):
        self.parent.paused = not self.parent.paused

