#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 22/08/25
# Email: ankit0.anand0@gmail.com
#---------------------------------


import sounddevice as sd
import numpy as np
import ipywidgets as widgets
from IPython.display import display, clear_output, Audio

def record():
	"""
	Create a UI to record audio in jupyter notebook, the 
	recorded signal is available as array.

	.. code-block:: python
		
		import modusa as ms
		result = ms.record()
		y, sr, title = result() # Keep it in the next cell

	Returns
	-------
	Callable
		A lambda function that returns y(audio signal), sr(sampling rate), title(title set in the UI)
	"""
	devices = sd.query_devices()
	device_options = [(d['name'][:30], i) for i, d in enumerate(devices) if d['max_input_channels'] > 0]
	
	# Controls
	device_dropdown = widgets.Dropdown(
		options=device_options,
		description="Microphone:",
		layout=widgets.Layout(width="300px")
	)
	
	sr_dropdown = widgets.Dropdown(
		options=[('16 Khz', 16000), ('22.05 Khz', 22050), ('44.1 Khz', 44100), ('48 Khz', 48000)],
		value=22050,
		description="Sample Rate:",
		layout=widgets.Layout(width="300px")
	)
	
	title_box = widgets.Text(
		placeholder="Title",
		description="Title:",
		layout=widgets.Layout(width="300px")
	)
	
	toggle_button = widgets.Button(
		description="Record",
		button_style="",
	)
	
	status = widgets.HTML(value="")
	out = widgets.Output()
	
	# State
	recording = {"data": None, "sr": None, "title": None}
	stream = {"obj": None, "frames": [], "recording": False}
	
	def callback(indata, frames, time, status):
		if not status:
			stream["frames"].append(indata.copy())
			
	def on_toggle(b):
		if not stream["recording"]:
			stream["frames"].clear()
			sr = sr_dropdown.value
			device_id = device_dropdown.value
			
			stream["obj"] = sd.InputStream(callback=callback, channels=1, samplerate=sr, device=device_id)
			stream["obj"].start()
			stream["recording"] = True
			
			toggle_button.description = "Stop"
			toggle_button.button_style = "danger"
			status.value = "Recording..."
		else:
			stream["obj"].stop()
			stream["obj"].close()
			
			sr = sr_dropdown.value
			y = np.concatenate(stream["frames"], axis=0).flatten()
			title = title_box.value.strip() or "Recording"
			
			recording["data"], recording["sr"], recording["title"] = y, sr, title
			record.result = (y, sr, title)
			stream["recording"] = False
			
			toggle_button.description = "Record"
			toggle_button.button_style = "success"
			
			with out:
				clear_output()
				display(Audio(y, rate=sr))
				
	toggle_button.on_click(on_toggle)
	
	# Layout
	ui = widgets.VBox([
		device_dropdown,
		sr_dropdown,
		title_box,
		widgets.HBox([toggle_button]),
		out
	])
	
	display(ui)
	record.result = None
	return lambda: record.result