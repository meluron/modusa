# modusa

`modusa` is a Python library providing utility tools for research.

It offers purpose-built tools especially for the audio domain but not limited to. It combines **audio loading**, **annotation handling**, **visualization**, and **analysis** in a unified, easy-to-use API. `modusa` simplifies common workflows so you can focus on **experimentation and insight**, not boilerplate code.

## Key Features

- **Flexible Audio Loader**
Load audio in multiple formats (`WAV`, `MP3`, `FLAC`, `M4A`, `AAC`, `OPUS`, `AIFF`) — even directly from YouTube links.

- **Unified Annotation Interface**
Work with `.txt` (Audacity labels) and `.ctm` (ASR/FA outputs) annotations seamlessly. `TextGrid` support coming soon.

- **Modular Plotter**
Create time-aligned visualizations combining waveforms, annotations, and spectrograms with minimal code.  
Supports multi-tier figures, dark mode, legends, tier IDs, and grouped color patterns.

- **Interactive Audio Player**
Play audio with visible annotation labels directly inside notebooks.

- **Built-in Audio Recorder**
Capture and instantly analyze microphone input from within Jupyter.

- **Analytical Tools**
Includes quick plotting utilities like distribution (hill) plots for comparing numerical features.

## Installation

> modusa is under active development. You can install the latest version via:

```
pip install modusa
```

## Tests

```
pytest tests/
```

## Status

modusa is in **early alpha**. Expect rapid iteration, breaking changes, and big ideas.  
If you like the direction, consider ⭐ starring the repo and opening issues or ideas.


## Few useful command for developers

To push doc changes
```
ghp-import -n -p -f docs/build/html
```

To create a dist
```
pdm build
```

To upload on pypi
```
twine upload dist/*
```

## About

**modusa** is developed and maintained by [meluron](https://www.github.com/meluron),

---

## License

MIT License. See `LICENSE` for details.

---

## Contributions

Pull requests, ideas, and discussions are welcome!  
No matter which domain you are in, if you work with any signal, we'd love your input.
