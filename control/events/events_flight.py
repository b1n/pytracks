#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
events_flight.

generic event superclass. What follows is a list of all events. None of these classes should
perform any tasks, as that could introduce vulnerabilities.

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "mlabru, sophosoft"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# control
from . import events_model as model

# < class CFlightExplode >--------------------------------------------------------------------------


class CFlightExplode(model.CEventsModel):
    """
    CFlightExplode event class.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, ls_callsign):
        """
        DOCUMENT ME!
        """
        # init super class
        super(CFlightExplode, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        self.s_name = "FlightExplode event"
        self.__s_callsign = ls_callsign

# < class CFlightKill >-----------------------------------------------------------------------------


class CFlightKill(model.CEventsModel):
    """
    CFlightKill event class.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, ls_callsign):
        """
        DOCUMENT ME!
        """
        # init super class
        super(CFlightKill, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        self.s_name = "FlightKill event"
        self.__s_callsign = ls_callsign

# < class CFlightUpdate >---------------------------------------------------------------------------


class CFlightUpdate(model.CEventsModel):
    """
    CFlightUpdate event class.
    """
    # ---------------------------------------------------------------------------------------------

    def __init__(self, ls_callsign):
        """
        DOCUMENT ME!
        """
        # init super class
        super(CFlightUpdate, self).__init__()

        # herdados de CEventsModel
        # self.s_name    # event name

        self.s_name = "FlightUpdate event"
        self.__s_callsign = ls_callsign

# < the end >--------------------------------------------------------------------------------------
