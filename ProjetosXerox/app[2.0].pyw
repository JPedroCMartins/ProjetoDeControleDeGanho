import threading
import tkinter

from ttkthemes import ThemedStyle
from tkinter import ttk
from tkinter import *

from Recursos import funcoes
from Recursos import colors
from Recursos import janela_opcoes

Funcs = funcoes.Funcs
Colors = colors.Colors
AppOpt = janela_opcoes.AppOpt

# Função Principal da Aplicação
class Application(Funcs):
    def __init__(self):
        ##IMPORTANTE: todas as funções criadas devem ser chamadas em ordem e antes do mainloop()
        super().__init__()
        root = Tk()
        thread = threading.Thread(target=self.atLabel)
        thread.start()
        self.colors = Colors()
        self.MontaTabela()
        self.frame_1 = None
        self.frame_2 = None
        self.btn_confirmar = None
        self.lbl4 = None
        self.rd_caixa = None
        self.rd_pix = None
        self.scrollTabela = None
        self.root = root
        self.tela()
        self.frame_da_tela()
        self.criando_widgets_frame1()
        self.tabela_frame2()
        self.atualizarCabeca()
        self.select_tabela()
        root.mainloop()

    ## Configuração da Tela
    def tela(self):

        style = ThemedStyle(self.root)
        style.set_theme(self.colors.theme)
    
        self.root.title("Gerenciamento de Ganhos [CAIXA]")
        self.root.configure(background=self.colors.background_color)
        self.root.geometry("720x1080")
        self.root.resizable(True, True)
        # self.root.maxsize(width=720, height=1080)
        self.root.minsize(width=420, height=720)

    ## Frames da Tela, na minha aplicação foi dividido em 2 Frames
    def frame_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, highlightbackground=self.colors.hgb_color, highlightthickness=3, background=self.colors.bg_color)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.36)
        self.frame_2 = Frame(self.root, bd=4, highlightbackground=self.colors.hgb_color, highlightthickness=3, background=self.colors.bg_color)
        self.frame_2.place(relx=0.02, rely=0.40, relwidth=0.96, relheight=0.56)

    ## Criação dos Widgets do Frame 1
    def criando_widgets_frame1(self):
        ##Botões
        self.btn_confirmar = Button(self.frame_1, text="Confirmar", bd=4, bg=self.colors.hgb_color, font=self.colors.fonte, command=self.confirmar, fg=self.colors.fg_green)
        self.btn_confirmar.place(relx=0.40, rely=0.85, relwidth=0.20, relheight=0.15)

        self.btn_outros = Button(self.frame_1, text="Outros", bd=4, bg=self.colors.hgb_color, font=self.colors.fonte, command=AppOpt, fg=self.colors.fg_green)
        self.btn_outros.place(relx=0.80, rely=0.85, relwidth=0.20, relheight=0.15)
        ##Labels
        self.lbl1 = Label(self.frame_1, text="PIX: ", font=self.colors.fonte, bd=4, highlightbackground=self.colors.hgb_color, highlightthickness=3, background=self.colors.background_color1, fg=self.colors.text_color)
        self.lbl1.place(relx=0.03, rely=0.03, relwidth=0.3)

        self.lbl2 = Label(self.frame_1, text="CAIXA: ", font=self.colors.fonte, bd=4, highlightbackground=self.colors.hgb_color, highlightthickness=3, background=self.colors.background_color1, fg=self.colors.text_color)
        self.lbl2.place(relx=0.03, rely=0.13, relwidth=0.3)

        self.lbl3 = Label(self.frame_1, text="TOTAL: ", font=self.colors.fonte, bd=4, highlightbackground=self.colors.hgb_color, highlightthickness=3, background=self.colors.background_color1, fg=self.colors.text_color)
        self.lbl3.place(relx=0.67, rely=0.03, relwidth=0.3)

        self.lbl_id = Label(self.frame_1, text="ID: ", font=self.colors.fonte, bd=4, highlightbackground=self.colors.hgb_color, highlightthickness=3, background=self.colors.background_color1, fg=self.colors.text_color)
        self.lbl_id.place(relx=0.67, rely=0.13, relwidth=0.3)

        self.lbl_paginas = Label(self.frame_1, text=f"", font=self.colors.fonte_small, bd=4, highlightbackground=self.colors.hgb_color, highlightthickness=3, background=self.colors.background_color1, fg=self.colors.text_color)
        self.lbl_paginas.place(relx=0.03, rely=0.85, relwidth=0.3)
        ##atualizar cabeçalho
        self.atualizarCabeca()
        ##Entry e Label da Entry
        self.entry_valor = Entry(self.frame_1, font=self.colors.fonte_entry, justify="center", bd=2, background=self.colors.background_color1, fg=self.colors.fg_green)
        self.entry_valor.place(relx=0.25, rely=0.30, relwidth=0.5, relheight=0.2)
        self.lbl4 = Label(self.frame_1, text="R$", font=self.colors.fonte, background=self.colors.background_color1, fg=self.colors.text_color)
        self.lbl4.place(relx=0.26, rely=0.31)
        ##Radiobuttons Pix e Caixa
        self.rd_opt = tkinter.IntVar(value=1)
        self.rd_caixa = Radiobutton(self.frame_1, text="CAIXA", variable=self.rd_opt, value=1, font=self.colors.fonte, background=self.colors.background_color1, fg=self.colors.text_color)
        self.rd_caixa.place(relx=0.25, rely=0.55, relwidth=0.5)
        self.rd_pix = Radiobutton(self.frame_1, text="PIX", variable=self.rd_opt, value=2, font=self.colors.fonte, background=self.colors.background_color1, fg=self.colors.text_color)
        self.rd_pix.place(relx=0.25, rely=0.65, relwidth=0.5)

    def tabela_frame2(self):

        style = ttk.Style()
        style.configure("Custom.Treeview", font=self.colors.fonte, foreground=self.colors.text_color)
        style.configure("Treeview.Heading", font=self.colors.fonte, background="#3c3f41", foreground=self.colors.text_color)
        ##Criação da tabela, especificado em qual frame ela é filha, o height, e as colunas
        self.tabela = ttk.Treeview(self.frame_2, height=3, columns=("id", "data", "forma", "total"))
        self.tabela.configure(style="Treeview")
        self.tabela.configure(style="Treeview.Heading")
        self.tabela.configure(style="Custom.Treeview")
        ##Heading, a criação do cabeçalho
        self.tabela.heading("#0", text="")
        self.tabela.heading("#1", text="Id", anchor="w")
        self.tabela.heading("#2", text="Data", anchor="w")
        self.tabela.heading("#3", text="Forma", anchor="w")
        self.tabela.heading("#4", text="Total", anchor="w")
        ##Alguns ajustes, CURIOSIDADE: essa tabela funciona como se "500" fosse 100%, ou seja, 200/500 = 0,4 que é 40%
        self.tabela.column("#0", width=1)
        self.tabela.column("#1", width=50)
        self.tabela.column("#2", width=200)
        self.tabela.column("#3", width=200)
        self.tabela.column("#4", width=100)
        self.tabela.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.95)
        ##Scroll da tabela
        self.scrollTabela = Scrollbar(self.frame_2, orient="vertical")
        self.tabela.configure(yscrollcommand=self.scrollTabela.set)
        self.scrollTabela.place(relx=0.97, rely=0.06, relwidth=0.02, relheight=0.90)
        ##DoubleClick
        # self.tabela.bind("<Double-1>", self.OnDoubleClick)

if __name__ == "__main__":
    Application()