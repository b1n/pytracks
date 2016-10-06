# ptracks
Gerador de rotas para controle do trafégo aeréo, feito em Python 

## Instalação (Ubuntu 14.04)


### Requisistos

 * git
 * mpi4py
 * qt4

```
sudo apt-get install git python-mpi4py python-qt4
```

### Download

Por favor faça o  download  da última versão pelo GitHub:

```
git clone https://github.com/contemmcm/ptracks.git
```

### Procedimento de Instalação


```
cd ptracks
sudo ./install
```

### Execução

Inicie a simulação e especifique o exercício que será executado. No exemplo abaixo, o exercício COREDEMO é usado:

```
service ptracks start COREDEMO
```

Abra um navegador e visite http://localhost:61000/ para visualizar a interface web da simulação

Em seguida para modificar o curso da aeronave na simulação, faça:

```
ptracks-pilot
```

Para encerrar a simulação, faça:

```
service ptracks stop
```
