import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    print('Obtendo dados...')
    ENDEREÇO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(ENDEREÇO_DADOS, sep = ';', encoding = 'iso-8859-1')
    df_estelionato = df_ocorrencias[['mes_ano', 'estelionato']]
    df_estelionato = df_estelionato.groupby('mes_ano', as_index = False)['estelionato'].sum()
    df_estelionato = df_estelionato.sort_values(by = 'estelionato', ascending = False)

except Exception as e:
    print(f'Erro ao acessar dados: {e}')

try:
    print("Calculndo medidas...")
    array_estelionato = np.array(df_estelionato['estelionato'])
    media_estelionato = np.mean(array_estelionato)
    mediana_estelionato = np.median(array_estelionato)
    q1 = np.quantile(array_estelionato, .25)
    q3 = np.quantile(array_estelionato, .75)
    distancia = abs(media_estelionato - mediana_estelionato / mediana_estelionato) / 100

    # intervalo interquartil
    iqr = q3 - q1
    limite_inferior = q1 - (1.5 * iqr)
    limite_superior = q3 + (1.5 * iqr)

    df_estelionato_maiores = df_estelionato[df_estelionato['estelionato'] > q3]
    df_estelionato_menores= df_estelionato[df_estelionato['estelionato'] < q1]

    # outliers
    df_estelionato_outliers_superiores = df_estelionato[df_estelionato['estelionato'] > limite_superior]
    df_estelionato_outliers_inferiores = df_estelionato[df_estelionato['estelionato'] < limite_inferior]

    print('\nPeriodos de Estelionatos')
    print(50 * '=')
    print(f'\nPeriodo com maiores registros acima de Q3: {df_estelionato_maiores.sort_values(by = 'estelionato', ascending = False)}')
    print(f'\nPeriodo com menores registros abaixo de Q1: {df_estelionato_menores.sort_values(by = 'estelionato', ascending = True)}')   

    print('\nObtendo padrões')
    print(50 * '=')
    print(f'\nMedia: {media_estelionato:.2f}')
    print(f'Mediana: {mediana_estelionato}')
    print(f'Assimetria da média: {distancia:.2f}%')

    print(f'\nObtendo comportamentos destuantes')
    print('Número acima do comportamento')
    print(df_estelionato_outliers_superiores.sort_values(by = 'estelionato', ascending = False))
    
    print('Número abaixo do comportamento')
    print(df_estelionato_outliers_inferiores.sort_values(by = 'estelionato', ascending = False))

    print(limite_inferior)
except Exception as e:
    print(f'Erro ao calcular medidas: {e}')

try:
    plt.figure(figsize=(18, 8))
    plt.subplots(2, 1)
    plt.subplot(2, 1, 1)
    plt.boxplot(array_estelionato, vert = False, showmeans = True) # vert = ativa ou desativa posição vertical, showmeans = ativa ou desativa mostrar media

    plt.subplot(2, 1, 2)
    plt.text(0.1, 0.9, f'Média: {media_estelionato}')
    plt.text(0.1, 0.8, f'Mediana: {mediana_estelionato}')
    plt.text(0.1, 0.7, f'Distancia: {distancia}')
    plt.text(0.1, 0.6, f'IQR: {iqr}')
    plt.text(0.1, 0.5, f'Limite Superior: {limite_superior}')
    plt.text(0.1, 0.4, f'Limite Inferior: {limite_inferior}')



    plt.show()

except Exception as e:
    print(f'Erro ao plotar gráfico: {e}')