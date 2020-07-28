import numpy as np
import pandas as pd
import copy
from global_variable import *


def sensor_initial(ResID_Total,PreID_Total):
    MeaData=sensors()
    MeaData.t=Sensor_T
    MeaData.SENSOR_NUM=len(ResID_Total)+len(PreID_Total)
    MeaData.ResID=[]
    MeaData.PreID=[]
    MeaData.FloID=[]
    MeaData.alpha=200
#initial fai
    MeaData.fai['Res']={}
    MeaData.fai['P']={}
    MeaData.fai['F']={}
    for id in ResID_Total:
        MeaData.fai['Res'][id]=450000
    for id in PreID_Total:
        MeaData.fai['P'][id]=15000
    MeaData.fai_predict=copy.deepcopy(MeaData.fai)
    #The following codes are the current version
    MeaData.fai_mat=np.identity(MeaData.SENSOR_NUM)*150000
    MeaData.fai_predict_mat=copy.deepcopy(MeaData.fai_mat)
#initial R
    MeaData.R['Res']={}
    MeaData.R['P']={}
    MeaData.R['F']={}
    for id in ResID_Total:
        MeaData.R['Res'][id]=MeaData.fai['Res'][id]/(MeaData.alpha-MeaData.SENSOR_NUM-1)
    for id in PreID_Total:
        MeaData.R['P'][id]=MeaData.fai['P'][id]/(MeaData.alpha-MeaData.SENSOR_NUM-1)
    return MeaData



def getfai_l(fai_predict_mat,residul):
    jacoby=pd.read_csv(JacobyMat,index_col=0,header=None)
    index=jacoby.index
    jacoby=jacoby.values
    demand_variance=pd.read_csv(DemandVariance,header=None).values
    GP=np.dot(jacoby,demand_variance)
    GPG=np.dot(GP,jacoby.T)

    resid=np.array(residul).reshape(SENSOR_NUM,1)
    fai_l_mat=fai_predict_mat+GPG+np.dot(resid,resid.T)
    return fai_l_mat


def getR(MeaData, fai_l,alpha):
    R={}
    R['Res']={}
    R['P']={}
    R['F']={}
    for id in MeaData.ResID:
        R['Res'][id]=fai_l['Res'][id]/(alpha-MeaData.SENSOR_NUM-1)
    for id in MeaData.PreID:
        R['P'][id]=fai_l['P'][id]/(alpha-MeaData.SENSOR_NUM-1)
    for id in MeaData.FloID:
        R['F'][id]=fai_l['F'][id]/(alpha-MeaData.SENSOR_NUM-1)
    return R


class sensors:
    def __init__(self):
        self.currentTime=0
        self.SENSOR_NUM=0
        self.t=0.99#IW分布全局参数
        self.alpha=0  #IW分布参数
        self.fai={} #IW分布参数
        self.fai_mat=[]
        self.R={}#协方差
        self.R_mat=[]
        self.alpha_predict={}  #IW分布参数
        self.fai_predict={} #IW分布参数
        self.ResID=[]
        self.PreID=[]    #pressure sensor ID
        self.FloID=[]    #Flow sensor ID
        self.Data={} #measured values
    def updateMeasured(self,ResMea,PreMea,time):
        self.ResID=[]
        self.PreID=[]
        self.FloID=[]
        self.currentTime=time
        self.Data['Res']={}
        self.Data['P']={}
        self.Data['F']={}
        #reading Res_ChengXi
        Res=ResMea.loc[time]
        ID=ResMea.keys()
        for id in ID:
            if not np.isnan(Res[id]):
                self.Data['Res'][id]=Res[id]
                self.ResID.append(id)

        Pre=PreMea.loc[time]
        ID=Pre.keys()
        for id in ID:
            if not np.isnan(Pre[id]):
                self.Data['P'][id]=Pre[id]#mpa to m
                self.PreID.append(id)

        self.SENSOR_NUM=len(self.ResID)+len(self.PreID)


    def predict(self):#prior value
        self.alpha_predict=self.t*(self.alpha-self.SENSOR_NUM-1)+self.SENSOR_NUM+1

        self.fai_predict_mat=np.dot(Sensor_B,self.fai_mat)
        self.fai_predict_mat=np.dot(self.fai_predict_mat,Sensor_B.T)


    def updatePara(self,alpha,fai_l):
        self.fai_mat=copy.deepcopy(fai_l)
        self.R_mat=self.fai_mat/(alpha-SENSOR_NUM-1)

        for i in range(len(ResID_Total)):
            id = ResID_Total[i]
            self.R['Res'][id]=self.R_mat[i][i]
        for i in range(len(PreID_Total)):
            id = PreID_Total[i]
            self.R['P'][id]=self.R_mat[i+len(ResID_Total)][i+len(ResID_Total)]
        for i in range(len(PipeID_Total)):
            id=PipeID_Total[i]
            self.R['F'][id]=self.R_mat[i+len(ResID_Total)+len(PreID_Total)][i+len(ResID_Total)+len(PreID_Total)]


