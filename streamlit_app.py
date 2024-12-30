import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os


def Resultado(dados):
    #st.subheader("Planilha de Resultados")
    DataFrame = st.dataframe(dados)
    dados = dados.to_csv()
    Mensagem = st.write("Clique no Botão abaixo e faça o Download do arquivo")
    Botao = st.download_button( label="Planilha de Resultados",file_name='Resultado.csv', data = dados)
    return DataFrame,Mensagem,Botao
# Função para verificar e resetar os dados se for um novo mês
def verificar_resetar_planilha():
    try:
        # Carregar as transações existentes
        df = pd.read_csv("transacoes.csv")
        
        # Verificar o mês da última transação
        df['Data'] = pd.to_datetime(df['Data'])
        ultimo_mes = df['Data'].max().month
        
        # Obter o mês atual
        mes_atual = datetime.datetime.now().month
        
        # Se o mês atual for diferente do último mês registrado, resetar a planilha
        if ultimo_mes != mes_atual:
            st.warning("Novo mês detectado. Resetando os dados.")
            # Resetar a planilha (apagar o conteúdo e manter o cabeçalho)
            df = pd.DataFrame(columns=["Tipo", "Categoria", "Valor", "Descrição", "Data"])
            df.to_csv("transacoes.csv", index=False)
            return df
        return df
    except FileNotFoundError:
        # Caso o arquivo não exista, criamos o DataFrame vazio
        df = pd.DataFrame(columns=["Tipo", "Categoria", "Valor", "Descrição", "Data"])
        df.to_csv("transacoes.csv", index=False)
        return df

# Título do aplicativo
st.title("Controle de Gastos e Receitas")

# Solicitar nível do usuário
nivel = st.selectbox("Selecione a opção:", ("Entrada", "Saída"))

# Criar uma lista de categorias para entradas (incluindo salário) e saídas
categorias_entrada = ["Salário", "Renda Extra"]
categorias_saida = ["Alimentação", "Transporte", "Saúde", "Lazer", "Outros"]

# Função para adicionar uma nova entrada ou saída
def adicionar_transacao(tipo, categoria, valor, descricao, data):
    # Carregar ou resetar o DataFrame
    df = verificar_resetar_planilha()
    
    # Adicionar a nova transação ao DataFrame
    nova_transacao = {
        "Tipo": tipo,
        "Categoria": categoria,
        "Valor": valor,
        "Descrição": descricao,
        "Data": data,
    }
    df = df.append(nova_transacao, ignore_index=True)

    # Salvar as transações de volta no arquivo CSV
    df.to_csv("transacoes.csv", index=False)

    return df

# Se o nível selecionado for "Entrada" (Receita)
if nivel == "Entrada":
    st.subheader("Adicionar Receita")

    categoria = st.selectbox("Categoria da Receita", categorias_entrada)
    valor = st.number_input("Valor da Receita", min_value=0.01, format="%.2f")
    descricao = st.text_input("Descrição da Receita")
    data = st.date_input("Data da Receita", value=datetime.date.today())

    if st.button("Adicionar Receita"):
        if valor > 0 and descricao:
            df = adicionar_transacao("Entrada", categoria, valor, descricao, data)
            st.success("Receita adicionada com sucesso!")
            st.write(df)  # Exibir as transações atualizadas
        else:
            st.error("Por favor, preencha todos os campos corretamente!")

# Se o nível selecionado for "Saída" (Despesa)
if nivel == "Saída":
    st.subheader("Adicionar Despesa")

    categoria = st.selectbox("Categoria da Despesa", categorias_saida)
    valor = st.number_input("Valor da Despesa", min_value=0.01, format="%.2f")
    descricao = st.text_input("Descrição da Despesa")
    data = st.date_input("Data da Despesa", value=datetime.date.today())

    if st.button("Adicionar Despesa"):
        if valor > 0 and descricao:
            df = adicionar_transacao("Saída", categoria, valor, descricao, data)
            st.success("Despesa adicionada com sucesso!")
            st.write(df)  # Exibir as transações atualizadas
        else:
            st.error("Por favor, preencha todos os campos corretamente!")

# Exibir os dados
st.subheader("Histórico de Transações")
df = verificar_resetar_planilha()  # Verifica e retorna a planilha atualizada
#st.write(df)
Resultado(df)

# Calcular o saldo (entradas - saídas)
if not df.empty:
    # Somar as receitas (entradas)
    df_receitas = df[df["Tipo"] == "Entrada"]
    total_receitas = df_receitas["Valor"].sum()

    # Somar as despesas (saídas)
    df_despesas = df[df["Tipo"] == "Saída"]
    total_despesas = df_despesas["Valor"].sum()

    saldo = total_receitas - total_despesas
    st.subheader("Resumo Financeiro")
    st.write(f"Total de Receitas: R${total_receitas:,.2f}")
    st.write(f"Total de Despesas: R${total_despesas:,.2f}")
    st.write(f"Saldo: R${saldo:,.2f}")

# Gráficos para visualizar as transações
if not df.empty:
    st.subheader("Visualização Gráfica")
    tipo_grafico = st.radio("Escolha o tipo de gráfico", ("Pizza", "Barra"))
    
    if tipo_grafico == "Pizza":
        df_entradas = df[df["Tipo"] == "Entrada"]
        df_saidas = df[df["Tipo"] == "Saída"]
        df_categoria_entradas = df_entradas.groupby("Categoria")["Valor"].sum()
        df_categoria_saidas = df_saidas.groupby("Categoria")["Valor"].sum()
        
        # Gráfico para entradas
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        df_categoria_entradas.plot.pie(autopct="%1.1f%%", ax=ax[0], title="Entradas")
        df_categoria_saidas.plot.pie(autopct="%1.1f%%", ax=ax[1], title="Saídas")
        st.pyplot(fig)
    
    elif tipo_grafico == "Barra":
        df_entradas = df[df["Tipo"] == "Entrada"]
        df_saidas = df[df["Tipo"] == "Saída"]
        df_categoria_entradas = df_entradas.groupby("Categoria")["Valor"].sum()
        df_categoria_saidas = df_saidas.groupby("Categoria")["Valor"].sum()
        
        # Gráfico de barras para entradas e saídas
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        ax[0].bar(df_categoria_entradas.index, df_categoria_entradas.values)
        ax[0].set_title("Entradas")
        ax[1].bar(df_categoria_saidas.index, df_categoria_saidas.values)
        ax[1].set_title("Saídas")
        st.pyplot(fig)
