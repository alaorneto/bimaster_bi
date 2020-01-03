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



''' Functions '''          

def obter_lista_cnpj(file):
    conjunto_cnpj = set()
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            cnpj = row["CNPJ OU CPF FAVORECIDO"]
            conjunto_cnpj.add(cnpj)
            #print(f'\t{cnpj}')

    return conjunto_cnpj
    
    

def armazena_cnpj(dados_cnpj):
    pass
    

def busca_cnpj(cnpj):
    url = 'http://receitaws.com.br/v1/cnpj/{0}'.format(cnpj)
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-agent',
         " Mozilla/5.0 (Windows NT 6.2; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0")]

    with opener.open(url) as fd:
        content = fd.read().decode()

    dic = json.loads(content)
    
    return dic



''' Main program '''
def main():
    lista_cnpj = obter_lista_cnpj("test.csv")
    for cnpj in lista_cnpj:
        print(f'Consultando CNPJ {cnpj}')
        dados_cnpj = busca_cnpj(cnpj)    
        print(f'CNPJ: {cnpj}, Atividade principal: {dados_cnpj["atividade_principal"][0]["text"]}' )
        time.sleep(10)
        #armazena_cnpj(dados_cnpj)
    
    
    


if __name__ == "__main__":
    sys.exit(main())