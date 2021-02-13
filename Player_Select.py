import arcade
from arcade import gui
import State


class PlayButton(gui.UIFlatButton):
    def __init__(self, ui_manager):
        super().__init__('Enter', State.state.screen_center.x, State.state.screen_center.y, 250, 50)
        self.ui_manager = ui_manager

    def on_click(self):
        import Exploration
        self.ui_manager.purge_ui_elements()
        State.state.window.show_view(Exploration.Explore())


class PlayerSelect(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = gui.UIManager()
        self.ui_manager.add_ui_element(PlayButton(self.ui_manager))
