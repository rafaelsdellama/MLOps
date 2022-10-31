# Primeiros passos com DVC

## Instalação
Antes de iniciar o controle de versão, você precisará do DVC instalado em seu sistema. 

O DVC pode ser instalado a partir de seu repositório ou pacote binário com base no 
sistema operacional do usuário, cujas etapas podem ser encontradas na [documento oficial sobre como instalar o DVC](https://dvc.org/doc/install).

No entanto, como o DVC também pode ser usado como uma biblioteca Python, ele pode 
ser instalado usando um gerenciador de pacotes como **pip**. 
Dependendo do tipo de armazenamento remoto usado no projeto, dependências opcionais 
podem ter que ser instaladas.

Exemplo de instalação o DVC (com o Amazon S3 remoto):

```
pip install dvc[s3]
```

Nesse caso, ele instala o *boto3* junto com o DVC. Para mais informações, consulte a
documentação oficial do DVC.

Agora, você pode digitar `dvc --help` para visualizar todos os comandos que podem ser usados com o DVC.

## Iniciando um projeto
Depois de instalar o DVC, criamos um diretório de projeto e o inicializamos como um 
repositório Git. 
Em seguida, usamos `dvc init` para inicializá-lo como um repositório DVC.

```
$ mkdir mlops_dvc 
$ cd mlops_dvc
$ git init 
$ git remote add origin <github-repo-link> 
$ git branch -M main
$ dvc init
```

Isso criará uma pasta `.dvc` com a estrutura mencionada abaixo, que contém os diretórios internos e os arquivos necessários para a operação do DVC.
Estes incluem os arquivos de configuração, cache local, plots e arquivos temporários ([mais informações](https://dvc.org/doc/user-guide/project-structure/internal-files)). 
A pasta criada pelo DVC é semelhante à pasta `.git` criada na inicialização de um repositório Git. 
O `dvc init`  também cria um arquivo `.dvcignore` (semelhante a `.gitignore`) para conter uma lista de caminhos para o DVC ignorar.

```
mlops_dvc
├── .dvc
│   ├── .gitignore
│   ├── config 
│   ├── plots  
│   │   ├── confusion.json
│   │   ├── confusion_normalized.json
│   │   ├── default.json
│   │   ├── linear.json
│   │   ├── scatter.json
│   │   └── smooth.json
│   └── tmp
│       ├── links
│       │   └── cache.db
│       └── md5s
│           └── cache.db
├── .dvcignore
└── .git
```

Agora, comitamos esses arquivos internos no repositório Git usando `git commit -m "Initialize DVC in repo"`.

## Rastreando um arquivo usando DVC
Depois que nosso repositório DVC for inicializado, podemos começar a adicionar dados e código 
ao nosso repositório Git, conforme exigido pelo nosso projeto ML. 
É bom manter uma boa estrutura de diretórios para seu projeto de ML para separar os dados, 
código, modelos, métricas, etc. 
A seguir está uma estrutura de diretórios genérica que pode ser adotada para a maioria 
dos projetos de ML:

```
mlops_dvc
├── data              # Directory with raw and intermediate data
│   ├── raw/
│   |   └── training.csv 
│   └── prepared/     # Processed dataset
├── metrics/          # Plots & logs with performance metrics
├── models/           # Trained models
├── src/              # Files for processing, training, evaluation
│   ├── __init__.py
│   ├── featurize.py
│   ├── pipeline.py
│   └── prepare.py
└── params.yaml
```

- data : o nosso dataset será armazenado nesta pasta. Neste exemplo, usamos o arquivo CSV como nosso arquivo de conjunto de treinamento
- model : o modelo treinado será armazenado nesta pasta
- métricas : outros artefatos de ML podem ser armazenados nesta pasta
- src : scripts python serão armazenados nesta pasta (por exemplo, train.py, validate.py)

O fluxo de trabalho das seguintes seções é mostrado na Figura 1 abaixo:

<figure>
    <img src="/doc/images/dvc.png" alt="Trulli" style="width:100%">
    <figcaption align = "center"><b>Figura 1 - Versionamento com DVC. Fonte: https://yizhenzhao.medium.com/mlops-data-versioning-with-dvc-part-%E2%85%B0-8b3221df8592
    </b></figcaption>
</figure>
<br/><br/>

**Controle de versão de artefatos de ML**

O DVC salva informações sobre os arquivos (ou diretórios) recém-adicionados em um arquivo `.dvc` (um pequeno arquivo de texto em formato legível). 
Esse arquivo de metadados serve como um espaço reservado para os dados reais e pode ser facilmente 
versionado usando o Git, assim como o código-fonte. 

Usando `dvc add` para iniciar o rastreamento de arquivos e gerar o arquivo .dvc 
```
$ dvc add data/raw/training.csv # Para começar a rastrear um arquivo ou diretório
```

O arquivo `*.dvc` que contém um hash md5 exclusivo para vincular o conjunto de dados ao projeto. 

Em segundo plano, o `dvc add` move os dados para o cache do projeto e os vincula de volta ao nosso espaço de trabalho. 
Você pode verificar se a pasta `.dvc/cache/` contém uma subpasta `a3` (o DVC usa as duas primeiras letras do hash como nome da pasta), com um arquivo chamado `04afb96060aad90176268345e10355`. 
O nome da subpasta e o nome do arquivo no cache é baseado no valor de hash MD5 gerado para o arquivo **training.csv** que acabamos de adicionar.

O conteúdo do arquivo `.dvc` será o seguinte:

```
outs:
- md5: a304afb96060aad90176268345e10355
  size: 158375420
  path: training.csv
  isexec: true
```

Após esta etapa, existem alguns novos arquivos gerados na pasta do seu projeto, mostrados abaixo (somente as pastas necessárias, arquivos nesta etapa):

```
mlops_dvc
├── data              # Directory with raw and intermediate data
│   ├── raw/
│   |   └── training.csv 
│   |   └── training.csv.dvc --> arquivo dvc para training.csv 
│   └── prepared/     # Processed dataset
├── metrics/          # Plots & logs with performance metrics
├── models/           # Trained models
├── src/              # Files for processing, training, evaluation
│   ├── __init__.py
│   ├── featurize.py
│   ├── pipeline.py
│   └── prepare.py
├── params.yaml
└── .dvc/ 
│   ├── cache
│   |   └── a3/ --> uma cópia de training.csv 
│   |   |   └── 04afb96060aad90176268345e10355 
│   ├── gitignore
│   └── config --> mantém informações sobre armazenamento remoto (veja a próxima seção)
```

Em seguida, use o Git (`git commit`) para versionamento do arquivo `.dvc`.
```
git add data/raw/training.csv.dvc data/raw/.gitignore 
git commit -m "Adicionar dados de treinamento"
```

Agora rastreamos o `training.csv.dvc` usando o Git, ignorando o `training.csv`.


### Armazenando dados remotamente
Depois que os dados são rastreados usando o DVC, eles podem ser armazenados remotamente com segurança 
(o DVC suporta várias opções de armazenamento remoto, conforme discutido anteriormente).

Para fazer isso, primeiro precisamos configurar o armazenamento remoto usando DVC e, em seguida, enviar os artefatos de ML para esse armazenamento remoto. 
Ao fazer isso, não precisamos manter o grande conjunto de dados em nosso repositório Git, o arquivo *.dvc leve e legível por humanos que contém o link para nosso conjunto de dados real será mantido no repositório Git.
Para mais informações, consulte a [documentação oficial](https://dvc.org/doc/command-reference/remote/add).


### Configurando o bucket do Amazon S3
Neste exemplo planejamos armazenar os dados no Amazon S3. Primeiro teremos que criar/configurar nosso bucket do S3 que armazenará nossos dados. 
Após criar o bucket também será necessário criar uma Chave de Acesso que permitirá que o DVC (em nosso sistema local) se conecte com o Bucket.
Agora, será necessário criar 2 variáveis de ambiente chamadas `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY` 
contendo sua chave de acesso e chave de acesso secreta, respectivamente, que serão utilizadas pela `boto3` quando tentarmos 
fazer upload/download de dados do nosso bucket do S3. Além disso, também será necessário definir a AWS_DEFAULT_REGION.

### Enviando dados para armazenamento remoto
Para armazenar remotamente os arquivos de dados e modelos rastreados por DVC, primeiro precisamos configurar o local de armazenamento remoto da seguinte forma:

```
$ dvc remote add -d [storage_name] s3://[bucket-name]/[dvc_storage]
$ git add .dvc/config
$ git commit -m "Configure remote storage"
```

O primeiro comando cria um controle de versão remoto nomeado `storage_name` e o vincula a uma pasta `dvc_storage` 
no bucket do S3. O `-d` garante que esse remoto seja o padrão usado para upload e download de dados.

Em seguida, enviamos nossos dados para o armazenamento remoto (`dvc push` copia os dados armazenados em cache localmente para o armazenamento remoto):
```
$ dvc push 
```

Depois de executar os comandos acima, um controle remoto será adicionado à configuração do DVC (`.dvc/config`), que se parece com:
```
['remote "storage_name"'] 
    url = s3://[bucket]/[dvc_storage] 
[core] 
    remote = storage_name
```

Na sequencia enviamos para nosso repositório GitHub:
```
$ git push origin main
```

Depois de concluir as etapas acima, você pode verificar pela UI do Amazon S3 que os dados foram enviados para seu bucket.
Ao inspecionar o repositório do GitHub, você deve observar que a pasta `data/raw/` contém apenas os arquivos `.gitignore` e `training.csv.dvc`, 
enquanto o arquivo `training.csv` não está armazenado no GitHub.

### Recuperando Dados Armazenados Remotamente

Dados e modelos rastreados pelo DVC podem ser recuperados e usados em outras versões do projeto 
usando o comando `dvc pull`. Geralmente é executado após `git clone & git pull`.

Como o arquivo DVC armazenado no repositório Git contém o hash para identificar exclusivamente os 
dados e as informações de armazenamento remoto são armazenadas na configuração do DVC, ele sabe onde 
encontrar os dados no armazenamento remoto e baixar os dados para o projeto local.

Para simular essa situação neste tutorial, a pasta `.dvc/cache/` e os arquivos `data/raw/training.csv` 
precisam ser excluídos, após enviarmos controle remoto do DVC.

```
$ rm -rf .dvc/cache
$ rm -f data/raw/training.csv
```

Usando dvc pull para baixar dados:
```
$ dvc pull
```

### Fazendo alterações no conjunto de dados
Em projetos de ML do mundo real, podemos usar várias versões dos dados e modelos nos experimentos. Algumas causas potenciais disso podem ser:
- Diferentes técnicas de pré-processamento sendo usadas em diferentes experimentos
- A entrada de novos dados no sistema de tempos em tempos de alguma fonte externa
- Modelos mais novos treinados com diferentes hiperparâmetros
Sob tais circunstâncias, o DVC ajuda a rastrear essas mudanças de forma eficaz. 

Ao fazer alterações no conjunto de dados localmente, o comando `dvc add` nos permite rastrear a versão mais recente do conjunto de dados. 
Ele atualizará o hash md5 dentro do arquivo DVC e, em seguida, a nova versão do conjunto de dados será vinculada ao projeto. 
Basicamente, ele segue as mesmas etapas anteriores.

Para simular tal situação, duplicamos nosso conjunto de dados original da seguinte forma:

```
# Copie o conteúdo de data.csv para um local temporário 
$ cp data/raw/training.csv /tmp/data.csv
# Anexa o conteúdo deste local ao final de training.csv 
$ cat /tmp/data.csv >> data/raw/training.csv
```

Podemos verificar essa modificação observando que o tamanho desse novo arquivo `training.csv` é duas vezes maior 
que o do arquivo antigo. Agora, estamos prontos para rastrear essa alteração e fazer upload do novo arquivo 
para nosso bucket do S3. Usando `dvc add` para rastrear a nova versão do dataset:
```
$ dvc add data/raw/training.csv 
```

Salva a nova versão no armazenamento remoto:
```
$ dvc push
```

Você pode verificar o push verificando se o hash MD5 atualizado no arquivo `data/raw/training.csv.dvc` corresponde ao caminho do arquivo no bucket do S3.

Agora você também pode enviar para o GitHub para acompanhar as novas alterações:
```
$ git add data/raw/training.csv.dvc 
$ git commit -m "onjunto de treinamento atualizado" 
```

### Alternando entre versões de dados
Assim que tivermos várias versões de nossos dados e modelos, é óbvio que talvez precisemos alternar entre 
essas versões várias vezes. Assim como o Git tem o comando `checkout` para alternar entre diferentes versões 
do nosso código, o DVC oferece o comando `checkout` para sincronizar os dados e modelos de acordo com os 
arquivos `.dvc`. A prática usual é executar `git checkout <...>` (para alternar uma ramificação ou fazer o checkout de uma versão do arquivo `.dvc`) , 
seguido por `dvc checkout <...>`.

Primeiro utilizamos o `git checkout` para alterar para o commit desejado:
```
$ git checkout <...>
```

Seguido de `dvc checkout` para sincronizar dados:
```
$ dvc checkout
```

Por exemplo, para reverter à versão anterior do nosso conjunto de dados, realizamos o seguinte:
```
$ git checkout HEAD~1 data/raw/training.csv.dvc 
$ dvc checkout 
$ git commit data/raw/training.csv.dvc -m "Reverter atualizações"
```

Observe que não precisamos fazer `dvc push` novamente porque essa versão do conjunto de dados já está 
armazenada em nosso bucket do S3. 
As versões do arquivo de dados são definidas pelo conteúdo do arquivo `.dvc`, enquanto o controle de versão é fornecido por meio do Git. 
O DVC então produz esses arquivos `.dvc`, os altera e sincroniza com eficiência os dados rastreados pelo DVC no espaço de trabalho para combiná-los.

### Acessando dados rastreados por DVC
Uma vez que podemos rastrear nossos dados e modelos de forma eficaz, o próximo pensamento que surge é 
como podemos acessar esses artefatos rastreados para reutilizar os conjuntos de dados ou implantar um modelo? 
Nesta seção, discutiremos a maneira como podemos procurar arquivos relevantes em um repositório rastreado por DVC e fazer download de dados dele.

#### Procurando arquivos/diretórios usando DVC
Para baixar dados e modelos, primeiro precisamos descobrir onde eles estão localizados e se estão acessíveis. 
Para explorar um repositório DVC hospedado em qualquer servidor Git, o comando `dvc list` pode ser usado. 
Ele lista o conteúdo do projeto, incluindo arquivos, modelos e diretórios rastreados por DVC e Git. 
A sintaxe para este comando é a seguinte: `dvc list <repo-url> [<file-path>]` (<file-path >é opcional).

#### Download de arquivos e diretórios relevantes
Ambos `dvc get` e `dvc import` podem ser usados para baixar arquivos ou diretórios de um repositório rastreado por DVC. 
No entanto, `dvc get` baixa os arquivos sem manter nenhum dos metadados que o conectam ao projeto, 
enquanto `dvc import` também cria os arquivos `.dvc` correspondentes para serem salvos no projeto.

`dvc import` é essencialmente uma combinação de `dvc get` & `dvc add` aplicados juntos.

A sintaxe desses comandos é a seguinte: `dvc get/import <repo-url> <file-path> -o <output-file-path>`

O arquivo `data.csv` armazenado em nosso S3 e rastreado pelo arquivo `data/data.csv.dvc` pode ser baixado em qualquer projeto da seguinte forma:
```
$ dvc get https://github.com/<your-username>/<repo-name> data/data.csv -o data_downloaded/data.csv
$ dvc import https://github.com/<your-username>/<repo-name> data/data.csv -o data_downloaded/data.csv
```
Nota: `dvc get`pode ser chamado de qualquer lugar, mas `dvc import deve ser chamado de um repositório rastreado por DVC.

#### API Python DVC
Como mencionado anteriormente, o DVC também pode ser usado como uma biblioteca Python 
importando como qualquer outro módulo Python usando `import dvc.api`. 
O objetivo desta API é dar aos desenvolvedores algum acesso programático aos dados ou modelos versionados 
em repositórios rastreados por DVC. Duas dessas funções são:

`get_url()`

Dado o URL do repositório GitHub rastreado por DVC (repo) e o caminho para o arquivo (path), 
ele retorna a string de URL do local de armazenamento onde o arquivo real está armazenado no DVC remoto.

```
import dvc.api
x = dvc.api.get_url(repo="https://github.com/<your-username>/<repo-name>", path="data/data.csv")
# x stores the URL of the corresponding file in your S3 bucket (like s3://mlopsdvc<your-roll-number>/dvcstore/<path-to-file>)
```

`open()`

Dado o URL do repositório GitHub rastreado por DVC (repo), o caminho para o arquivo (path) e o modo no qual 
o arquivo é aberto (mode), ele abre o arquivo de dados/modelo e gera o objeto de arquivo correspondente.

```
import dvc.api
import pandas
with dvc.api.open(
    repo="https://github.com/<your-username>/<repo-name>", 
    path="data/data.csv", 
    mode="r"
) as fd:
    df = pandas.read_csv(fd)
```
