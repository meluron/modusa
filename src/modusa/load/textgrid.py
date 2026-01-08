from ..models import annotation

from pathlib import Path
import warnings
import re


def textgrid(fp: str, tier: int = 0) -> annotation:
    """
    Loads a Praat TextGrid file as an Annotation object.
    Supports IntervalTier and PointTier.
    """

    fp = Path(fp)
    if not fp.exists():
        raise FileNotFoundError(f"{fp} does not exist.")

    data = []

    with open(fp, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f]

    tier_start_re = re.compile(r"item\s+\[(\d+)\]:")

    current_tier = -1
    in_target_tier = False
    tier_class = None

    # IntervalTier state
    in_interval = False
    s = e = None
    label = ""

    # PointTier state
    in_point = False
    t = None

    for line in lines:
        # -------- Tier start (ONLY numbered items)
        m = tier_start_re.match(line)
        if m:
            current_tier += 1
            in_target_tier = (current_tier == tier)

            tier_class = None
            in_interval = False
            in_point = False
            continue

        if not in_target_tier:
            continue

        # -------- Tier class
        if line.startswith("class ="):
            if "IntervalTier" in line:
                tier_class = "IntervalTier"
            elif "TextTier" in line:
                tier_class = "TextTier"
            else:
                warnings.warn(
                    f"Unsupported tier class in tier {tier}. Skipping."
                )
                return annotation([])
            continue

        # -------- IntervalTier
        if tier_class == "IntervalTier":
            if line.startswith("intervals ["):
                in_interval = True
                s = e = None
                label = ""
                continue

            if in_interval:
                if line.startswith("xmin ="):
                    s = float(line.split("=", 1)[1])

                elif line.startswith("xmax ="):
                    e = float(line.split("=", 1)[1])

                elif line.startswith("text ="):
                    label = line.split("=", 1)[1].strip().strip('"')

                    if s is not None and e is not None and label != "":
                        data.append((None, None, s, e, label, None, None))

                    in_interval = False

        # -------- PointTier
        elif tier_class == "TextTier":
            if line.startswith("points ["):
                in_point = True
                t = None
                label = ""
                continue

            if in_point:
                if line.startswith("number ="):
                    t = float(line.split("=", 1)[1])

                elif line.startswith("mark ="):
                    label = line.split("=", 1)[1].strip().strip('"')

                    if t is not None and label != "":
                        data.append((None, None, t, t, label, None, None))

                    in_point = False

    if current_tier < tier:
        raise IndexError(
            f"Requested tier {tier}, but TextGrid has only {current_tier + 1} tier(s)."
        )

    return annotation(data)
