#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
parse_utils

DOCUMENT ME!

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2015/out  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging

# PyQt library
from PyQt4 import QtCore

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------

def parse_aerodromo(f_element):
    """
    helper function to parse xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_aerodromo:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case of descrição (nome)
    if "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()
        # M_LOG.debug(u"ldct_tmp['descricao']:[{}]".format(ldct_tmp["descricao"]))

    # handle case of elevação
    elif "elevacao" == f_element.tagName():
        ldct_tmp["elevacao"] = f_element.text()

    # handle case of declmag
    elif "declmag" == f_element.tagName():
        ldct_tmp["declmag"] = f_element.text()

    # handle case of coord
    elif "coord" == f_element.tagName():

        # inicia o dicionário de dados
        ldct_crd = {}

        # obtém o primeiro nó da sub-árvore
        l_node = f_element.firstChild()
        assert l_node is not None

        # percorre a sub-árvore
        while not l_node.isNull():

            # tenta converter o nó em um elemento
            l_element = l_node.toElement()
            assert l_element is not None

            # o nó é um elemento ?
            if not l_element.isNull():

                # atualiza o dicionário de dados
                ldct_crd.update(parse_coord(l_element))

            # próximo nó
            l_node = l_node.nextSibling()
            assert l_node is not None

        # atualiza o dicionário com a coordenada
        ldct_tmp["coord"] = ldct_crd

    # handle case of posição
    elif "pista" == f_element.tagName():

        # inicia o dicionário de dados
        ldct_pst = {}

        # read identification if available
        if f_element.hasAttribute("nPst"):
            ldct_pst["nPst"] = str(f_element.attribute("nPst"))

        # obtém o primeiro nó da sub-árvore
        l_node = f_element.firstChild()
        assert l_node is not None

        # percorre a sub-árvore
        while not l_node.isNull():

            # tenta converter o nó em um elemento
            l_element = l_node.toElement()
            assert l_element is not None

            # o nó é um elemento ?
            if not l_element.isNull():

                # atualiza o dicionário de dados
                ldct_pst.update(parse_pista(l_element))

            # próximo nó
            l_node = l_node.nextSibling()
            assert l_node is not None

        # atualiza o dicionário com a pista
        ldct_tmp["pista"] = ldct_pst

    # logger
    # M_LOG.info("parse_aerodromo:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------

def parse_aeronave(f_element, f_hora_ini):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_aeronave:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case of indicativo (ID)
    if "indicativo" == f_element.tagName():
        ldct_tmp["indicativo"] = f_element.text()

    # handle case of descrição
    elif "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()

    # handle case of designador
    elif "designador" == f_element.tagName():
        ldct_tmp["designador"] = f_element.text()

    # handle case of ssr
    elif "ssr" == f_element.tagName():
        ldct_tmp["ssr"] = f_element.text()

    # handle case of origem
    elif "origem" == f_element.tagName():
        ldct_tmp["origem"] = f_element.text()

    # handle case of destino
    elif "destino" == f_element.tagName():
        ldct_tmp["destino"] = f_element.text()

    # handle case of procedimen
    elif "procedimento" == f_element.tagName():
        ldct_tmp["procedimento"] = f_element.text()

    # handle case of nivel
    elif "nivel" == f_element.tagName():
        ldct_tmp["nivel"] = f_element.text()

    # handle case of altitude
    elif "altitude" == f_element.tagName():
        ldct_tmp["altitude"] = f_element.text()

    # handle case of velocidade
    elif "velocidade" == f_element.tagName():
        ldct_tmp["velocidade"] = f_element.text()

    # handle case of proa
    elif "proa" == f_element.tagName():
        ldct_tmp["proa"] = f_element.text()

    # handle case of pilotagem
    elif "pilotagem" == f_element.tagName():
        ldct_tmp["pilotagem"] = f_element.text()

    # handle case of temptrafeg
    elif "temptrafeg" == f_element.tagName():
        # salva a tupla com a hora inicial corrigida
        ldct_tmp["temptrafeg"] = (f_element.text(), f_hora_ini)

    # handle case of numsg
    elif "numsg" == f_element.tagName():
        ldct_tmp["numsg"] = f_element.text()

    # handle case of tempmsg
    elif "tempmsg" == f_element.tagName():
        ldct_tmp["tempmsg"] = f_element.text()

    # handle case of rvsm
    elif "rvsm" == f_element.tagName():
        ldct_tmp["rvsm"] = f_element.text()

    # handle case of rota
    elif "rota" == f_element.tagName():
        ldct_tmp["rota"] = f_element.text()

    # handle case of eet
    elif "eet" == f_element.tagName():
        ldct_tmp["eet"] = f_element.text()

    # handle case of posição
    elif "posicao" == f_element.tagName():

        # inicia o dicionário de dados
        ldct_pos = {}

        # obtém o primeiro nó da sub-árvore
        l_node = f_element.firstChild()
        assert l_node is not None

        # percorre a sub-árvore
        while not l_node.isNull():

            # tenta converter o nó em um elemento
            l_element = l_node.toElement()
            assert l_element is not None

            # o nó é um elemento ?
            if not l_element.isNull():

                # atualiza o dicionário de dados
                ldct_pos.update(parse_posicao(l_element))

            # próximo nó
            l_node = l_node.nextSibling()
            assert l_node is not None

        # atualiza o dicionário com a posição
        ldct_tmp["posicao"] = ldct_pos

    # logger
    # M_LOG.info("parse_aeronave:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------

def parse_aproximacao(f_element):
    """
    helper function to parse xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_aproximacao:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case of nome
    if "nome" == f_element.tagName():
        ldct_tmp["nome"] = f_element.text()

    # handle case of aeródromo
    if "aerodromo" == f_element.tagName():
        ldct_tmp["aerodromo"] = f_element.text()

    # handle case of pista
    elif "pista" == f_element.tagName():
        ldct_tmp["pista"] = f_element.text()

    # handle case of flag ILS
    elif "ils" == f_element.tagName():
        ldct_tmp["ils"] = f_element.text()

    # handle case of flag apxPerdida
    elif "aproxperd" == f_element.tagName():
        ldct_tmp["aproxperd"] = f_element.text()

    # handle case of número da espera
    elif "espera" == f_element.tagName():
        ldct_tmp["espera"] = f_element.text()

    # handle case of break-point
    elif "breakpoint" == f_element.tagName():

        # inicia o dicionário de dados
        ldct_brk = {}

        # read identification if available
        if f_element.hasAttribute("nBrk"):
            ldct_brk["nBrk"] = int(f_element.attribute("nBrk"))

        # obtém o primeiro nó da sub-árvore
        l_node = f_element.firstChild()
        assert l_node is not None

        # percorre a sub-árvore
        while not l_node.isNull():

            # tenta converter o nó em um elemento
            l_element = l_node.toElement()
            assert l_element is not None

            # o nó é um elemento ?
            if not l_element.isNull():

                # atualiza o dicionário de dados
                ldct_brk.update(parse_breakpoint(l_element))

            # próximo nó
            l_node = l_node.nextSibling()
            assert l_node is not None

        # atualiza o dicionário com o break-point
        ldct_tmp["breakpoint"] = ldct_brk

    # logger
    # M_LOG.info("parse_aproximacao:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------

def parse_breakpoint(f_element):
    """
    helper function to parse xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_breakpoint:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case of altitude
    if "altitude" == f_element.tagName():
        ldct_tmp["altitude"] = f_element.text()

    # handle case of velocidade
    elif "velocidade" == f_element.tagName():
        ldct_tmp["velocidade"] = f_element.text()

    # handle case of razdes
    elif "razdes" == f_element.tagName():
        ldct_tmp["razdes"] = f_element.text()

    # handle case of razsub
    elif "razsub" == f_element.tagName():
        ldct_tmp["razsub"] = f_element.text()

    # handle case of procedimento
    elif "procedimento" == f_element.tagName():
        ldct_tmp["procedimento"] = f_element.text()

    # handle case of coord
    elif "coord" == f_element.tagName():

        # inicia o dicionário de dados
        ldct_crd = {}

        # obtém o primeiro nó da sub-árvore
        l_node = f_element.firstChild()
        assert l_node is not None

        # percorre a sub-árvore
        while not l_node.isNull():

            # tenta converter o nó em um elemento
            l_element = l_node.toElement()
            assert l_element is not None

            # o nó é um elemento ?
            if not l_element.isNull():

                # atualiza o dicionário de dados
                ldct_crd.update(parse_coord(l_element))

            # próximo nó
            l_node = l_node.nextSibling()
            assert l_node is not None

        # atualiza o dicionário com a coordenada
        ldct_tmp["coord"] = ldct_crd

    # logger
    # M_LOG.info("parse_breakpoint:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------

def parse_coord(f_element):
    """
    helper function to parse xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_coord:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case tipo de coordenada
    if "tipo" == f_element.tagName():
        ldct_tmp["tipo"] = f_element.text()

    # handle case of latitude/X/campoA
    elif "campoA" == f_element.tagName():
        ldct_tmp["campoA"] = f_element.text()

    # handle case of longitude/Y/campoB
    elif "campoB" == f_element.tagName():
        ldct_tmp["campoB"] = f_element.text()

    # handle case of campoC
    elif "campoC" == f_element.tagName():
        ldct_tmp["campoC"] = f_element.text()

    # handle case of campoD
    elif "campoD" == f_element.tagName():
        ldct_tmp["campoD"] = f_element.text()

    # logger
    # M_LOG.info("parse_coord:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------

def parse_espera(f_element):
    """
    helper function to parse xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_espera:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case of fixo (descrição)
    if "fixo" == f_element.tagName():
        ldct_tmp["fixo"] = f_element.text()

    # handle case of sentido
    elif "sentido" == f_element.tagName():
        ldct_tmp["sentido"] = f_element.text()

    # handle case of rumo
    elif "rumo" == f_element.tagName():
        ldct_tmp["rumo"] = f_element.text()

    # handle case of break-point
    elif "breakpoint" == f_element.tagName():

        # inicia o dicionário de dados
        ldct_brk = {}

        # read identification if available
        if f_element.hasAttribute("nBrk"):
            ldct_brk["nBrk"] = int(f_element.attribute("nBrk"))

        # obtém o primeiro nó da sub-árvore
        l_node = f_element.firstChild()
        assert l_node is not None

        # percorre a sub-árvore
        while not l_node.isNull():

            # tenta converter o nó em um elemento
            l_element = l_node.toElement()
            assert l_element is not None

            # o nó é um elemento ?
            if not l_element.isNull():

                # atualiza o dicionário de dados
                ldct_brk.update(parse_breakpoint(l_element))

            # próximo nó
            l_node = l_node.nextSibling()
            assert l_node is not None

        # atualiza o dicionário com o break-point
        ldct_tmp["breakpoint"] = ldct_brk

    # logger
    # M_LOG.info("parse_espera:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------

def parse_exercicio(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_exercicio:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case of descrição
    if "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()

    # handle case of hora início
    elif "horainicio" == f_element.tagName():
        ldct_tmp["horainicio"] = f_element.text()

    # handle case of meteorologia
    elif "meteorologia" == f_element.tagName():

        # inicia o dicionário de dados
        ldct_met = {}

        # obtém o primeiro nó da sub-árvore
        lo_node = f_element.firstChild()
        assert lo_node is not None

        # percorre a sub-árvore
        while not lo_node.isNull():

            # tenta converter o nó em um elemento
            lo_element = lo_node.toElement()
            assert lo_element is not None

            # o nó é um elemento ?
            if not lo_element.isNull():

                # atualiza o dicionário de dados
                ldct_met.update(parse_meteorologia(lo_element))

            # próximo nó
            lo_node = lo_node.nextSibling()
            assert lo_node is not None

        # atualiza o dicionário com a meteorologia
        ldct_tmp["meteorologia"] = ldct_met
    '''
    # handle case of consoles
    elif "consoles" == f_element.tagName():

        # inicia a lista de consoles
        l_lstCon = []

        l_node_list = f_element.elementsByTagName("console"))
        M_LOG.debug("l_node_list.len (console): %d" % l_node_list.length())

        # obtém o primeiro nó da sub-árvore
        lo_node = f_element.firstChild()
        assert(lo_node is not None

        # percorre a sub-árvore
        while not lo_node.isNull():

            # tenta converter o nó em um elemento
            lo_element = lo_node.toElement()
            assert lo_element is not None

            # o nó é um elemento ?
            if not lo_element.isNull():

                # atualiza o dicionário de dados
                l_lstCon.append(parseConsole(lo_element))

            # próximo nó
            lo_node = lo_node.nextSibling()
            assert lo_node is not None

        # atualiza o dicionário com a lista de consoles
        ldct_tmp["consoles"] = l_lstCon

    # handle case of mapas
    elif "mapas" == f_element.tagName():

        # inicia a lista de mapas
        l_lstMap = []

        l_node_list = f_element.elementsByTagName("subMapa"))
        M_LOG.debug("l_node_list.len (subMapa): %d" % l_node_list.length())

        for li_ndx in xrange(l_node_list.length()):

            lo_element = l_node_list.at(li_ndx).toElement()
            assert lo_element is not None

            # faz o parse do elemento
            l_lstMap.append(parse_mapa(lo_element))

        # atualiza o dicionário com a lista de consoles
        ldct_tmp["mapas"] = l_lstMap

    # handle case of situação
    elif "situacao" == f_element.tagName():

        # inicia o dicionário de situacao
        ldctSit = {}

        # obtém o primeiro nó da sub-árvore
        lo_node = f_element.firstChild()
        assert lo_node is not None

        # percorre a sub-árvore
        while(not lo_node.isNull()):

            # tenta converter o nó em um elemento
            lo_element = lo_node.toElement()
            assert lo_element is not None

            # o nó é um elemento ?
            if not lo_element.isNull():

                # faz o parse do elemento
                ldctSit.update(parse_situacao(lo_element))

            # próximo nó
            lo_node = lo_node.nextSibling()
            assert lo_node is not None

        # atualiza o dicionário com a lista de consoles
        ldct_tmp["situacao"] = ldctSit
    '''
    # logger
    # M_LOG.info("parse_exercicio:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------

def parse_fixo(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_fixo:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case of indicativo
    if "indicativo" == f_element.tagName():
        ldct_tmp["indicativo"] = f_element.text()

    # handle case of descrição
    elif "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()

    # handle case of tipo
    elif "tipo" == f_element.tagName():
        ldct_tmp["tipo"] = f_element.text()

    # handle case of posição
    elif "coord" == f_element.tagName():

        # inicia o dicionário de dados
        ldct_pos = {}

        # obtém o primeiro nó da sub-árvore
        l_node = f_element.firstChild()
        assert l_node is not None

        # percorre a sub-árvore
        while not l_node.isNull():

            # tenta converter o nó em um elemento
            l_element = l_node.toElement()
            assert l_element is not None

            # o nó é um elemento ?
            if not l_element.isNull():

                # atualiza o dicionário de dados
                ldct_pos.update(parse_coord(l_element))

            # próximo nó
            l_node = l_node.nextSibling()
            assert l_node is not None

        # atualiza o dicionário com a posição
        ldct_tmp["coord"] = ldct_pos

    # handle case of VOR
    # elif "VOR" == f_element.tagName():
        # ldct_tmp["VOR"] = f_element.text()

    # handle case of NDB
    # elif "NDB" == f_element.tagName():
        # ldct_tmp["NDB"] = f_element.text()

    # handle case of DME
    # elif "DME" == f_element.tagName():
        # ldct_tmp["DME"] = f_element.text()

    # handle case of freqüência
    # elif "frequencia" == f_element.tagName():
        # ldct_tmp["frequencia"] = f_element.text()

    # logger
    # M_LOG.info("parse_fixo:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
'''
def parse_hora(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_hora:>>")

    # inicia o dicionário de dados
    ldct_data = {}

    # handle case of hora
    if "hora" == f_element.tagName():
        ldct_data["hora"] = f_element.text()

    # handle case of minutos
    elif "min" == f_element.tagName():
        ldct_data["min"] = f_element.text()

    # logger
    # M_LOG.info("parse_hora:<<")

    # retorna o dicionário de dados
    return ldct_data
'''
# -------------------------------------------------------------------------------------------------

def parse_ils(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_ils:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case of aerodromo
    if "aerodromo" == f_element.tagName():
        ldct_tmp["aerodromo"] = f_element.text()

    # handle case of pista
    elif "pista" == f_element.tagName():
        ldct_tmp["pista"] = f_element.text()

    # handle case of altitudegp
    elif "altitudegp" == f_element.tagName():
        ldct_tmp["altitudegp"] = f_element.text()

    # handle case of angrampa
    elif "angrampa" == f_element.tagName():
        ldct_tmp["angrampa"] = f_element.text()

    # handle case of altitmapt
    elif "altitmapt" == f_element.tagName():
        ldct_tmp["altitmapt"] = f_element.text()

    # handle case of procedimento
    elif "procedimento" == f_element.tagName():
        ldct_tmp["procedimento"] = f_element.text()

    # handle case of break-point
    elif "breakpoint" == f_element.tagName():

        # inicia o dicionário de dados
        ldct_brk = {}

        # read identification if available
        if f_element.hasAttribute("nBrk"):
            ldct_brk["nBrk"] = int(f_element.attribute("nBrk"))

        # obtém o primeiro nó da sub-árvore
        l_node = f_element.firstChild()
        assert l_node is not None

        # percorre a sub-árvore
        while not l_node.isNull():

            # tenta converter o nó em um elemento
            l_element = l_node.toElement()
            assert l_element is not None

            # o nó é um elemento ?
            if not l_element.isNull():

                # atualiza o dicionário de dados
                ldct_brk.update(parse_breakpoint(l_element))

            # próximo nó
            l_node = l_node.nextSibling()
            assert l_node is not None

        # atualiza o dicionário com o break-point
        ldct_tmp["breakpoint"] = ldct_brk

    # logger
    # M_LOG.info("parse_ils:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
'''
def parse_mapa(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_mapa:>>")

    # handle case of subMapa
    if "subMapa" == f_element.tagName():
        li_num = f_element.text()

    # logger
    # M_LOG.info("parse_mapa:<<")

    # retorna o número do mapa
    return li_num
'''
# -------------------------------------------------------------------------------------------------

def parse_meteorologia(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_meteorologia:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case of altitude de transição
    if "alttrans" == f_element.tagName():
        ldct_tmp["alttrans"] = f_element.text()

    # handle case of indicativo de condição meteorológica
    elif "condmet" == f_element.tagName():
        ldct_tmp["condmet"] = f_element.text()

    # handle case of limite inferior do QNH
    elif "infqnh" == f_element.tagName():
        ldct_tmp["infqnh"] = f_element.text()

    # handle case of número da formação meteorológica
    elif "numForm" == f_element.tagName():
        ldct_tmp["numForm"] = f_element.text()

    # handle case of pendente do QNH
    elif "pendqnh" == f_element.tagName():
        ldct_tmp["pendqnh"] = f_element.text()

    # handle case of QNH
    elif "qnh" == f_element.tagName():
        ldct_tmp["qnh"] = f_element.text()

    # handle case of limite superior do QNH
    elif "supqnh" == f_element.tagName():
        ldct_tmp["supqnh"] = f_element.text()

    # logger
    # M_LOG.info("parse_meteorologia:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------

def parse_performance(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_performance:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case of descrição
    if "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()

    # handle case of esteira
    elif "esteira" == f_element.tagName():
        ldct_tmp["esteira"] = f_element.text()

    # handle case of teto de serviço (DIST) / altitude máxima
    elif "tetosv" == f_element.tagName():
        ldct_tmp["tetosv"] = f_element.text()

    # handle case of faixa
    elif "faixa" == f_element.tagName():
        ldct_tmp["faixa"] = f_element.text()

    # handle case of velocidade de decolagem (VELO) / velocidade mínima de decolagem
    elif "veldec" == f_element.tagName():
        ldct_tmp["veldec"] = f_element.text()

    # handle case of velocidade de subida na decolagem (VELO) / velocidade de subida
    elif "velsbdec" == f_element.tagName():
        ldct_tmp["velsbdec"] = f_element.text()

    # handle case of velocidade de aproximação (VELO) / velocidade máxima de pouso
    elif "velapx" == f_element.tagName():
        ldct_tmp["velapx"] = f_element.text()

    # handle case of velocidade de cruzeiro (VELO)
    elif "velcruz" == f_element.tagName():
        ldct_tmp["velcruz"] = f_element.text()

    # handle case of velocidade máxima de cruzeiro (VELO) / velocidade máxima
    elif "velmxcrz" == f_element.tagName():
        ldct_tmp["velmxcrz"] = f_element.text()

    # handle case of razão de subida na decolagem (VELO)
    elif "rzsubdec" == f_element.tagName():
        ldct_tmp["rzsubdec"] = f_element.text()

    # handle case of razão máxima subida na decolagem (VELO)
    elif "rzmxsbdec" == f_element.tagName():
        ldct_tmp["rzmxsbdec"] = f_element.text()

    # handle case of razão de subida de cruzeiro (VELO) / razão de subida
    elif "rzsbcrz" == f_element.tagName():
        ldct_tmp["rzsbcrz"] = f_element.text()

    # handle case of razão máxima de subida de cruzeiro (VELO)
    elif "rzmxsbcrz" == f_element.tagName():
        ldct_tmp["rzmxsbcrz"] = f_element.text()

    # handle case of razão de descida na aproximação (VELO)
    elif "rzdescapx" == f_element.tagName():
        ldct_tmp["rzdescapx"] = f_element.text()

    # handle case of razão máxima descida na aproximação (VELO)
    elif "rzmxdesapx" == f_element.tagName():
        ldct_tmp["rzmxdesapx"] = f_element.text()

    # handle case of razão de descida de cruzeiro (VELO) / razão de descida
    elif "rzdescrz" == f_element.tagName():
        ldct_tmp["rzdescrz"] = f_element.text()

    # handle case of razão máxima descida de cruzeiro (VELO) / razão máxima de descida
    elif "rzmxdescrz" == f_element.tagName():
        ldct_tmp["rzmxdescrz"] = f_element.text()

    # handle case of razão de variação de velocidade (aceleração) (ACEL) / aceleração de vôo
    elif "razvarvel" == f_element.tagName():
        ldct_tmp["razvarvel"] = f_element.text()

    # handle case of razão máxima variação de velocidade (aceleração) (ACEL)
    elif "rzmxvarvel" == f_element.tagName():
        ldct_tmp["rzmxvarvel"] = f_element.text()
    '''
    # handle case of desaceleração de vôo
    elif "desacelcrz" == f_element.tagName():
        ldct_tmp["desacelcrz"] = f_element.text()

    # handle case of aceleração mínima de decolagem
    elif "acelmindep" == f_element.tagName():
        ldct_tmp["acelmindep"] = f_element.text()

    # handle case of desaceleração máxima de pouso
    elif "desacelmaxarr" == f_element.tagName():
        ldct_tmp["desacelmaxarr"] = f_element.text()

    # handle case of velocidade de circuito
    elif "velckt" == f_element.tagName():
        ldct_tmp["velckt"] = f_element.text()

    # handle case of altitude de circuito
    elif "altckt" == f_element.tagName():
        ldct_tmp["altckt"] = f_element.text()

    # handle case of circuito
    elif "numckt" == f_element.tagName():
        ldct_tmp["numckt"] = f_element.text()

    # handle case of razão de curva em rota
    elif "razcrvrot" == f_element.tagName():
        ldct_tmp["razcrvrot"] = f_element.text()

    # handle case of razão de curva no solo
    elif "razcrvslo" == f_element.tagName():
        ldct_tmp["razcrvslo"] = f_element.text()

    # handle case of razão de curva no tráfego
    elif "razcrvtrf" == f_element.tagName():
        ldct_tmp["razcrvtrf"] = f_element.text()

    # handle case of velocidade máxima de taxi
    elif "velmaxtax" == f_element.tagName():
        ldct_tmp["velmaxtax"] = f_element.text()
    '''
    # logger
    # M_LOG.info("parse_performance:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------

def parse_pista(f_element):
    """
    helper function to parse xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_pista:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case of identificação (ID)
    if "nPst" == f_element.tagName():
        ldct_tmp["nPst"] = f_element.text()

    # handle case of comprimento
    # elif "comprimento" == f_element.tagName():
        # ldct_tmp["comprimento"] = f_element.text()

    # handle case of largura
    # elif "largura" == f_element.tagName():
        # ldct_tmp["largura"] = f_element.text()

    # handle case of rumo
    elif "rumo" == f_element.tagName():
        ldct_tmp["rumo"] = f_element.text()

    # handle case of coord
    elif "coord" == f_element.tagName():

        # inicia o dicionário de dados
        ldct_coord = {}

        # obtém o primeiro nó da sub-árvore
        l_node = f_element.firstChild()
        assert l_node is not None

        # percorre a sub-árvore
        while not l_node.isNull():

            # tenta converter o nó em um elemento
            l_element = l_node.toElement()
            assert l_element is not None

            # o nó é um elemento ?
            if not l_element.isNull():

                # atualiza o dicionário de dados
                ldct_coord.update(parse_coord(l_element))

            # próximo nó
            l_node = l_node.nextSibling()
            assert l_node is not None

        # atualiza o dicionário com a pista
        ldct_tmp["coord"] = ldct_coord

    # logger
    # M_LOG.info("parse_pista:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------

def parse_posicao(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_posicao:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case tipo de coordenada
    if "tipocoord" == f_element.tagName():
        ldct_tmp["tipocoord"] = f_element.text()

    # handle case of X/campoA
    elif "latitude" == f_element.tagName():
        ldct_tmp["latitude"] = f_element.text()

    # handle case of Y/campoB
    elif "longitude" == f_element.tagName():
        ldct_tmp["longitude"] = f_element.text()

    # handle case of Z/campoC
    elif "campoc" == f_element.tagName():
        ldct_tmp["campoc"] = f_element.text()

    # handle case of campoD
    elif "campod" == f_element.tagName():
        ldct_tmp["campod"] = f_element.text()

    # logger
    # M_LOG.info("parse_posicao:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------

def parse_radar(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_radar:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case of ID
    if "indicativo" == f_element.tagName():
        ldct_tmp["indicativo"] = f_element.text()

    # handle case of descrição
    elif "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()

    # handle case of elevação
    elif "elevacao" == f_element.tagName():
        ldct_tmp["elevacao"] = f_element.text()

    # handle case of alcancehor
    elif "alcancehor" == f_element.tagName():
        ldct_tmp["alcancehor"] = f_element.text()

    # handle case of alcancever
    elif "alcancever" == f_element.tagName():
        ldct_tmp["alcancever"] = f_element.text()

    # handle case of alcancesec
    elif "alcancesec" == f_element.tagName():
        ldct_tmp["alcancesec"] = f_element.text()

    # handle case of angmin
    elif "angmin" == f_element.tagName():
        ldct_tmp["angmin"] = f_element.text()

    # handle case of angmax
    elif "angmax" == f_element.tagName():
        ldct_tmp["angmax"] = f_element.text()

    # handle case of posição
    elif "posicao" == f_element.tagName():

        # inicia o dicionário de dados
        ldct_pos = {}

        # obtém o primeiro nó da sub-árvore
        l_node = f_element.firstChild()
        assert l_node is not None

        # percorre a sub-árvore
        while not l_node.isNull():

            # tenta converter o nó em um elemento
            l_element = l_node.toElement()
            assert l_element is not None

            # o nó é um elemento ?
            if not l_element.isNull():

                # atualiza o dicionário de dados
                ldct_pos.update(parse_posicao(l_element))

            # próximo nó
            l_node = l_node.nextSibling()
            assert l_node is not None

        # atualiza o dicionário com a posição
        ldct_tmp["posicao"] = ldct_pos

    # logger
    # M_LOG.info("parse_radar:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------

def parse_root_element(f_element):
    """
    helper function to parse xml entries

    @param f_element: root element to parse
    """
    # logger
    # M_LOG.info("parse_root_element:>>")

    # inicia o dicionário de dados
    ldct_root = {}

    # salva o tagName
    # ldct_root["tagName"] = f_element.tagName()
    ldct_root["tagName"] = f_element.tagName()

    # para todos os atributos...
    for li_ndx in xrange(f_element.attributes().size()):

        # obtém o atributo
        l_attr = f_element.attributes().item(li_ndx).toAttr()

        # associa o atributo ao valor
        # ldct_root[str(l_attr.name()).upper()] = l_attr.value()
        ldct_root[str(l_attr.name()).upper()] = l_attr.value()

    # logger
    # M_LOG.info("parse_root_element:<<")

    # retorna o dicionário de dados
    return ldct_root

# -------------------------------------------------------------------------------------------------
'''
def parse_situacao(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_situacao:>>")

    # inicia o dicionário de dados
    ldct_data = {}

    # handle case of hora de início
    if "horaIni" == f_element.tagName():

        # inicia o dicionário de situacao
        ldct_hor = {}

        # obtém o primeiro nó da sub-árvore
        lo_node = f_element.firstChild()
        assert lo_node is not None

        # percorre a sub-árvore
        while(not lo_node.isNull()):

            # tenta converter o nó em um elemento
            lo_element = lo_node.toElement()

            assert lo_element is not None

            # o nó é um elemento ?
            if not lo_element.isNull():

                # faz o parse do elemento
                ldct_hor.update(parse_hora(lo_element))

            # próximo nó
            lo_node = lo_node.nextSibling()
            assert lo_node is not None

        # atualiza o dicionário com a lista de consoles
        ldct_data["horaIni"] = ldct_hor

    # logger
    # M_LOG.info("parse_situacao:<<")

    # retorna o dicionário de dados
    return ldct_data
'''
# -------------------------------------------------------------------------------------------------

def parse_subida(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_subida:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case of nome (descrição)
    if "nome" == f_element.tagName():
        ldct_tmp["nome"] = f_element.text()

    # handle case of aeródromo
    elif "aerodromo" == f_element.tagName():
        ldct_tmp["aerodromo"] = f_element.text()

    # handle case of pista
    elif "pista" == f_element.tagName():
        ldct_tmp["pista"] = f_element.text()

    # handle case of break-point
    elif "breakpoint" == f_element.tagName():

        # inicia o dicionário de dados
        ldct_brk = {}

        # read identification if available
        if f_element.hasAttribute("nBrk"):
            ldct_brk["nBrk"] = int(f_element.attribute("nBrk"))

        # obtém o primeiro nó da sub-árvore
        l_node = f_element.firstChild()
        assert l_node is not None

        # percorre a sub-árvore
        while not l_node.isNull():

            # tenta converter o nó em um elemento
            l_element = l_node.toElement()
            assert l_element is not None

            # o nó é um elemento ?
            if not l_element.isNull():

                # atualiza o dicionário de dados
                ldct_brk.update(parse_breakpoint(l_element))

            # próximo nó
            l_node = l_node.nextSibling()
            assert l_node is not None

        # atualiza o dicionário com o break-point
        ldct_tmp["breakpoint"] = ldct_brk

    # logger
    # M_LOG.info("parse_subida:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------

def parse_trafego(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_trafego:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case of indicativo
    if "indicativo" == f_element.tagName():
        ldct_tmp["indicativo"] = f_element.text()

    # handle case of designador
    elif "designador" == f_element.tagName():
        ldct_tmp["designador"] = f_element.text()

    # handle case of ssr
    elif "ssr" == f_element.tagName():
        ldct_tmp["ssr"] = f_element.text()

    # handle case of origem
    elif "origem" == f_element.tagName():
        ldct_tmp["origem"] = f_element.text()

    # handle case of destino
    elif "destino" == f_element.tagName():
        ldct_tmp["destino"] = f_element.text()

    # handle case of procedimen
    elif "procedimento" == f_element.tagName():
        ldct_tmp["procedimento"] = f_element.text()

    # handle case of nivel
    elif "nivel" == f_element.tagName():
        ldct_tmp["nivel"] = f_element.text()

    # handle case of altitude
    elif "altitude" == f_element.tagName():
        ldct_tmp["altitude"] = f_element.text()

    # handle case of velocidade
    elif "velocidade" == f_element.tagName():
        ldct_tmp["velocidade"] = f_element.text()

    # handle case of proa
    elif "proa" == f_element.tagName():
        ldct_tmp["proa"] = f_element.text()

    # handle case of temptrafego
    elif "temptrafego" == f_element.tagName():
        ldct_tmp["temptrafego"] = f_element.text()

    # handle case of numsg
    elif "numsg" == f_element.tagName():
        ldct_tmp["numsg"] = f_element.text()

    # handle case of tempmsg
    elif "tempmsg" == f_element.tagName():
        ldct_tmp["tempmsg"] = f_element.text()

    # handle case of rvsm
    elif "rvsm" == f_element.tagName():
        ldct_tmp["rvsm"] = f_element.text()

    # handle case of rota
    elif "rota" == f_element.tagName():
        ldct_tmp["rota"] = f_element.text()

    # handle case of eet
    elif "eet" == f_element.tagName():
        ldct_tmp["eet"] = f_element.text()

    # handle case of niveltrj
    elif "niveltrj" == f_element.tagName():
        ldct_tmp["niveltrj"] = f_element.text()

    # handle case of veltrj
    elif "veltrj" == f_element.tagName():
        ldct_tmp["veltrj"] = f_element.text()

    # handle case of posição
    elif "coord" == f_element.tagName():

        # inicia o dicionário de dados
        ldct_pos = {}

        # obtém o primeiro nó da sub-árvore
        l_node = f_element.firstChild()
        assert l_node is not None

        # percorre a sub-árvore
        while not l_node.isNull():

            # tenta converter o nó em um elemento
            l_element = l_node.toElement()
            assert l_element is not None

            # o nó é um elemento ?
            if not l_element.isNull():

                # atualiza o dicionário de dados
                ldct_pos.update(parse_coord(l_element))

            # próximo nó
            l_node = l_node.nextSibling()
            assert l_node is not None

        # atualiza o dicionário com a posição
        ldct_tmp["coord"] = ldct_pos

    # logger
    # M_LOG.info("parse_trafego:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------

def parse_trajetoria(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # logger
    # M_LOG.info("parse_trajetoria:>>")

    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case of descrição
    if "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()

    # handle case of star
    elif "proa" == f_element.tagName():
        ldct_tmp["proa"] = f_element.text()

    # handle case of star
    elif "star" == f_element.tagName():
        ldct_tmp["star"] = f_element.text()

    # handle case of break-point
    elif "breakpoint" == f_element.tagName():

        # inicia o dicionário de dados
        ldct_brk = {}

        # read identification if available
        if f_element.hasAttribute("nBrk"):
            ldct_brk["nBrk"] = int(f_element.attribute("nBrk"))

        # obtém o primeiro nó da sub-árvore
        l_node = f_element.firstChild()
        assert l_node is not None

        # percorre a sub-árvore
        while not l_node.isNull():

            # tenta converter o nó em um elemento
            l_element = l_node.toElement()
            assert l_element is not None

            # o nó é um elemento ?
            if not l_element.isNull():

                # atualiza o dicionário de dados
                ldct_brk.update(parse_breakpoint(l_element))

            # próximo nó
            l_node = l_node.nextSibling()
            assert l_node is not None

        # atualiza o dicionário com o break-point
        ldct_tmp["breakpoint"] = ldct_brk

    # logger
    # M_LOG.info("parse_trajetoria:<<")

    # retorna o dicionário de dados
    return ldct_tmp

# < the end >--------------------------------------------------------------------------------------
