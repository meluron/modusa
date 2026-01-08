from modusa.models import annotation

from pathlib import Path

def as_ctm(ann: annotation, outfp):
    """
    Saves annotation in CTM format.

    Parameters
    ----------
    ann : annotation
        List of (uttid, ch, start, end, label, confidence, group)
    outfp : str
        Filepath to save the annotation.
    """
    output_fp = Path(outfp)
    output_fp.parent.mkdir(parents=True, exist_ok=True)

    with open(output_fp, "w") as f:
        for uttid, ch, start, end, label, confidence, _ in ann:
            dur = end - start
            f.write(f"{uttid} {ch} {start:.6f} {dur:.6f} {label} {confidence}\n")
