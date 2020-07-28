import numpy as np
import pandas as pd
import os
#define the GLOBAL variable
PATH=os.path.abspath('.')+'\\measuredData\\'#
PATH_Result=os.path.abspath('.')+'\\result\\'#
#define particle parameters
Simulation_Num=1000
VB_ITERS=2
#define the hyd_demand
DEMAND_NUM=381   #Number of nodal water demands
Number_PIPES=469
SENSOR_NUM=11
#define std
DEMAND_PREDICT_STD=[2]*DEMAND_NUM
MEASURED_DEMAND_STD_SCALE=10
Measured_Demand=[0]*DEMAND_NUM

#define initial demand
INITIAL_DEMAND=2
INITIAL_DEMAND_VARIANCE=50
#define IW patamerer
Sensor_T=0.97
Sensor_B=Sensor_T*np.identity(SENSOR_NUM)
#define the calibration file
ResID_Total=['407']
PreID_Total=['53','65','111','154','158','229','234','236','340','381']
PipeID_Total=[]
Inp='Case2_no_pattern.inp'  # 不能有模式
exePath = "iterative Sh-Mo_CUDA.exe"
InputData='case_2.obs'
ResultInp='result_2.inp'
DemandVariance='demand_var.csv'
JacobyMat='jacoby.csv'
#define

#define the result
SUMMARY_RESULT=[]
SUMMARY_R=[]