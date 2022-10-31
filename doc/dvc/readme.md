# Data Version Control (DVC)

## Versionamento em projetos de Machine Learning

O desenvolvimento de software inclui o processo contínuo de documentar e manter o 
código-fonte, modificá-lo e colaborar com outros desenvolvedores; 
e um sistema de controle de versão (como Git) facilita essa tarefa. 
Da mesma forma, em *Machine Learning* (ML) e *Data Science* (DS), criar e implantar modelos de ML em produção é 
um processo iterativo que exige versões para facilitar a manutenção e permitir a reprodutibilidade. 
Os projetos de ML e DS possuem uma grande diferença em relação aos projetos usuais de desenvolvimento de software 
porque o ML requer código e dados - portanto, **o controle de versão aqui não se restringe ao 
código, mas também envolve o controle de versão de dados, hiperparâmetros e outros metadados**.

Estamos familiarizados com o Git como uma ferramenta de controle de versão bem 
conhecida e amplamente usada no desenvolvimento de software. 
Então por que não é aconselhável (ou eficiente) usar apenas o Git para projetos de ML de controle de versão?

- Os projetos de Machine Learning (ML) / Deep Learning (DL) geralmente envolvem muitos dados, enquanto o limite superior do tamanho do arquivo que o Git permite ser enviado para um repositório do GitHub é de apenas 100 MB.
- Durante a colaboração entre pessoas em uma organização, pode ser necessário que o acesso aos dados (ou alguma outra parte do pipeline) seja restrito apenas a um determinado conjunto de pessoas. Se os dados forem rastreados diretamente junto com outro código em um repositório do GitHub, pode ser difícil fornecer níveis de acesso tão variados.
- Além disso, os dados reais para treinar um modelo já podem estar presentes remotamente em algum serviço de armazenamento (como Amazon S3, etc.) e seria um desperdício copiar todos esses dados em um repositório do GitHub e rastreá-los separadamente.
- Tudo isso exige algumas **ferramentas e estruturas específicas para resolver esse problema de controle de versão de artefatos de ML, como dados, hiperparâmetros e modelos que funcionam junto com ferramentas de controle de versão existentes** para fornecer uma experiência perfeita para o gerenciamento de projetos de ML.

Antes de falar de controle de versão de dados, primeiro vamos listar algumas das razões pelas quais dados e modelos mudam em um sistema de ML:
- Os dados podem ser alterados com frequência, exigindo atualizações periódicas em nosso modelo para um bom desempenho (modelos relacionados a indicadores financeiros por exemplo, a Selic, o IPCA, etc mudam constantemente);
- Os modelos podem ser retreinados com novos dados e talvez novas técnicas de treinamento;
- A distribuição dos dados podem mudar com o tempo (exemplo: idade média do publico de um e-commerce);
- Os modelos podem se degradar com o tempo;
- Modelos com baixo desempenho podem ser rapidamente revertidos para uma versão anterior.

## O que é Data Version Control (DVC) ?

O controle de versão de dados é uma coleção de ferramentas e procedimentos que tentam 
adaptar o processo de controle de versão ao mundo dos dados. 
Uma dessas ferramentas que ajuda os cientistas de dados a controlar seus dados e 
modelos e executar experimentos reproduzíveis é o **DVC** ou *Data Version Control*.

O DVC é um sistema de controle de versão de código aberto para projetos de Machine Learning.  
Para aproveitar o conjunto de ferramentas existente com o qual a maioria dos 
desenvolvedores está familiarizada, ele emula comandos e fluxos de trabalho do Git 
para que eles possam integrá-lo rapidamente à sua prática habitual do Git.

Controle de versão para projetos de ML, precisa considerar não apenas o código, mas também os dados e modelos. 
DVC é uma ferramenta fácil de usar que funciona no topo do Git. 
O DVC utiliza um arquivo `dvc` para ajudá-lo a controlar a versão de seus artefatos de ML e o Git é responsável pelo controle de versão do código e desse arquivo dvc.

O DVC usa um repositório remoto (incluindo suporte a todos os principais provedores de nuvem)
para armazenar todos os dados e modelos de um projeto (para mais informações consulte a [documentação](https://dvc.org/doc/command-reference/remote#description)). 
No repositório de código real, um ponteiro para esse local remoto é armazenado para acessar 
os artefatos reais.

Essa documentação mostra detalhes sobre:
- Como versionar dados em projetos de ML
- Como definir o armazenamento remoto que mantém seus artefatos de ML e recuperar artefatos de ML do armazenamento remoto para seu projeto local
- Como acompanhar os arquivos de dados quando você fez alterações ou adicionou um novo conjunto de dados
- Como alternar entre diferentes versões
- Como construir pipelines reprodutíveis de ML com DVC

Para mais informações, consulte a [documentação oficial](https://dvc.org/doc).

### Caracteristicas do DVC
O uso do DVC traz agilidade, reprodutibilidade e colaboração ao seu fluxo de 
trabalho de DS. Alguns dos principais recursos do DVC são:

- Compatível com Git: Ele roda em cima de qualquer repositório Git e é compatível com qualquer servidor ou provedor Git padrão (GitHub, GitLab, etc.)
- Versionamento de dados simplista: várias versões de dados e modelos são mantidas substituindo arquivos grandes, diretórios de conjuntos de dados, modelos de ML, etc. por pequenos metarquivos (arquivos ```.dvc```) contendo ponteiros para os dados originais;
- Independente de armazenamento: pode usar Amazon S3 , Microsoft Azure Blob Storage , Google Drive , Google Cloud Storage , disco como controle remoto para armazenar dados entre outros;
- Reprodutível: torna os projetos de ML reproduzíveis criando pipelines leves usando gráficos de dependência implícita e codificando os dados e artefatos envolvidos;
- Independente de linguagem e estrutura: é independente das linguagens de programação (Python, R, Julia, scripts de shell e assim por diante) ou bibliotecas de aprendizado de máquina (Keras, Tensorflow, PyTorch, Scipy e assim por diante) usadas no projeto
- Ramificação de baixo atrito: suporta ramificação instantânea do Git, mesmo com arquivos grandes e também evita a duplicação de dados entre experimentos;
- Fácil de usar: É rápido de instalar e não requer infraestrutura especial;

Nota: DVC NÃO substitui o Git, os meta-arquivos que contêm referências a dados e modelos originais 
no controle remoto variam com os dados durante o curso do projeto e precisam que o 
Git seja utilizado para o controle de versão.

Primeiros passos com DVC.

## [Primeiros passos com DVC](/doc/dvc/getting_started.md)
## [Usando DVC em um servidor compartilhado](/doc/dvc/shared_server.md)
## [DVC PipeLines](/doc/dvc/pipeline.md)

------

## Referências:
- [MLOps: Data versioning with DVC — Part Ⅰ](https://yizhenzhao.medium.com/mlops-data-versioning-with-dvc-part-%E2%85%B0-8b3221df8592)
- [The ultimate guide to building maintainable Machine Learning pipelines using DVC](https://towardsdatascience.com/the-ultimate-guide-to-building-maintainable-machine-learning-pipelines-using-dvc-a976907b2a1b)
- [Tracking ML Experiments With Data Version Control](https://www.analyticsvidhya.com/blog/2021/06/mlops-tracking-ml-experiments-with-data-version-control/)
- [Creating Data Science Pipelines using DVC](https://blog.koverhoop.com/creating-datascience-pipelines-using-dvc-ea7d934fafac)
- [Versioning Datasets with Git & DVC](https://www.analyticsvidhya.com/blog/2021/06/mlops-versioning-datasets-with-git-dvc/)
- [Fundamentals of MLOps — Part 2 | Data & Model Management with DVC](https://medium.com/analytics-vidhya/fundamentals-of-mlops-part-2-data-model-management-with-dvc-6be2ad284ec4)
- [mlops-guide.github.io](https://github.com/mlops-guide/mlops-guide.github.io/blob/main/docs/)
- [End to End Machine Learning Pipeline With MLOps Tools (MLFlow+DVC+Flask+Heroku+EvidentlyAI+Github Actions)](https://medium.com/@shanakachathuranga/end-to-end-machine-learning-pipeline-with-mlops-tools-mlflow-dvc-flask-heroku-evidentlyai-github-c38b5233778c)
- [https://madewithml.com/#mlops](https://madewithml.com/#mlops)
- [https://github.com/GokuMohandas/MLOps](https://github.com/GokuMohandas/MLOps)
- [https://github.com/shanakaChathu/churn_model](https://github.com/shanakaChathu/churn_model)
- [https://github.com/hzdr/mlops_comparison](https://github.com/hzdr/mlops_comparison)
