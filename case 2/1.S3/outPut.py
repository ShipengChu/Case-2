import numpy as np
import pandas as pd
from global_variable import *
import copy
import os



def outPutCalibrated(calibratedResult,ResID_Total,PREID_Total,PIPEID_Total,Simu_num):
    TOTAL_SENSOR_ID=ResID_Total+PREID_Total+PIPEID_Total
    _measured_calibrated={}
    _demand_calibrated={}
    _demand_vairance_calibrated={}
    _Nodal_Pressure_calibrated={}
    _Pipe_Flow_calibrated={}

    for id in TOTAL_SENSOR_ID:
        _measured_calibrated[id]=[]

    for i in range(DEMAND_NUM):
        _demand_calibrated[i]=[]
        _demand_vairance_calibrated[i]=[]
        _Nodal_Pressure_calibrated[i]=[]

    for i in range(Number_PIPES):
        _Pipe_Flow_calibrated[i]=[]


    time=[]
    for result in calibratedResult:
        time.append(result.time)
        for id in TOTAL_SENSOR_ID:
            if id in ResID_Total:
                _measured_calibrated[id].append(result.cali_sensor['Res'][id])
            if id in PREID_Total:
                _measured_calibrated[id].append(result.cali_sensor['P'][id])
            if id in PIPEID_Total:
                _measured_calibrated[id].append(result.cali_sensor['F'][id])
        for i in range(DEMAND_NUM):
            _demand_calibrated[i].append(result.cali_demand_values[i])
            _demand_vairance_calibrated[i].append(result.cali_demand_variance[i][i])
            _Nodal_Pressure_calibrated[i].append(result.cali_nodal_p[i])
        for i in range(Number_PIPES):
            _Pipe_Flow_calibrated[i].append(result.cali_pipe_f[i])

    df=pd.DataFrame(_measured_calibrated)
    df['time']=time
#    df.reset_index(['time'], inplace=True)
    df.to_csv(PATH_Result+'\\Measured_calibrated_VB_'+str(Simu_num)+'.csv')

    df=pd.DataFrame(_demand_calibrated)
    df['time']=time
#    df.reset_index(['time'], inplace=True)
    df.to_csv(PATH_Result+'\\Demand_calibrated_VB_'+str(Simu_num)+'.csv')

    df=pd.DataFrame(_demand_vairance_calibrated)
    df['time']=time
#    df.reset_index(['time'], inplace=True)
    df.to_csv(PATH_Result+'\\Demand_vairance_calibrated_VB_'+str(Simu_num)+'.csv')

    df=pd.DataFrame(_Nodal_Pressure_calibrated)
    df['time']=time
#    df.reset_index(['time'], inplace=True)
    df.to_csv(PATH_Result+'\\Nodal_Pressure_calibrated_VB_'+str(Simu_num)+'.csv')

    df=pd.DataFrame(_Pipe_Flow_calibrated)
    df['time']=time
#    df.reset_index(['time'], inplace=True)
    df.to_csv(PATH_Result+'\\Pipe_Flow_calibrated_VB_'+str(Simu_num)+'.csv')

def outPutMeasured(meauredResult,ResID_Total,PREID_Total,PIPEID_Total,Simu_num):
    TOTAL_SENSOR_ID=ResID_Total+PREID_Total+PIPEID_Total
    _measured_STD={}
    for id in TOTAL_SENSOR_ID:
        _measured_STD[id]=[]

    time=[]
    for result in meauredResult:
        time.append(result.currentTime)
        for id in TOTAL_SENSOR_ID:
            if id in ResID_Total:
                _measured_STD[id].append(result.R['Res'][id])
            if id in PREID_Total:
                _measured_STD[id].append(result.R['P'][id])
            if id in PIPEID_Total:
                _measured_STD[id].append(result.R['F'][id])
    df=pd.DataFrame(_measured_STD)
    df['time']=time
 #   df.reset_index(['time'], inplace=True)
    df.to_csv(PATH_Result+'\\Measured_STD_VB_'+str(Simu_num)+'.csv')