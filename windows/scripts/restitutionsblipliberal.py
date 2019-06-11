#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Module dédié aux fonctions de base associées aux restitutions

"""
# import 
import symuvia

#  blip function Orignal ===============================================
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

# blipLiberal ==========================================================
def blipLiberal(conditions, context, network, parameters):
	""" BlipLiberal:
	
	Sorties associées aux blips (pour affichage dans SymuPlayer.
	"""
	result = dict()
	
	# comme la condition d'activation de la BLIP est vrai sur changement uniquement, on doit garder trace de la valeur 
	
	# Activation .......................................................
	if conditions[parameters["condition_blip_active1"]]["result"]:
		context["active"] = True
	if conditions[parameters["condition_blip_active2"]]["result"]:
		context["active"] = True
	if conditions[parameters["condition_blip_active3"]]["result"]:
		context["active"] = True
	# Desactivation ....................................................
	if conditions[parameters["condition_blip_inactive1"]]["result"]:
		context["active"] = False
	
	# BLIP ............................................................
	result["BLIP"] = dict()
	result["BLIP"]["troncon"] = parameters["troncon"]
	result["BLIP"]["num_voie"] = parameters["num_voie"]
	result["BLIP"]["active"] = str(int(context["active"]))
	
	# return result ....................................................
	return result
	
