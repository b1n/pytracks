# ptracks
Gerador de rotas para controle do trafégo aeréo, feito em Python 

Guia de usuário do módulo Pilot em [Português Brasileiro](https://github.com/contemmcm/ptracks/blob/master/user-guide_pt-br.md)

## Instalação (Ubuntu 14.04)

Para a instalar o Gerador de rotas para controle de tráfego aéreo, inicialize uma janela de terminal no Ubuntu.

### Requisistos

O correto funcionamento do gerador depende da isntalação dos seguintes módulos previamente instalados:

 * git
 * mpi4py
 * qt4

Para isso faça a seguinte sequência de instruções:

```
sudo apt-get install git python-mpi4py python-qt4
```

### Download

Por favor faça o  download  da última versão pelo GitHub:

```
git clone https://github.com/contemmcm/ptracks.git
```

### Procedimento de Instalação

Para instalar o Gerador de rotas realizar a seguinte sequência de comandos:

```
cd ptracks
sudo ./install
```

### Execução

Inicie a simulação e especifique o EXERCÍCIO que será executado, como no comando abaixo.

```
service ptracks start EXERCÍCIO
```

Os EXERCÍCIOs disponíveis são:

 * COREDEMO
 * FLOOD
 * FLOOD2
 * FLOODBSBR
 * SPRINT5
 * TEST1961

### Visualização da simulação

Abra um navegador e visite http://localhost:61000/ para visualizar a interface web da simulação

Em seguida para modificar o curso da aeronave na simulação, faça:

```
ptracks-pilot
```

<Acho que seria interessante colocar o link para o guia de pilotagem para alguém que queira maiores detalhes>

Para instruções detalhadas de como realizar a pilotagem das aeronaves simuladas [clique aqui](ptracks/doc/user-guide_pt-br.md)

### Saindo da simulação

Para encerrar a simulação, faça:

```
service ptracks stop
```
