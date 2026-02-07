from GUI.ToggleButton import ToggleButton

class ToggleGroup:
    """A group that ensures only one toggle button can be pressed at a time."""
    
    def __init__(self):
        self.buttons: list[ToggleButton] = []
        self.selected: ToggleButton = None
    
    def add_button(self, button: ToggleButton):
        """Add a button to the group."""
        button.on_press = lambda: self.on_button_pressed(button)
        self.buttons.append(button)
    
    def on_button_pressed(self, button: ToggleButton):
        """Handle button press - deselect others and select this one."""
        if self.selected is not None and self.selected != button:
            self.selected.set_toggled(False)
        if button.on_press is not None:
            button.on_press()
        self.selected = button
    
    def remove_button(self, button: ToggleButton):
        """Remove a button from the group."""
        if button in self.buttons:
            self.buttons.remove(button)
        if self.selected == button:
            self.selected = None