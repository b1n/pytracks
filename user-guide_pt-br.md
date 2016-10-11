# Guia do Uso Rápido ptracks-pilot versão 0.1
Guia de uso do módulo de pilotagem do ptracks 

Documento versão: 0.01 (checar a necessidade de versão do documento)

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

### Identificação dos itens de pilotagem (Contribuição do Alexandre Magno)


1. Lista de Voos: processa e apresenta informações como: ICAO ID, Calssign, SSR, PRF, Latitude, Longitude, Proa, Velocidade, Razão e AGE. Essas informaçõpes são obtidas através de trocas de mensagens entre a IHM Piloto e o sistema “newton”.

2. Fichas de Progessão de Voo (Strips): local que será apresentado o plano de voo das aeronaves.

3. Status: apresenta o procedimento que a aeronave está cumprindo.
 
4. Comandos: será composto por uma área de botões que compreende os comandos: Direção, Velocidade, Altitude, Trajetória, Dir. Fixo, Espera, Aproximação, Apx.Perdida, ILS, Pouso, Decolagem, Cancdela, SSR, SPI e EMG.

5. Execução de Comandos ( √  ): recebe uma cadeia de comandos a serem executados.
Histórico de Comandos: armazena os comandos executados

(inserir a tela com as identificações )


### Alterar a direção da aeronave

1. Selecione a aeronave na lista de de Voos
2. Em comandos clique na opção "direção"
3. Abrirá uma caixa de dialogo com opções de Sentido, Direção e Razão de Curva
(inserir a imagem)
4. Escolha as opções desejadas, observe que ao selecionar, aparece o comando correspondente a escolha feita
(inserir a imagem)
5. Confirme clicando em "ok"
6. Observe que o campo "Execução de comandos" está com o comando escolhido. Execute o comando clicando no botão do "visto"
7. O comando executado aparecerá na lista de histórico de comandos executados

### Alterar a velocidade da aeronave

1. Selecione a aeronave na lista de de Voos
2. Em comandos clique na opção "velocidade"
3. Abrirá uma caixa de dialogo com a opção de Velocidade
(inserir a imagem)
4. Escolha a velocidade, observe que ao selecionar, aparece o comando correspondente a escolha feita
(inserir a imagem)
5. Confirme clicando em "ok"
6. Observe que o campo "Execução de comandos" está com o comando escolhido. Execute o comando clicando no botão do "visto"
7. O comando executado aparecerá na lista de histórico de comandos executados
8. Em Lista de voos, observe na aeronave que teve a velocidade alterada, a sua velocidade aumentando (inserir imagem)


### Alterar a altitude da aeronave

1. Selecione a aeronave na lista de de Voos
2. Em comandos clique na opção "altitude"
3. Abrirá uma caixa de dialogo com opções de Altitude e Razão
(inserir a imagem)
4. Escolha  as opções desejadas, observe que ao selecionar, aparece o comando correspondente a escolha feita
(inserir a imagem)
5. Confirme clicando em "ok"
6. Observe que o campo "Execução de comandos" está com o comando escolhido. Execute o comando clicando no botão do "visto"
7. O comando executado aparecerá na lista de histórico de comandos executados
8. Em Lista de voos, observe na aeronave que teve a altitude alterada, a sua velocidade aumentando (inserir imagem)

### Alterar a trajetória da aeronave

1. Selecione a aeronave na lista de de Voos
2. Em comandos clique na opção "trajetoria"
3. Abrirá uma caixa de dialogo para selecionar a trajetória
(inserir a imagem)
4. Escolha  a trajetória, observe que ao selecionar, aparece o comando correspondente a escolha feita
(inserir a imagem)
5. Confirme clicando em "ok"
6. Observe que o campo "Execução de comandos" está com o comando escolhido. Execute o comando clicando no botão do "visto"
7. O comando executado aparecerá na lista de histórico de comandos executados


### Alterar o dir.fixo da aeronave

Apesar de disponível, não exibe as opções

### Alterar a espera da aeronave

1. Selecione a aeronave na lista de de Voos
2. Em comandos clique na opção "espera"
3. Abrirá uma caixa de dialogo para selecionar a trajetória
(inserir a imagem)
4. Escolha  a trajetória, observe que ao selecionar, aparece o comando correspondente a escolha feita
(inserir a imagem)
5. Confirme clicando em "ok"
6. Observe que o campo "Execução de comandos" está com o comando escolhido. Execute o comando clicando no botão do "visto"
7. O comando executado aparecerá na lista de histórico de comandos executados


Observações:

apromixação apx.perdida, ils, decolagem, cancela, SSR, SPI e EMG estão desabilitados, assim como os botões abaixo do histórico dos comandos

pouso está habilitado mas nenhum comando é exibido, talvez apenas o botão esteja ativo, sem função


