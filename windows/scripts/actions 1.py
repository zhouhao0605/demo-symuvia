#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Module dédié aux fonctions de base associées aux actions
"""
import symuvia
import symuviautils

def forbid_movement(conditions, context, network, parameters):
    """
    Activation d'un mouvement autorisé
    """
    # récupération de l'objet mouvement correspondant
    # récupération de la connexion
    connexionID = parameters["connexion"]
    c = str()
    connexion = network.GetConnectionFromID(connexionID, c)
    if connexion is None:
        connexion = network.GetBrickFromID(connexionID)
    # recupération du tuyau amont
    troncon_amont = network.GetLinkFromLabel(parameters["troncon_amont"])
    # recuperation de la voie amont
    voie_amont = troncon_amont.GetLane(int(parameters["num_voie_amont"])-1)
    # recupération du tuyau aval
    troncon_aval = network.GetLinkFromLabel(parameters["troncon_aval"])
    # récupération du type de véhicule
    type_veh = network.GetVehicleTypeFromID(parameters["type_veh"])
    
    # Ajout du type à interdire à la liste des types interdits
    connexion.GetMovement(voie_amont, troncon_aval)[int(parameters["num_voie_amont"])-1].LstForbiddenVehicles.append(type_veh)

#    # Define the link where the Bus is in.
#    for vehicule in network.LstVehicles:
#        if vehicule.GetType().Label == 'Bus' :
#            tuyau = vehicule.GetLink(0)  
#            #if type_vehicule = vehicule.GetType():
#            # on regarde si le véhicule est positionné sur le troncon cible
#            if tuyau.Label == troncon_aval: # Bus on BLIP link.                   
#                # suppression du type de véhicule autorisé de la liste des véhicules interdits
#                lstTypesInterdits = connexion.GetMovement(voie_amont, troncon_aval)[int(parameters["num_voie_amont"])-1].LstForbiddenVehicles
#                for index in range(len(lstTypesInterdits)):
#                    if lstTypesInterdits[index].Label == type_veh.Label:
#                        del lstTypesInterdits[index]
#                          
#            elif  tuyau.Label != troncon_aval:  # Bus upstream BLIP link.                
#                # Ajout du type à interdire à la liste des types interdits
#                connexion.GetMovement(voie_amont, troncon_aval)[int(parameters["num_voie_amont"])-1].LstForbiddenVehicles.append(type_veh)


def authorize_movement(conditions, context, network, parameters):
    """
    Désactivation d'un mouvement autorisé
    """
    # récupération de l'objet mouvement correspondant
    # récupération de la connexion
    connexionID = parameters["connexion"]
    c = str()
    connexion = network.GetConnectionFromID(connexionID, c)
    if connexion is None:
        connexion = network.GetBrickFromID(connexionID)
    # recupération du tuyau amont
    troncon_amont = network.GetLinkFromLabel(parameters["troncon_amont"])
    # recuperation de la voie amont
    voie_amont = troncon_amont.GetLane(int(parameters["num_voie_amont"])-1)
    # recupération du tuyau aval
    troncon_aval = network.GetLinkFromLabel(parameters["troncon_aval"])
    # récupération du type de véhicule
    type_veh = network.GetVehicleTypeFromID(parameters["type_veh"])
    
    # suppression du type de véhicule autorisé de la liste des véhicules interdits
    lstTypesInterdits = connexion.GetMovement(voie_amont, troncon_aval)[int(parameters["num_voie_amont"])-1].LstForbiddenVehicles
    for index in range(len(lstTypesInterdits)):
        if lstTypesInterdits[index].Label == type_veh.Label:
            del lstTypesInterdits[index]
            
def forbid_lane_change(conditions, context, network, parameters):
    """
    Interdit le changment de voie vers une voie cible
    """
    troncon = network.GetLinkFromLabel(parameters["troncon"])
    num_voie_cible = int(parameters["num_voie_cible"])-1
    voie = troncon.GetLane(num_voie_cible)
    voie.SetTargetLaneForbidden(True)
    
def authorize_lane_change(conditions, context, network, parameters):
    """
    Autorise le changment de voie vers une voie cible.
    """
    troncon = network.GetLinkFromLabel(parameters["troncon"])
    num_voie_cible = int(parameters["num_voie_cible"])-1
    voie = troncon.GetLane(num_voie_cible)
    voie.SetTargetLaneForbidden(False)
    
def forbid_lane_change_before_guided_vehicule(conditions, context, network, parameters):
    """
    Interdit le changement de voie vers une voie cible si un véhicule guidé est en amont
    """
    troncon = network.GetLinkFromLabel(parameters["troncon"])
    num_voie_cible = int(parameters["num_voie_cible"])-1
    voie = troncon.GetLane(num_voie_cible)
    voie.SetPullBackInInFrontOfGuidedVehicleForbidden(True)

def change_sequence_length(conditions, context, network, parameters):
    """
    Change la durée d'une séquence
    """
    if len(context) == 0:
        context["index_sequence"] = int(parameters["num_sequence"])-1
        context["nouvelle_duree"] = float(parameters["nouvelle_duree"])
        
    cdf = network.GetTrafficLightControllerFromID(parameters["cdf"])
    
    # récupération du plan de feux actif
    timeSpan = symuvia.STimeSpan()    
    pdf = cdf.GetTrafficLightCycle(network.InstSimu, timeSpan)
    
    # recopie du plan de feux en modifiant la durée de la nouvelle séquence
    new_pdf = symuvia.CreateTrafficLightCycle("", symuvia.STime())
    seqNum = 0
    for seq in pdf.GetLstSequences():
        
        if seqNum == context["index_sequence"]:
            duree_seq = context["nouvelle_duree"]
        else:
            duree_seq = seq.GetTotalLength()
        newSeq = symuvia.CreateSequence(duree_seq, seqNum)
        
        # création des signaux
        for signal in seq.GetLstActiveSignals():
            newSignal = symuvia.CreateActiveSignal(signal.GetInputLink(), signal.GetOutputLink(), signal.GreenDuration, signal.OrangeDuration, signal.ActivationDelay)
            newSeq.AddActiveSignal(newSignal)
        
        new_pdf.AddSequence(newSeq)
        seqNum = seqNum + 1
    
    # détermination de la date à laquelle démarrer le nouveau plan de feux
    time_debut_pdf = symuviautils.calcul_date_fin_cycle_PDF(network, cdf)
    
    # mise en place du plan de feux
    cdf.GetLstTrafficLightCycles().AddVariation(time_debut_pdf, new_pdf)
            
def change_traffic_light_cycle(conditions, context, network, parameters):
    """
    Change de plan de feux pour le contrôleur spécifié
    """
    cdf = network.GetTrafficLightControllerFromID(parameters["cdf"])
    
    # index de la tranche
    index_tranche = conditions.values()[0]["tranche"]
    
    # construction du plan de feux à partir des paramètres reçus
    lstPlans = parameters["PLANS_DE_FEUX"][0]["PLAN_DE_FEUX"]
    for plan in lstPlans:
        if int(plan["index_tranche"]) == index_tranche:
            paramsPlan = plan
            break
            
    print u"plan a mettre en place : " + paramsPlan["id"]
            
    # instanciation de l'objet plan de feux à mettre en place
    pdf = symuvia.CreateTrafficLightCycle(str(paramsPlan["id"]), symuvia.STime())
    # ajout de chaque séquence
    seqNum = 0
    for sequence in plan["SEQUENCES"][0]["SEQUENCE"]:
        
        newSeq = symuvia.CreateSequence(float(sequence["duree_totale"]), seqNum)
        # définition de la séquence ...
        for signal in sequence["SIGNAUX_ACTIFS"][0]["SIGNAL_ACTIF"]:
            tuyau_entree = network.GetLinkFromLabel(signal["troncon_entree"])
            tuyau_sortie = network.GetLinkFromLabel(signal["troncon_sortie"])
            newSignal = symuvia.CreateActiveSignal(tuyau_entree, tuyau_sortie, float(signal["duree_vert"]), 0.0, float(signal["duree_retard_allumage"]))
            newSeq.AddActiveSignal(newSignal)
            
        pdf.AddSequence(newSeq)
        seqNum = seqNum + 1
        
    # détermination de la date à laquelle démarrer le nouveau plan de feux
    time_debut_pdf = symuviautils.calcul_date_fin_cycle_PDF(network, cdf)
    
    # mise en place du plan de feux
    cdf.GetLstTrafficLightCycles().AddVariation(time_debut_pdf, pdf)    
    
def speed_limit_exception(conditions, context, network, parameters):
    """
    Applique une exception à la vitesse réglementaire sur une portion de tronçon
    """
    # pas stocké dans le contexte car pointeur vers un objet SymuBruit : pb pour les snapshots
    troncon = network.GetLinkFromLabel(parameters["troncon"])
    
    if len(context) == 0:
        context["vitesse"] = float(parameters["vitesse"])
        if "position_debut" in parameters.keys():
            context["position_debut"] = float(parameters["position_debut"])
        else:
            context["position_debut"] = 0.0
        if "position_fin" in parameters.keys():
            context["position_fin"] = float(parameters["position_fin"])
        else:
            context["position_fin"] = troncon.GetLength()
            
        if "type_veh" in parameters.keys():
            context["type_veh"] = network.GetVehicleTypeFromID(parameters["type_veh"])
        else:
            context["type_veh"] = None
    
    
    # Création d'une exception à la vitesse réglementaire
    troncon.SendSpeedLimitPortion(network.InstSimu, context["type_veh"], context["position_debut"], context["position_fin"], context["vitesse"])
    
    
def speed_limit(conditions, context, network, parameters):
    """
    Applique une vitesse réglementaire sur un tronçon
    """
    # pas stocké dans le contexte car pointeur vers un objet SymuBruit : pb pour les snapshots
    troncon = network.GetLinkFromLabel(parameters["troncon"])
    
    if len(context) == 0:
        context["vitesse"] = float(parameters["vitesse"])
        context["nb_voies"] = len(troncon.GetLstVoie())
            
        if "type_veh" in parameters.keys():
            context["type_veh"] = network.GetVehicleTypeFromID(parameters["type_veh"])
        else:
            context["type_veh"] = None
    
    
    # Création d'une exception à la vitesse réglementaire
    troncon.SendSpeedLimit(network.InstSimu, context["type_veh"], context["vitesse"], context["nb_voies"])
    
    
def recompute_affectation(conditions, context, network, parameters):
    """
    Recalcul de l'affectation
    """
    network.GetAffectationModule().Run(network, network.InstSimu, 'R', None, None, None)
    
