import threading
import time
import csv
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
import sqlite3
from tkinter import *
import tkinter

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
        thread = threading.Thread(target=self.webstatus_impressora)
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
            self.paginas = "NaN"
            self.driver.quit()

    def webstatus_impressora(self):
        # Zerado dia 5 de Julho
        self.selenium()
        try:
            self.pg = self.paginas - 16620
            self.vlr = self.pg * 0.50
            self.lbl_paginas['text'] = f"Valor em Real de:\nImpressões tiradas: R$ {self.vlr}"
        except:
            self.lbl_paginas['text'] = f"Erro:\nServidor Web \nEmbutido da Impressora"
