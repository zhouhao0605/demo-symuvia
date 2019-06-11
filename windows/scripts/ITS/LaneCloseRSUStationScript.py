#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import symuvia
import symuviautils

def Run(network,parameters,timeStart,timeDuration):

	message = "Action;RunApplication/target;ChangeLaneAppliScript/Lane;2"
	parameters["this"].SendBroadcastMessage(message,timeStart,-1.0, False)