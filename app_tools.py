import tkinter as tk

DEFAULT_FONT = ("Helvetica, 16")

class ColorPicker:
    def __init__(self, last_color):
        """ Opens a top level window that allows user to pick
        a color to draw with.
        """
        self._color = last_color
        self._window = tk.Toplevel(width = 200, height = 132)
        self._window.title("Color")
        
        self._initialize()

    def get_color(self):
        return self._color

    def show_window(self):
        """ This toplevel window takes control of events.
        """
        self._window.grab_set()
        self._window.wait_window()

    def _initialize(self):
        """ Create entry section and button to confirm selection.
        """
        self._entry = tk.Entry(master = self._window)
        self._entry.focus_set()
        
        self._confirm_button = tk.Button(master = self._window,
                                         text = "Ok",
                                         font = DEFAULT_FONT,
                                         command = self._confirm_color)

        self._entry.grid(row = 0, column = 0,
                         padx = 10, pady = 10)
        self._confirm_button.grid(row = 1, column = 0,
                                  padx = 10, pady = 10)

        self._window.bind("<Return>", self._confirm_color)


    def _confirm_color(self, event = None):
        """ Check that color inputted is not an empty string
        and set color attribute to the entry value.
        """
        color = self._entry.get().strip()
        if color != "":
            self._color = color
        self._window.destroy()


        
