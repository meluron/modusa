#!/usr/bin/env python3

from IPython.display import Audio, HTML, display
import numpy as np

from IPython.display import Audio, HTML, display
import numpy as np

def play(y: np.ndarray, sr: float, clip: tuple[float, float] | None = None, label: str | None = None) -> None:
	"""
	Audio player with optional clip selection and transcription-style label.
	Displays a clean caption box with bold timing and text, followed by the player.
	"""
	start_time, end_time = 0.0, len(y) / sr
	
	# Optional clip selection
	if clip is not None:
		if not isinstance(clip, tuple) or len(clip) != 2:
			raise ValueError("`clip` must be a tuple of (start_time, end_time)")
		start_sample = int(clip[0] * sr)
		end_sample = int(clip[1] * sr)
		y = y[start_sample:end_sample]
		start_time, end_time = clip
		
	# Build HTML
	audio_html = Audio(data=y, rate=sr)._repr_html_()
	label_html = f"""
		<div style="
			margin-top:4px;
			padding:10px 12px;
			background:#f7f7f7;
			border-radius:6px;
			color:#222;
			font-size:14px;
			line-height:1.5;
		">
			<strong>{start_time:.2f}s → {end_time:.2f}s:</strong>
			<span style="margin-left:6px;">{label if label else ''}</span>
		</div>
	"""
	
	html = f"""
	<div style="
		display:inline-block;
		border:1px solid #e0e0e0;
		border-radius:10px;
		padding:12px 16px;
		background:#fff;
		font-family:sans-serif;
		max-width:800px;
		box-shadow:0 1px 3px rgba(0,0,0,0.05);
	">
		{label_html}
		<div style="margin-top:10px;">
			{audio_html}
		</div>
	</div>
	"""
	
	display(HTML(html))