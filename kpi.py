import streamlit as st
import mysql.connector
import pandas as pd
import datetime
import matplotlib.pyplot as plt

#________________________________________________Inicio tela 1  página inicial_______________________________________
# Criando um Título Principal
st.header("SISTEMA DE CONTROLE E REGISTROS ADMINISTRATIVO")
st.sidebar.image('logo1.png', width=200)
st.sidebar.header("Menu de Navegação")
st.link_button("Sistema PETLOVE", url="https://petlove.streamlit.app/", icon="🌐")

# Criando um menu lateral
menu = ['Página Inicial', 'Registro KPI','Recebimento Veículo','Saída Veículo','Operação Extra','Base de Dados','Dashboard','Fale Conosco']
choice = st.sidebar.selectbox("Selecione uma opção", menu)

# Função para criar a tabela no banco de dados
def criar_tabela():
    conexao = mysql.connector.connect(
        host="solution_bi.mysql.dbaas.com.br",
        user="solution_bi",
        password="J3aQqCZ5j32Eq@",
        database="solution_bi",
        port=3306
    )
    cursor = conexao.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS KPI_Clientes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        data DATE,
        cliente VARCHAR(255),
        qtde_faturamento INT,
        volume_recebido DECIMAL(10, 2),
        volume_expedido DECIMAL(10, 2),
        qtde_expedido INT,
        qtde_recebido INT,
        qtde_veiculos INT,
        qtde_ocupacao INT,
        taxa_estoque VARCHAR(50)
    )
    """
    cursor.execute(query)
    conexao.commit()
    cursor.close()
    conexao.close()

# Chama a função para criar a tabela
criar_tabela()

# Página Home
if choice == 'Página Inicial':
    st.title("Bem-vindo ao 1º Sistema próprio de registros de dados de KPI's e recebimento de veículos da Solution Logistica")
    url = "https://www.youtube.com/watch?v=M-X7Z7TT_7M"
    st.video(url)
    st.markdown("""
    A Solution Log Movidos por ir mais longe!
                
    Buscar novas oportunidades, ampliar nossos horizontes e abrir novos caminhos, está em nossa razão de ser. 
    Começamos a contar a nossa história em 2009, com um olhar do futuro, focado no presente.
    """)
    st.image('sol1.png',width=1500)
    st.image('sol2.png',width=1500)
    st.text("2024 - Aplicação desenvolvida por: Williams Rodrigues - Analista de Dados e Logística Tel.: (82) 98863-9394")
    st.sidebar.text("""
Solution Logística
R. João Monteiro da Silva, 1600
Tabuleiro do Martins, 
Maceió - AL, 57081-780
(81) 99977-8488 
(81) 99203-3222
comercial@solution-log.com
http://solution-log.com
""")
    
 
    
#________________________________________________Inicio tela 2 Registro KPI_______________________________________    
# Página de Registro
if choice == 'Registro KPI':
    st.title("Preencha os campos abaixo com as informações da Operação 📝")
    st.sidebar.text("""
Solution Logística
R. João Monteiro da Silva, 1600
Tabuleiro do Martins, 
Maceió - AL, 57081-780
(81) 99977-8488 
(81) 99203-3222
comercial@solution-log.com
http://solution-log.com
""")
    # Formulário de entrada de dados
    data = st.date_input("Selecione a data")
    cliente = st.selectbox("Selecione o Cliente", ["Selecione um Cliente", "Melitta", "Dr. Oetker", "Cargill", "Santa Helena", "Fugini", "Peccin", "Wilson", "Dubar Bebidas", "EAF", "ASA","PetLove","Laborlog"])
    qtde_faturamento = st.number_input('Qtde Faturamento', min_value=0, max_value=1000, value=0, step=1)
    volume_recebido = st.text_input("Volume_Recebido(Ton)")
    volume_expedido = st.text_input("Volume_Expedido(Ton)")
    qtde_expedido = st.text_input("Qtde_Expedido(Cx)")
    qtde_recebido = st.text_input("Qtde_Recebida(Cx)")
    qtde_veiculos = st.number_input('Qtde Veículos Recebidos', min_value=0, max_value=1000, value=0, step=1)
    umidade=st.text_input("Umidade")
    temperatura=st.text_input("Temperatura")
    qtde_ocupacao = st.number_input('Qtde Ocupação')
    taxa_estoque = st.text_input("Taxa de Ocupação Estoque")
    taxa_acuracidade = st.text_input("Taxa de Acuracidade")
        # Botão para envio
    col1 = st.button("Enviar 📝")
        
    if col1:
        if cliente == "Selecione um Cliente":
            st.error("Por favor, selecione um cliente válido.")
        else:
            # Salvar os dados no banco de dados
            conexao = mysql.connector.connect(
                host="solution_bi.mysql.dbaas.com.br",
                user="solution_bi",
                password="J3aQqCZ5j32Eq@",
                database="solution_bi",
                port=3306
            )
            cursor = conexao.cursor()
            query = """
            INSERT INTO KPI_Clientes (
                data, cliente, qtde_faturamento, volume_recebido, volume_expedido,
                qtde_expedido, qtde_recebido, qtde_veiculos, qtde_ocupacao, taxa_estoque
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (
                data, cliente, qtde_faturamento, volume_recebido, volume_expedido,
                qtde_expedido, qtde_recebido, qtde_veiculos, qtde_ocupacao, taxa_estoque
            )
            cursor.execute(query, valores)
            conexao.commit()
            cursor.close()
            conexao.close()
            
            st.success("Os dados foram enviados com sucesso!")
            

# Página Base Dados
# Página Base Dados
# Configuração da conexão ao banco de dados
def obter_conexao():
    return mysql.connector.connect(
        host="solution_bi.mysql.dbaas.com.br",
        user="solution_bi",
        password="J3aQqCZ5j32Eq@",
        database="solution_bi",
        port=3306
    )
      
# Função para tratar valores None e atribuir um valor padrão
def tratar_valor(valor, tipo="string"):
    if valor is None:
        if tipo == "date":
            return datetime.date(1900, 1, 1)  # Data padrão
        elif tipo == "time":
            return datetime.time(0, 0)  # Hora padrão
        else:
            return ""  # String vazia para valores textuais
    return valor
#________________________________________________Inicio tela 3 Recebimento Veículo_______________________________________

if choice == 'Recebimento Veículo':  # Verifica se o usuário está na página de Recebimento Veículo
    st.sidebar.text("""Solution Logística
    R. João Monteiro da Silva, 1600
    Tabuleiro do Martins, 
    Maceió - AL, 57081-780
    (81) 99977-8488 
    (81) 99203-3222
    comercial@solution-log.com
    http://solution-log.com
    """)
      
    st.write("Filtrar por Número de nota fiscal:")
    nota_fiscal = st.text_input("Digite o Número da nota fiscal")

    if nota_fiscal:
        st.write("Número da nota fiscal:", nota_fiscal)

    try:
        # Configuração da conexão ao banco de dados
        conexao = obter_conexao()
        
        with conexao.cursor() as cursor:  # Gerenciamento automático do cursor
                        
            # Query segura com parâmetro
            query = "SELECT * FROM recebimento_veiculos WHERE nota_fiscal = %s"
            cursor.execute(query, (nota_fiscal,))
            resultados = cursor.fetchall()
            
            #Preencher as variáveis
            
            if resultados:
                for resultado in resultados:
                    nota_fiscal = tratar_valor(resultado[0], "string")
                    data_recebimento = tratar_valor(resultado[1], "date")
                    hora_recebimento = tratar_valor(resultado[2], "time")
                    recebedor = tratar_valor(resultado[3], "string")
                    cliente = tratar_valor(resultado[4], "string")
                    tipo_veiculo = tratar_valor(resultado[5], "string")
                    tipo_operacao = tratar_valor(resultado[6], "string")
                    ordem_chegada = tratar_valor(resultado[7], "string")
                    origem_saida = tratar_valor(resultado[8], "string")
                    nota_fiscal = tratar_valor(resultado[9], "string")
                    motorista = tratar_valor(resultado[10], "string")
                    tipo_documento = tratar_valor(resultado[11], "string")
                    contato = tratar_valor(resultado[12], "string")
                    placa_veiculo = tratar_valor(resultado[13], "string")
                    transportadora = tratar_valor(resultado[14], "string")
                   
                    
                    st.write("Recebedor:", cliente)  # Exemplo de exibição
                    # Adicione outros campos conforme necessário
            else:
                st.warning("Para Consultar uma NF, digite o Número da NF.")
    
    except Exception as e:
        st.error(f"Erro ao buscar os dados: {e}")
    
    finally:
        if conexao:
            conexao.close()


    # Controle de Recebimento de Veículos
    st.title("Controle de Recebimento de Veículos 🚚")
    data_recebimento = st.date_input("Data do Recebimento")
    hora_recebimento = st.time_input("Hora do Recebimento", value=datetime.time(20, 30))
    recebedor = st.text_input("Recebedor")
    cliente = st.selectbox("Selecione o Cliente", ["Selecione um Cliente", "Melitta", "Dr. Oetker", "Cargill", "Santa Helena", "Fugini", "Peccin", "Wilson", "Dubar Bebidas", "EAF", "ASA", "PetLove"])
    tipo_veiculo = st.selectbox("Tipo Veículo", ["Selecione um tipo", "Carreta", "Caminhão Truck", "Caminhão Toco", "Rodotrem", "Caminhão 3/4", "Mini Caminhão", "VAN", "Carro Passeio", "Outros Não Listado"])
    tipo_operacao = st.selectbox("Tipo Operação", ["Selecione um tipo", "Recebimento", "Expedição", "Recebimento Devolução", "Transf. Interna"])
    ordem_chegada = st.select_slider("Qual a ordem de chegada do veículo?", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30])
    origem_saida = st.text_input("Origem e Saída")
    nota_fiscal = st.text_input("Nota Fiscal")
    motorista = st.text_input("Nome do Motorista")
    tipo_documento = st.selectbox("Tipo de Documento", ["Selecione um tipo", "CNH", "Carteira de Motorista", "Passaporte", "Carteira de Trabalho", "Carteira de Identidade", "Outros"])
    documento = st.text_input("Documento")
    contato = st.text_input("Telefone Contato")
    placa_veiculo = st.text_input("Placa do Veículo")
    transportadora = st.text_input("Transportadora")

       # Botão para envio
    if st.button("Registrar Recebimento 📝"):
        # Estabelecendo a conexão
        conexao = mysql.connector.connect(
            host="solution_bi.mysql.dbaas.com.br",
            user="solution_bi",
            password="J3aQqCZ5j32Eq@",
            database="solution_bi",
            port=3306
        )

        # Função para criar a tabela no banco de dados
        def criar_tabela():
            cursor = conexao.cursor()
            # Query para criar a tabela (caso não exista)
            query = """
            CREATE TABLE IF NOT EXISTS recebimento_veiculos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                data_recebimento DATE,
                hora_recebimento TIME,
                recebedor VARCHAR(255),
                cliente VARCHAR(255),
                tipo_veiculo VARCHAR(255),
                tipo_operacao VARCHAR(255),
                ordem_chegada INT,
                origem_saida VARCHAR(255),
                nota_fiscal VARCHAR(255),
                motorista VARCHAR(255),
                tipo_documento VARCHAR(255),
                documento VARCHAR(255),
                contato VARCHAR(255),
                placa_veiculo VARCHAR(255),
                transportadora VARCHAR(255),
                registrar_saida VARCHAR(255),
                data_saida DATE,
                hora_saida TIME
            )
            """
            cursor.execute(query)
            conexao.commit()
            cursor.close()

        # Chama a função para criar a tabela (caso necessário)
        criar_tabela()

        # Query de inserção
        query = """
        INSERT INTO recebimento_veiculos (
            data_recebimento, hora_recebimento, recebedor, cliente, tipo_veiculo, tipo_operacao, ordem_chegada,
            origem_saida, nota_fiscal, motorista, tipo_documento, documento, contato, placa_veiculo, transportadora,
            registrar_saida, data_saida, hora_saida
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Definindo os valores a serem inseridos
        valores = (data_recebimento, hora_recebimento, recebedor, cliente, tipo_veiculo, tipo_operacao, ordem_chegada,
                  origem_saida, nota_fiscal, motorista, tipo_documento, documento, contato, placa_veiculo, transportadora,
                  )
        
        cursor = conexao.cursor()
        cursor.execute(query, valores)
        conexao.commit()
        cursor.close()

        st.success("Recebimento de veículo registrado com sucesso!")

def obter_conexao():
    try:
        conexao = mysql.connector.connect(
            host="solution_bi.mysql.dbaas.com.br",
            user="solution_bi",
            password="J3aQqCZ5j32Eq@",
            database="solution_bi"  # Substitua pelo nome correto do banco
        )
        return conexao
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para salvar dados no banco (se necessário)
def salvar_dados_kpi(conexao, data, cliente, qtde_faturamento, volume_recebido, volume_expedido,
                     qtde_expedido, qtde_recebido, qtde_veiculos, qtde_ocupacao, taxa_estoque):
    try:
        cursor = conexao.cursor()
        query = """
            INSERT INTO registro_kpi (data, cliente, qtde_faturamento, volume_recebido, volume_expedido,
                                       qtde_expedido, qtde_recebido, qtde_veiculos, qtde_ocupacao, taxa_estoque)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (data, cliente, qtde_faturamento, volume_recebido, volume_expedido,
                               qtde_expedido, qtde_recebido, qtde_veiculos, qtde_ocupacao, taxa_estoque))
        conexao.commit()
        st.success("Dados enviados com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar os dados: {e}")
    finally:
        cursor.close()
# ________________________________________________ Início tela 5 Formulário Saída de Veículos _______________________________________

# Função para obter a conexão com o banco de dados
def obter_conexao():
    try:
        return mysql.connector.connect(
            host="solution_bi.mysql.dbaas.com.br",
            user="solution_bi",
            password="J3aQqCZ5j32Eq@",
            database="solution_bi",
            port=3306
        )
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para criar a tabela de saída de veículos
def criar_tabela():
    conexao = obter_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS saida_veiculos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nota_fiscal VARCHAR(255),
                data_saida DATE,
                hora_saida TIME,
                responsavel VARCHAR(255)
            )
            """
            cursor.execute(query)
            conexao.commit()
        except Exception as e:
            st.error(f"Erro ao criar tabela: {e}")
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

# Função para registrar a saída de veículo
def registrar_saida(nota_fiscal, data_saida, hora_saida, responsavel):
    conexao = obter_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()
            query = """
            INSERT INTO saida_veiculos (nota_fiscal, data_saida, hora_saida, responsavel)
            VALUES (%s, %s, %s, %s)
            """
            values = (nota_fiscal, data_saida, hora_saida, responsavel)
            cursor.execute(query, values)
            conexao.commit()
        except Exception as e:
            st.error(f"Erro ao registrar saída: {e}")
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

# Tela de Saída de Veículo
if choice == "Saída Veículo":
    st.title("Registro de Saída e liberação de Veículos 🚛")
    nota_fiscal = st.text_input("Digite o Número da Nota Fiscal")
    data_saida = st.date_input("Data de Saída")
    hora_saida = st.time_input("Hora de Saída")
    responsavel = st.text_input("Responsável")

    if st.button("Registrar Saída"):
        if not nota_fiscal or not responsavel:
            st.error("Por favor, preencha todos os campos obrigatórios.")
        else:
            criar_tabela()  # Garantir que a tabela exista
            registrar_saida(nota_fiscal, data_saida, hora_saida, responsavel)
            st.success("Saída de veículo registrada com sucesso!")
 
# ________________________________________________ Início tela 5 Operação Extras _______________________________________
# Função para obter a conexão com o banco de dados
def obter_conexao():
    try:
        return mysql.connector.connect(
            host="solution_bi.mysql.dbaas.com.br",
            user="solution_bi",
            password="J3aQqCZ5j32Eq@",  # Use variável de ambiente para senha
            database="solution_bi",
            port=3306
        )
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para criar a tabela
def criar_tabela_operacao_extra():
    conexao = obter_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS operacao_extra (
                id INT AUTO_INCREMENT PRIMARY KEY,
                data_operacao DATE NOT NULL,
                cliente VARCHAR(255) NOT NULL,
                local VARCHAR(255) NOT NULL,
                turno VARCHAR(255) NOT NULL,
                tipo_operacao VARCHAR(255) NOT NULL,
                valor_operacao FLOAT,
                observacoes TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(query)
            conexao.commit()
        except Exception as e:
            st.error(f"Erro ao criar tabela: {e}")
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

# Função para registrar os dados
def registrar_operacao_extra(data, cliente, local, turno, tipo, valor, observacoes):
    conexao = obter_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()
            query = """
            INSERT INTO operacao_extra (data_operacao, cliente, local, turno, tipo_operacao, valor_operacao, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores = (data, cliente, local, turno, tipo, valor, observacoes)
            cursor.execute(query, valores)
            conexao.commit()
            st.success("Operação registrada com sucesso.")
        except Exception as e:
            st.error(f"Erro ao registrar operação: {e}")
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

if choice == "Operação Extra":
    st.title("Tela de Operação Extra ⚙️")
    st.sidebar.text("""Solution Logística
    R. João Monteiro da Silva, 1600
    Tabuleiro do Martins, 
    Maceió - AL, 57081-780
    (81) 99977-8488 
    (81) 99203-3222
    comercial@solution-log.com
    http://solution-log.com
    """)

    data_operacao = st.date_input("Data operação", value=datetime.date.today())
    cliente = st.selectbox("Cliente", ["Selecione um cliente", "Melitta", "Dr. Oetker", "Cargill", "Santa Helena", "Fugini", "Peccin", "Wilson", "Dubar Bebidas", "EAF", "ASA", "Laborlog", "PetLove"])
    local = st.selectbox("Centro de Distribuição", ["Selecione um Local", "CD 01", "CD 02", "CD 03", "CD 04", "Recife"])
    turno = st.selectbox("Turno", ["Selecione um Turno","Manhã e Noite", "Matutino", "Vespertino", "Noturno"])
    tipo_operacao = st.selectbox("Tipo de Operação", ['Selecione um tipo', 'Administrativa', 'Recebimento e Expedição','Expedição', 'Recebimento', 'Recebimento Devolução', 'Transf. Interna', 'Inventário', 'Organização Estoque', 'Limpeza Armazém', 'Outros'])
    valor_operacao = st.text_input("R$ Valor da Operação", "R$ 0,00")
    observacoes = st.text_input("Observações")

    if st.button("Registrar Operação Extra"):
        if cliente != "Selecione um cliente" and local != "Selecione um Local" and turno != "Selecione um Turno" and tipo_operacao != "Selecione um tipo":
            registrar_operacao_extra(data_operacao, cliente, local, turno, tipo_operacao, valor_operacao, observacoes)
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")

    criar_tabela_operacao_extra()
 
# ________________________________________________ Início tela 6 tabelas downloads _______________________________________

if choice == "Base de Dados":
    st.title("Tabelas de Registros e Dados para Acompanhamentos 📊" )
    st.sidebar.text("""Solution Logística
    R. João Monteiro da Silva, 1600
    Tabuleiro do Martins, 
    Maceió - AL, 57081-780
    (81) 99977-8488 
    (81) 99203-3222
    comercial@solution-log.com
    http://solution-log.com
    """)
  

    # Função para criar a conexão com o banco
    def obter_conexao():
        try:
            conexao = mysql.connector.connect(
                host="solution_bi.mysql.dbaas.com.br",  # Atualize com suas credenciais
                user="solution_bi",
                password="J3aQqCZ5j32Eq@",
                database="solution_bi",  # Certifique-se de usar o nome correto do banco
                port=3306
            )
            return conexao
        except Exception as e:
            st.error(f"Erro ao conectar ao banco de dados: {e}")
            return None

    # Exibindo tabela de registro KPI       
    def KPI_Clientes():
        conexao = obter_conexao()   
        if conexao:
            try:
                # Consultando os dados
                query = "SELECT * FROM KPI_Clientes"
                df_registro_kpi = pd.read_sql_query(query, conexao)           
                # Exibindo os dados
                st.write("Registros de KPI:")
                st.dataframe(df_registro_kpi)
                # Contagem total de registros
                st.write("Total de Registros:", len(df_registro_kpi))
            except Exception as e:
                st.error(f"Erro ao carregar os dados: {e}")
            finally:
                # Fechando a conexão
                if conexao.is_connected():
                    conexao.close()

    # Função para exibir o DataFrame de recebimento de veículos
    def recebimento_veiculos():
        conexao = obter_conexao()
        if conexao:
            try:
                # Consultando os dados
                query = "SELECT * FROM recebimento_veiculos"
                df_veiculos = pd.read_sql_query(query, conexao)
                # Exibindo os dados
                st.write("Registros de Recebimento de Veículos:")
                st.dataframe(df_veiculos)
                # Contagem total de registros
                st.write("Total de Registros:", len(df_veiculos))
            except Exception as e:
                st.error(f"Erro ao carregar os dados: {e}")
            finally:
                # Fechando a conexão
                if conexao.is_connected():
                    conexao.close()


    # Chamar as funções para exibir as tabelas
    st.write("_________________________________________________________________________________________")
    KPI_Clientes()
    st.write("_________________________________________________________________________________________")
    recebimento_veiculos()
  
# ________________________________________________ Início tela 7 Gráficos  _______________________________________
    
if choice == "Dashboard":
    st.title("Dashboard de KPI 📊 📈")
    st.sidebar.text("""Solution Logística
    R. João Monteiro da Silva, 1600
    Tabuleiro do Martins, 
    Maceício - AL, 57081-780
    (81) 99977-8488 
    (81) 99203-3222
    comercial@solution-log.com
    http://solution-log.com
    """)
  
# Gráfico de linhas de KPI em Matplotlib
    # Configuração da conexão ao banco de dados
    conexao = obter_conexao()
    if conexao: 
        try:
            # Consultando os dados
            query = "SELECT * FROM KPI_Clientes"
            df_registro_kpi = pd.read_sql_query(query, conexao)
           
            # Exibindo os dados
            st.write("Registros de KPI:")
            st.dataframe(df_registro_kpi)
            # Contagem total de registros
            st.write("Total de Registros:", len(df_registro_kpi))
        except Exception as e:
            st.error(f"Erro ao carregar os dados: {e}")
        finally:
            # Fechando a conexão
            if conexao.is_connected():
                conexao.close() 

    # Gráfico de barras de KPI em Matplotlib
    st.write('Qtde de Veículos Recebidos por Cliente')
    grafico1=st.bar_chart(df_registro_kpi, x='cliente', y='qtde_veiculos', width=500, height=300, use_container_width=True,color='#e63946')
    st.write('Taxa de Estoque por Cliente')
    grafico2=st.bar_chart(df_registro_kpi, x='cliente', y='taxa_estoque', width=500, height=300, use_container_width=True,color='#2a9d8f')

    # Criando um gráfico de média da taxa de estoque para cada cliente gráfico KPI
    st.write('Taxa de Estoque por Cliente')
    grfico3=st.line_chart(df_registro_kpi, x='cliente', y='taxa_estoque', width=500, height=300, use_container_width=True,color='#e63946')
   

# ________________________________________________ Início tela 8 Fale Conosco _______________________________________

# Função para obter a conexão com o banco de dados
def obter_conexao():
    try:
        return mysql.connector.connect(
            host="solution_bi.mysql.dbaas.com.br",
            user="solution_bi",
            password="J3aQqCZ5j32Eq@",
            database="solution_bi",
            port=3306
        )
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para criar a tabela de contato
def criar_tabela_contato():
    conexao = obter_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()
            query = """
                CREATE TABLE IF NOT EXISTS fale_conosco (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(255),
                    email VARCHAR(255),
                    telefone_contato VARCHAR(255),
                    assunto VARCHAR(255),
                    mensagem TEXT,
                    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            cursor.execute(query)
            conexao.commit()
        except Exception as e:
            st.error(f"Erro ao criar tabela: {e}")
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

# Função para salvar os dados no banco
def salvar_contato(nome, email, telefone, assunto, mensagem):
    conexao = obter_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()
            query = """
                INSERT INTO fale_conosco (nome, email, telefone_contato, assunto, mensagem)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (nome, email, telefone, assunto, mensagem)
            cursor.execute(query, values)
            conexao.commit()
            st.success("Mensagem enviada com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar a mensagem: {e}")
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

# Tela "Fale Conosco"
if choice == "Fale Conosco":
    st.title("Fale conosco, sobre dúvidas, sugestões ou Reclamações  💬")
    st.sidebar.text("""Solution Logística
    R. João Monteiro da Silva, 1600
    Tabuleiro do Martins,
    Maceió - AL, 57081-780
    (81) 99977-8488
    (81) 99203-3222
    comercial@solution-log.com
    http://solution-log.com
    """)

    # Criar tabela de contato (executado uma única vez)
    criar_tabela_contato()

    # Formulário
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    telefone = st.text_input("Telefone de Contato")
    assunto = st.selectbox("Assunto", ['Selecione um Assunto', 'Sugestão', 'Dúvida', 'Reclamação', 'Outro'])
    mensagem = st.text_area("Mensagem")

    if st.button("Enviar"):
        st.rerun()
  
    if not nome or not email or not telefone or not assunto or not mensagem:
            st.error("Por favor, preencha todos os campos.")
    else:
            salvar_contato(nome, email, telefone, assunto, mensagem)
   
    st.markdown("""
---
**Sistema Desenvolvido por:**  
**Williams Rodrigues**  
📊 Analista de Dados e Logística  
📞 **Telefone:** (82) 98863-9394 / 98109-0042 
📧 **E-mail:** dateanalytics@outlook.com  
🌐 **Website:** [Linkedin](https://www.linkedin.com/in/williams-rodrigues-9b350a6a?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app )  
""")

#________________________________________________________________ FIM DO Programa __________________________________________________________________
