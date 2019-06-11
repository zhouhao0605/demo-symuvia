#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Module dédié aux fonctions de base associées aux conditions
"""
import symuvia
import symuviautils

import os

def light_setting_change(sensors, context, network, parameters):

	T_changeSetting = 180    # change the setting of trafic lights every 3mins 
	T_lightcycle = 60        # cycle of trafic light
 
	if (network.InstSimu) % T_changeSetting == 0: # if going to reach the time (every 3 mins in here), change traffic light
		result = True
	else:
		result = False
		
	if len(context) == 0:
			# initialisations qu'on en fait qu'au premier appel
			context["capteurs"] = parameters["capteurs"].split()
		else:
			context["capteurs"] = parameters["capteurs"].split()
    
    flow_twoBranch = list()   
    for capteur in context["capteurs"]:
		# si pas de débit : on n'est pas sur une fin de période d'agrégation des capteurs... pas la peine d'aller plus loin
        if "debit" in sensors[capteur].keys():
			flow_twoBranch.append(sensors[capteur]["debit"])
        else:
			result = False
				context["result"] = result
				return result
        
    # set green time according to the flows 
    greenTime1 = T_lightcycle * float(flow_twoBranch[0]) / (flow_twoBranch[0] + flow_twoBranch[1])
    greenTime2 = T_lightcycle * float(flow_twoBranch[1]) / (flow_twoBranch[0] + flow_twoBranch[1])
            
    if "greenTime1" not in context.keys():
		context["greenTime1"] = greenTime1
		elif context["greenTime1"] != greenTime1:
			context["greenTime1"] = greenTime1

	if "greenTime2" not in context.keys():
		context["greenTime2"] = greenTime2
		elif context["greenTime2"] != greenTime2:
			
   context["greenTime2"] = greenTime2		
        
	context["result"] = result
	return result


def sensor_consultation(sensors, context, reseau, parameters):
	"""
	Fonction permettant de comparer une mesure capteur à une valeur de référence passée en paramètres
	"""
	result = False
	
	# récupération de la mesure du capteur à évaluer
	if parameters["capteur"] not in sensors.keys() or parameters["mesure"] not in sensors[parameters["capteur"]]:
		# si on n'a pas la mesure, la condition est fausse par défaut
		return result
	else:
		mesure = sensors[parameters["capteur"]][parameters["mesure"]]
	
	# récupération de la valeur de référence et cast vers le type correspondant à la mesure
	type_mesure = type(mesure)
	reference = type_mesure(parameters["reference"])
	
	# évaluation de la condition en fonction de l'operation
	operateur = parameters["operateur"]
	if operateur == "egal":
		result = mesure == reference
	elif operateur == "strictement_superieur":
		result = mesure > reference
	elif operateur == "superieur_egal":
		result = mesure >= reference
	elif operateur == "inferieur_egal":
		result = mesure <= reference
	elif operateur == "strictement_inferieur":
		result = mesure < reference
	else:
		raise Exception(u"L'opérateur " + operateur + u" n'est pas implementé !")
		
	###############################################
	# gestion du paramètres "mode_declenchement"
	###############################################
	if "mode_declenchement" in parameters.keys() and parameters["mode_declenchement"] == "changement":
		if "oldResult" not in context.keys():
			# premier passage : on ne fait que noter le premier résultat
			context["oldResult"] = result
		else:
			oldResult = context["oldResult"]
			context["oldResult"] = result
			if result == oldResult:
				# dans ce cas on ne doit pas activer le déclenchement
				result = False	

	context["result"] = result
	return result

def flow_range_change(sensors, context, network, parameters):
	"""
	Evalue si on change de tranche de débit ou non
	"""
	result = False
	
	if len(context) == 0:
		# initialisations qu'on en fait qu'au premier appel
		context["capteurs"] = parameters["capteurs"].split()
		context["lstTranches"] = parameters["tranches_debits"].split()
	
	# calcul du débit agrégé
	debit_total = 0
	for capteur in context["capteurs"]:
		# si pas de débit : on n'est pas sur une fin de période d'agrégation des capteurs... pas la peine d'aller plus loin
		if "debit" in sensors[capteur].keys():
			debit_total = debit_total + sensors[capteur]["debit"]
		else:
			result = False
			context["result"] = result
			return result
				
	# détermination du numéro de tranche associé
	num_tranche = 0
	for borne in context["lstTranches"]:
		if debit_total < float(borne):
			break
		else:
			num_tranche = num_tranche + 1
			
	if "tranche" not in context.keys():
		# premier calcul de tranche : on active forcément un des plans de feux
		result = True
		context["tranche"] = num_tranche
	elif context["tranche"] != num_tranche:
		result = True
		context["tranche"] = num_tranche

	context["result"] = result
	return result
	
	
def time_reached(sensors, context, network, parameters):
	"""
	Teste si l'heure passée en paramètres est atteinte ou non.
	"""
	
	# construction de l'objet heure correspondant au paramètre
	if len(context) == 0:
		heure_cible = parameters["heure"].split(':')
		context["heure_cible"] = float(int(heure_cible[0])*3600 + int(heure_cible[1])*60 + int(heure_cible[2]))
		heure_debut_simu = network.GetSimuStartTime()
		context["heure_debut_simu"] = float(heure_debut_simu.second + 60*heure_debut_simu.minute + 3600*heure_debut_simu.hour)
	
	instant_fin_pdt = context["heure_debut_simu"] + network.InstSimu
	instant_debut_pdt = instant_fin_pdt - network.GetTimeStep()
	
	if context["heure_cible"] <= instant_fin_pdt and context["heure_cible"] > instant_debut_pdt:
		result = True
	else:
		result = False
	
	context["result"] = result
	return result
	
def blip_activation_nico(sensors, context, network, parameters):
	"""
	Teste si on doit activer la BLIP en temporisant jusqu'à la fin du cycle de feux en cours pour le contrôleur de feux indiqué
	"""
	result = False
	
	# on regarde si un véhicule prioritaire est détecté
	vehicule_prioritaire_present = sensors[parameters["capteur"]]["nombre_vehicules"] > 0
	
	# Si on a pas déjà une activation en cours, on en déclenche une si un véhicule est détecté
	if "instant_activation" not in context.keys():
		if vehicule_prioritaire_present:
			cdf = network.GetTrafficLightControllerFromID(parameters["cdf"])
			time_fin_pdf = symuviautils.calcul_date_fin_cycle_PDF(network, cdf)
			context["instant_activation"] = float(time_fin_pdf.hour*3600 + time_fin_pdf.minute*60 + time_fin_pdf.second)
	else:
		# Si pas de véhicule mais activation en cours, le véhicule prioritaire est déjà sorti : on annule l'activation
		if not vehicule_prioritaire_present:
			context.clear()
		
	# Si l'instant d'activation est arrivé, on active la condition
	if "instant_activation" in context.keys():
		simu_start_time = network.GetSimuStartTime()
		if context["instant_activation"] <= network.InstSimu + float(simu_start_time.hour*3600 + simu_start_time.minute*60 + simu_start_time.second):
			context.clear()
			result = True
	
	context["result"] = result
	return result
	
