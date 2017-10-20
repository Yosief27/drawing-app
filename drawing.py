import app_tools
import drawing_tools
import tkinter as tk

DEFAULT_FONT = ("Helvetica, 16")
DEBUG = False
DEFAULT_COLOR = "#000000"
DEFAULT_SIZE = 30
DEFAULT_TOOL = drawing_tools.Brush(DEFAULT_SIZE, DEFAULT_COLOR)
BRUSH_SIZES = range(5,85,5)

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

class DrawErMain:
    def __init__(self):
        ''' Initializes main window for user to draw in. '''

        ## Root window.
        self._root = tk.Tk()
        self._root.title("Drawing")

        ## Attributes
        self._current_tool = DEFAULT_TOOL
        self._button1_is_down = False
        self._previous_coords = (0,0)
        self._current_color = DEFAULT_COLOR
        self._current_size = DEFAULT_SIZE
        self._last_outline = None

        self._create_widgets()
        self._grid_widgets()

        ## This allows canvas to resize while keeping everything else in
        ## its place
        self._root.rowconfigure(1, weight = 1)
        self._root.columnconfigure(1, weight = 1)

        self._drawing_frame.rowconfigure(0, weight = 1)
        self._drawing_frame.columnconfigure(0, weight = 1)
        

        ## Event binding
        self._canvas.bind('<Button-1>', self._on_button_one_down_with_brush)
        self._canvas.bind('<ButtonRelease-1>', self._on_button_one_release)
        self._canvas.bind('<Motion>', self._on_mouse_move_with_brush)
        self._color_picker.bind('<Button-1>', self._on_color_picker_selected)


    def run(self):
        self._root.mainloop()


    #########################################
    ## Widget creation and gridding

    def _create_widgets(self):
        ## Create all top, side, bottom, and canvas frames
        self._top_frame = tk.Frame(master = self._root, bg = "#f1f1f1")
        self._sidebar_frame = tk.Frame(master = self._root, bg = "#f1f1f1")
        self._bottom_frame = tk.Frame(master = self._root, bg = "#f1f1f1")
        self._drawing_frame = tk.Frame(master = self._root, bg = "#f1f1f1")

        self._top_frame.grid(row = 0, column = 1,
                             sticky = tk.W + tk.E)
        self._sidebar_frame.grid(row = 1, column = 0,
                                 sticky = tk.N + tk.S)
        self._bottom_frame.grid(row = 2, column = 0, columnspan = 2,
                                sticky = tk.W + tk.E)
        self._drawing_frame.grid(row = 1, column = 1,
                                 sticky = tk.N + tk.S + tk.E + tk.W)

        ## Canvas for drawing and placing shapes.
        self._canvas = tk.Canvas(master = self._drawing_frame,
                                 width = CANVAS_WIDTH,
                                 height = CANVAS_HEIGHT,
                                 bg = '#ffffff')


        ## Size menu, label, and menu button
        self.dropVar = tk.IntVar(self._root)
        self.dropVar.set(DEFAULT_SIZE)
        self._size_label = tk.Label(master = self._top_frame,
                                    text = "Size")
        self._size_menu_button = tk.OptionMenu(self._top_frame,
                                               self.dropVar,
                                               *BRUSH_SIZES,
                                               command = self._update_brush_size)

 
        ## Quit and clear button
        self._quit_button = tk.Button(master = self._bottom_frame,
                                      text = "Quit",
                                      font = DEFAULT_FONT,
                                      command = self._root.destroy)
        
        self._clear_all_button = tk.Button(master = self._bottom_frame,
                                                text = 'Clear',
                                                font = DEFAULT_FONT,
                                                command = self._clear_canvas)
        

        ## Shape and brush selection buttons
        self._eraser_select = tk.Button(master = self._sidebar_frame,
                                        text = "E",
                                        font = DEFAULT_FONT,
                                        command = self._on_eraser_select)
        
        self._pencil_select = tk.Button(master = self._sidebar_frame,
                                        text = "/",
                                        font = DEFAULT_FONT,
                                        command = self._on_pencil_select)

        self._brush_select = tk.Button(master = self._sidebar_frame,
                                       text = "b",
                                       font = DEFAULT_FONT,
                                       command = self._on_brush_select)
        
        self._square_select = tk.Button(master = self._sidebar_frame,
                                        text = "[]",
                                        font = DEFAULT_FONT,
                                        command = self._on_square_select)

        self._circle_select = tk.Button(master = self._sidebar_frame,
                                        text = "O",
                                        font = DEFAULT_FONT,
                                        command = self._on_circle_select)

        self._triangle_select = tk.Button(master = self._sidebar_frame,
                                          text = "/\\",
                                          font = DEFAULT_FONT,
                                          command = self._on_triangle_select)


        ## Color picker
        self._color_picker = tk.Canvas(master = self._sidebar_frame,
                                       width = 25, height = 25,
                                       bg = DEFAULT_COLOR)


    def _grid_widgets(self):
        """ Grid all widgets within their frames
        """
        self._canvas.grid(row = 0, column = 0,
                          sticky = tk.N + tk.S + tk.E + tk.W)

        self._size_label.grid(row = 0, column = 0)
        self._size_menu_button.grid(row = 0, column = 1)
        
        self._quit_button.grid(row = 0, column = 1)
        self._clear_all_button.grid(row = 0, column = 2)

        self._eraser_select.grid(row = 0, column = 0)
        self._pencil_select.grid(row = 1, column = 0)
        self._brush_select.grid(row = 2, column = 0)
        self._square_select.grid(row = 3, column = 0)
        self._circle_select.grid(row = 4, column = 0)
        self._triangle_select.grid(row = 5, column = 0)
        self._color_picker.grid(row = 6, column = 0)
        


    #########################################
    ## Canvas related fucntions

    def _clear_canvas(self) -> None:
        ''' Clears the entire canvas
        '''            
        self._canvas.delete(tk.ALL)
        
        
    #########################################
    ## Event binding functions

    def _on_button_one_down_with_brush(self, event: tk.Event) -> None:
        ''' When left button is pressed; draw '''
        self._button1_is_down = True
        self._previous_coords = (event.x, event.y)

        # For brushes we need to draw a shape when user first clicks
        oldX, oldY = self._previous_coords
        self._current_tool.create(self._canvas, oldX, oldY,
                                  event.x+1, event.y+1)

    def _on_button_one_down_with_shape(self, event: tk.Event) -> None:
        ''' When left button is pressed; remember the click point ''' 
        self._button1_is_down = True
        self._previous_coords = (event.x, event.y)

    def _on_button_one_release(self, event: tk.Event) -> None:
        ''' Updates button one condition and forgets the last shape that
        was drawn, so that we do not erase it.
        '''        
        self._button1_is_down = False
        self._last_outline = None

    def _on_mouse_move_with_brush(self, event: tk.Event):
        """ Also includes pencil tool
        Draw with brush and update previous coordinates to current mouse
        position.
        """
        if self._button1_is_down:
            oldX, oldY = self._previous_coords
            self._current_tool.create(self._canvas, oldX, oldY,
                                      event.x, event.y)
            self._previous_coords = (event.x, event.y)

    def _on_mouse_move_with_shape(self, event: tk.Event):
        """ Creates the illusion of click and drag shape resizing.
        First deletes the old shape drawn, then draws a new shape using the original
        click point and the current mouse position.
        """
        if self._button1_is_down:
            self._canvas.delete(self._last_outline)
            originalX, originalY = self._previous_coords
            self._last_outline = self._current_tool.create(self._canvas,
                                                           originalX, originalY,
                                                           event.x, event.y)

    def _on_color_picker_selected(self, event: tk.Event):
        """ Update the current color attribute and the current tool's color
        """
        color_tool = app_tools.ColorPicker(self._current_color)
        color_tool.show_window()

        self._current_color = color_tool.get_color()
        self._color_picker.config(bg = self._current_color)
        self._current_tool.configure(color = self._current_color)


    #########################################
    ## Functions for tools and options selected

    def _update_brush_size(self, value: int):
        """ Updates the the current size attribute and the size of the
        current tool
        """
        self._current_size = value
        self._current_tool.configure(size = value)

        
    def _on_eraser_select(self):
        """ Create a brush tool with the color white
        """
        self._canvas.bind('<Button-1>', self._on_button_one_down_with_brush)
        self._canvas.bind('<Motion>', self._on_mouse_move_with_brush)
        self._current_tool = drawing_tools.Brush(self._current_size,
                                                    "#ffffff")
        
    def _on_pencil_select(self):
        """ When the pencil tool is selected, bind the correct
        Motion function and update the current tool to the Pencil tool.
        """
        self._canvas.bind('<Button-1>', self._on_button_one_down_with_brush)
        self._canvas.bind('<Motion>', self._on_mouse_move_with_brush)
        self._current_tool = drawing_tools.Pencil(self._current_size,
                                                    self._current_color)

    def _on_brush_select(self):
        """ Bind the correct Motion function and update the
        current tool to Brush tool.
        """
        self._canvas.bind('<Button-1>', self._on_button_one_down_with_brush)
        self._canvas.bind('<Motion>', self._on_mouse_move_with_brush)
        self._current_tool = drawing_tools.Brush(self._current_size,
                                                    self._current_color)
        
    def _on_square_select(self):
        """ Bind the correct Motion function and update the
        current tool to Square tool.
        """
        self._canvas.bind('<Button-1>', self._on_button_one_down_with_shape)
        self._canvas.bind('<Motion>', self._on_mouse_move_with_shape)
        self._current_tool = drawing_tools.Square(self._current_size,
                                                    self._current_color)

    def _on_circle_select(self):
        """ Bind the correct Motion function and update the
        current tool to Circle tool.
        """
        self._canvas.bind('<Button-1>', self._on_button_one_down_with_shape)
        self._canvas.bind('<Motion>', self._on_mouse_move_with_shape)
        self._current_tool = drawing_tools.Circle(self._current_size,
                                                    self._current_color)

    def _on_triangle_select(self):
        """ Bind the correct Motion function and update the
        current tool to Triangle tool.
        """
        self._canvas.bind('<Button-1>', self._on_button_one_down_with_shape)
        self._canvas.bind('<Motion>', self._on_mouse_move_with_shape)
        self._current_tool = drawing_tools.Triangle(self._current_size,
                                                    self._current_color)
        
        


if __name__ == "__main__":
    DrawErMain().run()
