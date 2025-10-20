#!/usr/bin/env python3

from IPython.display import Audio, HTML, display
import numpy as np

def play(y: np.ndarray, sr: float, clip: tuple[float, float] | None = None, label: str | None = None) -> None:
		"""
		Simple audio player with optional clip selection and label, 
		displayed neatly in a small table.

		Parameters
		----------
		y : np.ndarray
				Mono audio data (1D numpy array).
		sr : float
				Sampling rate.
		clip : tuple[float, float] | None
				(start_time, end_time) in seconds. Plays whole audio if None.
		label : str | None
				Optional label to describe the clip (e.g. "Chorus", "Intro").

		Returns
		-------
		None
		"""
		start_time, end_time = 0.0, len(y) / sr
	
		if clip is not None:
				if not isinstance(clip, tuple) or len(clip) != 2:
						raise ValueError("`clip` must be a tuple of (start_time, end_time)")
				start_sample = int(clip[0] * sr)
				end_sample = int(clip[1] * sr)
				y = y[start_sample:end_sample]
				start_time, end_time = clip
			
		# Build the HTML table
		audio_html = Audio(data=y, rate=sr)._repr_html_()
		label_html = label if label is not None else "-"
	
		table_html = f"""
		<div style="display:inline-block; border:1px solid #ccc; border-radius:6px; overflow:hidden;">
			<table style="border-collapse:collapse; font-family:sans-serif; font-size:14px;">
				<tr style="background-color:#f8f8f8;">
					<th style="padding:6px 12px; text-align:left;">Timing</th>
					<th style="padding:6px 12px; text-align:left;">Label</th>
					<th style="padding:6px 12px; text-align:left;">Audio</th>
				</tr>
				<tr>
					<td style="padding:6px 12px; border-top:1px solid #ddd;">{start_time:.2f}s → {end_time:.2f}s</td>
					<td style="padding:6px 12px; border-top:1px solid #ddd;">{label_html}</td>
					<td style="padding:6px 12px; border-top:1px solid #ddd;">{audio_html}</td>
				</tr>
			</table>
		</div>
		"""
	
		display(HTML(table_html))

		
		
		