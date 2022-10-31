# MLOPS

MLOps ou ML Ops é um conjunto de práticas que visa implantar e manter modelos de aprendizado de máquina em produção de maneira confiável e eficiente. 
A palavra é um composto de "aprendizado de máquina" e a prática de desenvolvimento contínuo de DevOps na área de software.


Enquanto o aprendizado de máquina e a IA se propagam na indústria, academia e pesquisa e lentamente se tornam a principal abordagem para resolver problemas complexos. 
Porém muitas equipes de IA ainda estão tendo dificuldades para rastrear experimentos de ML e gerenciar dados de treinamento/validação e todo o ciclo de vida de ML, incluindo a implantação do modelo na produção.

Não é fácil acompanhar todos os dados que você usou em experimentos e modelos produzidos. 
O Git é usado para versionar o código, mas não é adequado para manter grandes dados ou arquivos de modelo. 


## Ferramentas que serão utilizadas

- Cookiecutter: Data science project structure
- Data version control (DVC): Version control of the data assets and to make pipeline
- Github: For code version control
- GitHub Actions: To create the CI-CD pipeline
- EvidentlyAI: To evaluate and monitor ML models in production
- Pytest: To implement the unit tests

## Instalação

```console
$ git clone 
$ cd dvc_cml_pipeline
```

Crie uma [virtualenv](https://virtualenv.pypa.io/en/stable/) e instale o requirements da pipeline que deseja executar:

```console
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ cd pipelines/PIPELINE
$ pip install -r src/requirements.txt
```