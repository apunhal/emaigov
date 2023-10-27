``` 
    ⠀⠀⠀⠀⠀⠀⢀⣤⣀⣀⣀⠀⠻⣷⣄
    ⠀⠀⠀⠀⢀⣴⣿⣿⣿⡿⠋⠀⠀⠀⠹⣿⣦⡀ Lutar, Criar, Poder Popular!
    ⠀⠀⢀⣴⣿⣿⣿⣿⣏⠀⠀⠀⠀⠀⠀⢹⣿⣧
    ⠀⠀⠙⢿⣿⡿⠋⠻⣿⣿⣦⡀⠀⠀⠀⢸⣿⣿⡆
    ⠀⠀⠀⠀⠉⠀⠀⠀⠈⠻⣿⣿⣦⡀⠀⢸⣿⣿⡇
    ⠀⠀⠀⠀⢀⣀⣄⡀⠀⠀⠈⠻⣿⣿⣶⣿⣿⣿⠁
    ⠀⠀⠀⣠⣿⣿⢿⣿⣶⣶⣶⣶⣾⣿⣿⣿⣿⡁  este código é da Cooperativa
    ⢠⣶⣿⣿⠋⠀⠀⠉⠛⠿⠿⠿⠿⠿⠛⠻⣿⣿⣦⡀ -- abelino.punhal@gmail.com
    ⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⡿
```
Instalação:

- instalar o Poetry - https://pypi.org/project/poetry/
- instalar dependências: `poetry install`

Exemplos de execução:

- Gravar todos os resultados desta eleição por local
`poetry run ./emaigov/gravar_resultados.py --eleicao legislativas --ano 2022`

- Gravar os resultados referentes aos locais com os códigos indicados, todos os tipos de orgãos
`poetry run ./emaigov/gravar_resultados.py --eleicao presidenciais --ano 2021 --codigos 500000 080102 080105`

- Gravar os resultados referentes aos locais com os códigos indicados e orgão indicado em tipos
`poetry run ./emaigov/gravar_resultados.py --eleicao autarquicas --ano 2021 --codigos 500000 080102 --tipos CM`
