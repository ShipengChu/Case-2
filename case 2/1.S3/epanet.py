from epanettools import epanet2 as et
from epanettools.examples import simple
from global_variable import *
import numpy as np
import pandas as pd
import copy
def openEPANET(INP):
    errcode=et.ENopen(INP,"BUFF.rpt","")
    if(errcode>100):
        print('error in open INP')

def saveInpfile(fileName):
    errcode=et.ENsaveinpfile(fileName)

def closeEPANET():
    errcode=et.ENclose()

def getResidulSqure_EPA(MeaData):
    errcode=et.ENopen(ResultInp,"BUFF.rpt","")
    errcode=et.ENsolveH()
    ResidulSqure={}
    ResidulSqure['Res']={}
    ResidulSqure['P']={}
    ResidulSqure['F']={}
    print_R_RES=0
    print_R_Pre=0
    print_R_Flo=0
    residul=[]
    for id in MeaData.ResID:
        [errcode,index]=et.ENgetnodeindex(id)
        [errcode,value]=et.ENgetnodevalue(index,et.EN_DEMAND)
        ResidulSqure['Res'][id]=(value-MeaData.Data['Res'][id])**2
        print_R_RES=print_R_RES+ResidulSqure['Res'][id]
        residul.append(value-MeaData.Data['Res'][id])
    if(len(MeaData.ResID)>0):
        print_R_RES=print_R_RES/len(MeaData.ResID)

    for id in MeaData.PreID:
        [errcode,index]=et.ENgetnodeindex(id)
        [errcode,value]=et.ENgetnodevalue(index,et.EN_PRESSURE)
        ResidulSqure['P'][id]=(value-MeaData.Data['P'][id])**2
        print_R_Pre=print_R_Pre+ResidulSqure['P'][id]
        residul.append(value-MeaData.Data['P'][id])
    if(len(MeaData.PreID)>0):
        print_R_Pre=print_R_Pre/len(MeaData.PreID)

    for id in MeaData.FloID:
        [errcode,index]=et.ENgetlinkindex(id)
        [errcode,value]=et.ENgetlinkvalue(index,et.EN_FLOW)
        ResidulSqure['F'][id]=(value-MeaData.Data['F'][id])**2
        print_R_Flo=print_R_Flo+ResidulSqure['F'][id]
        residul.append(value-MeaData.Data['F'][id])
    if(len(MeaData.FloID)>0):
        print_R_Flo=print_R_Flo/len(MeaData.FloID)

    errcode=et.ENclose()
    print('ave Squre error:          Res          Flo               Pre')
    print('               '+str(print_R_RES)+'    '+str(print_R_Flo)+'    '+str(print_R_Pre))
    return [ResidulSqure,residul]


def generateEstimateDemandResult(ResID_Total,PreID_Total):

    result=estimateDemandResult()
    result.time=0
    result.demand_dim=DEMAND_NUM
    result.sensorID_Res=ResID_Total
    result.sensorID_P=PreID_Total    #pressure sensor ID

    result.cali_demand_values=[INITIAL_DEMAND]*DEMAND_NUM
    result.cali_demand_variance=INITIAL_DEMAND_VARIANCE*np.identity(DEMAND_NUM)
    result.cali_nodal_p=[]  #nodal pressure
    result.cali_pipe_f=[]  #pipe flow

    result.measured_sensor={}
    result.cali_sensor={}
    result.cali_resid={}
    return result


class estimateDemandResult:
    def _init_(self):
        self.time=0
        self.demand_dim=0
        self.sensorID_Res=[]
        self.sensorID_P=[]    #pressure sensor ID
        self.sensorID_F=[]    #Flow sensor ID

        self.cali_demand_values=[]#外部更新
        self.cali_demand_variance=[]#外部更新

        self.cali_nodal_p=[]  #nodal pressure
        self.cali_pipe_f=[]  #pipe flow
        self.measured_sensor={}
        self.cali_sensor={}
        self.cali_resid={}

    def hyd_simulation(self,ResultInp):
        errcode=et.ENopen(ResultInp,'r.rtp','')
        errcode=et.ENsolveH()
    
    def readDemandVariance(self,demandVariance):
        self.cali_demand_variance=[]
        demand_variance=pd.read_csv(DemandVariance,header=None).values.tolist()
        self.cali_demand_variance=copy.deepcopy(demand_variance)


    def updateResult(self,ResultInp):
        errcode=et.ENopen(ResultInp,'r.rtp','')
        errcode=et.ENsolveH()
        #########update the calibrated value at sensors#########
        Res={}
        P={}
        F={}

        for id in self.sensorID_Res:
            [errcode,index]=et.ENgetnodeindex(id)
            [errcode,demand]=et.ENgetnodevalue(index,et.EN_DEMAND)
            Res[id]=demand
        for id in self.sensorID_P:
            [errcode,index]=et.ENgetnodeindex(id)
            [errcode,pressure]=et.ENgetnodevalue(index,et.EN_PRESSURE)
            P[id]=pressure

 #       for id in self.sensorID_F:
 #           [errcode,index]=et.ENgetlinkindex(id)
 #           [errcode,flow]=et.ENgetlinkvalue(index,et.EN_FLOW)
 #           F[id]=flow
        self.cali_sensor['Res']=Res
        self.cali_sensor['P']=P#Save the simulated sensor pressure
 #       self.cali_sensor['F']=F#Save the simulated sensor flow
        #########update the calibrated nodal pressure and pipe flow rate#########
        self.cali_demand_values=[]
        self.cali_nodal_p=[]#需要初始化
        self.cali_pipe_f=[]
        for index in range(self.demand_dim):
            [errcode,pressure]=et.ENgetnodevalue(index+1,et.EN_PRESSURE)
            self.cali_nodal_p.append(pressure)
            [errcode,demand]=et.ENgetnodevalue(index+1,et.EN_DEMAND)
            self.cali_demand_values.append(demand)
        for index in range(Number_PIPES):
            [errcode,flow]=et.ENgetlinkvalue(index+1,et.EN_FLOW)
            self.cali_pipe_f.append(flow)
        errcode=et.ENclose()
        

    def measuredResid(self,MeaData):
        self.cali_resid={}
        self.cali_resid['Res']={}
        self.cali_resid['P']={}
        self.cali_resid['F']={}

        for id in MeaData.ResID:
            self.cali_resid['Res'][id]=self.cali_sensor['Res'][id]-MeaData.Data['Res'][id]
        for id in MeaData.PreID:
            self.cali_resid['P'][id]=self.cali_sensor['P'][id]-MeaData.Data['P'][id]
 #       for id in MeaData.FloID:
 #           self.cali_resid['F'][id]=self.cali_sensor['F'][id]-MeaData.Data['F'][id]



