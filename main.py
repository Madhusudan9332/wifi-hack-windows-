
from kivy.app import App
from ui.main_screen import WifiUI

class WifiConnectorApp(App):
    def build(self):
        return WifiUI()

if __name__ == '__main__':
    WifiConnectorApp().run()
