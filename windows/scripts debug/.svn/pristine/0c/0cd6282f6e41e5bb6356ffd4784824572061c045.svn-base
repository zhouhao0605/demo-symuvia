#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Module de fonctions utilitaires pour les scripts de régulation de SymuVia
"""
import symuvia

def calcul_date_fin_cycle_PDF(network, cdf):
	"""
	Méthode utilitaire pour déterminer la date de fin du cycle courant d'un plan de feux
	"""
	# récupération du plan de feux actif
	timeSpan = symuvia.STimeSpan()	
	pdf = cdf.GetTrafficLightCycle(network.InstSimu, timeSpan)
	
	# Calcul de l'instant de fin d'une séquence du plan de feux actuel ...
	heure_debut_pdf_actuel = pdf.GetStartTime()
	instant_debut_PDF = heure_debut_pdf_actuel.second + 60*heure_debut_pdf_actuel.minute + 3600*heure_debut_pdf_actuel.hour
	inst_debut_simu = network.GetSimuStartTime()
	instant_debut_SIMU = inst_debut_simu.second + 60*inst_debut_simu.minute + 3600*inst_debut_simu.hour
	nb_secondes_ecoulees_PDF = network.InstSimu  + instant_debut_SIMU - instant_debut_PDF
	duree_cycle_restante = pdf.GetCycleLength() - (nb_secondes_ecoulees_PDF%pdf.GetCycleLength())
	
	# nombre de sécondes correspondant à l'instant à créer
	nb_secondes = instant_debut_PDF + nb_secondes_ecoulees_PDF + duree_cycle_restante
	# création du STime de début du nouveau plan de feux
	time_debut_pdf = symuvia.STime()
	time_debut_pdf.seconde = int(nb_secondes%60)
	reste = nb_secondes / 60
	time_debut_pdf.minute = int(reste%60)
	reste = reste / 60
	if reste > 23:
		raise Exception("Attention, dépassement de l'heure sur le jour suivant non gérée par SymuVia")
	time_debut_pdf.hour = int(reste % 24)
	
	return time_debut_pdf