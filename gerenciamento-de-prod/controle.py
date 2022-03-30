from PyQt5 import uic,QtWidgets # ler o uic e torna visivel pelo qtwidgets 
import mysql.connector 
#import sqlite3
from reportlab.pdfgen import canvas # gerar pdf

numero_id = 0 #variavel criada para ser usada como global 

#banco = sqlite3.connect 


banco = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='cadastro_produtos'
) 
# O comando cursor vai ser muito usado para manipular o banco de dados




def funcao_principal():
    linha1 = formulario.lineCod.text()
    linha2 = formulario.lineProd.text()
    linha3 = formulario.lineQuant.text()

    categoria='' #definir a categoria como vazia pois sera selecioanda pelo usuario mais de uma opcao
    
    if formulario.radioButton_rede.isChecked() : #selecniona o nome da categoria por meio do botao
        print("Categoria Rede  selecionada")
        categoria = 'Rede'

    elif formulario.radioButton_material.isChecked() :
        print("Categoria Material :) selecionada")
        categoria = 'Material'

    else :
        print("Categoria Outros:) selecionada")
        categoria = 'Outros :)'

    print("Codigo:",linha1)
    print("Produto:",linha2)
    print("Quantidade",linha3) 


    #trecho de codigo sql
    cursor = banco.cursor() #nao esquecer 'banco' eh a instancia definida por mim para o mysql.connector
    comando_SQL = 'INSERT INTO produtos (codigo,produto,quantidade,categoria) values (%s,%s,%s,%s)'
    dados = (str(linha1),str(linha2),str(linha3),categoria,) #aqui é o que vai ser ecrito inde tem a "%s"
    cursor.execute(comando_SQL,dados)
    banco.commit()
    formulario.lineCod.setText('') #Essa função é vazia para que apos o botao de enviar for selecionado o campo ficar limpo
    formulario.lineProd.setText('')
    formulario.lineQuant.setText('')




def chama_segunda_tela():  #direcinar à segunda pagina
    segunda_tela.show()    #carrega a tela

    cursor = banco.cursor()
    comando_SQL = 'select * from produtos'
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall() #ele vai pegar o q foi feito na ultima linha do cursor


    segunda_tela.tableWidget.setRowCount(len(dados_lidos)) #lista || setRowCount eh o comando pars q a contagem da lista aconteça e apareça na tela a quantidade certa da quantidade de produtos
    segunda_tela.tableWidget.setColumnCount(5) #colunas || setColumnCount eh o comando para aparecer as colunas
    # "segunda_tela.tableWidget" seleciona o tablwidgts que tem na segunda tela, tablewigets pode ser redefinido o nome no qt designer
    #setRowCount vai determinar as linhas q a tabela vai ter passando como parametro com o len todos os dados lidos

    #Agora para que possa ser mostrado na tela o conteudi da lista:
    for i in range (0, len(dados_lidos)): #ele vai de 0 ate a quantidade de listas q a tabela possuir
        for j in range (0,5): #vai de 0 a 5 pq o tamanho de colunas eh fixo
            segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))  #colocou str antes para converter tudo em string uma vez q ele so aceita string




def editar_dados():
    global numero_id
    linha = segunda_tela.tableWidget.currentRow() #qual linha o usuario selecionou       
    
    cursor = banco.cursor() #entrar no banco de dados
    cursor.execute("SELECT id FROM produtos") #executa o id no banco de dados para selecionar onde sera editado
    dados_lidos = cursor.fetchall() #variaval para salvar todos os id uma vez que o cursor anteriormente foi executado apenas ao id
    valor_id = dados_lidos[linha][0] 
    cursor.execute("SELECT * FROM produtos WHERE id="+str(valor_id)) #Ele seleciona todos os segmentos do id no banco de dados
    produto = cursor.fetchall() #retornar todos os produtos
    tela_editar.show() #mostra a tela

    numero_id = valor_id  #a variavel global vai pegar o numero selecionado para que na hora de editar possa ser salvo

    tela_editar.lineEdit_ID.setText(str(produto[0][0]))
    tela_editar.lineEdit_Cod.setText(str(produto[0][1]))
    tela_editar.lineEdit_Prod.setText(str(produto[0][2]))
    tela_editar.lineEdit_Quant.setText(str(produto[0][3]))
    tela_editar.lineEdit_Categ.setText(str(produto[0][4]))  



def salvar_dados_editados():
    global numero_id #pega o numero do id
    
    #Valor digitado no LineEdit
    codigo = tela_editar.lineEdit_Cod.text()
    produto = tela_editar.lineEdit_Prod.text()
    quantidade = tela_editar.lineEdit_Quant.text()
    categoria = tela_editar.lineEdit_Categ.text()

    # atualizar os dados no banco    
    cursor = banco.cursor() 
    cursor.execute("UPDATE produtos SET codigo = '{}', produto = '{}', quantidade = '{}', categoria ='{}' WHERE id = {}".format(codigo,produto,quantidade,categoria,numero_id))
    banco.commit()
    #atualizar as janelas 

    tela_editar.close() #vai fechar a janela apois salvar a edição
    segunda_tela.close() 
    chama_segunda_tela() #essa função vai carregar a sengunda tela novamente ja atualizada



def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow() #metodo para selecionar qual linha o usuario selecionou       
    segunda_tela.tableWidget.removeRow(linha) #metodo para remover a linha no grafico visual || dentro dos () coloca onde vai ser removido
    
    cursor = banco.cursor() #entrar no banco de dados
    cursor.execute("SELECT id FROM produtos") #executa o id no banco de dados para selecionar onde sera exluido
    dados_lidos = cursor.fetchall() #variaval para salvar todos os id uma vez que o cursor anteriormente foi executado apenas ao id
    valor_id = dados_lidos[linha][0] #coloca 0 pois tem uma virgula depois do id quando roda no terminal aqui 
    cursor.execute("DELETE FROM produtos WHERE id =" + str(valor_id)) #aqui deleta do banco de dados




def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = 'select * from produtos' #ler os dados do banco
    cursor.execute(comando_SQL) #executa no banco de dados 
    dados_lidos = cursor.fetchall() #salva os dados na variavel dados_lidos
    y=0 #variavel q vai usar no pdf
    pdf = canvas.Canvas('cadastro_produtos.pdf') #nome do arquivo q ele vai gerar
    pdf.setFont('Times-Bold', 25) # Definir a fonte do titulo que vem a segui:
    pdf.drawString(200,800,'Produtos Cadastrados:') # esse 200 eh o tamanho da distancia lateral e o 800 a distancia veertical
    
    pdf.setFont('Times-Bold', 10) # diminuo a fonte para os dados a seguir:

    pdf.drawString(10, 750, 'ID')  #750 eh o valor imutavel pois eh reerente as colunas
    pdf.drawString(110, 750, 'CODIGO')
    pdf.drawString(210, 750, 'PRODUTO')
    pdf.drawString(310, 750, 'QUANTIDADE') 
    pdf.drawString(510, 750, 'CATEGORIA')

    for i in range (0, len(dados_lidos)): #o i aqui sera o valor das listas
        y = y + 50 #a variavel y definida como 0 para ser encrementada para quando escrever os dados pule uma linha
        pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410, 750 - y, str(dados_lidos[i][4]))


    pdf.save()
    print ('PDF FOI GERADO COM SUCESSO')  




#            COMANDO PARA DEFINIR O NOME FORMULARIO E SEGUNDA TELA LIGANDO ELAS PARA SUAS RESPECITVAS PAGINAS 


app=QtWidgets.QApplication([]) 
formulario=uic.loadUi("formulario2.ui") #esse comando loadUid é para importar a tela do formulario
segunda_tela=uic.loadUi("listar_dados.ui") #esse comando loadUid é para importar a segunda tela
tela_editar=uic.loadUi("editar_produto.ui") #tela_editar estara recebendo a terceira tela

#                            COMANDO BOTÃO 

formulario.btn_enviar.clicked.connect(funcao_principal) #comando para o botao de enviar, ele carrega tudo q ta no def da função principal
formulario.btn_lista.clicked.connect(chama_segunda_tela) #comando para o botao de lista e ele vai chamar a segunda tela pelo def
segunda_tela.btn_pdf.clicked.connect(gerar_pdf) #Botao de gerar pdf
segunda_tela.btn_excluir.clicked.connect(excluir_dados) #Botao de excluir
segunda_tela.btn_edit.clicked.connect(editar_dados) #Botao de editar
tela_editar.btn_salvar.clicked.connect(salvar_dados_editados) #Botao de salvar na 3 tela


formulario.show() #a função show vai ser usado pra carregar a tela de formulario
app.exec()





'''
BANCO DE DADOS UTILIZADO:

create database cadastro_produtos;  
use cadastro_produtos;

create table produtos(
id INT NOT NULL AUTO_INCREMENT,
codigo int,
produto varchar(50),
quantidade int,
categoria varchar(20),
PRIMARY KEY (id)
);  

describe produtos;

select * from produtos;


SITE PRA VISUALIZAR :

localhost/phpmyadmin/
''' 

