from ..models import annotation

from pathlib import Path
import warnings


def ctm(fp: str) -> annotation:
    """
    Loads ctm file as Annotation object.
    
    Parameters
    ----------
    fp: Path|str
      Filepath of the ctm file.

    Returns
    -------
    ms.annotation
      Loaded annotation object.
    """

    fp: Path = Path(fp)
    if not fp.exists(): raise FileExistsError(f"{fp} does not exist.")

    data: list = [] # To store [(start, end, label, confidence, group), ...]

    with open(str(fp), "r") as f:
      lines = f.read().splitlines()
    
    for line in lines:
      # 04-12-2025 [Ankit Anand]: Ignore empty lines before parsing.
      if not line.strip():
        continue
      
      parts = line.split() # [utterance_id, channel, start, duration, label, confidence(optional)]

      # 04-12-2025 [Ankit Anand]: Handle ctm files that do not have confidence score.
      if len(parts) == 5:
        utt_id, ch, start, dur, label = parts
        start, dur = float(start), float(dur)
        confidence = None

      # 04-12-2025 [Ankit Anand]: Handle ctm files that have confidence score.
      elif len(parts) == 6:
        utt_id, ch, start, dur, label, confidence = parts
        start, dur = float(start), float(dur)
        confidence = float(confidence)
      
      # 04-12-2025 [Ankit Anand]: Handle any anamolies in any of the lines of the ctm.
      else:
        warnings.warn(f"'{line}' is not a standard ctm line <utterance_id channel start dur label confidence[optional]>.")
        continue
        
      data.append((utt_id, ch, start, start + dur, label, confidence, None))

    return annotation(data)
