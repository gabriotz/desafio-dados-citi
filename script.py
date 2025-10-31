import pandas as pd
import numpy as np

def carregar_dados(caminho_arquivo):
    #abrir arquivo dos dados
    try:
        df = pd.read_csv(caminho_arquivo)
        print(f"Arquivo {caminho_arquivo} carregado com sucesso.")
        return df
    except FileNotFoundError:
        print(f"ERRO: Arquivo {caminho_arquivo} não encontrado.")
        print("Certifique-se de que o script está na mesma pasta que o CSV.")
        return None

def tratar_senioridade(df):
    #Padronizar a senerioridade
    print("Iniciando Etapa 1: Padronizar Nivel_Senioridade...")
    
    # Dicionário para mapear variações
    mapa_senioridade = {
        'Jr': 'Júnior',
        'JR': 'Júnior',
        'P': 'Pleno',
        'pleno': 'Pleno',
        'senior': 'Sênior'
        
    }
    
    # Aplica o mapeamento
    df['Nivel_Senioridade'] = df['Nivel_Senioridade'].replace(mapa_senioridade)
    
    # Substitui 'N/D' por um valor nulo padrão (NaN)
    df['Nivel_Senioridade'] = df['Nivel_Senioridade'].replace('N/D', np.nan)
    
    moda_senioridade = df['Nivel_Senioridade'].mode()[0]
    
    df['Nivel_Senioridade'].fillna(moda_senioridade, inplace=True)
    
    return df

def tratar_avaliacoes(df):
    print("Iniciando Etapa 2: Padronizar Avaliações...")

    df['Avaliacao_Tecnica'] = pd.to_numeric(df['Avaliacao_Tecnica'], errors='coerce')
    df['Avaliacao_Comportamental'] = pd.to_numeric(df['Avaliacao_Comportamental'], errors='coerce')

    media_tecnica = df['Avaliacao_Tecnica'].mean()
    df['Avaliacao_Tecnica'].fillna(media_tecnica, inplace=True)
    
    media_comportamental = df['Avaliacao_Comportamental'].mean()
    df['Avaliacao_Comportamental'].fillna(media_comportamental, inplace=True)
    
    return df

def tratar_engajamento(df):
    print("Iniciando Etapa 3: Tratar Engajamento_PIGs...")
    
    df['Engajamento_PIGs'] = df['Engajamento_PIGs'].replace('$N/A^{\prime}', np.nan)
    
    # Limpa o '%' e converte para numérico
    df['Engajamento_PIGs'] = df['Engajamento_PIGs'].str.replace('%', '', regex=False)
    df['Engajamento_PIGs'] = pd.to_numeric(df['Engajamento_PIGs'], errors='coerce')
    df['Engajamento_PIGs'] = df['Engajamento_PIGs'] / 100
    
    media_engajamento = df['Engajamento_PIGs'].mean()
    
    df['Engajamento_PIGs'].fillna(media_engajamento, inplace=True)
    
    return df

def criar_colunas_calculadas(df):
    print("Iniciando Etapa 4: Calcular Score_Desempenho...")
    
    df['Score_Desempenho'] = (df['Avaliacao_Tecnica'] * 0.5) + (df['Avaliacao_Comportamental'] * 0.5)
    
    print("Iniciando Etapa 5: Criar Status_Membro...")
    
    condicao_destaque = (df['Score_Desempenho'] >= 7.0) & (df['Engajamento_PIGs'] >= 0.8)
    
    df['Status_Membro'] = np.where(condicao_destaque, 'Em Destaque', 'Padrão')
    
    return df

def salvar_arquivos_finais(df):
    print("Salvando arquivos finais...")
    
    df.to_csv('Base_Membros_Tratada.csv', index=False, decimal=',', sep=';')
    
    df.to_excel('Base_Membros_Tratada.xlsx', index=False)
    
    print("Arquivos 'Base_Membros_Tratada.csv' e 'Base_Membros_Tratada.xlsx' gerados com sucesso.")


if __name__ == "__main__":
    
    arquivo_entrada = 'dados/Base_Membros_Desempenho - Base_Membros_Desempenho.csv'
    
    df_dados = carregar_dados(arquivo_entrada)
    
    if df_dados is not None:
        df_tratado = tratar_senioridade(df_dados)
        df_tratado = tratar_avaliacoes(df_tratado)
        df_tratado = tratar_engajamento(df_tratado)
        df_tratado = criar_colunas_calculadas(df_tratado)
        
        # Salva os arquivos
        salvar_arquivos_finais(df_tratado)