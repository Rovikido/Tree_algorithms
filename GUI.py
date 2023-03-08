from tkinter import *
from tkinter import messagebox
import threading
import validation
import Morse


class GUINode:
    circle_size = 30

    def __init__(self, char, master):
        self.char = char
        self.master = master

    def create_node(self, canvas, x=100, y=100, size_mult=1):
        self.sise_mult = size_mult
        self.circle = canvas.create_oval(x - self.circle_size*size_mult / 2, y - self.circle_size*size_mult / 2, x + self.circle_size*size_mult / 2, y + self.circle_size*size_mult / 2, width=2, fill="#d9d9d9")
        self.char_text = canvas.create_text(x, y, text=self.char, font='Times 20')
        self.canvas = canvas
        return self

    def move_to(self, x, y):
        self.canvas.move(self.circle, x, y)
        self.canvas.move(self.char_text, x + self.circle_size * self.sise_mult / 2, x + self.circle_size * self.sise_mult / 2)

    def light(self, col="green", delay=35):
        self.changed=False
        self.canvas.itemconfig(self.circle, fill=col)
        def func():
            self.canvas.itemconfig(self.circle, fill="#d9d9d9")
            self.changed = True
        self.canvas.after(delay, lambda: func())


class InputWin:
    def __init__(self, master, bg_col='#CDCDD6'):
        self.master = master
        self.master.title("Tree Algorithms")
        self.change_icon()
        self.master.resizable(width=False, height=False)
        self.master.configure(bg=bg_col)
        self.canvas = Canvas(master, width=1550, height=500)
        self.__options_frame = Frame(master=self.master, bg=bg_col)
        self.create_inputs(self.__options_frame, bg_col)
        self.create_result(self.__options_frame, bg_col)
        self.create_buttons(self.__options_frame, bg_col)

        self.__options_frame.pack()
        self.create_confirmation()

        self.morse_table_container = Morse.MorseTableContainer()
        self.morse_table_container.assign_morse_values()
        self.canvas.pack()
        self.create_tree()

    def change_icon(self):
        self.master.iconbitmap(r"C:\Users\User\PycharmProjects\Tree_algorithms\icon.ico")

    def thread(func):
        def wrapper(*args, **kwargs):
            current_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            current_thread.start()

        return wrapper


    def create_tree_recursive(self, obj, x, y, width, pattern, prev_x, prev_y):
        line = self.canvas.create_line(x, y, prev_x, prev_y, dash=pattern, width=3)
        self.canvas.tag_lower(line)
        node = GUINode(obj.char, master=self.master).create_node(self.canvas, x=x, y=y)
        obj.add_gui_node(node)
        if obj.dot:
            self.create_tree_recursive(obj.dot, (x-width/3-self.padding_x), y + self.padding_y, width/3, (1, 1), x, y)
        if obj.dash:
            self.create_tree_recursive(obj.dash, (x + width / 3+self.padding_x), y + self.padding_y, width/3, (100, 1), x, y)


    def create_tree(self, levels=5, padding_x=12, padding_y=60):
        self.padding_x = padding_x
        self.padding_y = padding_y
        width = (GUINode.circle_size + self.padding_x) * pow(2, levels)
        height = (GUINode.circle_size + self.padding_y) * levels
        node = GUINode("START", master=self.master).create_node(self.canvas, x=(width/2) + 100, y=(700-175-height), size_mult=3.2)
        self.morse_table_container.table.root.add_gui_node(node)
        cst = (width / 2)
        self.create_tree_recursive(self.morse_table_container.table.root.dot, cst / 3 + 200, (700 - 175 - height) + padding_y, width/3, (1, 1), (width/2) + 100, (700-175-height))
        self.create_tree_recursive(self.morse_table_container.table.root.dash, cst / 3 + cst + 200, (700 - 175 - height) + padding_y, width/3, (100, 1), (width/2) + 100, (700-175-height))

    @thread
    def start_text(self):
        if not self.start_code_status and not self.start_text_status:
            try:
                self.start_text_status = True
                algorithms = [self.pre_order_val.get(), self.in_order_val.get(), self.post_order_val.get(), self.level_order_val.get()]

                validation.validate_checks(algorithms)
                text = self.text_input.get()
                validation.validate_text(text)

                self.res_text.delete('1.0', END)
                self.res_text.insert(END, text + ": \n")
                if algorithms[0]:
                    self.morse_table_container.string_to_code(text, "pre_order", res_text=self.res_text)
                if algorithms[1]:
                    self.morse_table_container.string_to_code(text, "in_order", res_text=self.res_text)
                if algorithms[2]:
                    self.morse_table_container.string_to_code(text, "post_order", res_text=self.res_text)
                if algorithms[3]:
                    self.morse_table_container.string_to_code(text, "level_order", res_text=self.res_text)
            except Exception as e:
                messagebox.showerror('Incorrect Input', e)
                pass
            finally:
                self.start_text_status = False

    @thread
    def start_code(self):
        if not self.start_code_status and not self.start_text_status:
            try:
                self.start_code_status = True
                code = self.code_input.get()
                validation.validate_code(code, self.morse_table_container.code_list)
                self.res_text.delete('1.0', END)
                code, n = re.subn('[\*\·\.]', '•', code)
                code, n = re.subn('[-\_\—\–]', '–', code)
                self.res_text.insert(END, code + ": \n")
                self.morse_table_container.code_to_string(code, res_text=self.res_text)
            except Exception as e:
                messagebox.showerror('Incorrect Input', e)
                pass
            finally:
                self.start_code_status = False


    def create_inputs(self, master, col='#CDCDD6', col2='#DCDCE2'):
        input_frame = Frame(master=master, bg=col)
        text_label = Label(master=input_frame, text='Text to translate into Morse', font='Comfortaa 12', bg=col)
        self.text_input = Entry(input_frame, font='Consolas 15', relief='raised', justify='left', bg=col2, width=20)

        code_label = Label(master=input_frame, text='Morse to translate into text', font='Comfortaa 12', bg=col)
        self.code_input = Entry(input_frame, font='Consolas 15', relief='raised', justify='left', bg=col2, width=20)

        text_label.pack(anchor="w")
        self.text_input.pack(anchor="w")
        code_label.pack(anchor="w", pady=(5, 0))
        self.code_input.pack(anchor="w")
        input_frame.pack(side=LEFT, pady=(15, 40), padx=(15, 30), fill=BOTH, expand=True)
        # choice_frame
        self.__input_frame = input_frame


    def create_buttons(self, master, col='#CDCDD6'):
        btn_frame = Frame(master=master, bg=col)

        algorithm_label = Label(master=btn_frame, text='Choose algorithms', font='Comfortaa 12',
                                  bg=col)
        self.pre_order_val = BooleanVar(self.master, False)
        pre_order_checkbox = Checkbutton(master=btn_frame, text='Pre-order',
                                         font='Comfortaa 12', bg=col, activebackground=col,
                                         variable=self.pre_order_val)

        self.in_order_val = BooleanVar(self.master, False)
        in_order_checkbox = Checkbutton(master=btn_frame, text='In-order',
                                              font='Comfortaa 12', bg=col, activebackground=col,
                                              variable=self.in_order_val)

        self.post_order_val = BooleanVar(self.master, False)
        post_order_checkbox = Checkbutton(master=btn_frame, text='Post-order',
                                             font='Comfortaa 12', bg=col, activebackground=col,
                                             variable=self.post_order_val)

        self.level_order_val = BooleanVar(self.master, False)
        level_order_checkbox = Checkbutton(master=btn_frame, text='Level-order',
                                               font='Comfortaa 12', bg=col, activebackground=col,
                                               variable=self.level_order_val)

        pre_order_checkbox.pack(anchor="w")
        in_order_checkbox.pack(anchor="w")
        post_order_checkbox.pack(anchor="w")
        level_order_checkbox.pack(anchor="w")
        btn_frame.pack(pady=(15, 15), padx=(30, 25), side=TOP, fill=X)
        self.__btn_frame = btn_frame


    def create_result(self, master, col='#CDCDD6', col2='#DCDCE2'):
        res_frame = Frame(master=master, bg=col)
        scroll_bar = Scrollbar(res_frame)
        self.res_text = Text(res_frame, height=6, width=40, yscrollcommand=scroll_bar.set, font='Consolas 12')


        scroll_bar.pack(side=RIGHT, fill=Y, pady=1)
        self.res_text.pack(side=LEFT)

        self.res_text.insert('1.0', "Result will be displayed here!")
        res_frame.pack(side=RIGHT, pady=(15, 30), padx=(0, 25), fill=Y)
        self.res_frame = res_frame


    def create_confirmation(self, col='#CDCDD6', col2='#DCDCE2'):
        conf_frame = Frame(master=self.master, bg=col)

        conf_button_text = Button(text='Text to Morse', font='Consolas 15', bg=col2,
                             command=self.start_text, master=conf_frame, width=15)
        self.start_text_status = False
        conf_button_code = Button(text='Morse to text', font='Consolas 15', bg=col2,
                             command=self.start_code, master=conf_frame, width=15)
        self.start_code_status = False
        conf_button_text.pack(side=LEFT)
        conf_button_code.pack(side=RIGHT)
        conf_frame.pack(pady=(0, 20), ipadx=15)
        self.__conf_frame = conf_frame

#
# root = Tk()
# win = InputWin(root)
# win.create_tree()
# root.mainloop()

# pyinstaller main.py --onefile --noconsole --icon="icon.ico" --name "Tree Algorithms"

