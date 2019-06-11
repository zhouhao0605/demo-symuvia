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
	if Vehicle.GetLink(0).Label != "T_829318118_FRef":
		return
	num = Vehicle.GetVoie(0).GetNum()
	nbVoie = Vehicle.GetLink(0).getNbVoies()
	data = message.GetData()
	listData = data.split("/")
	closingLane = int(listData[-1].split(";")[-1])
	moveDirection = 1
	if closingLane == 0:
		moveDirection = 1
	else:
		moveDirection = -1
	newNum = num + moveDirection
	if newNum >= 0 and newNum < nbVoie:
		Vehicle.SetDesiredLane(newNum)
	if newNum == nbVoie:
		Vehicle.SetDesiredLane(num)
