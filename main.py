import sys, time, pyaudio, wave, keyboard
from screen_recorder_sdk import screen_recorder 



now = time.strftime("%Y-%m-%d-%H-%M-%S")
screen_recorder.enable_dev_log ()

params = screen_recorder.RecorderParams ()

screen_recorder.init_resources (params)

print('Video Started')
filename = "Audio/{}.mp3".format(now)
chunk = 1024
FORMAT = pyaudio.paInt16
channels = 1
sample_rate = 44100
#record_seconds = (hours*3600+seconds)+1
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
    channels=channels,
    rate=sample_rate,
    input=True,
    output=True,
    frames_per_buffer=chunk)
frames = []

print("Audio Recording...")
screen_recorder.start_video_recording ('Video/{}.mp4'.format(now), 60, 9000000, True)
while True:
    data = stream.read(chunk)
    frames.append(data)
    if keyboard.is_pressed('F9'):
        break

while True:
    try:
        if keyboard.is_pressed('F9'):
            p.terminate()
            wf = wave.open(filename, "wb")
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(sample_rate)
            wf.writeframes(b"".join(frames))
            wf.close()
            screen_recorder.stop_video_recording ()
            stream.stop_stream()
            stream.close()
            print("Audio finished recording.")
            print('Video Stopped')
            break
    except KeyboardInterrupt:
        break