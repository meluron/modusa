# ---------------------------------
# Author: Ankit Anand
# Date: 23-11-2025
# Email: ankit0.anand0@gmail.com
# ---------------------------------

from pathlib import Path
import re


class Annotation:
    """
    A modusa model class for annotation for audio data.

    Annotation wraps around
    [[uttid, ch, start_time, end_time, label, confidence, group], ...]
    """

    def __init__(
        self,
        data: list[
            tuple[str, int, float, float, str, float | None, int | None]
        ]
        | None = None,
    ):
        self._data = data

    # ============================================
    # Properties
    # ============================================
    @property
    def data(self):
        return self._data

    @property
    def size(self):
        """Returns the total number of annotation entries"""
        return len(self)

    # ============================================
    # Dunder methods
    # ============================================
    def __len__(self):
        """Returns total number of annotation entries."""
        return len(self.data)

    def __getitem__(self, key: slice | int):
        """Get item(s) from the annotation."""
        if isinstance(key, slice):
            return Annotation(self.data[key])
        else:
            return self.data[key]

    def __iter__(self):
        """Allows iteration over the annotation entries."""
        return iter(self.data)

    def __repr__(self):
        if self.size == 0:
            return "Annotation([])"

        entries_str = []

        for entry in self:
            entry_str = ", ".join(str(element) for element in entry)
            entries_str.append(f"({entry_str})")

        indent = "  "
        return (
            "Annotation([\n"
            + indent
            + f"\n{indent}".join(entries_str)
            + "\n])"
        )

    # ============================================
    # Trim feature
    # ============================================
    def trim(self, from_, to_):
        """
        Return a new annotation object trimmed to a segment.
        """
        raw_ann = [
            (uttid, channel, start, end, label, confidence, group)
            for (uttid, channel, start, end, label, confidence, group) in self.data
            if start >= from_ and end <= to_
        ]

        return Annotation(raw_ann)

    # ============================================
    # Search feature
    # ============================================
    def search(self, for_: str, case_insensitive: bool = True):
        """
        Return a new annotation object with labels matching the query.

        Custom pattern:
            *L  => label ends with 'L'
            L*  => label starts with 'L'
            *L* => label contains 'L'
            L   => label exactly equals 'L'
        """
        case_sensitivity_flag = re.IGNORECASE if case_insensitive else 0

        if for_.startswith("*") and for_.endswith("*"):
            regex_pattern = re.compile(
                re.escape(for_.strip("*")), case_sensitivity_flag
            )
        elif for_.startswith("*"):
            regex_pattern = re.compile(
                re.escape(for_.strip("*")) + r"$", case_sensitivity_flag
            )
        elif for_.endswith("*"):
            regex_pattern = re.compile(
                r"^" + re.escape(for_.strip("*")), case_sensitivity_flag
            )
        else:
            regex_pattern = re.compile(
                "^" + re.escape(for_) + "$", case_sensitivity_flag
            )

        new_raw_ann = [
            (start, end, label, confidence, group)
            for (start, end, label, confidence, group) in self.data
            if regex_pattern.search(label)
        ]

        return Annotation(new_raw_ann)

    # ============================================
    # Group feature
    # ============================================
    def group(self, by_: str | list[str], case_insensitive: bool = True):
        """
        Assign group numbers based on label pattern(s).
        """
        if isinstance(by_, str):
            patterns = [by_]
        else:
            patterns = by_

        case_sensitivity_flag = re.IGNORECASE if case_insensitive else 0

        regex_patterns = []
        for pattern in patterns:
            if pattern.startswith("*") and pattern.endswith("*"):
                regex = re.compile(
                    re.escape(pattern.strip("*")), case_sensitivity_flag
                )
            elif pattern.startswith("*"):
                regex = re.compile(
                    re.escape(pattern.strip("*")) + r"$",
                    case_sensitivity_flag,
                )
            elif pattern.endswith("*"):
                regex = re.compile(
                    r"^" + re.escape(pattern.strip("*")),
                    case_sensitivity_flag,
                )
            else:
                regex = re.compile(
                    "^" + re.escape(pattern) + "$", case_sensitivity_flag
                )

            regex_patterns.append(regex)

        new_raw_ann = []

        for uttid, ch, start, end, label, confidence, _ in self.data:
            group_num = None
            for i, regex in enumerate(regex_patterns):
                if regex.search(label):
                    group_num = i
                    break

            new_raw_ann.append(
                (uttid, ch, start, end, label, confidence, group_num)
            )

        return Annotation(new_raw_ann)

    # ============================================
    # Add entry feature
    # ============================================
    def append(
        self,
        utt_id: str,
        ch: int,
        start: float,
        end: float,
        label: str,
        confidence: float | None = None,
        group: int | None = None,
    ):
        """Append a new annotation entry."""
        self.data.append(
            [utt_id, ch, start, end, str(label), confidence, group]
        )

    # ============================================
    # Remove entry feature
    # ============================================
    def remove(self, this_: str, case_insensitive: bool = True):
        """
        Remove entries whose labels match the pattern.
        """
        case_sensitivity_flag = re.IGNORECASE if case_insensitive else 0

        if this_.startswith("*") and this_.endswith("*"):
            pattern = re.compile(
                re.escape(this_.strip("*")), case_sensitivity_flag
            )
        elif this_.startswith("*"):
            pattern = re.compile(
                re.escape(this_.strip("*")) + r"$",
                case_sensitivity_flag,
            )
        elif this_.endswith("*"):
            pattern = re.compile(
                r"^" + re.escape(this_.strip("*")),
                case_sensitivity_flag,
            )
        else:
            pattern = re.compile(
                "^" + re.escape(this_) + "$", case_sensitivity_flag
            )

        new_raw_ann = [
            (str(uid), int(ch), float(s), float(e), str(lbl), float(conf), int(grp))
            for (uid, ch, s, e, lbl, conf, grp) in self.data
            if not pattern.search(lbl)
        ]

        return Annotation(new_raw_ann)
