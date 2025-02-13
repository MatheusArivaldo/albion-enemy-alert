import customtkinter

class Visual(customtkinter.CTk):
    def __init__(self, onStartButtonClicked, onVolumeSliderChanged):
        super().__init__()
        self.geometry("200x150")

        self.title("Albion Enemy Alert")
        self.resizable(False, False)

        self.onStartButtonClicked = onStartButtonClicked
        self.onVolumeSliderChanged = onVolumeSliderChanged

        self.button = customtkinter.CTkButton(self, text="Iniciar Verificar", command=self.start_btn_callback)
        self.button.pack(padx=20, pady=20)

        self.slider = customtkinter.CTkSlider(self, from_=0, to=1, command=self.volume_slider_callback)
        self.slider.pack(padx=20, pady=20)

    def start_btn_callback(self):
        print("Iniciar Verificação")
        if self.onStartButtonClicked is not None:
            self.onStartButtonClicked()

    def volume_slider_callback(self, value):
        print(f"Volume: {value}")
        if self.onVolumeSliderChanged is not None:
            self.onVolumeSliderChanged(value)

    def set_button_text(self, text):
        self.button.configure(text=text)

    def set_button_color(self, color):
        self.button.configure(fg_color=color)
