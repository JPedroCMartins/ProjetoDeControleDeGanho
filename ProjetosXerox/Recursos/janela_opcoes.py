from Recursos import funcoes
from Recursos import colors
from ttkthemes import ThemedStyle
from tkinter import ttk
from tkinter import *
import tkinter
Colors = colors.Colors
Funcs = funcoes.Funcs
class AppOpt(Funcs):
    def __init__(self):
        self.opt_root = Tk()
        self.colors = Colors()
        self.tela()
        self.widget()
        self.opt_root.mainloop()
    def tela(self):

        style = ThemedStyle(self.opt_root)
        style.set_theme(self.colors.theme)

        self.opt_root.title("Opções")
        self.opt_root.configure(background=self.colors.background_color)
        self.opt_root.geometry("480x720")
        self.opt_root.resizable(False, False)
        # self.root.maxsize(width=720, height=1080)
        self.opt_root.minsize(width=420, height=720)
    def widget(self):
        self.btn_plan = Button(self.opt_root, text="Criar Planilha", command=self.opt_table, bd=4, bg=self.colors.hgb_color, font=self.colors.fonte, fg=self.colors.fg_green)
        self.btn_plan.place(relx=0.05, rely=0.05, relwidth=0.50, relheight=0.05)
        self.btn_contexto_impressora = Button(self.opt_root, text="Contexto Impressão", bd=4, command=self.contextoImpress, bg=self.colors.hgb_color, font=self.colors.fonte, fg=self.colors.fg_green)
        self.btn_contexto_impressora.place(relx=0.05, rely=0.10, relwidth=0.50, relheight=0.05)


        self.lbl_plan_status = Label(self.opt_root, text="STATUS", font=self.colors.fonte, bd=4, highlightbackground=self.colors.hgb_color, highlightthickness=3, background=self.colors.background_color1, fg=self.colors.text_color)
        self.lbl_plan_status.place(relx = 0.58, rely=0.05, relwidth=0.40, relheight=0.05)

        self.lbl_contexto = Label(self.opt_root, text="STATUS", font=self.colors.fonte, bd=4, highlightbackground=self.colors.hgb_color, highlightthickness=3, background=self.colors.background_color1, fg=self.colors.text_color)
        self.lbl_contexto.place(relx = 0.58, rely=0.10, relwidth=0.40,relheight=0.05)
if __name__ == "__main__":
    AppOpt()