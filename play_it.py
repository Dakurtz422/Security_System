import concurrent.futures
import simpleaudio

def alert(lst):
    wave_obj = simpleaudio.WaveObject.from_wave_file("ss.wav")
    play_obj = wave_obj.play()


def PlayIt(lst):
    with concurrent.futures.ThreadPoolExecutor() as exe:
        exe.map(alert, lst)
