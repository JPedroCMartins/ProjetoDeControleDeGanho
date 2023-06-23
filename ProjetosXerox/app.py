import os
import time
from tkinter import *
from tkinter import font
from tkinter import ttk
from janelas import janelaCaixa
from banco import banco

class janelaPrincipal():
    def __init__(self):
        def caixa():
            root.destroy()
            janelaCaixa.openWindow()

        root = Tk()
        root.title("Janela de Apoio")

        #Geometria---------------
        largura_janela = 500
        altura_janela = 300

        largura_tela = root.winfo_screenwidth()
        altura_tela = root.winfo_screenheight()

        pos_x = (largura_tela - largura_janela) // 2
        pos_y = (altura_tela - altura_janela) // 2

        root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        #------------------------

        frm = ttk.Frame(root)
        frm.grid()

        btn_prjtCaixa = ttk.Button(frm, text="Projeto Caixa", command=caixa)
        btn_prjtCaixa.grid(column=0, row=0)

        root.mainloop()
if __name__ == "__main__":
    banco.criarBnc()
    janelaPrincipal()