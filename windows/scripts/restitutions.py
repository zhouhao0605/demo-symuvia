#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Module dédié aux fonctions de base associées aux restitutions
"""
import symuvia

def rest_change_light_settings(conditions, context, network, parameters):
	
	result = dict()
	
	context["active"] = False
	
	if conditions[parameters["activation"]]["result"]:
		context["active"] = True
		
	result["change_light_settings"] = dict()
	result["change_light_settings"]["active"] = str(int(context["active"]))
	
	return result
	
def blip(conditions, context, network, parameters):
	"""
	Sorties associées aux blips (pour affichage dans SymuPlayer
	"""
	result = dict()
	
	# comme la condition d'activation de la BLIP est vrai sur changement uniquement, on doit garder trace de la valeur 
	# d'activation :
	if conditions[parameters["condition_blip_active"]]["result"]:
		context["active"] = True
		
	if conditions[parameters["condition_blip_inactive"]]["result"]:
		context["active"] = False
	
	result["BLIP"] = dict()
	result["BLIP"]["troncon"] = parameters["troncon"]
	result["BLIP"]["num_voie"] = parameters["num_voie"]
	result["BLIP"]["active"] = str(int(context["active"]))
	
	return result

