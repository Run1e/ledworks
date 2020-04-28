import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import librosa
from ledworks import log_filterbank

CHANNELS = 2
RATE = 44100
SAMPLE_SIZE = 16
CHUNK = 512
HALF_CHUNK = CHUNK // CHANNELS
TIMESTEP = 1.0 / RATE
LED_COUNT = 128

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, figsize=(15, 7))

pcm_xrange = np.arange(0, 2 * CHUNK, 2)

line, = ax1.plot(pcm_xrange, np.zeros(CHUNK), '-', lw=2)

ax1.set_ylim(-1, 1)
ax1.set_xlim(0, CHUNK)
plt.setp(
	ax1, yticks=[-1, 1],
	xticks=[0, HALF_CHUNK, CHUNK],
)

fft_xrange = np.linspace(0, RATE / 2, HALF_CHUNK + 1)

line_fft, = ax2.plot(fft_xrange, np.zeros(HALF_CHUNK + 1), '-', lw=2)

plt.setp(ax2)
ax2.set_xlim(0, RATE / 2)
ax2.set_ylim(0, 1)

line_semi, = ax3.semilogx(fft_xrange, np.zeros(HALF_CHUNK + 1), '-', lw=2)

plt.setp(ax3)
ax3.set_xlim(0, RATE / 2)
ax3.set_ylim(0, 1)

led_xrange = np.linspace(0, LED_COUNT, LED_COUNT)

line_mel, = ax4.plot(led_xrange, np.zeros(LED_COUNT), '-', lw=2)

plt.setp(ax4)
ax4.set_xlim(0, LED_COUNT)
ax4.set_ylim(0, 1)

line_log, = ax5.plot(led_xrange, np.zeros(LED_COUNT), '-', lw=2)

plt.setp(ax5)
ax5.set_xlim(0, LED_COUNT)
ax5.set_ylim(0, 1)

plt.show(block=False)



p = pyaudio.PyAudio()

# for n in range(p.get_device_count()):
#print(p.get_device_info_by_index(4))

stream = p.open(
	format=pyaudio.paInt16,
	channels=CHANNELS,
	rate=RATE,
	input=True,
	frames_per_buffer=CHUNK,
	input_device_index=4,
	as_loopback=True
)

mel = librosa.filters.mel(sr=RATE, n_fft=CHUNK, n_mels=LED_COUNT)

log = log_filterbank(rate=RATE, bins=LED_COUNT, n_fft=CHUNK)

while True:
	raw_data = stream.read(CHUNK, exception_on_overflow=False)

	stereo = np.frombuffer(raw_data, dtype=np.int8) # 2x len of CHUNK

	mono = stereo[::2]

	fft_complex = np.fft.fft(mono)[:HALF_CHUNK]

	fft_data = np.abs(fft_complex) * 2 / (256 * HALF_CHUNK)

	print(fft_data)

	#print(mel.shape, mel.shape[1] / mel.shape[0])

	#mel_data = mel.dot(fft_data)
	#log_data = log.dot(fft_data)

	line.set_ydata(mono)
	line_fft.set_ydata(fft_data)
	line_semi.set_ydata(fft_data)
	#line_log.set_ydata(log_data)
	#line_mel.set_ydata(mel_data)


	fig.canvas.draw()
	fig.canvas.flush_events()


	#print(data)

	# [1, 2, 3] -> [(1, 1, 1), (2, 2, 2), (3, 3, 3)]
	#out = np.repeat(data, 3).reshape(-1, 3)

	# self.strip.data = np.repeat(d1[0], 3 * size).reshape(-1, 3)