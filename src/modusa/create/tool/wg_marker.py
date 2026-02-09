import csv
from pathlib import Path

import ipywidgets as widgets
from IPython.display import display


class WGMarker:
    """
    A tool for numerical n-state annotation of words and gaps.
    """

    def __init__(
        self,
        *args,
        n_word_states=2,
        n_gap_states=3,
        audio_fp=None,  # New parameter for audio file path
        title="",
        header="Word & Gap Marker",
    ) -> None:
        if len(args) == 0:
            raise ValueError("Expected a list of words or a CSV file path.")

        self.n_word_states = n_word_states
        self.n_gap_states = n_gap_states
        self.audio_fp = audio_fp
        self.header = header
        self.title = title
        self.data: list = []

        if isinstance(args[0], list):
            for word in args[0]:
                self.data.append([word, 0, 0])
        elif isinstance(args[0], (str, Path)):
            self._load_from_csv(Path(args[0]))
        else:
            raise ValueError("Invalid input.")

        self._build_interface()

    def _load_from_csv(self, csv_fp: Path):
        with csv_fp.open(mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                word, g_val, w_val = row
                self.data.append([word, int(g_val), int(w_val)])

    def _update_word_ui(self, idx):
        val = self.data[idx][2]
        stars = "*" * val if val > 0 else "&nbsp;"

        self.word_indicators[idx].value = (
            f"<div style='font-size: 16px; text-align: center; color: #ef8c03; "
            f"font-weight: bold; width: 100%; line-height: 0.8; margin-bottom: -4px;'>{stars}</div>"
        )

        if val > 0:
            self.word_buttons[idx].style.font_weight = "bold"
            self.word_buttons[idx].style.text_color = "#ef8c03"
        else:
            self.word_buttons[idx].style.font_weight = "normal"
            self.word_buttons[idx].style.text_color = "black"

    def _on_word_click(self, b):
        self.data[b.idx][2] = (self.data[b.idx][2] + 1) % self.n_word_states
        self._update_word_ui(b.idx)

    def _on_gap_click(self, b):
        self.data[b.idx][1] = (self.data[b.idx][1] + 1) % self.n_gap_states
        val = self.data[b.idx][1]
        b.description = "|" * val if val > 0 else "-"

    def _build_interface(self):
        css_style = widgets.HTML("""
            <style>
                .jupyter-widgets:focus { outline: none !important; }
                .jupyter-button:focus { outline: none !important; }
                .jupyter-button { border: none !important; box-shadow: none !important; background: transparent !important; }
            </style>
        """)

        # 1. Audio Widget Construction
        audio_widget = widgets.Box()
        if self.audio_fp:
            try:
                with open(self.audio_fp, "rb") as f:
                    audio_data = f.read()
                audio_player = widgets.Audio(
                    value=audio_data,
                    format=Path(self.audio_fp).suffix[1:],  # e.g., 'wav' or 'mp3'
                    autoplay=False,
                    loop=False,
                    layout=widgets.Layout(width="100%", margin="10px 0px"),
                )
                audio_widget = audio_player
            except Exception as e:
                audio_widget = widgets.HTML(
                    f"<p style='color:red;'>Error loading audio: {e}</p>"
                )

        self.word_indicators = []
        self.word_buttons = []
        all_units = []

        for i, (word, g_val, w_val) in enumerate(self.data):
            indicator = widgets.HTML(
                layout=widgets.Layout(height="auto", margin="0", width="100%")
            )
            self.word_indicators.append(indicator)

            word_btn = widgets.Button(
                description=str(word),
                layout=widgets.Layout(width="auto", margin="0", padding="0"),
                style={"button_color": "white"},
            )
            word_btn.idx = i
            word_btn.on_click(self._on_word_click)
            word_btn.style.font_size = "18px"
            self.word_buttons.append(word_btn)

            gap_btn = widgets.Button(
                description="|" * g_val if g_val > 0 else "-",
                layout=widgets.Layout(
                    width="34px", height="30px", margin="12px 2px 0px 2px"
                ),
                style={"button_color": "#f8f9fa", "font_size": "18px"},
            )
            gap_btn.idx = i
            gap_btn.on_click(self._on_gap_click)

            self._update_word_ui(i)

            word_stack = widgets.VBox(
                [indicator, word_btn],
                layout=widgets.Layout(align_items="center", spacing="0"),
            )
            unit = widgets.HBox(
                [word_stack, gap_btn],
                layout=widgets.Layout(align_items="center", margin="4px"),
            )
            all_units.append(unit)

        flex_box = widgets.HBox(
            all_units, layout=widgets.Layout(flex_flow="row wrap", width="100%")
        )

        header_html = widgets.HTML(
            f"<h2 style='color: #ef8c03; text-align: center; margin-bottom: 0px;'>{self.header}</h2>"
        )

        title_widget = widgets.Box()
        if self.title:
            title_widget = widgets.HTML(
                f"<p style='text-align: center; font-weight: bold; font-size: 16px; margin-top: 5px; color: #555;'>{self.title}</p>"
            )

        main_display = widgets.VBox(
            [
                css_style,
                header_html,
                title_widget,
                audio_widget,  # Display the player here
                widgets.Box(layout=widgets.Layout(height="10px")),
                flex_box,
            ],
            layout=widgets.Layout(
                width="100%",
                border="2px solid #ef8c03",
                padding="20px",
                border_radius="12px",
            ),
        )

        display(main_display)

    def save(self, path: str):
        path = Path(path)
        with path.open(mode="w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["word", "gap_state_idx", "word_state_idx"])
            writer.writerows(self.data)
        print(f"Data saved to {path}")
