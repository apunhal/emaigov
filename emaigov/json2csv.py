#!/usr/bin/env python
""" script para converter ficheiros json em CSV """
import os
import argparse
import glob
import json
import pandas as pd

def extract_filename(filename):
    """ extrai variaveis do nome do ficheiro json """
    actual_filename = filename.split("/")[-1]
    
    parts = actual_filename.split("-")

    if len(parts) != 3:
        raise ValueError( f"ignorando o ficheiro {filename}. " + \
                          "Formato esperado: 'TIPO-CODIGO-ORGAO.json'" )

    return parts

def create_csv_file(filename,raw_data):
    """ create a CSV file from parsing JSON data """
    df = pd.DataFrame(raw_data['currentResults']['resultsParty'],
                      columns=['acronym','votes','percentage','mandates'])

    tipo, codigo, orgao = extract_filename(filename)

    data_votacao = 'XXXX-XX-XX'
    nulos = raw_data['currentResults']['nullVotes']
    em_branco = raw_data['currentResults']['blankVotes']
    votantes = raw_data['currentResults']['numberVoters']
    validos = votantes - nulos - em_branco
    inscritos = raw_data['currentResults']['subscribedVoters']
    per_nulos = raw_data['currentResults']['nullVotesPercentage']
    per_em_branco = raw_data['currentResults']['blankVotesPercentage']
    per_votantes = raw_data['currentResults']['percentageVoters']
    per_validos = validos * 100 / votantes
    per_inscritos = 100

    # cleanups
    df.rename({'acronym': 'partido', 'votes': 'num_votos', 'percentage' : 'perc_votos',
               'mandates' : 'mandatos'}, axis=1, inplace=True)

    df.insert(0,'tipo',tipo)
    df = pd.concat([ pd.DataFrame([['NULOS', '', nulos, per_nulos, None]], columns=df.columns), df])
    df = pd.concat([ pd.DataFrame([['EM_BRANCO', '', em_branco, per_em_branco, None]],
                                  columns=df.columns), df])
    df = pd.concat([ pd.DataFrame([['VALIDOS', '', validos, per_validos, None]],
                                  columns=df.columns), df])
    df = pd.concat([ pd.DataFrame([['VOTANTES', '', votantes, per_votantes, None]],
                                  columns=df.columns), df])
    df = pd.concat([ pd.DataFrame([['INSCRITOS', '', inscritos, per_inscritos, None]],
                                  columns=df.columns), df])

    df = df.sort_index().reset_index(drop=True)

    df.insert(0,'codigo',codigo)
    df.insert(1,'nome',raw_data['territoryFullName'])
    df.insert(3,'data',data_votacao)

    #df['num_votos'].apply(np.ceil)
    df['perc_votos'] = df['perc_votos'].round( decimals = 2 )

    file_path = os.path.dirname(filename)
    orgao = orgao.split(".")[0]
    filename = f'{file_path}/{tipo}-{codigo}-{orgao}.csv'
    df.to_csv(filename, encoding='utf-8', index=False)

def process_file(file_path):
    """ converte o ficheiro em CSV """
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            data = json.load(file)
            # Now 'data' contains the content of the JSON file
            print(f"Processing file: {file_path}")
            create_csv_file(file_path, data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {file_path}: {e}")

def main():
    """ main function """
    parser = argparse.ArgumentParser(description='converte ficheiros segundo padrão especificado.')
    parser.add_argument('file', help='converte ficheiros segundo padrão especificado')
    args = parser.parse_args()

    files = glob.glob(args.file)

    if not files:
        print(f"Não encontrei ficheiros segundo o padrão especificado: {args.pattern}")
        return

    for file_path in files:
        process_file(file_path)

if __name__ == '__main__':
    main()
