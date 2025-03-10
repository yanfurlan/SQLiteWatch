import sqlite3
import os
import time
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Caminho do diretório e do banco de dados
DB_FOLDER = r"PASTA"
DB_PATH = os.path.join(DB_FOLDER, "monitoring.db")

# Criar a pasta "monitoring" caso não exista
os.makedirs(DB_FOLDER, exist_ok=True)

def create_database():
    """Cria o banco de dados SQLite e a tabela de logs se não existirem."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            # Criar tabela de logs
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS query_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT,
                    execution_time REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Criar tabela de exemplo para monitoramento
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    email TEXT
                )
            ''')

            # Criar Trigger para registrar consultas em todas as tabelas (INSERT, UPDATE, DELETE)
            cursor.execute('''
                CREATE TRIGGER IF NOT EXISTS log_insert_usuarios AFTER INSERT ON usuarios
                BEGIN
                    INSERT INTO query_logs (query, execution_time) 
                    VALUES ('INSERT INTO usuarios', 0);
                END;
            ''')

            cursor.execute('''
                CREATE TRIGGER IF NOT EXISTS log_update_usuarios AFTER UPDATE ON usuarios
                BEGIN
                    INSERT INTO query_logs (query, execution_time) 
                    VALUES ('UPDATE usuarios', 0);
                END;
            ''')

            cursor.execute('''
                CREATE TRIGGER IF NOT EXISTS log_delete_usuarios AFTER DELETE ON usuarios
                BEGIN
                    INSERT INTO query_logs (query, execution_time) 
                    VALUES ('DELETE FROM usuarios', 0);
                END;
            ''')

            conn.commit()
        print(f"Banco de dados criado com sucesso em: {DB_PATH}")
    except sqlite3.Error as e:
        print(f"Erro ao criar o banco de dados: {e}")

def log_query(query, execution_time):
    """Registra a consulta e o tempo de execução no banco de dados."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('PRAGMA busy_timeout = 5000')  # Aumenta o tempo de espera para 5 segundos
            cursor = conn.cursor()
            cursor.execute("INSERT INTO query_logs (query, execution_time) VALUES (?, ?)", (query, execution_time))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao registrar o log da consulta: {e}")

def execute_query(query):
    """Executa a consulta e registra o tempo de execução."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('PRAGMA busy_timeout = 5000')  # Aumenta o tempo de espera para 5 segundos
            cursor = conn.cursor()

            start_time = time.time()
            cursor.execute(query)
            conn.commit()
            execution_time = time.time() - start_time

            # Registrar a consulta SELECT manualmente
            log_query(query, execution_time)

            # Verificar se a consulta é um SELECT e retornar os resultados
            if query.strip().upper().startswith("SELECT"):
                return execution_time, cursor.fetchall()
            return execution_time, []
    except sqlite3.Error as e:
        print(f"Erro ao executar a consulta: {e}")
        return None, []

def analyze_database():
    """Obtém estatísticas básicas do banco de dados."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            # Estatísticas do banco
            cursor.execute("PRAGMA page_count;")
            page_count = cursor.fetchone()[0]
            cursor.execute("PRAGMA page_size;")
            page_size = cursor.fetchone()[0]

        return {"page_count": page_count, "page_size": page_size}
    except sqlite3.Error as e:
        print(f"Erro ao analisar o banco de dados: {e}")
        return {}

def clear_logs():
    """Limpa os logs de consulta do banco de dados."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM query_logs")
            conn.commit()
        print("Logs limpos com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao limpar os logs: {e}")

def display_paginated_results(df):
    """Exibe os resultados paginados."""
    if len(df) == 0:
        st.write("Nenhum log de consulta encontrado.")
        return
    
    results_per_page = 10
    total_results = len(df)
    total_pages = (total_results // results_per_page) + (1 if total_results % results_per_page != 0 else 0)

    if total_pages > 1:
        page = st.slider("Escolha a página", 1, total_pages, 1)
        start_idx = (page - 1) * results_per_page
        end_idx = start_idx + results_per_page
    else:
        page = 1
        start_idx = 0
        end_idx = total_results

    st.write(f"Mostrando resultados da página {page} de {total_pages}")
    st.dataframe(df[start_idx:end_idx])

def show_dashboard():
    """Exibe o dashboard no Streamlit."""
    st.title("SQLite Monitor Dashboard")

    try:
        # Conectar ao banco de dados
        with sqlite3.connect(DB_PATH) as conn:
            # Listar todas as tabelas no banco de dados
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tabelas = cursor.fetchall()

            if len(tabelas) == 0:
                st.write("Não há tabelas no banco de dados.")
            else:
                for tabela in tabelas:
                    tabela_nome = tabela[0]
                    st.write(f"### Tabela: {tabela_nome}")
                    
                    # Consultar os dados da tabela
                    query = f"SELECT * FROM {tabela_nome}"
                    df = pd.read_sql(query, conn)
                    
                    if df.empty:
                        st.write("Nenhum dado encontrado.")
                    else:
                        st.write(f"Mostrando dados da tabela {tabela_nome}")
                        display_paginated_results(df)

        stats = analyze_database()
        st.write("### Estatísticas do Banco de Dados")
        st.json(stats)

        # Gráficos de tempo de execução
        st.write("### Gráfico de Tempo de Execução das Consultas")
        with sqlite3.connect(DB_PATH) as conn:
            query_times = pd.read_sql("SELECT timestamp, execution_time FROM query_logs", conn)

        if len(query_times) > 0:
            fig, ax = plt.subplots()
            ax.plot(query_times['timestamp'], query_times['execution_time'], marker='o', linestyle='-', color='b')
            ax.set_xlabel("Timestamp")
            ax.set_ylabel("Tempo de Execução (segundos)")
            ax.set_title("Tempo de Execução das Consultas")
            plt.xticks(rotation=45)
            st.pyplot(fig)
    except sqlite3.Error as e:
        print(f"Erro ao exibir o dashboard: {e}")

if __name__ == "__main__":
    create_database()

    st.sidebar.title("Monitoramento de SQLite")
    opcao = st.sidebar.selectbox("Escolha uma opção", ["Executar Query", "Visualizar Dashboard", "Limpar Log"])

    if opcao == "Executar Query":
        query = st.text_area("Digite sua query")
        if st.button("Executar"):
            tempo_execucao, resultados = execute_query(query)
            if tempo_execucao is not None:
                st.success(f"Query executada em {tempo_execucao:.4f} segundos")
                if resultados:
                    st.write("### Resultados da Consulta")
                    st.dataframe(resultados)
                else:
                    st.write("Nenhum resultado encontrado ou comando de escrita executado.")

    elif opcao == "Visualizar Dashboard":
        show_dashboard()

    elif opcao == "Limpar Log":
        limpar = st.radio("Você deseja limpar os logs de consulta?", ("Não", "Sim"))
        if limpar == "Sim":
            if st.button("Confirmar Limpeza"):
                clear_logs()
                st.success("Logs limpos com sucesso.")
        else:
            st.write("Logs não foram limpos.")

