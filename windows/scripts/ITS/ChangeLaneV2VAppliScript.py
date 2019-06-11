#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import symuvia
import symuviautils

def RunApplication(network,parameters,message,station):
	if station == None:
		return
	Vehicle = station.GetDynamicParent()
	if Vehicle == None:
		return
	num = Vehicle.GetVoie(0).GetNum()
	if num != 1:
		return
	
	nbVoie = Vehicle.GetLink(0).getNbVoies()
	if nbVoie <= 2:
		return
		
	Vehicle.SetDesiredLane(2)