#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Module dédié aux fonctions de base associées aux capteurs
"""
import symuvia

def longitudinal_sensor(context, network, parameters):
	"""
	Fonction associée aux capteurs longitudinaux, permettant la mesure des éléments suivants :
	- nombre_vehicules
	- ...
	"""
	
	resultat = 0
	
	# traitement des paramètres
	# construction de la liste des labels des tuyaux à partir de l'attribut "troncons"
	tuyauxCapteur = parameters["troncons"].split()
	nbTuyauxCapteur = len(tuyauxCapteur)
	pos_debut = float(parameters["position_debut"])
	pos_fin = float(parameters["position_fin"])
	type_vehicule = None
	
	
	# on boucle sur la liste des véhicules pour voir quels sont ceux du bon type présent sur les tronçons couverts par le capteur
	for vehicule in network.LstVehicles:
		if vehicule.GetType().Label == str(parameters["type_veh"]) :
			type_vehicule = vehicule.GetType()
			# on regarde si le véhicule est positionné sur le capteur longitudinal
			tuyau = vehicule.GetLink(0)
			# pour chaque tuyau de la portée du capteur ...
			for iTuyauCapteur in range(nbTuyauxCapteur):
				# le véhicule doit être sur un tronçon asocié au capteur
				if tuyauxCapteur[iTuyauCapteur] == tuyau.Label:
					# si le véhicule est sur le premier tronçon, on doit comparer sa position à la position de début du capteur
					if iTuyauCapteur == 0:
						if vehicule.GetPosition(0) >= pos_debut:
							resultat = resultat+1
					elif iTuyauCapteur == nbTuyauxCapteur-1:
						if vehicule.GetPosition(0) <= pos_fin:
							resultat = resultat+1
					else:
						resultat = resultat+1
		
	# mise en forme du résultat
	result = dict()
	result["nombre_vehicules"] = resultat
	
	return result
	

def _compte_nb_passages(network, tuyau_capteur, position_capteur):
	"""
	Fonction permettant de compter le nombre de véhicules passant la position indiqué en cours de PDT.
	Code inspiré de la méthode C++ GestionCapteur::CalculInfoCapteurs
	"""
	nbVehicules = 0
	for vehicule in network.LstVehicles:
		# Sinon la nouvelle position du véhicule n'a pas été calculée (pas encore rentré sur le réseau)
		if  vehicule.GetPosition(0) >= 0 or vehicule.GetExitInstant() > 0:		
			# Le capteur est-il placé sur le même tuyau que le véhicule au début du pas de temps ?
			tuyau_avant = vehicule.GetLink(1)
			if tuyau_avant is not None and tuyau_avant.Label == tuyau_capteur:
				# Le capteur est positionné en aval du véhicule au début du pas de temps ?
				if vehicule.GetPosition(1) < position_capteur:
					# Le véhicule est-il positionné après le capteur à la fin du pas de temps
					# ou a t'il changé de tuyau ?
					if vehicule.GetPosition(0) >= position_capteur or vehicule.GetLink(0) is None or vehicule.GetLink(0).Label != tuyau_capteur:
						nbVehicules = nbVehicules + 1 # le véhicule est détecté par le capteur
			else:
				# On regarde si le capteur considéré est sur le tuyau sur lequel est placé le véhicule à la
				# fin du pas de temps. Si le véhicule ne change pas de tuyau, pas la peine d'aller
				# plus loin puisqu'il n'y a pas de capteur sur le tuyau initial
				
				# rmq : comparaison sur les identifiants des tuyaux
				str_avant = ""
				if vehicule.GetLink(1) is not None:
					str_avant = vehicule.GetLink(1).Label
				str_apres = ""
				if vehicule.GetLink(0) is not None:
					str_apres = vehicule.GetLink(0).Label
				if str_avant != str_apres:
					# Le capteur est-il sur le tuyau final ?
					tuyau_apres = vehicule.GetLink(0)
					if tuyau_apres is not None and tuyau_apres.Label == tuyau_capteur:
						if vehicule.GetPosition(0) >= position_capteur:
							nbVehicules = nbVehicules + 1 # le véhicule est détecté par le capteur
					else:
						# Le capteur est-il situé sur un des tronçons traversés ?
						for voieEmpr in vehicule.LstUsedLanes:
							if voieEmpr.GetParent().Label == tuyau_capteur:
								nbVehicules = nbVehicules + 1 # le véhicule est détecté par le capteur
								break
				
	return nbVehicules
	
	
def ponctual_sensor(context, network, parameters):
	"""
	Fonction associée aux capteurs ponctuels, permettant la mesure des éléments suivants :
	- nombre_passages
	- instant_dernier_passage
	- temps_ecoule_depuis_dernier_passage
	- débit (moyenné pendant la période d'agrégation)
	"""
	result = dict()
	
	# on initialise les valeurs du contexte
	if len(context) == 0:
		context["instant_dernier_passage"] = network.InstSimu - network.GetTimeStep() # (retranché car exécution à la fin du premier pas de temps)
		context["temps_ecoule_depuis_dernier_passage"] = 0
		if "periode_agregation" in parameters.keys():
			context["periode_agregation"] = float(parameters["periode_agregation"])
			context["debut_periode"] = network.InstSimu - network.GetTimeStep() # (retranché car exécution à la fin du premier pas de temps)
			context["nombre_passages_agrege"] = 0.0 
	
	tuyau_amont = str(parameters["troncon"])
	position_capteur = float(parameters["position"])
	result["nombre_passages"] = _compte_nb_passages(network, tuyau_amont, position_capteur)
	if "periode_agregation" in parameters.keys():
		context["nombre_passages_agrege"] = context["nombre_passages_agrege"] + result["nombre_passages"]
	if result["nombre_passages"] > 0:
		context["instant_dernier_passage"] = network.InstSimu
		context["temps_ecoule_depuis_dernier_passage"] = 0
	else:
		context["temps_ecoule_depuis_dernier_passage"] = context["temps_ecoule_depuis_dernier_passage"] + network.GetTimeStep()
		
	# traitements associés à la fin de la période :
	if "periode_agregation" in parameters.keys():
		if network.InstSimu >= context["debut_periode"] + context["periode_agregation"]:
			result["debit"] = context["nombre_passages_agrege"] / (network.InstSimu - context["debut_periode"])
			# rajouter ici d'éventuelles autres valeurs relatives à la période d'agrégation terminée
			
			#préparation de la période suivante
			context["nombre_passages_agrege"] = 0.0 
			context["debut_periode"] = network.InstSimu
			
	result["temps_ecoule_depuis_dernier_passage"] = context["temps_ecoule_depuis_dernier_passage"]
	result["instant_dernier_passage"] = context["instant_dernier_passage"]
	
	return result
	