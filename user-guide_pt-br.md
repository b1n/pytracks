# Guia do Uso Rápido ptracks-pilot versão 0.1
Guia de uso do módulo de pilotagem do ptracks 


## Execução do piloto

Para executar o módulo, é necessário iniciar uma simulação de tráfego aereo. Desta forma execute a simulação e especifique o exercício que será executado. No exemplo abaixo, o exercício COREDEMO é usado:

```
service ptracks start COREDEMO
```

Agora é possível executar o piloto, faça:

```
ptracks-pilot
```

Com isso inicia a interface de pilotagem

![alt tag] (https://github.com/contemmcm/ptracks/blob/master/pilot.png)


### Identificação dos itens de pilotagem (Contribuição do Alexandre Magno, Me.)


- Lista de Voos: processa e apresenta informações como: ICAO ID, Calssign, SSR, PRF, Latitude, Longitude, Proa, Velocidade, Razão e AGE. Essas informaçõpes são obtidas através de trocas de mensagens entre a IHM Piloto e o sistema “newton”.

![alt tag] (https://github.com/contemmcm/ptracks/blob/master/lista-voo.png)


- Fichas de Progessão de Voo (Strips): local que será apresentado o plano de voo das aeronaves.

![alt tag] (https://github.com/contemmcm/ptracks/blob/master/strips.png)


- Status: apresenta o procedimento que a aeronave está cumprindo.

![alt tag] (https://github.com/contemmcm/ptracks/blob/master/status.png)
 

- Comandos: será composto por uma área de botões que compreende os comandos: Direção, Velocidade, Altitude, Trajetória, Dir. Fixo, Espera, Aproximação, Apx.Perdida, ILS, Pouso, Decolagem, Cancdela, SSR, SPI e EMG.

![alt tag] (https://github.com/contemmcm/ptracks/blob/master/comandos.png)


- Execução de Comandos ( √ ): recebe uma cadeia de comandos a serem executados.

![alt tag] (https://github.com/contemmcm/ptracks/blob/master/execucao.png)


- Histórico de Comandos: armazena os comandos executados

![alt tag] (https://github.com/contemmcm/ptracks/blob/master/historico.png)



### Alterar a direção da aeronave

1. Selecione a aeronave na lista de de Voos
![alt tag] (https://github.com/contemmcm/ptracks/blob/master/seleciona-aeronave.png)

2. Em comandos clique na opção "direção"

3. Abrirá uma caixa de dialogo com opções de Sentido, Direção e Razão de Curva. Escolha as opções desejadas, observe que ao selecionar, aparece o comando correspondente a escolha feita 
![alt tag] (https://github.com/contemmcm/ptracks/blob/master/direcao.png)

4. Confirme clicando em "ok"

5. Observe que o campo "Execução de comandos" está com o comando escolhido. Execute o comando clicando no botão do "visto":
![alt tag] (https://github.com/contemmcm/ptracks/blob/master/direcao-comandos.png)

6. O comando executado aparecerá na lista de histórico de comandos executados

### Alterar a velocidade da aeronave

1. Selecione a aeronave na lista de de Voos
2. Em comandos clique na opção "velocidade"
3. Abrirá uma caixa de dialogo com a opção de Velocidade
4. Escolha a velocidade, observe que ao selecionar, aparece o comando correspondente a escolha feita
5. Confirme clicando em "ok"
6. Observe que o campo "Execução de comandos" está com o comando escolhido. Execute o comando clicando no botão do "visto"
7. O comando executado aparecerá na lista de histórico de comandos executados
8. Em Lista de voos, observe na aeronave que teve a velocidade alterada, a sua velocidade aumentando


### Alterar a altitude da aeronave

1. Selecione a aeronave na lista de de Voos
2. Em comandos clique na opção "altitude"
3. Abrirá uma caixa de dialogo com opções de Altitude e Razão
4. Escolha  as opções desejadas, observe que ao selecionar, aparece o comando correspondente a escolha feita
5. Confirme clicando em "ok"
6. Observe que o campo "Execução de comandos" está com o comando escolhido. Execute o comando clicando no botão do "visto"
7. O comando executado aparecerá na lista de histórico de comandos executados
8. Em Lista de voos, observe na aeronave que teve a altitude alterada, a sua velocidade aumentando

### Alterar a trajetória da aeronave

1. Selecione a aeronave na lista de de Voos
2. Em comandos clique na opção "trajetoria"
3. Abrirá uma caixa de dialogo para selecionar a trajetória
4. Escolha  a trajetória, observe que ao selecionar, aparece o comando correspondente a escolha feita
5. Confirme clicando em "ok"
6. Observe que o campo "Execução de comandos" está com o comando escolhido. Execute o comando clicando no botão do "visto"
7. O comando executado aparecerá na lista de histórico de comandos executados


### Alterar o dir.fixo da aeronave

Apesar de disponível, não exibe as opções

### Alterar a espera da aeronave

1. Selecione a aeronave na lista de de Voos
2. Em comandos clique na opção "espera"
3. Abrirá uma caixa de dialogo para selecionar a trajetória
4. Escolha  a trajetória, observe que ao selecionar, aparece o comando correspondente a escolha feita
5. Confirme clicando em "ok"
6. Observe que o campo "Execução de comandos" está com o comando escolhido. Execute o comando clicando no botão do "visto"
7. O comando executado aparecerá na lista de histórico de comandos executados


Observações:

apromixação apx.perdida, ils, decolagem, cancela, SSR, SPI e EMG estão desabilitados, assim como os botões abaixo do histórico dos comandos

pouso está habilitado mas nenhum comando é exibido.


