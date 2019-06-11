#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import symuvia
import symuviautils

messageStart = "target;ChangeLaneV2VStationScript/vehId;"

def Run(network,parameters,timeStart,timeDuration):
	vehicle = parameters["this"].GetDynamicParent()
	if vehicle is not None:
		# TODO - voir pour anticiper avec le tuyau amont également ?
		if vehicle.GetLink(0) and vehicle.GetLink(0).Label == parameters["merging_link"] and vehicle.GetVoie(0) and vehicle.GetVoie(0).GetNum() == 0:
			message = messageStart + str(vehicle.ID)
			parameters["this"].SendBroadcastMessage(message,timeStart,-1.0, False)
			
			
def TreatMessageData(network,parameters,message):
	station = parameters['this']
	vehicle = station.GetDynamicParent()
	if vehicle is not None and vehicle.GetLink(0).Label == parameters["merging_link"] and vehicle.GetVoie(0) and vehicle.GetVoie(0).GetNum() == 1 :
		data = message.GetData()
		if data.startswith(messageStart):
			# TODO - au final dans cet exemple simpliste, on n'exploite pas les donnes envoyees par le vehicule emetteur : si on 
			# recoit le message, un vehicule veut s'insérer et est à portée : on se pousse de toute façon.
			listData = data.split("/")
			vehId = int(listData[-1].split(";")[-1])
			prioritaryVeh = None
			for veh in network.LstVehicles:
				if veh.ID == vehId:
					prioritaryVeh = veh
					break

			if prioritaryVeh is not None:
				new_message = "Action;RunApplication/target;ChangeLaneV2VAppliScript"
				station.SendUniqueMessage(station.GetEntityID(), new_message,message.GetTimeReceive(),symuvia.EMessageType.Unicast, -1, False)
