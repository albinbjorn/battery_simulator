import numpy as np

def determine_P_instruct(load, P_activate, P_battery_max):
	if load <= P_activate and (P_activate - load >= P_battery_max):
		P_instruct = P_battery_max
	elif load <= P_activate and (P_activate - load < P_battery_max):
		P_instruct = P_activate - load
	elif load >= P_activate and (load - P_activate > P_battery_max):
		P_instruct = -P_battery_max
	elif load >= P_activate and (load - P_activate <= P_battery_max):
		P_instruct = -(load - P_activate)

	return P_instruct

def determine_P_actual(P_instruct, SoC_current, SoC_max):
	if P_instruct >= 0 and SoC_current == SoC_max:
		P_actual = 0
	elif P_instruct <= 0 and SoC_current == 0:
		P_actual = 0
	elif P_instruct > 0 and SoC_current == 0:
		P_actual = P_instruct
	elif P_instruct >= 0 and SoC_current <= (SoC_max - P_instruct):
		P_actual = P_instruct
	elif P_instruct <= 0 and SoC_current >= abs(P_instruct):
		P_actual = P_instruct
	elif P_instruct >= 0 and P_instruct > (SoC_max - SoC_current):
		P_actual = SoC_max - SoC_current
	elif P_instruct <= 0 and abs(P_instruct) > SoC_current:
		P_actual = -SoC_current

	return P_actual

def batt_algo(loadvec, P_activate, P_battery_max, SoC_max, SoC_initial):
	loadvec = np.array(loadvec).reshape(-1,1)
	SoC = np.zeros((loadvec.shape[0]+1,1))
	SoC[0] = SoC_initial
	P_battery = np.zeros(loadvec.shape)

	for i in range(loadvec.shape[0]):
		P_instruct = determine_P_instruct(loadvec[i], P_activate, P_battery_max)
		
		P_battery[i] = determine_P_actual(P_instruct, SoC[i], SoC_max)
		

		SoC[i+1] = SoC[i] + P_battery[i]

		

	SoC = SoC[1:]
	return P_battery, SoC