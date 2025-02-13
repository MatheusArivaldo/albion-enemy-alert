import customtkinter

class Visual(customtkinter.CTk):
    def __init__(self, onStartButtonClicked, onVolumeSliderChanged, onThresholdSliderChanged):
        super().__init__()
        self.geometry("350x250")

        self.title("Albion Enemy Alert")
        self.resizable(False, False)

        self.onStartButtonClicked = onStartButtonClicked
        self.onVolumeSliderChanged = onVolumeSliderChanged
        self.onThresholdSliderChanged = onThresholdSliderChanged

        self.button = customtkinter.CTkButton(self, text="Iniciar Verificar", command=self.start_btn_callback)
        self.button.pack(padx=10, pady=20)

        self.label = customtkinter.CTkLabel(self, text="Threshold")
        self.label.pack()
        self.threshold = customtkinter.CTkSlider(self, from_=0, to=1, number_of_steps=20, variable=customtkinter.DoubleVar(value=0.8), command=self.threshold_slider_callback)
        self.threshold.pack(padx=10, pady=10)

        self.label = customtkinter.CTkLabel(self, text="Volume")
        self.label.pack()
        self.slider = customtkinter.CTkSlider(self, from_=0, to=1,command=self.volume_slider_callback)
        self.slider.pack(padx=10, pady=20)

    def start_btn_callback(self):
        print("Iniciar Verificação")
        if self.onStartButtonClicked is not None:
            self.onStartButtonClicked()

    def volume_slider_callback(self, value):
        print(f"Volume: {value}")
        if self.onVolumeSliderChanged is not None:
            self.onVolumeSliderChanged(value)

    def threshold_slider_callback(self, value):
        print(f"Threshold: {value}")
        if self.onThresholdSliderChanged is not None:
            self.onThresholdSliderChanged(value)

    def set_button_text(self, text):
        self.button.configure(text=text)

    def set_button_color(self, color):
        self.button.configure(fg_color=color)
