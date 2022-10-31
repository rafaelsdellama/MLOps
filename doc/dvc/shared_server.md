# Usando DVC em um servidor compartilhado
Normalmente, computadores individuais não são usados para trabalho computacionalmente intensivo em muitos 
contextos acadêmicos e profissionais, pois não são poderosos o suficiente para lidar com grandes volumes de 
dados ou processamento intenso. Em vez disso, as equipes confiam na nuvem ou nas estações de trabalho locais, 
onde várias pessoas frequentemente colaboram no mesmo servidor de desenvolvimento. 
Embora isso permita uma melhor utilização de recursos, como acesso à GPU e armazenamento de dados centralizado, 
há uma grande chance de duplicação desnecessária dos mesmos dados em vários usuários e repositórios se não for gerenciado corretamente.

Dada essa configuração, o DVC pode desempenhar um papel crucial na manutenção de um cache compartilhado 
no servidor de desenvolvimento, de modo que todos os usuários possam ter restauração quase instantânea 
do espaço de trabalho e velocidades de comutação simplesmente usando o comando `dvc checkout`.

Depois que um repositório DVC é inicializado com `dvc init`, por padrão, o DVC coloca o cache na pasta 
`.dvc/cache` do repositório. Para criar e usar um cache compartilhado no servidor, um diretório para o 
cache externo deve ser criado configurado com as permissões e links apropriados.

Abaixo está um exemplo passo a passo de como configurar um cache DVC compartilhado em um servidor e 
usá-lo em um repositório rastreado por DVC:

```
# Cria uma pasta para se comportar como cache externo 
$ mkdir -p /home/shared/dvc-cache         
# Move o cache do repositório atual para o cache externo (opcional) 
$ mv .dvc/cache/* /home/shared/dvc-cache  
# Defina o cache do repositório rastreado por DVC como pasta criada acima 
$ dvc cache dir /home/shared/dvc-cache    
# Definir permissões de grupo em novos arquivos de cache 
$ dvc config cache.shared group           
# Habilite links simbólicos para evitar cópias do cache para o espaço de trabalho 
$ dvc config cache.type symlink
```

Ao inspecionar o arquivo `.dvc/config` no repositório, aparece a seguinte seção:

```
[cache]
    dir = /home/shared/dvc-cache
    shared = group
    type = symlink
```

O `cache.type` poderia ser reflink, hardlink, ou copies. Depois que qualquer alteração é feita no `cache.type`, 
o DVC precisa ser informado explicitamente sobre isso `dvc checkout --relink` antes que a alteração ocorra.