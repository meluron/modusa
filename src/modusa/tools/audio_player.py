#!/usr/bin/env python3

import numpy as np
from IPython.display import display, HTML, Audio

def play(y: np.ndarray, sr: float, title = None, t0: float = 0.0, regions = None) -> None:
		"""
		Plays audio clips for given regions in Jupyter Notebooks.

		Parameters
		----------
		y : np.ndarray
			- Audio data.
			- Mono (1D) numpy array.
		sr: float
			- Sampling rate of the audio.
		title : str | None
			- Title to display above audio players.
		t0: float
			- Starting timestamp, incase the audio is cropped
			- Default: 0.0 → Starts from 0.0 sec
		regions : list[tuple[float, float, str]] | tuple[float, float, str] | None
			- Regions to extract and play (in sec), e.g. [(0, 10.2, "tag")]
			- If there is only one region, a tuple should also work. e.g. (0, 10.2, "tag")
			- Default: None → The entire song is selected.

		Returns
		-------
		None
		"""
		if title:
			display(HTML(f"<p style='font-size:15px; font-weight:600; text-decoration: underline; margin-left:10px'>{title}</p>"))
			
		clip_tags = []
		timings = []
		players = []
	
		if isinstance(regions, tuple): regions = [regions] # (10, 20, "Region 1") -> [(10, 20, "Region 1")]
	
		if regions is not None:
			for region in regions:
				assert len(region) == 3
				
				start_sec = region[0] - t0
				end_sec = region[1] - t0
				tag = region[2]
				
				start_sample, end_sample = int(start_sec * sr), int(end_sec * sr)
				clip = y[start_sample: end_sample]
				audio_player = Audio(data=clip, rate=sr)._repr_html_()
				
				clip_tags.append(f"<td style='text-align:center; border-right:1px solid #ccc; padding:6px;'>{tag}</td>")
				timings.append(f"<td style='text-align:center; border-right:1px solid #ccc; padding:6px;'>{start_sec:.2f}s → {end_sec:.2f}s</td>")
				players.append(f"<td style='padding:6px;'>{audio_player}</td>")
		else:
			audio_player = Audio(data=y, rate=sr)._repr_html_()
			
			start_sec = t0
			end_sec = t0 + y.shape[0] / sr
			
			clip_tags.append(f"<td style='text-align:center; border-right:1px solid #ccc; padding:6px;'>1</td>")
			timings.append(f"<td style='text-align:center; border-right:1px solid #ccc; padding:6px;'>{start_sec:.2f}s → {end_sec:.2f}s</td>")
			players.append(f"<td style='padding:6px;'>{audio_player}</td>")
			
		# Wrap rows in a table with border
		table_html = f"""
		<div style="display:inline-block; border:1px solid #ccc; border-radius:6px; overflow:hidden;">
			<table style="border-collapse:collapse;">
				<tr style="background-color:#f2f2f2;">
					<th style="text-align:left; padding:6px 12px;">Clip</th>
					{''.join(clip_tags)}
				</tr>
				<tr style="background-color:#fcfcfc;">
					<th style="text-align:left; padding:6px 12px;">Timing</th>
					{''.join(timings)}
				</tr>
				<tr>
					<th style="text-align:left; padding:6px 12px;">Player</th>
					{''.join(players)}
				</tr>
			</table>
		</div>
		"""
	
		return HTML(table_html)

		
		
		