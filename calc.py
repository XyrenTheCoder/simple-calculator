import tkinter as tk
import matplotlib.pyplot as plt

from sympy import *

from decimal import Decimal

from functools import partial

from numpy import e
from numpy import pi
from numpy import linspace
from numpy import real as Re
from numpy import imag as Im

from scipy.special import erf
from scipy.special import zeta
from scipy.special import lambertw as W

root = tk.Tk()
root.geometry("450x600")
root.config(bg = '#121212')
root.wm_attributes('-alpha', '0.9')

text = tk.Text(root, height=5, width=60, fg = '#ffffff', bg='#2c2c2b')
text.bind("<Key>", lambda e : "break")
text.pack()

key_buffer = str()

class Operations:
    def __init__(self, key_buffer):
        self.key_buffer = key_buffer

    def comb(self, n, r):
        return factorial(n) / (factorial(r) * factorial(n - r))

    def perm(self, n, r):
        return factorial(n) / factorial(n - r)

    '''
    def check_continuity(self, func : callable, lim, symbol) -> bool | None: # python >= 3.10
        return limit(func, symbol, lim).is_real and not func.has(zoo, nan)

    def check_continuity(self, func : callable, lim, symbol) -> Union[bool, None]: # python < 3.10
        return limit(func, symbol, lim).is_real and not func.has(zoo, nan)
    '''

class Buttons:
    def __init__(self, key_buffer):
        self.key_buffer = key_buffer

    def basic_operation(self, symbol):
        symbols = ["*", "/", "+", "-"]
        symbols.remove(symbol)
        if len(self.key_buffer) == 0:
            self.a(0)
            self.key_buffer += symbol
            if symbol == "*": text.insert(tk.END, " × ")
            else: text.insert(tk.END, f" {symbol} ")
        elif self.key_buffer[len(self.key_buffer) - 1] == symbol: return
        elif self.key_buffer[len(self.key_buffer) - 1] in symbols:
            text.delete(tk.END)
            self.key_buffer[::-1].replace(self.key_buffer[len(self.key_buffer) - 1], symbol, 1)
            if symbol == "*": text.insert(tk.END, " × ")
            else: text.insert(tk.END, f" {symbol} ")
        else:
            self.key_buffer += symbol
            if symbol == "*": text.insert(tk.END, " × ")
            else: text.insert(tk.END, f" {symbol} ")

    def a(self, n):
        # try:
        #     if not n.isdigit() and text.get("end-2c") != "." and text.get("end-2c") != "":
        #         self.key_buffer += "*"
        # except AttributeError:
        #     pass
        if n == e:
            text.insert(tk.END, "e")
            self.key_buffer += "e"
        elif n == pi:
            text.insert(tk.END, "π")
            self.key_buffer += "pi"
        else:
            text.insert(tk.END, n)
            self.key_buffer += str(n)

    def dot(self):
        if "." not in self.key_buffer:
            if len(self.key_buffer) == 0:
                self.a(0)
            self.key_buffer += "."
            text.insert(tk.END, ".")

    def sign(self):
        if self.key_buffer.startswith("-"):
            self.key_buffer = self.key_buffer[1:]
            text.delete("1.0")
        else:
            text.insert('1.0', "-")
            self.key_buffer = "-" + self.key_buffer

    def a_function(self, a, b):
        text.insert(tk.END, f"{a}(")
        self.key_buffer += f"{b}("

    def plus(self):
        self.basic_operation("+")

    def minus(self):
        self.basic_operation("-")

    def div(self):
        self.basic_operation("/")

    def mult(self):
        self.basic_operation("*")

    def sqrt(self):
        self.a_function("√", "sqrt")

    def ln(self):
        self.a_function("ln", "ln")

    def log(self):
        self.a_function("log", "log")

    def fac(self):
        self.a_function("factorial", "factorial")

    def _pow(self):
        if len(self.key_buffer) == 0:
            text.insert(tk.END, "0")
            self.key_buffer += "0"
        text.insert(tk.END, "^")
        self.key_buffer += "**"

    def equals(self, print_res=True, plot=False):
        if len(self.key_buffer) == 0: return
        if plot and print_res:
            print_res = False
        try:
            print(key_buffer)

            x = Symbol("x")
            r = eval(self.key_buffer)

            def f(t : int):
                return eval(str(r.subs(x, t)))

            if plot:
                xpoints = list(linspace(-5, 5, 100))
                y = []

                for i in xpoints:
                    y.append(N(f(i)))
                try:
                    i = 0
                    while i < len(y) - 1:
                        if y[i] != y[i] or not y[i].is_real:
                            y.pop(i)
                            xpoints.pop(i)
                        else:
                            i += 1
                except TypeError: pass

                fig = plt.figure()
                ax = fig.add_subplot(1, 1, 1)
                ax.spines['left'].set_position('center')
                ax.spines['bottom'].set_position('zero')
                ax.spines['right'].set_color('none')
                ax.spines['top'].set_color('none')
                ax.xaxis.set_ticks_position('bottom')
                ax.yaxis.set_ticks_position('left')

                plt.plot(xpoints,y, 'r')
                plt.show()

            if print_res: text.insert(tk.END, f"\n= {Decimal(str(N(r))).normalize()}")
        except SyntaxError:
            self.clear()
            text.insert(tk.END, "Syntax Error: Missing one or more elements")
        except ZeroDivisionError:
            self.clear()
            text.insert(tk.END, "Math Error: Division by zero")
        except AttributeError:
            self.clear()
            text.insert(tk.END, "Plot Error: Illegal elements (Constant or Invalid syntax)")
        if print_res: text.config(state=tk.DISABLED)

    def plot(self):
        self.equals(print_res=False, plot=True)

    def delete(self):
        full_delete_kw = {"ln(" : "ln(", "log(" : "log(", "√(" : "sqrt(", "factorial(" : "factorial(", " + " : "+", " - " : "-", " × " : "*", " / " : "/"}
        for i in full_delete_kw.keys():
            if text.get("1.0", "end-1c").endswith(i):
                text.delete(f"end-{len(i) + 1}c", tk.END)
                for j in full_delete_kw[i]:
                    self.key_buffer = self.key_buffer[:-1]
                return
        text.delete("end-2c", tk.END)
        self.key_buffer = self.key_buffer[:-1]

    def clear(self):
        text.config(state=tk.NORMAL)
        self.key_buffer = str()
        text.delete("1.0", tk.END)

    def init(self):
        # colors for buttons
        black = '#8f8f8f'
        red = '#e91e63'

        lblack = '#696969'
        lred = '#ad1146'
        # not so nice colors

        coords = [(10, 220), (10, 180), (70, 180), (130, 180), (10, 140), (70, 140), (130, 140), (10, 100), (70, 100), (130, 100)]
        for i in range(9, -1, -1):
            f = partial(self.a, i)
            locals()[f"button{i}"] = tk.Button(root, text=i, command=f, height=1, width=3, bg=black, activebackground=lblack)
            locals()[f"button{i}"].place(x=coords[i][0], y=coords[i][1])

        op = partial(self.a, "(")
        cp = partial(self.a, ")")
        _e = partial(self.a, e)
        _pi = partial(self.a, pi)
        _x = partial(self.a, "x")
        cm = partial(self.a, ",")

        button_dot = tk.Button(root, text=".", command=self.dot, height=1, width=3, bg=black, activebackground=lblack)
        button_sign = tk.Button(root, text="+/-", command=self.sign, height=1, width=3, bg=black, activebackground=lblack)
        button_plus = tk.Button(root, text="+", command=self.plus, height=1, width=3, bg=black, activebackground=lblack)
        button_minus = tk.Button(root, text="-", command=self.minus, height=1, width=3, bg=black, activebackground=lblack)
        button_mult = tk.Button(root, text="×", command=self.mult, height=1, width=3, bg=black, activebackground=lblack)
        button_div = tk.Button(root, text="/", command=self.div, height=1, width=3, bg=black, activebackground=lblack)
        button_eq = tk.Button(root, text="=", command=self.equals, height=1, width=3, bg=black, activebackground=lblack)
        button_ac = tk.Button(root, text="AC", command=self.clear, height=1, width=3, bg=red, activebackground=lred)
        button_del = tk.Button(root, text="DEL", command=self.delete, height=1, width=3, bg=red, activebackground=lred)
        button_op = tk.Button(root, text="(", command=op, height=1, width=3, bg=black, activebackground=lblack)
        button_cp = tk.Button(root, text=")", command=cp, height=1, width=3, bg=black, activebackground=lblack)
        button_pow = tk.Button(root, text="aᵇ", command=self._pow, height=1, width=3, bg=black, activebackground=lblack)
        button_sqrt = tk.Button(root, text="√", command=self.sqrt, height=1, width=3, bg=black, activebackground=lblack)
        button_ln = tk.Button(root, text="ln", command=self.ln, height=1, width=3, bg=black, activebackground=lblack)
        button_log = tk.Button(root, text="log", command=self.log, height=1, width=3, bg=black, activebackground=lblack)
        button_cm = tk.Button(root, text=",", command=cm, height=1, width=3, bg=black, activebackground=lblack)
        button_plt = tk.Button(root, text="plot", command=self.plot, height=1, width=3, bg=black, activebackground=lblack)
        button_e = tk.Button(root, text="e", command=_e, heigh=1, width=3, bg=black, activebackground=lblack)
        button_pi = tk.Button(root, text="π", command=_pi, heigh=1, width=3, bg=black, activebackground=lblack)
        button_fac = tk.Button(root, text="n!", command=self.fac, height=1, width=3, bg=black, activebackground=lblack)
        button_x = tk.Button(root, text="x", command=_x, height=1, width=3, bg=black, activebackground=lblack)

        button_e.place(x=10, y=260)
        button_pi.place(x=70, y=260)
        button_dot.place(x=70, y=220)
        button_sign.place(x=130, y=220)
        button_plus.place(x=190, y=100)
        button_minus.place(x=190, y=140)
        button_mult.place(x=190, y=180)
        button_div.place(x=190, y=220)
        button_eq.place(x=190, y=260)
        button_plt.place(x=190, y=300)
        button_ac.place(x=250, y=100)
        button_op.place(x=310, y=100)
        button_cp.place(x=370, y=100)
        button_pow.place(x=250, y=220)
        button_sqrt.place(x=250, y=180)
        button_ln.place(x=310, y=140)
        button_log.place(x=370, y=140)
        button_cm.place(x=310, y=180)
        button_del.place(x=250, y=140)
        button_fac.place(x=310, y=220)
        button_x.place(x=130, y=260)

b = Buttons(key_buffer)

b.init()
tk.mainloop()