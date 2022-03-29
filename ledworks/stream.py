import pyaudio

p = pyaudio.PyAudio()


def print_streams():
	# Set default to first in list or ask Windows
	try:
		default_device_index = p.get_default_input_device_info()
	except IOError:
		default_device_index = -1

	# Select Device
	for i in range(0, p.get_device_count()):
		info = p.get_device_info_by_index(i)
		print(str(info["index"]) + ": \t %s \n \t %s \n" % (
			info["name"], p.get_host_api_info_by_index(info["hostApi"])["name"]))

		if default_device_index == -1:
			default_device_index = info["index"]

	# Handle no devices available
	if default_device_index == -1:
		print("No device available. Quitting.")
		exit()


def get_stream(index):
	useloopback = False

	# Use module
	p = pyaudio.PyAudio()

	# Get device info
	device_info = p.get_device_info_by_index(index)

	# Choose between loopback or standard mode
	is_input = device_info["maxInputChannels"] > 0
	is_wasapi = (p.get_host_api_info_by_index(device_info["hostApi"])["name"]).find("WASAPI") != -1
	if is_input:
		print("Selection is input using standard mode.\n")
	else:
		if is_wasapi:
			useloopback = True
			print("Selection is output. Using loopback mode.\n")
		else:
			print("Selection is input and does not support loopback mode. Quitting.\n")
			exit()

	input_channels = device_info["maxInputChannels"]
	output_channels = device_info["maxOutputChannels"]

	channel_count = max(input_channels, output_channels)

	return p.open(
		format=pyaudio.paInt16,
		channels=channel_count,
		rate=int(device_info["defaultSampleRate"]),
		input=True,
		frames_per_buffer=128,
		input_device_index=device_info["index"],
		as_loopback=useloopback
	)