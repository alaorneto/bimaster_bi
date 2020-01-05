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



''' Functions '''          

def obter_lista_cnpj(file, db):
    conjunto_cnpj = set()
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            cnpj = row["CNPJ OU CPF FAVORECIDO"]
            conjunto_cnpj.add(cnpj)
            #print(f'\t{cnpj}')


    cursor = db.cursor()
    aux_conjunto = conjunto_cnpj.copy()
    for cnpj in aux_conjunto: 
        query = f"SELECT cnpj FROM favorecidos WHERE cnpj = '{cnpj}';"
        cursor.execute(query)
        if cursor.rowcount != 0:
            conjunto_cnpj.remove(cnpj)
            print("Já está na base")
        

    cursor.close()
    
    return conjunto_cnpj
    
    

def armazenar_cnpj(cnpj, dados_cnpj, db):
    atividade_principal = dados_cnpj["atividade_principal"][0]["text"]
    uf = dados_cnpj["uf"]
    municipio = dados_cnpj["municipio"]
    
    
    cursor = db.cursor()
    query = f"INSERT INTO favorecidos(cnpj, atividadePrincipal, uf, municipio) VALUES('{cnpj}', '{atividade_principal}', '{uf}', '{municipio}');"
    cursor.execute(query)
    
    print(f"Inserido CNPJ {cnpj}")
    
    cursor.close()
    
    
    

def buscar_cnpj(cnpj):
    url = 'http://receitaws.com.br/v1/cnpj/{0}'.format(cnpj)
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', " Mozilla/5.0 (Windows NT 6.2; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0")]

    with opener.open(url) as fd:
        content = fd.read().decode()

    dic = json.loads(content)
    
    return dic

def conectar_postgre():
    db = psycopg2.connect("host=localhost dbname=sa user=postgres")
    
    return db

''' Main program '''
def main():
    
    db = conectar_postgre()
    lista_cnpj = obter_lista_cnpj("test.csv", db)
    
    count = 1
    for cnpj in lista_cnpj:
        dados_cnpj = buscar_cnpj(cnpj)
        armazenar_cnpj(cnpj, dados_cnpj, db)
        if count == 3:
            time.sleep(60)
            count = 1
        else:
            count+=1
        #armazena_cnpj(dados_cnpj)
    db.close()
    
    


if __name__ == "__main__":
    sys.exit(main())