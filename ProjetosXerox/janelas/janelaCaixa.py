import tkinter
from tkinter import ttk
from tkinter import *
from datetime import datetime
from banco import banco

data_atual = datetime.now()
data_formatada = data_atual.strftime("%d/%m/%y")
class openWindow():
    def __init__(self):
        def test():
            data_atual = datetime.now()
            data_formatada = data_atual.strftime("%d/%m/%y")

            modo = var_opcao.get()
            if modo == 1:
                modo = "PIX"
            elif modo == 2:
                modo = "CAIXA"

            i = "X"
            try:
                total = float(txt1.get())
            except:
                string = str(txt1.get())
                string = string.replace(",", ".")
                total = float(string)

            banco.add(data_formatada, modo, str(total))
            atualizarCabeca()
            atualizarTree()
            txt1.delete(0, tkinter.END)

        def atualizarCabeca():
            try:
                valor_total_pix = banco.soma("p")
                valor_total_caixa = banco.soma("c")
                valor_bruto_total = float(valor_total_pix) + float(valor_total_caixa)
                lbl1.config(text=f"Valor Caixa: R$ {valor_total_caixa}")
                lbl2.config(text=f"Valor Pix: R$ {valor_total_pix}")
                lbl3.config(text=f"Valor Total: R$ {valor_bruto_total}")
            except:
                print("Sem Valor")

        def atualizarTree():
            tabela.delete(*tabela.get_children())
            dados = banco.ver()

            for linha in dados:
                nome_com_prefixo = "R$ " + linha[3]
                tabela.insert("", tkinter.END, text=linha[0], values=(linha[0], linha[1], linha[2], nome_com_prefixo))
                tabela.see(tabela.get_children()[-1])

        root = Tk()
        root.title("Caixa")
        # Geometria---------------
        largura_janela = 768
        altura_janela = 1366

        #largura_tela = root.winfo_screenwidth()
        #altura_tela = root.winfo_screenheight()

        #pos_x = (largura_tela - largura_janela) // 2
        #pos_y = (altura_tela - altura_janela) // 2

        root.geometry(f"{largura_janela}x{altura_janela}")
        # ------------------------

        frm = ttk.Frame(root, padding=10)
        frm.place(relx=0.01, rely=0.01, relheight=1, relwidth=1)

        valor_total_pix = banco.soma("p")
        valor_total_caixa = banco.soma("c")

        valor_bruto_total = int(valor_total_pix) + int(valor_total_caixa)

        lbl1 = ttk.Label(frm, text=f"Valor Caixa: R$ {valor_total_caixa}", font = ('verdana', 16, 'bold'))
        lbl1.place(relx=0.05, rely=0.01)

        lbl2 = ttk.Label(frm, text=f"Valor Pix: R$ {valor_total_pix}", font = ('verdana', 16, 'bold'))
        lbl2.place(relx=0.05, rely=0.03)

        lbl3 = ttk.Label(frm, text=f"Valor Total: R$ {valor_bruto_total}", font = ('verdana', 16, 'bold'))
        lbl3.place(relx=0.05, rely=0.05)

        txt1 = ttk.Entry(frm, font = ('verdana', 55, 'bold'), width=12, justify='center')
        txt1.place(relx=0.05, rely=0.10)

        lbl4 = ttk.Label(frm, text=f"R$", font=('verdana', 16, 'bold'))
        lbl4.place(relx=0.05, rely=0.125)

        var_opcao = tkinter.IntVar(value=2)


        style = ttk.Style()
        style.configure("Custom.TRadiobutton", font = ('verdana', 22), indicatorsize=50, indicatormargin=25)
        style.configure("Custom.TButton", font = ('verdana', 22))


        rd_pix = ttk.Radiobutton(frm, text="PIX", variable=var_opcao, value=1, style="Custom.TRadiobutton")
        rd_pix.place(relx=0.05, rely=0.20)

        rd_caixa = ttk.Radiobutton(frm, text="CAIXA", variable=var_opcao, value=2, style="Custom.TRadiobutton")
        rd_caixa.place(relx=0.20, rely=0.20)

        btn1 = ttk.Button(frm, text="Confirmar", command=test, style="Custom.TButton")
        btn1.place(relx=0.62, rely=0.23)


        tabela = ttk.Treeview(frm)
        scrollbar = ttk.Scrollbar(frm, orient="vertical", command=tabela.yview)
        scrollbar.pack(side="right", fill="y")

        tabela["columns"] = ("id", "Data", "Forma", "TOTAL")
        tabela.column("#0", width=0, stretch=tkinter.NO)
        tabela.column("id", width=50, stretch=tkinter.NO)
        tabela.column("Data", width=200, stretch=tkinter.NO)
        tabela.column("Forma", width=200, stretch=tkinter.NO)
        tabela.column("TOTAL", width=150, stretch=tkinter.NO)

        tabela.configure(yscrollcommand=scrollbar.set)

        tabela.heading("#0", text="")
        tabela.heading("id", text="Id")
        tabela.heading("Data", text="Data")
        tabela.heading("Forma", text="Forma de Pagamento")
        tabela.heading("TOTAL", text="Total")

        atualizarTree()

        tabela.place(relx=0.05, rely=0.30, relwidth=0.85, relheight=0.60)

        root.mainloop()



if __name__ == "__main__":
    banco.criarBnc()
    #banco.add("00/00/00", "PIX", "0")
    #banco.soma("c")
    openWindow()
