from utils import resource_path
from pygame import mixer

class AudioPlayer():
    def __init__(self, audio_file_path):
        self.mixer = mixer
        self.mixer.init()
        self.mixer.music.load(resource_path(audio_file_path))
        self.mixer.music.set_volume(0.5)

    def play(self):
        self.mixer.music.play()
        print("Audio played")

    def stop(self):
        self.mixer.music.stop()
        print("Audio stopped")

    def set_volume(self, volume):
        self.mixer.music.set_volume(volume)
        print(f"Audio volume set to {volume}")
