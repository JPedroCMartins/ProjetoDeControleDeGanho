import sqlite3

def criarBnc():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()

    sql_code = '''CREATE TABLE IF NOT EXISTS banco_clientes ( id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT NOT NULL, forma TEXT NOT NULL, total TEXT NOT NULL)'''

    cursor.execute(sql_code)

def ver():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()

    sql_code = "SELECT * FROM banco_clientes"
    cursor.execute(sql_code)

    dados = cursor.fetchall()
    #for row in dados:
    #    print(row)
    return dados

def add(data, forma, total):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()

    sql_code = f"INSERT INTO banco_clientes (data, forma, total) VALUES ('{data}', '{forma}', '{total}')"

    cursor.execute(sql_code)

    conn.commit()
    cursor.close()
    conn.close()

def soma(p_ou_c):
    if p_ou_c == "p":
        forma = "PIX"
    elif p_ou_c == "c":
        forma = "CAIXA"



    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()

    sql_code = f"SELECT SUM(total) FROM banco_clientes WHERE forma = '{forma}'"
    cursor.execute(sql_code)

    resultado = cursor.fetchone()[0]

    try:
        resultado = float(resultado)
        return resultado
    except:
        resultado = 0
        return resultado

if __name__ == "__main__":
    criarBnc()