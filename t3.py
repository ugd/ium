
try:
    import pyaudio
    import numpy as np
    import pylab
    import matplotlib.pyplot as plt
    from scipy.io import wavfile
    import time
    import sys
    import seaborn as sns
except:
    print ("Something didn't import")

i=0
ax = plt.subplot()

# Prepare the Plotting Environment with random starting values
x = np.arange(10000)
y = np.random.randn(10000)

# Plot 0 is for raw audio data

# plt.pause(0.01)
audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=pyaudio.paInt16,
                    channels=2,
                    rate=44100,
                    input=True)#,
                    #frames_per_buffer=CHUNK)

global keep_going
keep_going = True
li, = ax.plot(x, y)
ax.set_xlim(0,1000)
ax.set_ylim(-5000,5000)
def plot_data(in_data):

    audio_data = np.frombuffer(in_data, np.int16)
    li.set_xdata(np.arange(len(audio_data)))
    li.set_ydata(audio_data)

    plt.pause(0.001)
    if keep_going:
        return True
    else:
        return False
stream.start_stream()

while keep_going:
    try:
        plot_data(stream.read(1024))
    except KeyboardInterrupt:
        keep_going=False
    except:
        pass
stream.stop_stream()
stream.close()

audio.terminate()