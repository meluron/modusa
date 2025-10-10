#!/usr/bin/env python3

import logging

class PATHS:
	from pathlib import Path
	ROOT_DP: Path = Path(__file__).parents[2].resolve()
	AUDIO_DP: Path = ROOT_DP / "data" / "audio"
	EXAMPLE_AUDIO_FP: Path = AUDIO_DP / "Arko - Nazm Nazm.mp3"
	LABELS_CSV_FP: Path = ROOT_DP / "data" / "label_data.csv"
	REPORTS_DP: Path = ROOT_DP / "data" / "reports"

class DEFAULT_SETTINGS:
	SR: int = 44100
	LOG_LEVEL = logging.WARNING
	
	class STFT:
		N_FFT: int = 2048
		WIN_SIZE: int = 2048
		HOP_SIZE: int = 512
		WINDOW: str = "hann"
	
	class NOVELTY:
		GAMMA: int = 10
		LOCAL_AVG: int = 40