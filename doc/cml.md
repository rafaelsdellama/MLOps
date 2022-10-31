# Continuous Machine Learning (CML)

Você já deve ter ouvido falar de CI/CD (Integração Contínua/Implantação Contínua) em que as equipes de engenharia de software, 
integram perfeitamente novas alterações, correções de bugs e aprimoramentos e implantam o aplicativo mais recente. 
Isso funciona em cenários de software, pois existem ferramentas e tecnologias disponíveis para fazer isso.

As equipes teriam seus repositórios de código em algum serviço de hospedagem de repositório. 
À medida que as novas alterações de código e correções de bugs são corrigidas, os desenvolvedores começarão a 
enviar o código para as branchs do repositório. Depois que o código é verificado, uma solicitação pull é gerada 
para mergiar as alterações com a branch principal; depois de mesclar o código mais recente, um pipeline é acionado 
para verificar e testar o código, uma vez aprovado, o código pode ser implantado.

Agora imagine uma equipe de aprendizado de máquina (ML) e cientistas de dados tentando alcançar o mesmo, 
mas com um modelo de ML. Existem algumas complexidades envolvidas:

- Desenvolver um modelo de ML não é o mesmo que desenvolver um software. A maior parte do código é essencialmente uma caixa preta, difícil de identificar problemas no código ML. 
- Verificar o código de ML é uma arte em si, verificações de código estático e verificações de qualidade de código usadas no código de software não são suficientes, precisamos de verificações de dados, verificações de sanidade e verificação de viés. 
- O desempenho do modelo de ML depende dos dados usados para treinar e testar. 
- Desenvolvimento de Software padronizou arquitetura e padrões de design, ML não possui padrões de design amplamente adotados, cada equipe pode seguir seu próprio estilo. 
- Vários classificadores e algoritmos podem ser usados para resolver o mesmo problema.

Todas essas complexidades levantam a questão importante — o ML pode ser executado em um estilo de integração contínua?

O CML é uma biblioteca de código aberto focada no fornecimento de CI/CD para projetos de aprendizado de máquina. 
Seus princípios incluem: 
- GitFlow: usando o fluxo de trabalho Git para gerenciar experimentos juntamente com dados e modelos de versão DVC. 
- Relatórios automáticos para experimentos: a CML pode gerar relatórios em solicitações pull com métricas e gráficos, ajudando a equipe a tomar decisões informadas e orientadas por dados. Como estamos usando o Github como nosso repositório Git, as ações do Github serão usadas para configurar o CML. O Github Actions é gerenciado pelo Github, portanto, não há necessidade de se preocupar em dimensionar e operar a infraestrutura, assim como outras ferramentas como o Jenkins.


**Por que precisaríamos de CML?**
Considere o processo de obtenção de um modelo de ML para produção – vários cientistas de dados trabalham no problema, buscam os dados, 
criam um modelo, treinam-no nos dados, testam e avaliam. Se for bom o suficiente, eles irão implantá-lo. 
Nesse processo, precisamos garantir certas validações:

- Um modelo criado por um cientista de dados pode ser reproduzido por outros em diferentes sistemas e ambientes?
- A versão adequada dos dados está sendo usada para treinamento?
- As métricas de desempenho do modelo são verificáveis?
- Como rastreamos e garantimos que o modelo está melhorando? 
- Uma vez concluído o treinamento, há um relatório que nos forneça os detalhes da sessão de treinamento para comparação posterior? 
- As mesmas verificações aconteceriam durante o retreinamento do modelo?

Essas etapas são necessárias para garantir que o modelo melhore ao longo do tempo. 
Isso se torna extremamente tedioso para acompanhar à medida que as equipes aumentam ou à medida que o modelo se torna mais complexo.

O CML melhora e agiliza este processo; introduzindo um fluxo de trabalho contínuo para provisionar instâncias de nuvem, 
treinar modelo nelas, coletar métricas, avaliar o desempenho do modelo e publicar relatórios resumidos. 
Ele permite que os desenvolvedores introduzam uma série de pontos de verificação que são mais fáceis de rastrear e reproduzir em diferentes cenários.

Os fluxos de trabalho CML tornam tudo isso possível sem pilha de tecnologia extra e com algumas linhas de código integradas perfeitamente ao 
processo de desenvolvimento existente com o qual a maioria dos desenvolvedores está familiarizada.

Isso adiciona uma camada de visibilidade ao processo de desenvolvimento, os cientistas de dados agora têm acesso a vários relatórios de treinamento e métricas para comparar e avaliar o modelo. 
Isso ajuda as equipes a desenvolver e levar o modelo para produção mais rapidamente, reduz muito o esforço manual e o retrabalho envolvido na 
correção do modelo caso haja uma degradação no desempenho.

## Como o CML funciona?
O CML cria automação de estilo CI/CD no workflow. A maioria das configurações são definidas em um arquivo 
`cml.yaml` de configuração mantido no repositório. 
O CML funciona com um conjunto de funções chamadas Funções CML. 
Esses são funções predefinidos que ajudam nosso workflow, como permitir que esses relatórios sejam publicados 
como comentários ou até mesmo iniciar um cloud runner para executar o restante do fluxo de trabalho. 
Você pode ver um exemplo de workflow abaixo:

<figure>
    <img src="/doc/images/cml.png" alt="Trulli" style="width:100%">
    <figcaption align = "center"><b>Figura 1 - Workflow CML. Fonte: https://towardsdatascience.com/continuous-machine-learning-e1ffb847b8da
    </b></figcaption>
</figure>
<br/><br/>

Você pode consultar todas as funções CML disponíveis [aqui](https://cml.dev/doc/usage#cml-commands).

## Exemplos de Workflow


### Testes com GitHub Actions

No primeiro exemplo vamos garantir queos testes e o check do Black sejam executados toda vez que houver 
um novo push para o repositório no Github. Isso é importante para obter redundância nos testes do projeto 
e evitar que o código seja executado sem erros em nenhum ambiente e não apenas no computador do desenvolvedor.

```
name: Python Package and Test

    on: [push]

    jobs:
        build:

        runs-on: ubuntu-latest
        strategy:
        matrix:
            python-version: [3.9]

        steps:
        - uses: actions/checkout@v2
        - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v2
        with:
        python-version: ${{ matrix.python-version }}
        - name: Install dependencies
        run: |
        python -m pip install --upgrade pip
        pip install pytest black
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        - name: Test with pytest
        run: |
        pytest
        - name: Python Black
        run: |
        black . --check
```

Primeiro definimos o nome do workflow:
```
name: Python Package and Test
```

Escolhendo quando o workflow será executado. Neste caso faz com que seja executado toda vez que há um push no repositório.
```
on: [push]
```

Configurando uma instância do Github para executá-la.
Neste exemplo o Github configurará uma instância gratuita do Ubuntu para nós, usando a versão oficial mais recente.
```
runs-on: ubuntu-latest
```

Escolhendo a versão do Python.
```
matrix:
    python-version: [3.9]
```

Instalando os requisitos de teste
```
python -m pip install --upgrade pip
pip install pytest black
```

Instalando os requisitos do projeto
```
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
```

Executando o Pytest
```
- name: Test with pytest
    run: |
    pytest
```

Executando o check do black, que verifica se cada arquivo Python está formatado de acordo com Black.
```
- name: Python Black
     run: |
     black . --check
```

### Reproduzir nosso pipeline em push e gerar um relatório automatizado em pull requests
Neste exemplo vamos nos concentrar em reproduzir a pipeline a cada push e gerar um relatório automatizado 
em pull requests para comparar o experimento com o modelo no branch principal.

Para reproduzir nossa pipeline de experimentos, precisamos começar a extrair nossos dados versionados pelo DVC. 
Como o Github Actions executará nossa pipeline dentro de um container pré-configurado pelo CML que não possui 
nossas credenciais para obter os dados, será necessário configurar nossas credenciais no Github Secrets.

```
name: model-training-evaluate
    on: [push]
    jobs:
     run:
     runs-on: [ubuntu-latest]
     container: docker://dvcorg/cml-py3:latest
     steps:
     - uses: actions/checkout@v2
     - name: 'Train and Evaluate model'
     shell: bash
     env:
     repo_token: ${{ secrets.GITHUB_TOKEN }}
     AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
     AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
     run: |
     # Install requirements
     pip install -r requirements.txt

     # Pull data & run-cache from IBM COS and reproduce pipeline
     dvc pull --run-cache
     dvc repro

     # Report metrics
     echo "## Metrics" >> report.md
     git fetch --prune
     dvc metrics diff master --show-md >> report.md

     # Publish ROC Curve and 
     echo -e "## Plots\n### ROC Curve" >> report.md
     cml-publish ./results/roc_curve.png --md >> report.md
     echo -e "\n### Precision and Recall Curve" >> report.md
     cml-publish ./results/precision_recall_curve.png --md >> report.md
     cml-send-comment report.md
```

Como configurar um contêiner pré-configurado CML
```
container: docker://dvcorg/cml-py3:latest
```

Configurando credenciais de ambiente acessar o armazenamento remoto do DVC:
```
env: repo_token: ${{ secrets.GITHUB_TOKEN }} 
AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY}}
```

Instalação das dependencias
```
pip install -r requirements.txt
```

Extraia os dados versionados e reproduza o pipeline completo de treinamento e avaliação
```
dvc pull --run-cache
dvc repro
```

Formatação de títulos de seção de relatório
```
echo "## Metrics" >> report.md
echo -e "## Plots\n### ROC Curve" >> report.md
echo -e "\n### Precision and Recall Curve" >> report.md
```

Comparar métricas e publicá-las no relatório
```
dvc metrics diff master --show-md >> report.md
```

Publicação de números do experimento no relatório
```
cml-publish ./results/roc_curve.png --md >> report.md
cml-publish ./results/precision_recall_curve.png --md >> report.md
```

Devolva o relatório final formatado como um comentário no Commit ou Pull Request
```
cml-send-comment report.md
```

O Relatório deve ter a seguinte aparência:

<figure>
    <img src="/doc/images/cml_report.png" alt="Trulli" style="width:100%">
    <figcaption align = "center"><b>Figura 2 - Exemplo de relatório gerado pelo CML. Fonte: https://mlops-guide.github.io/CICD/cml_testing/
    </b></figcaption>
</figure>
<br/><br/>

------

## Referências:
- [CML](https://github.com/iterative/cml)
- [CML with DVC use case](https://github.com/iterative/cml_dvc_case)
- [DVC CI/CD MLOps Pipeline](https://github.com/mlops-guide/dvc-gitactions)
- [Continuous Machine Learning](https://towardsdatascience.com/continuous-machine-learning-e1ffb847b8da)
- [Continuous Integration with CML and Github Actions](https://mlops-guide.github.io/CICD/cml_testing/)
