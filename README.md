
# SQLite Monitor Dashboard

Este projeto é uma aplicação de monitoramento para banco de dados SQLite, com o objetivo de registrar e analisar o desempenho das consultas executadas. Ele utiliza **Streamlit** para criar uma interface web onde você pode:

- Executar consultas SQL diretamente no banco de dados.
- Visualizar logs de consultas realizadas, com informações sobre o tempo de execução.
- Analisar estatísticas do banco de dados, como número de páginas e tamanho das páginas.
- Gerar gráficos sobre o tempo de execução das consultas.

## Funcionalidades

1. **Executar Consultas SQL**
   - Você pode executar consultas SQL diretamente na aplicação. As consultas são registradas no banco de dados, incluindo o tempo de execução, permitindo o acompanhamento de performance.

2. **Visualizar Logs de Consultas**
   - O sistema registra todas as consultas realizadas, incluindo comandos `INSERT`, `UPDATE` e `DELETE` nas tabelas monitoradas. Estes logs podem ser visualizados na interface de maneira paginada.

3. **Análise do Banco de Dados**
   - O banco de dados fornece informações sobre seu tamanho e número de páginas, além de registrar estatísticas sobre o desempenho das consultas.

4. **Gráficos de Performance**
   - A aplicação gera gráficos sobre o tempo de execução das consultas, ajudando a identificar possíveis gargalos no banco de dados.

## Tecnologias Usadas

- **Python**: Linguagem de programação principal.
- **SQLite**: Banco de dados utilizado para armazenar os logs e as tabelas.
- **Streamlit**: Framework para criação da interface web interativa.
- **Matplotlib**: Biblioteca para geração de gráficos.

## Requisitos

Antes de rodar o projeto, certifique-se de ter o seguinte instalado:

- Python 3.x
- SQLite (geralmente já incluso com o Python)
- Streamlit (`pip install streamlit`)
- Pandas (`pip install pandas`)
- Matplotlib (`pip install matplotlib`)

## Instalação

1. Clone este repositório para o seu ambiente local:

   ```bash
   git clone <https://github.com/yanfurlan/SQLiteWatch>
   ```

2. Instale as dependências necessárias:

   ```bash
   pip install -r requirements.txt
   ```

## Como Usar

1. **Executar o Banco de Dados:**
   - O banco de dados será automaticamente criado na primeira execução, junto com a tabela de logs e a tabela de exemplo.

2. **Executar a Aplicação:**
   - Execute o Streamlit com o comando:

     ```bash
     streamlit run app.py
     ```

3. **Interagir com o Dashboard:**
   - Abra o navegador e acesse o URL fornecido pelo Streamlit (geralmente `http://localhost:8501`).
   - No painel lateral, você pode escolher entre:
     - **Executar Query**: Inserir e executar suas consultas SQL.
     - **Visualizar Dashboard**: Visualizar os dados das tabelas, logs de consultas e gráficos de performance.
     - **Limpar Log**: Limpar os logs de consulta registrados no banco de dados.

## Estrutura do Projeto

```
/monitoring
    /monitoring.db           # Banco de dados SQLite
    app.py                   # Código principal do Streamlit
    requirements.txt         # Arquivo de dependências
```

## Considerações Finais

Este projeto tem como objetivo facilitar o monitoramento e análise de consultas SQL em um banco de dados SQLite. Ele permite que você visualize o desempenho do banco de dados e otimize suas consultas.

Se você encontrar algum erro ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.
