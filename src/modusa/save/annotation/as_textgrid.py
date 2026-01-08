from modusa.models import annotation

from pathlib import Path

def as_textgrid(ann: annotation, outfp: str, tier_name: str = "labels"):
    """
    Saves annotation as a Praat TextGrid.

    Parameters
    ----------
    ann : annotation
        List of (uttid, ch, start, end, label, confidence, group)
    outfp : str
        Filepath to save the annotation.
    tier_name : str
        Name of the TextGrid tier.
    """
    output_fp = Path(outfp)
    output_fp.parent.mkdir(parents=True, exist_ok=True)

    xmin = min(start for _, _, start, _, _, _, _ in ann) if ann else 0.0
    xmax = max(end for _, _, _, end, _, _, _ in ann) if ann else 0.0

    with open(output_fp, "w") as f:
        f.write('File type = "ooTextFile"\n')
        f.write('Object class = "TextGrid"\n\n')
        f.write(f"xmin = {xmin:.6f}\n")
        f.write(f"xmax = {xmax:.6f}\n")
        f.write("tiers? <exists>\n")
        f.write("size = 1\n")
        f.write(f"item []:\n")
        f.write("    item [1]:\n")
        f.write('        class = "IntervalTier"\n')
        f.write(f'        name = "{tier_name}"\n')
        f.write(f"        xmin = {xmin:.6f}\n")
        f.write(f"        xmax = {xmax:.6f}\n")
        f.write(f"        intervals: size = {len(ann)}\n")

        for i, (_, _, start, end, label, _, _) in enumerate(ann, start=1):
            f.write(f"        intervals [{i}]:\n")
            f.write(f"            xmin = {start:.6f}\n")
            f.write(f"            xmax = {end:.6f}\n")
            f.write(f'            text = "{label}"\n')
