# Guia do Uso Rápido ptracks-pilot versão 0.1
Guia de uso do módulo de pilotagem do ptracks 


## Execução do piloto

Para executar o módulo, é necessário iniciar uma simulação de tráfego aereo. Detalhes de como proceder a inicialização de uma simulação podem ser enontradas [Clicando Aqui]( ptracks/README.md )
<Desta forma execute a simulação e especifique o exercício que será executado. No exemplo abaixo, o exercício COREDEMO é usado:>

<```>
<service ptracks start COREDEMO>
<```>

Agora é possível executar o piloto com o seguinte comando:

```
ptracks-pilot
```

Com isso inicia a interface de pilotagem, conforme a figura abaixo:

![alt tag] (https://github.com/contemmcm/ptracks/blob/master/doc/figs/pilot.png)


### Identificação dos itens de pilotagem (Contribuição do Alexandre Magno, Me.)

A seguir são descritos os principais componentes que constituem a tela de pilotagem mostrada anteriormente.

- Lista de Voos: processa e apresenta informações como: ICAO ID, Calssign, SSR, PRF, Latitude, Longitude, Proa, Velocidade, Razão e AGE, como mostra a figura abaixo. Essas informaçõpes são obtidas através de trocas de mensagens entre a IHM Piloto e o sistema “newton”.

![alt tag] (https://github.com/contemmcm/ptracks/blob/master/doc/figs/lista-voo.png)


- Fichas de Progressão de Voo (Strips): local que será apresentado o plano de voo das aeronaves no formato mostrado a seguir.

![alt tag] (https://github.com/contemmcm/ptracks/blob/master/doc/figs/strips.png)


- Status: apresenta o procedimento que a aeronave está cumprindo, como se pode observar na figura abaixo.

![alt tag] (https://github.com/contemmcm/ptracks/blob/master/doc/figs/status.png)
 

- Comandos: é composto por uma área de botões que compreende os comandos: Direção, Velocidade, Altitude, Trajetória, Dir. Fixo, Espera, Aproximação, Apx.Perdida, ILS, Pouso, Decolagem, Cancdela, SSR, SPI e EMG, distribuidos no layout mostrado a seguir.

![alt tag] (https://github.com/contemmcm/ptracks/blob/master/doc/figs/comandos.png)


- Execução de Comandos ( √ ): recebe uma cadeia de comandos a serem executados quando pressionado. Seu símbolo é mostrado abaixo juntamente com a linha de comando a ser executada de acordo com as configurações escolhidas através dos botões de comandos apresentados anteriormente.

![alt tag] (https://github.com/contemmcm/ptracks/blob/master/doc/figs/execucao.png)


- Histórico de Comandos: armazena os comandos executados que são mostrados na tela da figura abaixo.

![alt tag] (https://github.com/contemmcm/ptracks/blob/master/doc/figs/historico.png)


## Altereando comportamento da aeronave
Este capítulo se destina a apresentar os principais parâmetros de navegação que se pode alterar através do Piloto.

### Alterar a direção da aeronave
Para alterar a direção em que a aeronave está se descolocando na simulação, são necessários os seguintes passos:

1. Selecione a aeronave na lista de de Voos
![alt tag] (https://github.com/contemmcm/ptracks/blob/master/doc/figs/seleciona-aeronave.png)

2. Em comandos clique na opção "direção". Abrirá uma caixa de dialogo com opções de Sentido, Direção e Razão de Curva como a mostrada na figura a seguir.

3. Escolha as opções desejadas, observe que ao selecionar, aparece o comando correspondente a escolha feita, no espaço destacado da figura. 
![alt tag] (https://github.com/contemmcm/ptracks/blob/master/doc/figs/direcao.png)

4. Confirme clicando em "ok"

5. Observe que o campo "Execução de comandos" está com o comando escolhido. Execute o comando clicando no botão do " √ "
![alt tag] (https://github.com/contemmcm/ptracks/blob/master/doc/figs/direcao-comando.png)

6. O comando executado aparecerá na lista de histórico de comandos executados conforme pode ser visto na região em destaque da figura abaixo.
![alt tag] (https://github.com/contemmcm/ptracks/blob/master/doc/figs/historico-direcao.png)

### Alterar a velocidade da aeronave

1. Selecione a aeronave na lista de de Voos
2. Em comandos clique na opção "velocidade"
3. Abrirá uma caixa de dialogo com a opção de Velocidade, conforme pode ser visto na figura abaixo.
![alt tag]
4. Escolha a velocidade, observe que ao selecionar, aparece o comando correspondente a escolha feita. Note que a velocidade é limitada a um máximo determinada pelo tipo de aeronave selecionada.
5. Confirme clicando em "ok"
6. Observe que o campo "Execução de comandos" está com o comando escolhido. Execute o comando clicando no botão do " √ "
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

