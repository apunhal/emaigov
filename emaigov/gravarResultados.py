#!/usr/bin/env python
import requests
import json
import os
import argparse, sys

# constants
BASE_TARGET_PATH = "./target"

def get_children(session, config, id):
    post_url = config["children_url"] % (id)
    url = f'{config["url"]}/{post_url}'
    print(f'url={url}')
    response = session.get(url)
    return json.loads(response.content)

def init_session():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"}
    session = requests.Session()
    session.trust_env = False
    session.headers = headers
    return session

def cli_parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("--eleicao", required=True, help="Tipo de Eleição: legislativas, regionais, presidenciais, europeias e autarquicas")
    parser.add_argument("--ano", required=True, type=int, help="Ano da Eleição: YYYY")
    parser.add_argument("--codigos", nargs="*", help="Código(s) do(a) distrito, concelho, freguesia pretendido(s)")
    parser.add_argument("--tipos", nargs="*", help="Código(s) do(s) orgão(s) a eleger")
    parser.add_argument("--indice", action='store_true', help="mostra um indice com a correspondencia de cada código")
    return parser.parse_args()

def read_config(args):
    with open('config.json', 'r') as file:
        config = json.loads(file.read())
    if config[args.eleicao]:
        cfg = next((item for item in config[args.eleicao] if item['ano'] == args.ano), None)
    if not cfg:
        raise ValueError("Configuração não encontrada")
    #print(cfg)
    return cfg

def create_target_dir(args):
    # create data dir for this election
    path = f'{BASE_TARGET_PATH}/{args.eleicao}-{args.ano}' 
    path_exists = os.path.exists(path)
    if not path_exists:
        os.makedirs(path)
        print(f"The new directory {path} is created!")
    return path

def get_results_and_write(session,config,path,codigo,tipo):
    # get results and write to file
    post_url = config["results_url"] % (codigo, tipo)
    url = f'{config["url"]}/{post_url}'
    #print (url)
    response = session.get(url)
    filename = f"{path}/{codigo}-{tipo}.json"
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(response.text)

def filtered_territory_key(key):
    return key.replace('LOCAL-','')

def create_index(session,config):
    index = []
    distritos = get_children(session,config,f'LOCAL-{config["raiz"]}')
    for d in distritos:             # para cada distrito
        d = dict((x, y) for x, y in d.items())
        d["tipo"]='Distrito'
        index.append(d)            
        concelhos = get_children(session,config,d["territoryKey"])
        for c in concelhos:         # para cada concelho
            c = dict((x, y) for x, y in c.items())
            c["tipo"]='Concelho'
            index.append(c)
            freguesias = get_children(session,config,c["territoryKey"])
            for f in freguesias:    # para cada freguesia
                f = dict((x, y) for x, y in f.items())
                f["tipo"]='Freguesia'
                index.append(f)
                break
            break
        break
    return index

def print_index(items):
    for i in items:
        key = i['territoryKey'].replace("LOCAL-","")
        print(f'{key};{i["name"]};{i["tipo"]}')

def main():
    args = cli_parse_args()
    config = read_config(args)
    path = create_target_dir(args)

    session = init_session()

    if args.indice:
        indice = create_index(session,config)
        print_index(indice)
        exit(0)
    elif args.codigos:
        for c in args.codigos:
            tipos = args.tipos
            if not args.tipos:
                tipos = config['tipos']
            for t in tipos:
                territory_key = f'LOCAL-{c}'
                get_results_and_write(session,config,path,territory_key,t)
        exit(0)
    
    indice = create_index(session,config)
    for i in indice:
        for t in config['tipos']:
            get_results_and_write(session,config,path,i["territoryKey"],t)

if __name__ == "__main__":
    main()