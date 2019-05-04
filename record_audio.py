import pyaudio
import wave
import datetime
from pathlib import Path



def record(s, output_dir):

    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = s
    WAVE_OUTPUT_FILENAME = output_dir.joinpath(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".wav")
    
    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(
        format=FORMAT, 
        channels=CHANNELS,
        rate=RATE, 
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open(str(WAVE_OUTPUT_FILENAME), 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()



if __name__ == '__main__':

    output_dir = Path('recordings').joinpath(datetime.datetime.now().strftime("%Y-%m-%d"))

    output_dir.mkdir(parents = True, exist_ok = True)

    minute_chunk = 10

    hours = 11

    for j in range(int((60 / minute_chunk) * hours)):

        print(j, 'beginning recording..', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))

        try:

          record(s = 60 * minute_chunk, output_dir = output_dir)

        # if OSError: [Errno -9981] Input overflowed happens try again
        except OSError: 

          record(s = 60 * minute_chunk, output_dir = output_dir)





