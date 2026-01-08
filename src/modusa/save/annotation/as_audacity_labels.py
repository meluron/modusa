from modusa.models import annotation

from pathlib import Path

def as_audacity_labels(ann: annotation, outfp):
    """
    Saves annotation as a tab-delimited text file compatible with Audacity.

    Parameters
    ----------
    ann : list[tuple[str, int, float, float, str, float|None, int|None]]
        List of (uttid, ch, start, end, label, confidence, group)
    outfp : str
        Filepath to save the annotation.
    """
    output_fp = Path(outfp)
    output_fp.parent.mkdir(parents=True, exist_ok=True)

    with open(output_fp, "w") as f:
        for _, _, start, end, label, _, _ in ann:
            f.write(f"{start:.6f}\t{end:.6f}\t{label}\n")
