import RPi.GPIO as GPIO
import pyaudio
import wave
import time
from AnalogPin import Pin

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 4096
RECORD_SECONDS = 3 # change this to a variable
dev_index = 2
WAVE_OUTPUT_FILENAME = "out.wav"

p = pyaudio.PyAudio()

#GPIO pin setup for button
ledPin = 18 #BCM 24
startpot = 19 #BCM 10
finishpot = 21 #BCM 9
buttonPin = 23 #BCM 11
buttonPin2 = 24 #BCM 8

#set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#enable LED and button (button with pull-up)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
apot = Pin(startpot, minResistance=2200, capacitance=0.000001, timeout=0.03333)
bpot = Pin(finishpot, minResistance=2200, capacitance=0.000001, timeout=0.03333)
# setup other 2 pot start and finish pins

#set LED to OFF
GPIO.output(ledPin, GPIO.LOW)

def map_pots(start, finish):
    # change this math based on experiments
    scaled_start = start/1
    scaled_finish = finish/1
    return scaled_start, scaled_finish

while True:
    #wait for button to be pressed
    time.sleep(0.2)
    GPIO.wait_for_edge(buttonPin, GPIO.FALLING)

    frames = []
    try:
        stream = audio.open(format = FORMAT,rate = RATE,channels = CHANNELS, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=CHUNK)
        #turn on LED when recording starts
        GPIO.output(ledPin, GPIO.HIGH)

        print("Recording")
        #record as long as button held down
        while GPIO.input(buttonPin) == 1:
            print("button held down")
            data = stream.read(CHUNK)
            frames.append(data)
        # button released
        print("Done Recording")
        GPIO.output(ledPin, GPIO.LOW)
        stream.stop_stream()
        stream.close()
        p.terminate()
    except IOError:
        break

    #make wave file from recorded data stream
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()   

    while GPIO.input(buttonPin2) == 0: # while you dont press the second button
        wave_file = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
        apot = Pin(startpot, minResistance=2200, capacitance=0.000001, timeout=0.03333)
        bpot = Pin(finishpot, minResistance=2200, capacitance=0.000001, timeout=0.03333)
        start, length = map_pots(apot.measurement, bpot.measurement)
        p2 = pyaudio.PyAudio()

        stream2 = p2.open(format=p2.get_format_from_width(wave_file.getsampwidth()),
                       channels=wave_file.getnchannels(),
                       rate=wave_file.getframerate(),
                       output=True)

        n_frames = int(start * wave_file.getframerate())
        wave_file.setpos(n_frames)
        n_frames = int(length * wave_file.getframerate())
        frames = wave_file.readframes(n_frames)
        stream2.write(frames)
        # close the file and terminate the second stream
        stream2.close()
        p2.terminate()
        wave_file.close()
    
    # if you're here u pressed the second button to break the while loop. start over        