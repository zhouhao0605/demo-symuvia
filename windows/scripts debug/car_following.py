#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Module dédié aux fonctions de définition des lois de poursuite
"""
import symuvia

import math
import sys

def gipps(network, car_following_model, parameters, context, prev_context, time_step, instant):
	"""
	Loi de poursuite de Gipps
	"""
	
	vehicle = car_following_model.GetVehicle()
	
	# Calcul de la vitesse libre désirée
	#####################################
	computed_speed = 0
	free_flow_state = True
	if len(context.GetLstLanes()) != 0:
		first_lane = context.GetLstLanes()[0]
		max_speed_on_lane = first_lane.GetParent().GetSpeedLimit(vehicle.GetType(),instant,context.GetStartPosition(), first_lane.GetNum())
		max_speed_on_lane = min(max_speed_on_lane, vehicle.GetMaxSpeed());
		maximum_acceleration = vehicle.GetType().GetMaxAcc(vehicle.GetSpeed(1))
		computed_speed = vehicle.GetSpeed(1) + float(parameters["alpha"]) * maximum_acceleration * time_step * (1 - vehicle.GetSpeed(1)/max_speed_on_lane) * pow(float(parameters["beta"])+vehicle.GetSpeed(1)/max_speed_on_lane, float(parameters["gamma"]))
		
	if len(context.GetLeaders()) != 0:
		first_leader = context.GetLeaders()[0]
		vehicle_distance = context.GetLeaderDistances()[0]
		maximum_deceleration = - vehicle.GetType().ComputeDeceleration()
		leader_maximum_deceleration = - first_leader.GetType().ComputeDeceleration()
		
		# dans SymuVia, si aucune décélération n'est renseignée pour un type de véhicule, la valeur de deceleration vaut 0.
		# Pour être cohérent, il faut interpreter cette valeur comme étant une délécération infinie (le véhicule peut "piler").
		if maximum_deceleration == 0:
			maximum_deceleration = - sys.float_info.max
		if leader_maximum_deceleration == 0:
			leader_maximum_deceleration = - sys.float_info.max
			
		factor = maximum_deceleration * (time_step/2 + float(parameters["teta"]))
		sqrtContent = factor*factor - maximum_deceleration * (2 * (vehicle_distance - (first_leader.GetLength() + vehicle.GetType().GetSpacingAtStop()))
			- vehicle.GetSpeed(1)*time_step - first_leader.GetSpeed(1)*first_leader.GetSpeed(1) / leader_maximum_deceleration)
		if sqrtContent >= 0:
			congested_speed = factor + math.sqrt(sqrtContent)
		else:
			# rmq. : le modèle GIPPS ne prévoit pas que les véhicules puissent se rentrer dedans. Si ca arrive, pour pas avoir une vitesse indéfinie, on met une vitesse nulle.
			congested_speed = 0
			
		if congested_speed  < computed_speed:
			free_flow_state = False
			computed_speed = congested_speed
		
	context.SetFreeFlow(free_flow_state)
	car_following_model.SetComputedTravelSpeed(computed_speed)
	
	return
	
def gipps_max_influence_distance(network, car_following_model, parameters, context, prev_context):
	# remarque : Pour gipps, on prend un multiple de la distance max marcourue pendant un pas de temps. Peut être possible de faire mieux.
	return 3 * car_following_model.GetVehicle().GetMaxSpeed() * network.GetTimeStep()
	
def gipps_approx_speed(network, car_following_model, parameters, context, prev_context, distance_between_vehicles, leader, vehicle):
	# pas fait pour l'instant : problème en cas de boucle impliquant des véhicules Newell et Gipps. Tant qu'on ne fait pas de simulation mixte avec ces deux modèles, on ne risque rien
	print 'not implemented yet'
	return 0;
	
def gipps_lane_speed(network, car_following_model, parameters, context, prev_context, target_lane):
	# pas fait pour l'instant : on n'utilise pas le mode de changement de voie 'F'
	print 'not implemented yet'
	return 0;
	
def idm(network, car_following_model, parameters, context, prev_context, time_step, instant):
	"""
	Loi de poursuite de IDM
	"""
	
	vehicle = car_following_model.GetVehicle()
	
	computed_acceleration = 0
	free_flow_state = True
	

	if len(context.GetLstLanes()) != 0:
		first_lane = context.GetLstLanes()[0]
		max_speed_on_lane = first_lane.GetParent().GetSpeedLimit(vehicle.GetType(),instant,context.GetStartPosition(), first_lane.GetNum())
		max_speed_on_lane = min(max_speed_on_lane, vehicle.GetMaxSpeed());
		maximum_acceleration = vehicle.GetType().GetMaxAcc(vehicle.GetSpeed(1))
		deceleration = vehicle.GetType().ComputeDeceleration()
		
		# dans SymuVia, si aucune décélération n'est renseignée pour un type de véhicule, la valeur de deceleration vaut 0.
		# Pour être cohérent, il faut interpreter cette valeur comme étant une délécération infinie (le véhicule peut "piler").
		if deceleration == 0:
			deceleration = sys.float_info.max
			
		# Calcul de Z
		if len(context.GetLeaders()) != 0:
			first_leader = context.GetLeaders()[0]
			vehicle_distance = context.GetLeaderDistances()[0]
			delta_s_prime = vehicle.GetType().GetSpacingAtStop() + max( float(parameters["T"]) * vehicle.GetSpeed(1)
				+ vehicle.GetSpeed(1) * ( vehicle.GetSpeed(1) - first_leader.GetSpeed(1)) / (2 * math.sqrt(maximum_acceleration * deceleration)),0)
			if vehicle_distance > first_leader.GetLength():
				z = delta_s_prime / (vehicle_distance - first_leader.GetLength())
			else:
				z = sys.float_info.max
			free_flow_state = z < 1
		else:
			z = 0
		
		# Calcul de l'acceleration
		if int(parameters["improved"]) == 1:
			if vehicle.GetSpeed(1) <= max_speed_on_lane:
				if z >= 1:
					computed_acceleration = maximum_acceleration * (1 - z*z)
				else:
					a_free = maximum_acceleration * (1 - pow(vehicle.GetSpeed(1) / max_speed_on_lane, float(parameters["alpha"])))
					if a_free != 0:
						computed_acceleration = a_free * (1 - pow(z, float(parameters["beta"]) * maximum_acceleration / a_free))
					else:
						computed_acceleration = 0
			else:
				a_free = - deceleration * (1 - pow(max_speed_on_lane / vehicle.GetSpeed(1), maximum_acceleration * float(parameters["alpha"]) / deceleration))
				if z >= 1:
					computed_acceleration = a_free + maximum_acceleration * (1 - pow(z, float(parameters["beta"])))
				else:
					computed_acceleration = a_free
		else:
			if z == sys.float_info.max:
				# Pour se prémunir d'une OverFlowError si on dépasse la valeur max d'un float
				computed_acceleration = -sys.float_info.max
			else:
				free_flow_component = pow(vehicle.GetSpeed(1) / max_speed_on_lane, float(parameters["alpha"]))
				congested_component = pow(z, float(parameters["beta"]))
				computed_acceleration = maximum_acceleration * (1 - free_flow_component - congested_component)
			
	context.SetFreeFlow(free_flow_state)
	car_following_model.SetComputedTravelAcceleration(computed_acceleration)
	
	return
	
def idm_max_influence_distance(network, car_following_model, parameters, context, prev_context):
	deceleration = car_following_model.GetVehicle().GetType().GetDeceleration()
	
	# dans SymuVia, si aucune décélération n'est renseignée pour un type de véhicule, la valeur de deceleration vaut 0.
	# Pour être cohérent, il faut interpreter cette valeur comme étant une délécération infinie (le véhicule peut "piler").
	if deceleration == 0:
		deceleration = sys.float_info.max
		
	max_speed = car_following_model.GetVehicle().GetMaxSpeed()
	max_desired_spacing = car_following_model.GetVehicle().GetType().GetSpacingAtStop() + max(float(parameters["T"])*max_speed + max_speed*max_speed/(2*math.sqrt(car_following_model.GetVehicle().GetType().GetMaxAcc(max_speed) * deceleration)),0)
	return 3 * max_desired_spacing
	
def idm_approx_speed(network, car_following_model, parameters, context, prev_context):
	# pas fait pour l'instant : problème en cas de boucle impliquant des véhicules Newell et IDM. Tant qu'on ne fait pas de simulation mixte avec ces deux modèles, on ne risque rien
	print 'not implemented yet'
	return 0;
	
def idm_lane_speed(network, car_following_model, parameters, context, prev_context, target_lane):
	# pas fait pour l'instant : on n'utilise pas le mode de changement de voie 'F'
	print 'not implemented yet'
	return 0;
	return 0;

def ll(network, car_following_model, parameters, context, prev_context, time_step, instant):
	"""
	Loi de poursuite de Jorge (LL)
	"""
	
	vehicle = car_following_model.GetVehicle()
	
	# Calcul de la vitesse libre désirée
	#####################################
	computed_distance = 0
	free_flow_state = True
	if len(context.GetLstLanes()) != 0:
		first_lane = context.GetLstLanes()[0]
		u = first_lane.GetParent().GetSpeedLimit(vehicle.GetType(),instant,context.GetStartPosition(), first_lane.GetNum())
		u = min(u, vehicle.GetMaxSpeed());
		
		# distance parcourue au maximum avec accélération infinie
		utau = u * time_step
		
		# prise en compte de l'acceleration max (rmq. : si on défini des plages d'accélération,
		# celà reste-t-il valable ? faut-il parcourir les plages pour récupérer la valeur max ?)
		am = vehicle.GetType().GetMaxAcc(vehicle.GetSpeed(1))
		# rmq. on suppose une pente de la route nulle ce qui simplifie l'équation
		x_bar = u * time_step - ((1-math.exp(-time_step*am/u))*(u - vehicle.GetSpeed(1))) / (am/u)
		computed_distance = min(utau,x_bar)
		
	if len(context.GetLeaders()) != 0:
		first_leader = context.GetLeaders()[0]
		vehicle_distance = context.GetLeaderDistances()[0]
        # rmq. non précisé dans le papier, mais apparemment il faut bien prendre le Kmax du leader.
		delta = 1/first_leader.GetDiagFonda().Kmax
		congested_distance = vehicle_distance - delta
		if congested_distance < computed_distance:
			computed_distance = congested_distance
			free_flow_state = False
		
	context.SetFreeFlow(free_flow_state)
	car_following_model.SetComputedTravelledDistance(computed_distance)
		
	return
	
def ll_max_influence_distance(network, car_following_model, parameters, context, prev_context):
	# remarque : on utilise la même formule que pour Newell
	return 1 / network.GetMinKv()
	
def ll_approx_speed(network, car_following_model, parameters, context, prev_context, distance_between_vehicles, leader, vehicle):
	# pas fait pour l'instant : problème en cas de boucle impliquant des véhicules Newell et LL. Tant qu'on ne fait pas de simulation mixte avec ces deux modèles, on ne risque rien
	print 'not implemented yet'
	return 0;
	
def ll_lane_speed(network, car_following_model, parameters, context, prev_context, target_lane):
	# pas fait pour l'instant : on n'utilise pas le mode de changement de voie 'F'
	print 'not implemented yet'
	return 0;
	
