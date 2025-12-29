import ipywidgets as widgets
from IPython.display import display
from pathlib import Path

class BPMarker:
    """
    A notebook-based tool for annotating boundary and 
    prominence labels for each element (word) in a list.

    Boundary annotations support three possible values:
        - 0: No boundary
        - 1: Phrase boundary
        - 2: Sentence boundary


    Prominence annotations support two possible values:
        - 0: Not prominent
        - 1: Prominent

    Although the tool is designed specifically for 
    boundary and prominence annotation, it can be adapted
    for other use cases where a similar categorical 
    interpretation is appropriate.
    """

    def __init__(self, data: list, title: str="Untitled"):

        if not isinstance(data, list):
            raise ValueError(f"`data` must be of type `list`, got `{type(data)}` instead.")

        self.data: list = data
        self.title: str = str(title)
        self.boundary_states = dict() # key:value => element index: [0: No Boundary, 1: Phrase Boundary, 2: Sentence Boundary]
        self.prominence_states = dict() # key:value => element index: [0: Not Prominent, 1: Prominent]

        self.prominence_buttons: list[widgets.Button] = []
        self.boundary_buttons: list[widgets.Button] = []

        self._create_widgets()

    def _create_widgets(self):
        """
        Create button widgets for each element and also 
        add gap button for marking boundary.
        """

        self.word_buttons: list[widgets.Button] = []
        self.gap_buttons: list[widgets.Button] = []

        # ==========================================
        # For each element, set the default boundary
        # and prominence state
        # ==========================================
        for i in range(len(self.data)):
            self.boundary_states[i] = 0 # Set to 0 (No Boundary)
            self.prominence_states[i] = 0 # Set to 0 (Not Prominent)

        # ==========================================
        # Create button widgets for marking the 
        # prominence and the boundary
        # ==========================================
        for i, element in enumerate(self.data):

            # ======================
            # Prominence button
            # ======================
            prominence_button = widgets.Button(
                description=str(element),
                layout=widgets.Layout(width='auto', margin='2px 0px'),
                style={'button_color': 'white'}
            )
            prominence_button.id: int = i # To keep track of which element it belongs to
            prominence_button.on_click(self._on_click_prominence_button)
            self.prominence_buttons.append(prominence_button)

            # ======================
            # Boundary button
            # ======================
            boundary_button = widgets.Button(
                description='-',
                layout=widgets.Layout(width='20px', margin='2px 0px', padding='0px'),
                style={'button_color': 'white'},
            )

            boundary_button.id: int = i
            boundary_button.on_click(self._on_click_boundary_button)
            self.boundary_buttons.append(boundary_button)

        self.display()
    
    def _on_click_prominence_button(self, button: widgets.Button):
        """
        Update the prominence state dictionary value for
        the selected index.
        """
        curr_prominence_state = self.prominence_states[button.id]
        self.prominence_states[button.id] += 1
        self.prominence_states[button.id] %= 2
 

        if self.prominence_states[button.id] == 1:
            button.style.text_color = "purple"
            button.style.font_weight = "bold"
        else:
            button.style.text_color = "black"
            button.style.font_weight = "normal"   
        

    def _on_click_boundary_button(self, button: widgets.Button):
        """
        Update the boundary state dictionary value for
        the selected index.
        """
        self.boundary_states[button.id] += 1
        self.boundary_states[button.id] %= 3

        if self.boundary_states[button.id] == 0:
            button.description = "-"
            button.style.text_color = "black"
            button.style.font_weight = "normal"
        elif self.boundary_states[button.id] == 1:
            button.description = "|"
            button.style.text_color = "red"
            button.style.font_weight = "bold"
        elif self.boundary_states[button.id] == 2:
            button.description = "||"
            button.style.text_color = "red"
            button.style.font_weight = "bold"

    def get_markings(self):
        """
        Returns marking in a user-friendly pythonic format.
        list[(label, boundary, prominence)] [('word 1', 0, 1), ('word 2', 1, 0), ...]
        """

        result: list[tuple] = []

        for i in range(len(self.data)):
            result.append((str(self.data[i]), self.boundary_states[i], self.prominence_states[i]))
        return result

    def display(self):
        """
        Display the widgets in a formatted layout with heading and styled container.
        """
        all_widgets = []
        
        for i in range(len(self.data)):
            all_widgets.append(self.prominence_buttons[i])
            all_widgets.append(self.boundary_buttons[i])
        
        # Create heading
        heading = widgets.HTML(
            value="<h3 style='margin: 0 0 8px 0; color: #ef8c03; text-align: center;'>Boundary & Prominence Marking Tool</h3>"
        )

        # Create title
        title = widgets.HTML(
            value=f"<h4 style='margin: 0 0 8px 0; color: black; text-align: left;'>{self.title}</h3>"
        )
        
        # Create description
        description = widgets.HTML(
                value="""
                <div style='display: flex; justify-content: right; gap: 20px; margin-bottom: 12px;'>
                    <table style='font-size: 12px; border-collapse: collapse;'>
                        <thead>
                            <tr>
                                <th colspan='2' style='padding: 4px 8px; border: 1px solid #ddd; background-color: #f0f0f0; font-weight: bold;'>Prominence</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td style='padding: 4px 8px; border: 1px solid #ddd;'><span style='color: #555;'>word</span></td>
                                <td style='padding: 4px 8px; border: 1px solid #ddd;'>Not Prominent</td>
                            </tr>
                            <tr>
                                <td style='padding: 4px 8px; border: 1px solid #ddd;'><span style='color: purple; font-weight: bold;'>word</span></td>
                                <td style='padding: 4px 8px; border: 1px solid #ddd;'>Prominent</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <table style='font-size: 12px; border-collapse: collapse;'>
                        <thead>
                            <tr>
                                <th colspan='2' style='padding: 4px 8px; border: 1px solid #ddd; background-color: #f0f0f0; font-weight: bold;'>Boundary</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td style='padding: 4px 8px; border: 1px solid #ddd;'><span style='color: #555;'>-</span></td>
                                <td style='padding: 4px 8px; border: 1px solid #ddd;'>No Boundary</td>
                            </tr>
                            <tr>
                                <td style='padding: 4px 8px; border: 1px solid #ddd;'><span style='color: red; font-weight: bold;'>|</span></td>
                                <td style='padding: 4px 8px; border: 1px solid #ddd;'>Phrase Boundary</td>
                            </tr>
                            <tr>
                                <td style='padding: 4px 8px; border: 1px solid #ddd;'><span style='color: red; font-weight: bold;'>||</span></td>
                                <td style='padding: 4px 8px; border: 1px solid #ddd;'>Sentence Boundary</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                """
            )
        
        # Layout: wrap words nicely
        words_box = widgets.HBox(
            all_widgets,
            layout=widgets.Layout(
                display='flex',
                flex_flow='row wrap',
                align_items='center',
                width='100%',
                padding='12px',
                border='1px solid #ef8c03',
                border_radius='8px',
                background_color='#f8f9fa'
            )
        )
        
        # Combine everything in a VBox with rounded container
        container = widgets.VBox(
            [heading, description, title, words_box],
            layout=widgets.Layout(
                padding='20px',
                border='2px solid #ef8c03',
                border_radius='12px',
                background_color='white',
                box_shadow='0 2px 8px rgba(0,0,0,0.1)',
                width='auto',
                max_width='900px'
            )
        )
        
        display(container)
    
    def save(self, path: str | Path, overwrite: bool = False):
        """
        Save the markings as a csv file.
        """
        path = Path(path)

        # Ensure the parent directory exists to avoid FileNotFoundError
        path.parent.mkdir(parents=True, exist_ok=True)

        # 'x' mode fails if file exists; 'w' overwrites.
        mode = "w" if overwrite else "x"

        try:
            with path.open(mode=mode, encoding="utf-8") as f:
                f.write('Label,Boundary,Prominence\n')
                for line in self.get_markings():
                    label, boundary, prominence = line
                    f.write(f"{label},{boundary},{prominence}\n")
            print(f"Successfully saved to {path}")
        except FileExistsError:
            print(f"Error: The file '{path}' already exists and overwrite is set to False.")

