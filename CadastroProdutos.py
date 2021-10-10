from PyQt5 import uic,QtWidgets
import mysql.connector
from mysql.connector import cursor
from reportlab.pdfgen import canvas

banco = mysql.connector.connect(
    host='localhost',
    user='root', 
    password='', 
    database='bancopython'
)

Form, formulario = uic.loadUiType("formulario.ui")

def funcao_principal(self):

    print("Apertei o botao")
    codigo = formulario.lineCodigo.text()
    descricao = formulario.lineDescricao.text()
    preco = formulario.linePreco.text()

    categoria = ""

    if formulario.radioInformatica.isChecked():
        print ("CATEGORIA INFORMÁTICA FOI SELECIONADA!")
        categoria = "Informatica"
    if formulario.radioAlimentos.isChecked():
        print ("CATEGORIA ALIMENTOS FOI SELECIONADA!")
        categoria = "Alimentos"
    elif formulario.radioEletronicos.isChecked():
        print ("CATEGORIA ELETRONICOS FOI SELECIONADA!")
        categoria = "Eletronicos"
    
    print("CODIGO: ", codigo)
    print("DESCRICAO: ", descricao)
    print("PRECO: ", preco)
    
    cursor = banco.cursor()
    cadastro_SQL = "INSERT INTO produtos (CODIGO, DESCRICAO, PRECO ,CATEGORIA) VALUES (%s,%s,%s,%s)"
    dados = (str(codigo), str(descricao), str(preco), categoria)
    cursor.execute(cadastro_SQL,dados)
    banco.commit()

    formulario.lineCodigo.setText("")
    formulario.lineDescricao.setText("")
    formulario.linePreco.setText("")

def listar_produtos():

    listar_dados.show()
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    listar_dados.tableProdutos.setRowCount(len(dados_lidos))
    listar_dados.tableProdutos.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0,5):
            listar_dados.tableProdutos.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def gerar_pdf():

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    y = 0

    pdf = canvas.Canvas("CadastroDeProdutos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200,800, "Produtos Cadastrados:")
    pdf.setFont("Times-Bold", 15)

    pdf.drawString(0,725 -y, str("_" * 100))
    pdf.drawString(10,700, "ID")
    pdf.drawString(50,700, "|")
    pdf.drawString(90,700, "CODIGO")
    pdf.drawString(170,700, "|")
    pdf.drawString(210,700, "PRODUTO")
    pdf.drawString(330,700, "|")
    pdf.drawString(370,700, "PREÇO")
    pdf.drawString(450,700, "|")
    pdf.drawString(490,700, "CATEGORIA")
    pdf.drawString(0,695 -y, str("_" * 100))

    for i in range(0, len(dados_lidos)):
        y = y + 30
        pdf.drawString(10,700 -y, str(dados_lidos[i][0]))
        pdf.drawString(50,700 -y, "|")
        pdf.drawString(90,700 -y, str(dados_lidos[i][1]))
        pdf.drawString(170,700 -y, "|")
        pdf.drawString(210,700 -y, str(dados_lidos[i][2]))
        pdf.drawString(330,700 -y, "|")
        pdf.drawString(370,700 -y, "R$")
        pdf.drawString(395,700 -y, str(dados_lidos[i][3]))
        pdf.drawString(450,700 -y, "|")
        pdf.drawString(490,700 -y, str(dados_lidos[i][4]))
        pdf.drawString(0,695 -y, str("_" * 100))

    pdf.save()
    print("PDF FOI GERADO COM SUCESSO")

def excluir_produto():
    linha = listar_dados.tableProdutos.currentRow()
    listar_dados.tableProdutos.removeRow(linha)
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    print(valor_id)
    cursor.execute("DELETE FROM produtos WHERE ID="+str(valor_id))
    banco.commit()

app = QtWidgets.QApplication([])
formulario = uic.loadUi("formulario.ui")
listar_dados = uic.loadUi("Listar_Dados.ui")
formulario.btnEnviar.clicked.connect(funcao_principal)
formulario.btnListar.clicked.connect(listar_produtos)
listar_dados.btnPDF.clicked.connect(gerar_pdf)
listar_dados.btnExcluir.clicked.connect(excluir_produto)


formulario.show()
app.exec()