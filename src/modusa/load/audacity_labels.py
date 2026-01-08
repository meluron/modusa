from ..models import annotation

from pathlib import Path

def audacity_labels(fp: str) -> annotation:
    """
    Load an Audacity label file as an Annotation object.

    Parameters
    ----------
    fp : str
        Path to the label file. Must be a tab-delimited file:
        start_time (s) <tab> end_time (s) <tab> label text
        Example:
            0.00    1.23    hello
            1.50    2.50    world

    Returns
    -------
    annotation
        Annotation object with entries (start, end, label, confidence=None, group=None)
    """

    fp: Path = Path(fp)
    if not fp.exists():
        raise FileExistsError(f"{fp} does not exist.")

    data: list = []  # To store [(start, end, label, confidence, group), ...]

    with open(str(fp), "r") as f:
        lines = f.read().splitlines()  # ["start end label", ...]

    for line in lines:
        # -- Ankit Anand on 04-12-2025 --
        # Ignore empty lines before parsing.
        if not line.strip():
            continue

        start, end, label = line.split("\t")
        start, end = float(start), float(end)
        data.append((None, None, start, end, label, None, None))  # The last two entries (confidence, group) are set to None

    return annotation(data)
