import time
from tkinter import END, Text

class Queue:
    def __init__(self):
        self.__q = []

    def __len__(self):
        return len(self.__q)

    def __next__(self):
        # check for size
        obj = self.__q[0]
        self.deque()
        return obj

    def enque(self, elem, path=""):
        self.__q.append(elem)

    def deque(self):
        if len(self.__q) > 0:
            return self.__q.pop(0)
        else: # raise error
            pass

    def not_empty(self):
        return len(self.__q) > 0


class Node:
    def __init__(self, data="", path=""):
        self.path = path
        self.char = data
        self.dot = None
        self.dash = None
        self.gui_node = None

    def add_gui_node(self, node):
        self.gui_node = node


class MorseTableContainer:
    def __init__(self):
        self.table = MorseTable()
        self.code_list = []

    def assign_morse_values(self):
        self.__create_node("•–", "a")
        self.__create_node("–•••", "b")
        self.__create_node("–•–•", "c")
        self.__create_node("–••", "d")
        self.__create_node("•", "e")
        self.__create_node("••–•", "f")
        self.__create_node("––•", "g")
        self.__create_node("••••", "h")
        self.__create_node("••", "i")
        self.__create_node("•–––", "j")
        self.__create_node("–•–", "k")
        self.__create_node("•–••", "l")
        self.__create_node("––", "m")
        self.__create_node("–•", "n")
        self.__create_node("–––", "o")
        self.__create_node("•––•", "p")
        self.__create_node("––•–", "q")
        self.__create_node("•–•", "r")
        self.__create_node("•••", "s")
        self.__create_node("–", "t")
        self.__create_node("••–", "u")
        self.__create_node("•••–", "v")
        self.__create_node("•––", "w")
        self.__create_node("–••–", "x")
        self.__create_node("–•––", "y")
        self.__create_node("––••", "z")
        self.__create_node("•––––", "1")
        self.__create_node("••–––", "2")
        self.__create_node("•••––", "3")
        self.__create_node("••••–", "4")
        self.__create_node("•••••", "5")
        self.__create_node("–••••", "6")
        self.__create_node("––•••", "7")
        self.__create_node("–––••", "8")
        self.__create_node("––––•", "9")
        self.__create_node("–––––", "0")

    def __create_node(self, code, char):
        char = char.upper()
        node = self.table.get_node_from_path(code, self.table.root, create=True)
        self.code_list.append(code)
        node.char = char
        node.path = code

    def code_to_string(self, code, res_text=None):
        text = ""
        for i in code.split():
            if i == "/":
                res = " "
            else:
                res = self.table.get_node_from_path(i, self.table.root, display=True).char
            if res_text:
                res_text.insert(END, res)
                res_text.see(END)
            text += res
        return text

    def string_to_code(self, string, algorithm="pre_order", res_text=None):
        morse = ""
        string = string.upper()
        res_text.insert(END, "\n" + algorithm + ": ")
        for c in string:
            if c == " ":
                res = " / "
            else:
                res = self.char_to_code(c, algorithm) + " "

            if res_text:
                res_text.insert(END, res)
                res_text.see(END)
            morse += res
        return morse

    def char_to_code(self, char, algorithm="pre_order"):
        if algorithm == "pre_order":
            code = self.table.pre_order(char, self.table.root)[0]
        elif algorithm == "in_order":
            code = self.table.in_order(char, self.table.root)[0]
        elif algorithm == "post_order":
            code = self.table.post_order(char, self.table.root)[0]
        elif algorithm == "level_order":
            code = self.table.level_order(char, self.table.root)[0]
        return code


class MorseTable:
    def __init__(self):
        self.root = Node(" ")

    def get_node_from_path(self, path, start, create=False, node=None, display=False):
        if node:
            return node
        if start:
            if len(path) == 0:
                return start
            if display and start.gui_node:
                start.gui_node.light(delay=100)
                while not start.gui_node.changed:
                    time.sleep(0.01)
            if path[:1] == "*" or path[:1] == "·" or path[:1] == "." or path[:1] == "•":
                obj = start.dot
                if not obj and create:
                    start.dot = Node()
                    obj = start.dot
                return self.get_node_from_path(path[1:], obj, create, display=True)

            elif path[:1] == "-" or path[:1] == "_" or path[:1] == "—" or path[:1] == "–":
                obj = start.dash
                if not obj and create:
                    start.dash = Node()
                    obj = start.dash
                return self.get_node_from_path(path[1:], obj, create, display=True)

    # root->dot->dash
    def pre_order(self, char, start, path="", found=False):
        if start:
            start.gui_node.light()
            while not start.gui_node.changed:
                time.sleep(0.01)
            if start.char == char or found:
                return [path, True]
            l = self.pre_order(char, start.dot, path + "•", found)
            if l[1]:
                return l
            l2 = self.pre_order(char, start.dash, path + "–", found)
            if l2[1]:
                return l2
        return [path, False]

    # dot->root->dash
    def in_order(self, char, start, path="", found=False):
        if start:
            start.gui_node.light()
            while not start.gui_node.changed:
                time.sleep(0.01)
            l = self.pre_order(char, start.dot, path + "•", found)
            if l[1]:
                return l
            if start.char == char or found:
                return [path, True]
            l2 = self.pre_order(char, start.dash, path + "–", found)
            if l2[1]:
                return l2
        return [path, False]

    # dot->dash->root
    def post_order(self, char, start, path="", found=False):
        if start:
            start.gui_node.light()
            while not start.gui_node.changed:
                time.sleep(0.01)
            l = self.pre_order(char, start.dot, path + "•", found)
            if l[1]:
                return l
            l2 = self.pre_order(char, start.dash, path + "–", found)
            if l2[1]:
                return l2
            if start.char == char or found:
                return [path, True]
        return [path, False]

    def level_order(self, char, start):
        q = Queue()
        q.enque(start)
        while q.not_empty():
            node = next(q)
            node.gui_node.light()
            while not node.gui_node.changed:
                time.sleep(0.01)
            if node.char == char:
                return [node.path, True]
            if node.dot:
                q.enque(node.dot)
            if node.dash:
                q.enque(node.dash)
        return None


# mtc = MorseTableContainer()
# mtc.assign_morse_values()
# print(mtc.string_to_code("UUUUsd"))
# print(mtc.code_to_string("*·- **- **- **- *** -**"))
