from requests_html import HTMLSession

# Criando uma sessão do requests_html
session = HTMLSession()

# Fazendo uma solicitação GET para obter o conteúdo da página
response = session.get('http://192.168.0.254/#hId-pgUsageReport')

# Renderizando a página para executar scripts JavaScript
response.html.render()

# Executando JavaScript
script = 'console.log("Executando JavaScript!")'
response.html.render(script=script)

# Acessando o conteúdo da página renderizada
content = response.html.html
print(content)
