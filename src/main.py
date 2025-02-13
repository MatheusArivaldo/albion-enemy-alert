from visual import Visual
from audio import AudioPlayer
from scanner import Scanner

def toggle_scan():
    if scanner.running:
        scanner.stop()
        visual.set_button_text("Iniciar Verificar")
    elif not scanner.running:
        scanner.start()
        visual.set_button_text("Parar Verificar")

if __name__ == "__main__":
    audio = AudioPlayer("assets\\audio\\alert.mp3")
    scanner = Scanner(1, "assets\\images\\target_image.png", audio.play, audio.stop)

    visual = Visual(toggle_scan, audio.set_volume)
    visual.mainloop()
