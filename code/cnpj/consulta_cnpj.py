#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 13:00:21 2020

@author: Maicon Melo Alves (maiconmelo.ufrj@gmail.com)
"""

''' Importing additional modules'''
import json
import sys
import urllib.request
import csv
import time
import psycopg2
import argparse
import configparser


''' Constants '''
c_api_receita = 'http://receitaws.com.br/v1/cnpj/'
c_user_agent = 'User-agent'
c_user_agent_parameters = 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
c_acessos_por_minuto = 3
c_tempo_espera = 60
c_municipio = 'municipio'
c_uf = 'uf'
c_atividade_principal = 'atividade_principal'
c_situacao = 'situacao'
c_situacoes_inativas = {'BAIXADA', 'INAPTA'}
c_atividade_sem_descricao = 'Sem descrição'
c_texto_atividade = 'text'
c_cnpj_invalidos = {'-2'}
c_campo_cnpj_favorecido = 'CNPJ OU CPF FAVORECIDO'
c_arquivo_ini = 'config.ini'
c_tipo_csv = "csv"
c_tipo_cnpj = "cnpj"


''' Functions '''          
def cnpj_valido(cnpj):
    return False if (len(cnpj) != 14 or cnpj in c_cnpj_invalidos) else True

def ler_dados_csv(arquivo):
    conjunto_cnpj = set()
    with open(arquivo, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            cnpj = row[c_campo_cnpj_favorecido]
            if cnpj_valido(cnpj):
                conjunto_cnpj.add(cnpj)
    return conjunto_cnpj

def ler_dados_txt(arquivo):
    conjunto_cnpj = set()
    with open(arquivo, mode='r') as txt_file:
        conteudo = txt_file.readlines()
        for cnpj in conteudo:
            cnpj = cnpj.rstrip()
            if cnpj_valido(cnpj):
                conjunto_cnpj.add(cnpj)
    return conjunto_cnpj
    
def obter_lista_cnpj(arquivo, tipo, bd):
    
    if tipo == c_tipo_csv:
        conjunto_cnpj = ler_dados_csv(arquivo)
    else:
        conjunto_cnpj = ler_dados_txt(arquivo)
            
    aux_conjunto = conjunto_cnpj.copy()
    for cnpj in aux_conjunto: 
        sql = f"SELECT cnpj FROM favorecidos WHERE cnpj = '{cnpj}';"
        cnpj_ja_gravado = executar_consulta_postgre(bd, sql)
        if cnpj_ja_gravado:
            conjunto_cnpj.remove(cnpj)
    
    return conjunto_cnpj
    
def executar_consulta_postgre(bd, sql):
    cursor = bd.cursor()
    cursor.execute(sql)
    cursor.close()
    if cursor.rowcount != 0:
        return True
    return False

def inserir_dados_postgre(bd, sql):
    cursor = bd.cursor()
    cursor.execute(sql)
    bd.commit()
    cursor.close()

def armazenar_cnpj(cnpj, dados_cnpj, bd):
    print(f"Armazenando CNPJ {cnpj}...")
    atividade_principal = dados_cnpj[c_atividade_principal][0][c_texto_atividade]
    uf = dados_cnpj[c_uf]
    municipio = (dados_cnpj[c_municipio]).replace("'","")
    situacao = dados_cnpj[c_situacao]
    if situacao in c_situacoes_inativas:
        atividade_principal = c_atividade_sem_descricao
    sql = f"INSERT INTO favorecidos(cnpj, atividadePrincipal, uf, municipio) VALUES('{cnpj}', '{atividade_principal}', '{uf}', '{municipio}');"
    inserir_dados_postgre(bd, sql)
    print(f"CNPJ {cnpj} inserido com sucesso!")    

def buscar_cnpj(cnpj):
    url_receita = c_api_receita + cnpj
    requisicao_http = urllib.request.build_opener()
    requisicao_http.addheaders = [(c_user_agent, c_user_agent_parameters)]
    with requisicao_http.open(url_receita) as fd:
        retorno_http = fd.read().decode()
    dados_cnpj = json.loads(retorno_http)
    return dados_cnpj

def abrir_sessao_postgre(config):
    bd = psycopg2.connect(host=config["host_bd"], database=config["nome_bd"], user=config["usuario_bd"])
    return bd

def encerrar_sessao_postgre(bd):
    bd.close()

def interpretar_argumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument('--arquivo')
    parser.add_argument('--tipo')
    argumentos = parser.parse_args()
    return argumentos.arquivo, argumentos.tipo

def multiplo(m, n):
	return True if m % n == 0 else False

def dormir(tempo):
    time.sleep(tempo)

def ler_configuracao():
    config = configparser.ConfigParser()
    config.read(c_arquivo_ini)
    configuracao = {}
    configuracao["nome_bd"] = config['BD']['NOME']
    configuracao["usuario_bd"] = config['BD']['USUARIO']
    configuracao["host_bd"] = config['BD']['HOST']
    return configuracao

def gravar_cnpj(lista_cnpj, num_arquivos):
    total_cnpjs = len(lista_cnpj)
    cnpjs_por_arquivo = total_cnpjs/num_arquivos
    indice_arquivo = 1
    conteudo = ""
    for indice, cnpj in enumerate(lista_cnpj):
        cnpjs_consultados = indice + 1
        conteudo = conteudo + cnpj + '\n'
        if multiplo(cnpjs_consultados, cnpjs_por_arquivo):
            nome_arquivo = f"../../dados/dados_segregados/CNPJ{indice_arquivo}.txt"
            with open(nome_arquivo, 'w') as arquivo:
                arquivo.write(conteudo)
            conteudo = ""
            indice_arquivo = indice_arquivo + 1 

''' Main program '''
def main():
    (arquivo, tipo) = interpretar_argumentos()
    configuracao = ler_configuracao()
    bd = abrir_sessao_postgre(configuracao)
    lista_cnpj = obter_lista_cnpj(arquivo, tipo, bd)
    total_cnpjs = len(lista_cnpj)
    print(f"Total de CNPJs a serem consultados: {total_cnpjs}")
    
    for indice, cnpj in enumerate(lista_cnpj):
        dados_cnpj = buscar_cnpj(cnpj)
        armazenar_cnpj(cnpj, dados_cnpj, bd)
        cnpjs_consultados = indice + 1
        if multiplo(cnpjs_consultados, c_acessos_por_minuto):
            progresso = "{0:.2f}".format((cnpjs_consultados / total_cnpjs) * 100)
            print(f"Indo dormir. Consultados {cnpjs_consultados} CNPJs de um total de {total_cnpjs} (progresso: {progresso}%). ")
            dormir(c_tempo_espera)

    encerrar_sessao_postgre(bd)


if __name__ == "__main__":
    sys.exit(main())