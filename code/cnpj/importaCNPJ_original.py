import json
import sys
import urllib.request

def usage():
    print('Este script busca inforamções online sobre números de CNPJ')
    print('Modo de uso: {0} "CNPJ[1]" "CNPJ[2]" ... "CNPJ[N]"'.format(sys.argv[0]))
    sys.exit(1)


def valida_cnpj(cnpj):
    'Recebe um CNPJ e retorna True se formato válido ou False se inválido'

    cnpj = parse_input(cnpj)
    if len(cnpj) != 14 or not cnpj.isnumeric():
        return False

    verificadores = cnpj[-2:]
    lista_validacao_um = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    lista_validacao_dois = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    'Calcular o primeiro digito verificador'
    soma = 0
    for numero, ind in zip(cnpj[:-1], range(len(cnpj[:-2]))):
        soma += int(numero) * int(lista_validacao_um[ind])

    soma = soma % 11
    digito_um = 0 if soma < 2 else 11 - soma

    'Calcular o segundo digito verificador'
    soma = 0
    for numero, ind in zip(cnpj[:-1], range(len(cnpj[:-1]))):
        soma += int(numero) * int(lista_validacao_dois[ind])

    soma = soma % 11
    digito_dois = 0 if soma < 2 else 11 - soma

    return verificadores == str(digito_um) + str(digito_dois)


def parse_input(i):
    'Retira caracteres de separação do CNPJ'

    i = str(i)
    i = i.replace('.', '')
    i = i.replace(',', '')
    i = i.replace('/', '')
    i = i.replace('-', '')
    i = i.replace('\\', '')
    return i


def busca_cnpj(cnpj):
    url = 'http://receitaws.com.br/v1/cnpj/{0}'.format(cnpj)
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-agent',
         " Mozilla/5.0 (Windows NT 6.2; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0")]

    with opener.open(url) as fd:
        content = fd.read().decode()

    dic = json.loads(content)

    if dic['status'] == "ERROR":
        print('CNPJ {0} rejeitado pela receita federal\n\n'.format(cnpj))
    else:
        try:
            RelacaoCNPJ = open('CNPJ/CNPJ_'+cnpj+'.txt', 'w')
            RelacaoCNPJ.write('Nome: {0}\n'.format(dic['nome']))
            RelacaoCNPJ.write('Nome fantasia: {0}\n'.format(dic['fantasia']))
            RelacaoCNPJ.write('CNPJ: {0}\nData de abertura: {1}\n'.format(dic['cnpj'], dic['abertura']))
            RelacaoCNPJ.write('Natureza: {0}\n'.format(dic['natureza_juridica']))
            RelacaoCNPJ.write('Situação: {0}\nSituação especial: {1}  Tipo: {2}\n'.format(dic['situacao'],
                                                                            dic['situacao_especial'],
                                                                            dic['tipo']))
            RelacaoCNPJ.write('Motivo Situação especial: {0}\n'.format(dic['motivo_situacao']))
            RelacaoCNPJ.write('Data da situação: {0}\n'.format(dic['data_situacao']))
            RelacaoCNPJ.write('Atividade principal:')
            RelacaoCNPJ.write(' {0} - {1}\n'.format(dic['atividade_principal'][0]['code'],
                                              dic['atividade_principal'][0]['text']))
            RelacaoCNPJ.write('Atividades secundárias:')
            for elem in dic['atividades_secundarias']:
                RelacaoCNPJ.write(' {0} - {1}\n'.format(elem['code'], elem['text']))

            RelacaoCNPJ.write('Endereço:')
            RelacaoCNPJ.write(' {0}, {1}, '.format(dic['logradouro'],
                                             dic['numero']))
            RelacaoCNPJ.write('{0}'.format(dic['complemento']))
            RelacaoCNPJ.write(' {0}, {1}\n'.format(dic['municipio'],
                                             dic['uf']))
            RelacaoCNPJ.write('Telefone: {0}\n'.format(dic['telefone']))
            RelacaoCNPJ.write('Email: {0}\n\n'.format(dic['email']))
            RelacaoCNPJ.close()
            
        except KeyError:
            pass


if __name__ == '__main__':

    
    if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
        usage()

    for listaCNPJ in sys.argv[1:]:
        if not valida_cnpj(listaCNPJ):
            print('CNPJ "{0}" tem formato inválido'.format(listaCNPJ))
        else:
            busca_cnpj(parse_input(listaCNPJ))