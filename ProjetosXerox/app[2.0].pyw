import threading

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from ttkthemes import ThemedStyle
from selenium import webdriver
from datetime import datetime
from tkinter import ttk
import multiprocessing
from tkinter import *
import sqlite3
import tkinter
import time
import csv

#Classe para as funções da aplicação
class Funcs():
    total: float
    # Função do botão confirmar
    def __init__(self):
        self.lbl1 = None
        self.lbl2 = None
        self.lbl3 = None
        self.lbl_id = None
        self.tabela = None
        self.forma = None
        self.rd_opt = None
        self.data = None
        self.cursor = None
        self.conn = None
        self.entry_valor = None

    def confirmar(self):
        self.add_valores()
        self.select_tabela()
        self.atualizarCabeca()
        self.entry_valor.delete(0, END)
        thread = threading.Thread(target=self.atLabel)
        thread.start()

    # Integração com banco de dados
    def conectaDB(self):
        self.conn = sqlite3.connect("banco.db")
        self.cursor = self.conn.cursor()

    # Integração com banco de dados
    def desconectaDB(self):
        self.conn.close()

    # Função importante: ela cria o banco
    def MontaTabela(self):
        self.conectaDB()
        sql_code = '''CREATE TABLE IF NOT EXISTS banco_clientes ( id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT NOT 
        NULL, forma TEXT NOT NULL, total TEXT NOT NULL)'''
        self.cursor.execute(sql_code)
        self.conn.commit()
        self.desconectaDB()

    # Função para adicionar os valores no banco, chamado na função confirmar()
    def add_valores(self):
        data_atual = datetime.now()
        data_formatada = data_atual.strftime("%d/%m/%y - %H:%M:%S")
        self.data = data_formatada
        # self.data = data_atual
        self.forma = self.rd_opt.get()
        if self.forma == 1:
            self.forma = "CAIXA"
        elif self.forma == 2:
            self.forma = "PIX"
        total_str = str(self.entry_valor.get())
        total_str = total_str.replace(",", ".")
        self.total = float(total_str)
        self.conectaDB()
        sql_code = f"INSERT INTO banco_clientes (data, forma, total) " \
                   f"VALUES ('{self.data}', '{self.forma}', '{self.total}')"
        self.cursor.execute(sql_code)
        self.conn.commit()
        self.desconectaDB()

    # Função que Atualiza a tabela
    def select_tabela(self):
        self.tabela.delete(*self.tabela.get_children())
        self.conectaDB()
        lista = self.cursor.execute("""SELECT id, data, forma, total FROM banco_clientes""")
        for i in lista:
            nome_com_prefixo = "R$ " + i[3]
            self.tabela.insert("", tkinter.END, text="", values=(i[0], i[1], i[2], nome_com_prefixo))
            self.tabela.see(self.tabela.get_children()[-1])
        self.desconectaDB()

    # Função que faz a soma dos valores do banco, chamada em atualizarCabeca()
    def soma(self, p_ou_c):
        if p_ou_c == "p":
            self.forma = "PIX"
        elif p_ou_c == "c":
            self.forma = "CAIXA"
        self.conectaDB()
        sql_code = f"SELECT SUM(total) FROM banco_clientes WHERE forma = '{self.forma}'"
        self.cursor.execute(sql_code)
        resultado = self.cursor.fetchone()[0]
        self.desconectaDB()
        try:
            resultado = float(resultado)
            return resultado
        except:
            resultado = 0
            return resultado

    def maiorId(self):
        self.conectaDB()
        self.cursor.execute('SELECT MAX(id) FROM banco_clientes')
        maior_id = self.cursor.fetchone()[0]
        self.desconectaDB()
        try:
            res = int(maior_id)
            return res
        except:
            return 0

    # def deleta_linha(self):
    #    self.conectaDB()
    #    self.cursor.execute("""DELETE FROM banco_cliente WHERE id = ?""", (self.id))
    #    self.desconectaDB()
    #    self.valor_entry.delete(0, END)
    # def OnDoubleClick(self, event):
    #    self.entry_valor.delete(0, END)
    #    self.tabela.selection()
    #    for n in self.tabela.selection():
    #        col1, col2, col3, col4 = self.tabela.item(n, 'values')
    #        self.entry_valor.insert(END, col4)
    # Função que atualiza as informações do cabeçalho

    def opt_table(self):
        time.sleep(0.5)
        self.conectaDB()
        # Recupere a lista de tabelas no banco de dados
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = self.cursor.fetchall()

        # Exporte cada tabela para um arquivo CSV
        for tabela in tabelas:
            nome_tabela = tabela[0]
            nome_arquivo = f'{nome_tabela}.csv'

            # Recupere os dados da tabela
            self.cursor.execute(f"SELECT * FROM {nome_tabela};")
            dados = self.cursor.fetchall()

            # Escreva os dados no arquivo CSV
            with open(nome_arquivo, 'w', newline='') as arquivo_csv:
                writer = csv.writer(arquivo_csv)
                writer.writerows(dados)

        # Feche a conexão com o banco de dados
        self.desconectaDB()
        self.lbl_plan_status.config(text="Tabela Criada!")
        time.sleep(1)

    def atualizarCabeca(self):
        try:
            valor_total_pix = self.soma("p")
            valor_total_caixa = self.soma("c")
            valor_bruto_total = float(valor_total_pix) + float(valor_total_caixa)
            id = self.maiorId() + 1
            self.lbl1.config(text=f"Pix: R$ {valor_total_pix}")
            self.lbl2.config(text=f"Caixa: R$ {valor_total_caixa}")
            self.lbl3.config(text=f"Total: R$ {valor_bruto_total}")
            self.lbl_id.config(text=f"ID: {id}")

        except():
            print("Sem Valor")

    def selenium(self):
        try:
            options = Options()
            options.add_argument("--headless")
            options.log.level = "FATAL"

            self.driver = webdriver.Firefox(options=options)
            self.driver.get("http://192.168.0.254/#hId-pgUsageReport")
            time.sleep(3)
            element = self.driver.find_element(By.XPATH, '//*[@id="appUsageReport-ti"]')
            time.sleep(0.5)
            self.paginas = int(element.text)
            self.driver.quit()
            print("webdriver[FECHADO]")
            print(f"paginas[{self.paginas}]")
        except:
            self.paginas = 1
            self.driver.quit()

    def atLabel(self):
        # Zerado dia 5 de Julho
        self.selenium()
        self.pg = self.paginas - 16620
        self.vlr = self.pg * 0.50
        self.lbl_paginas['text'] = f"Valor em Real de:\nImpressões tiradas: R$ {self.vlr}"

class Colors:
    def __init__(self):
        self.theme = "classic"
        self.background_color = "#3c3f41"
        self.background_color1 = "#2b2b2b"
        self.fonte = ("verdana", 14, 'bold')
        self.fonte_small = ("verdana", 9, "italic")
        self.fonte_entry = ("verdana", 26, 'bold')
        self.hgb_color = "#323232"
        self.fg_green = "green"
        self.bg_color = "#3c3f41"
        self.text_color = "#747a80"
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

        self.lbl_plan_status = Label(self.opt_root, text="STATUS", font=self.colors.fonte, bd=4, highlightbackground=self.colors.hgb_color, highlightthickness=3, background=self.colors.background_color1, fg=self.colors.text_color)
        self.lbl_plan_status.place(relx = 0.58, rely=0.05, relwidth=0.40, relheight=0.05)
# Função Principal da Aplicação
class Application(Funcs):
    def __init__(self):
        ##IMPORTANTE: todas as funções criadas devem ser chamadas em ordem e antes do mainloop()
        super().__init__()
        root = Tk()
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