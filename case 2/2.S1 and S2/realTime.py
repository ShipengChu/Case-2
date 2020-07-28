import numpy as np
import pandas as pd
import os
from global_variable import *
from Sensors import *
from priorDistribution import *
from calibration import *
from outPut import *

ResMea = pd.read_csv(PATH+'measuredRes.csv',parse_dates=True,index_col=0,encoding = 'utf-8')
PreMea=pd.read_csv(PATH+'measuredPressure.csv',parse_dates=True,index_col=0,encoding = 'utf-8')
DemandMea=pd.read_csv(PATH+'measuredDemand.csv',parse_dates=True,index_col=0,encoding = 'utf-8')
DemandMea_std=pd.read_csv(PATH+'DemandStd.csv',parse_dates=True,index_col=0,encoding = 'utf-8')
TIME=PreMea.index

MeaData=sensor_initial(ResID_Total,PreID_Total)
result_previous=generateEstimateDemandResult(ResID_Total,PreID_Total)
priorDist=generatePriorDist()

Simu_num=0
copyInp(Inp)
for time in TIME:
    copyInp(Inp)
    if Simu_num>Simulation_Num:
        break
    print(time)
    #update inp elevation
    if time in range(ElevationTime[0][0],ElevationTime[0][1]):
        setElevation(ElevationID[0],ElevationChang[0])
    if time in range(ElevationTime[1][0],ElevationTime[1][1]):
        setDiameter(PipeDiameterID,PipeDiaChange)

    ##update measurements
    MeaData.updateMeasured(ResMea,PreMea,time)
    MeaData.predict()
    alpha=MeaData.alpha_predict+1
    fai_predict_mat=MeaData.fai_predict_mat
    fai_l_mat=copy.deepcopy(fai_predict_mat) #initization fai_l for the following loopp
    ##update prior distribution
    priorDist.predictUpdate(result_previous)
    priorDist.updatePrior(DemandMea,DemandMea_std,time)
#    priorDist.updatePriorVariance()
    for iter in range(VB_ITERS):
        MeaData.updatePara(alpha,fai_l_mat)#更新MeaData.fai和MeaData.R
        generateInputFile(MeaData,priorDist)#更新input data
        WDS_Calibration(exePath,InpCopy,InputData,ResultInp)#最大化step 1
        [ResidulSqure,residul]=getResidulSqure_EPA(MeaData)#计算均方残差
        fai_l_mat=getfai_l(fai_predict_mat,residul)#更新fai_l
#end loop for the VB iterations
    MeaData.alpha=alpha
    MeaData.updatePara(alpha,fai_l_mat)

    SUMMARY_R.append(copy.deepcopy(MeaData))

    result_previous.time=time
    result_previous.updateResult(ResultInp)
    result_previous.readDemandVariance(DemandVariance)
    result_previous.measuredResid(MeaData)
    SUMMARY_RESULT.append(copy.deepcopy(result_previous))
    Simu_num=Simu_num+1
    
    if(Simu_num%144==0):
        try:
            outPutCalibrated(SUMMARY_RESULT,ResID_Total,PreID_Total,PipeID_Total,Simu_num)
            outPutMeasured(SUMMARY_R,ResID_Total,PreID_Total,PipeID_Total,Simu_num)
        except:
            print('error')
    print('#############################################################################')
outPutCalibrated(SUMMARY_RESULT,ResID_Total,PreID_Total,PipeID_Total,Simu_num)
outPutMeasured(SUMMARY_R,ResID_Total,PreID_Total,PipeID_Total,Simu_num)