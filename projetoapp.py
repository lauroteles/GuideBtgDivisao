import pandas as pd
import streamlit as st
import numpy as np
import altair as alt
from PIL import Image
import plotly as opx
import io
import openpyxl as op
import xlsxwriter
from xlsxwriter import Workbook


opcoes_de_abas = 'BTG','Guide'
selecionar = st.selectbox('Selecione a corretora', opcoes_de_abas)

if selecionar == 'BTG':


    df = None
    daf=None
    daf2=None

    st.sidebar.image("images.jpg")

    def le_excel(x):
        x+='.xlsx'
        df=pd.read_excel(x)
        return df

    ###     Upload files direct in streamlit


    upload_file = st.sidebar.file_uploader(
                            label='Solte o arquivo de PL',
                            type=['xlsx'],
                            key='upload1'
                            )


    if upload_file  is not None:
        
        print('hello')
        try:
            df = pd.read_excel(upload_file)
        except Exception as e:
            st.write(f'Faltando arquivos:{e}')

    ####    arquivo 2


    upload_file2 = st.sidebar.file_uploader(
                            label='Solte o arquivo de SALDO',
                            type=['xlsx'],
                            key='upload2'
                            )

    if upload_file2  is not None:
        print('hello')
        try:
            daf = pd.read_excel(upload_file2)
        except Exception as e:
            st.write(f'Faltando arquivos:{e}')
    
    ##### arquivo 3 
    

    upload_file3 = st.sidebar.file_uploader(
                            label='Solte o arquivo da planilha de CONTROLE',
                            type=['xlsx'],
                            key='upload3'
                            )



    if upload_file  is not None:
        print('hello')
        try:
            daf2 = pd.read_excel(upload_file3)
        except Exception as e:
            st.write(f'Faltando arquivos:{e}')  


    if df is not None and daf is not None and daf2 is not None:


        pl = df
        saldo = daf
        controle = daf2


        #####       Limpando arquivo e retirando colunas

        pl = pl.drop(columns='NOME')
        saldo = saldo.drop(columns='NOME')

        
        controle =  controle.iloc[:,[1,2,6,12,16,17,18]]
        
        
        controle = controle.rename(columns = {'Unnamed: 2':'CONTA'})

        controle = controle.rename(columns= 
                                            {'Mesa de Operação':'Operador'})

        ####        Mesclando arquivos e adicionando variaveis

        juncao = pd.merge(pl,saldo,
                        how='outer',
                            on= 'CONTA')
        # Filtros para adicionar operadores

        filtro_nov1 =  juncao.SALDO> 1000
        filtro_nov2 = juncao.SALDO < 0
        
        juncao = juncao.loc[(
            filtro_nov1|filtro_nov2
            )]


        ###         Adicionando 00 para mesclar os arquivos ###
        controle['CONTA']=controle['CONTA'].astype(str)


        controle['CONTA'] = list(
            map(
                lambda x:'00'+ x,controle['CONTA']
                )
                    )


        arquivo_final = pd.merge(
            controle,juncao,
            on='CONTA',
            how= 'outer'
        )
            ####        Mesclando arquivos e adicionando variaveis

        # Filtros para adicionar operadores
        #Filtro Breno
        filtro = arquivo_final.VALOR<100000
        filtro1 = arquivo_final.Operador == 'Edu'
        
        arquivo_filtro_breno = arquivo_final.loc[filtro&filtro1]
        arquivo_filtro_breno['Operador'] = arquivo_filtro_breno['Operador'].str.replace('Edu','Breno')
        #Filtro Edu
        filtro2 = arquivo_final.VALOR>100000
        filtro3 = arquivo_final.Operador == 'Edu'
        
        arquivo_filtro_edu = arquivo_final.loc[filtro2&filtro3]
        #filtro Bruno
        filtro4 = arquivo_final.VALOR<100000
        filtro5 = arquivo_final.Operador == 'Léo'
        
        arquivo_filtro_bruno = arquivo_final.loc[filtro4&filtro5]
        arquivo_filtro_bruno['Operador'] = arquivo_filtro_bruno['Operador'].str.replace('Léo','Bruno')
        #Filtro Léo
        filtro6 = arquivo_final.VALOR>100000
        filtro7 = arquivo_final.Operador == 'Léo'
        
        arquivo_filtro_leo = arquivo_final.loc[filtro6&filtro7]

        lista_concat = [
            arquivo_filtro_edu,
            arquivo_filtro_bruno,
            arquivo_filtro_breno,
            arquivo_filtro_leo
        ]

        def concat(lista):
            df = pd.concat(lista)
            return df
        
        arquivo_final2 = concat(lista_concat)
        
        
        #### Criando funcao para alterar o nome dos operardores de acordo com criterios #### 


        arquivo_final2['SALDO'].astype(int)
        arquivo_final2 = arquivo_final2.reset_index()
        
        arquivo_final2 = arquivo_final2.sort_values(by='SALDO',ascending=False)
        
        arquivo_final2 = arquivo_final2.rename(columns=
                                            {'Mesa de Operação.2':'Lembretes Mesa'})

        arquivo_final2 = arquivo_final2.rename(columns=
                                            {'VALOR':'PL Total'})
        arquivo_final2 = arquivo_final2.rename(columns=
                                            {'Saldo':'Saldo Disponivel'})
        arquivo_final2 = arquivo_final2.rename(columns=
                                            {'Unnamed: 1':'Nome'})
        #>>>>25/10
        arquivo_final2 = arquivo_final2.rename(columns=
                                            {'Unnamed: 12':'Perfil da Carteira'})
        arquivo_final2 = arquivo_final2.iloc[:,[2,1,9,4,5,6,7,3,8]]
        print(arquivo_final2.columns)
        #Alterações dia 25/10
    
        print(arquivo_final.columns)

        ######### Manipulacao do streamlit ##############
        
        arquivo_final2.insert(loc = 0,
                            column='Checkbox',
                            value=st.checkbox('arquivo_final2'
                                            )
                                            )


        barra1 = st.selectbox('Selecione o Operador',
                            options=arquivo_final2['Operador'].unique())

        df7 = arquivo_final2.loc[arquivo_final2['Operador'] == barra1]
        df6 = arquivo_final2['Operador'].value_counts()
        
        data_frame_of = st.data_editor(df7,
                                    width=2000,
                                    height=500,
                                    num_rows='dynamic')


        ########################################        GUIDE >>>>>>>>

if selecionar == 'Guide':
    df = None
    daf=None
    daf2=None

    #st.sidebar.image('transferir.jpg')

    def le_excel(x):
        x+='.xlsx'
        df=pd.read_excel(x)
        return df

    ###     Upload files direct in streamlit


    upload_file4 = st.sidebar.file_uploader(
                            label='Solte o arquivo de PL',
                            type=['xlsx'],
                            key='upload4'
                            )


    if upload_file4  is not None:
        
        print('hello')
        try:
            df = pd.read_excel(upload_file4)
        except Exception as e:
            st.write(f'Faltando arquivos:{e}')

    ####    arquivo 2


    upload_file5 = st.sidebar.file_uploader(
                            label='Solte o arquivo de SALDO',
                            type=['xlsx'],
                            key='upload5'
                            )

    if upload_file5  is not None:
        print('hello')
        try:
            daf = pd.read_excel(upload_file5)
        except Exception as e:
            st.write(f'Faltando arquivos:{e}')
    
    ##### arquivo 3 
    

    upload_file6 = st.sidebar.file_uploader(
                            label='Solte o arquivo da planilha de CONTROLE',
                            type=['xlsx'],
                            key='upload6'
                            )



    if upload_file6  is not None:
        print('hello')
        try:
            daf2 = pd.read_excel(upload_file6)
        except Exception as e:
            st.write(f'Faltando arquivos:{e}')  


    if df is not None and daf is not None and daf2 is not None:


        pl = df
        saldo = daf
        controle = daf2

        # Separa as colunas nescessarias

        pl = pl[[
            'CLIE_ID',
            'SALDO_BRUTO'
        ]]
        saldo = saldo[[
            'Cod. Conta',
            'Saldo Previsto',
            'Vl. Total'
        ]]
        print(controle.columns)
       
        
        controle =  controle.iloc[:,[1,2,6,11,20,19,18]]
        
        
        controle = controle.rename(
            columns = {
                'Unnamed: 2':'Conta'
                })
        controle = controle.rename(
            columns = {
                'Mesa de Operação':'Operador'
                })
        saldo = saldo.rename(
            columns = {
                'Cod. Conta':'Conta'
                })    
        pl = pl.rename(
            columns = {
                'SALDO_BRUTO':'PL'
                })
        pl = pl.rename(
            columns = {
                'CLIE_ID':'Conta'
                })
        
        
        # agrupamento da coluna de PL

        pl = pl.groupby('Conta')['PL'].sum()
        pl = pl.reset_index()
        
        
        # Retirando um caractere da coluna Conta
        controle['Conta'] = controle['Conta'].astype(str)
        pl['Conta'] = pl['Conta'].astype(str)
        saldo['Conta'] = saldo['Conta'].astype(str)
        controle['Conta'] = controle['Conta'].str[:-1]


    
    

        # Funcao para mesclar arquivos
            
        def juntar_arquivos(df,df2):
            df3 = pd.merge(df,df2,on='Conta', how='outer')
            
            return df3
        

        primeira_juncao = juntar_arquivos(controle,pl)
        segunda_juncao = juntar_arquivos(primeira_juncao,saldo)


    
        # Filtros para adicionar operadores
        #Filtro Breno
        filtro = segunda_juncao.PL<100000
        filtro1 = segunda_juncao.Operador == 'Edu'
        
        arquivo_filtro_breno = segunda_juncao.loc[filtro&filtro1]
        arquivo_filtro_breno['Operador'] = arquivo_filtro_breno['Operador'].str.replace('Edu','Breno')
        #Filtro Edu
        filtro2 = segunda_juncao.PL>100000
        filtro3 = segunda_juncao.Operador == 'Edu'
        
        arquivo_filtro_edu = segunda_juncao.loc[filtro2&filtro3]
        #filtro Bruno
        filtro4 = segunda_juncao.PL<100000
        filtro5 = segunda_juncao.Operador == 'Léo'
        
        arquivo_filtro_bruno = segunda_juncao.loc[filtro4&filtro5]
        arquivo_filtro_bruno['Operador'] = arquivo_filtro_bruno['Operador'].str.replace('Léo','Bruno')
        #Filtro Léo
        filtro6 = segunda_juncao.PL>100000
        filtro7 = segunda_juncao.Operador == 'Léo'
        
        arquivo_filtro_lo = segunda_juncao.loc[filtro6&filtro7]
        
        #Juntando arquivos filtrados
        def concatenando(dfs):
            df=pd.concat(dfs)
            return df
        
        filtrado_arquivo = [arquivo_filtro_bruno,
                            arquivo_filtro_breno,
                            arquivo_filtro_edu,
                            arquivo_filtro_lo]
        
        arquivo_final = concatenando(filtrado_arquivo)

        arquivo_final = arquivo_final[[
            'Backoffice ',
            'Conta',
            'Unnamed: 11',
            'Saldo Previsto',
            'Vl. Total',
        'Backoffice .2',
            'Gestão/ Head comercial',
            'Mesa de Operação ',
            'PL',
        'Operador'
        ]]

        arquivo_final = arquivo_final.sort_values(by='Saldo Previsto',ascending=False)
    ######### Manipulacao do streamlit ##############
        
        arquivo_final.insert(loc = 0,
                            column='Checkbox',
                            value=st.checkbox('arquivo_final'
                                            )
                                            )


        barra1 = st.selectbox('Selecione o Operador',
                            options=arquivo_final['Operador'].unique())

        df7 = arquivo_final.loc[arquivo_final['Operador'] == barra1]
        df6 = arquivo_final['Operador'].value_counts()
        
        data_frame_of = st.data_editor(df7,
                                    width=2000,
                                    height=500,
                                    num_rows='dynamic')


else:
    st.header('')

