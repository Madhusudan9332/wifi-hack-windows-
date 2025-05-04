
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from core.wifi_manager import WifiManager
from core.file_handler import FileHandler

class WifiUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)

        self.ssid_spinner = Spinner(text='Select Wi-Fi Network')
        self.add_widget(self.ssid_spinner)

        self.file_label = Label(text='No file selected')
        self.add_widget(self.file_label)

        self.file_chooser = FileChooserIconView(filters=['*.txt', '*.xml'])
        self.file_chooser.bind(selection=self.on_file_selected)
        self.add_widget(self.file_chooser)

        self.checkbox_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        self.algorithm_checkbox = CheckBox()
        self.checkbox_layout.add_widget(self.algorithm_checkbox)
        self.checkbox_layout.add_widget(Label(text='Use SSID-based Algorithm'))
        self.add_widget(self.checkbox_layout)

        self.connect_button = Button(text='Connect')
        self.connect_button.bind(on_press=self.connect_wifi)
        self.add_widget(self.connect_button)

        self.output = TextInput(readonly=True, size_hint_y=2)
        self.add_widget(self.output)

        self.wifi_manager = WifiManager()
        self.file_handler = FileHandler()
        self.load_networks()

    def load_networks(self):
        ssids = self.wifi_manager.scan_networks()
        self.ssid_spinner.values = ssids

    def on_file_selected(self, instance, selection):
        if selection:
            self.file_label.text = selection[0]

    def connect_wifi(self, instance):
        ssid = self.ssid_spinner.text
        file_path = self.file_label.text
        use_algorithm = self.algorithm_checkbox.active

        if use_algorithm:
            results = self.wifi_manager.connect_with_algorithm(ssid)
            for line in results:
                self.output.text += line
            return

        if file_path.endswith('.xml'):
            self.output.text += self.wifi_manager.connect_with_profile(ssid, file_path)
        elif file_path.endswith('.txt'):
            results = self.wifi_manager.connect_with_passwords(ssid, file_path)
            for line in results:
                self.output.text += line
        else:
            self.output.text += "Unsupported file type.\n"
