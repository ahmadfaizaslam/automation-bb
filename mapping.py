#%%
import pandas as pd
import numpy as np
import os
import math

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

print('1. Loading Files...\n')
master =  pd.read_csv(dir_path + r"\bb.txt",
                           delimiter = "\t",
                           header =0,
                           na_values='?',
                           engine='python',
                           parse_dates=['NPL_Date','RISK_RATG_DT'],
                           dtype={'Party_Id':object,'SPL_MENTION_ACCT_IND':object})
master.rename(columns={"Party_Id": "GCIF"},inplace= 'true')
print('Master file loaded completed.')


GIL_BCraw = pd.read_excel(dir_path+r"\Code and reference\GIL by BC Dec20.xlsx",sheet_name='GILDec20',skiprows=3,dtype={'GCIF #':str,'Stage 3 Reason':str})
LB_Funded = pd.read_excel(dir_path+r"\Code and reference\LB Dec20.xlsx",sheet_name='Funded',skiprows=2,dtype={'M_Cus_No':str})
NOB_Code = pd.read_excel(dir_path+r"\Code and reference\\NOB Code Value Chain (Jan 2017).xlsx",sheet_name='Latest aftr Renew. Energy Align',skiprows = 2)
LB_NFunded = pd.read_excel(dir_path+r"\Code and reference\LB Dec20.xlsx",sheet_name='Unfunded',dtype={'M_Cus_No':str})
# %%
# GIL_BCraw.head()
# %%
def gil_bc(frame,master):
    conditions = [ (GIL_BCraw['Stage 3 Reason']=="NPL Flag Y"),
                   (GIL_BCraw['Stage 3 Reason']=="Impairment Status Y"),
                   (GIL_BCraw['Stage 3 Reason']=="Rescheduled"),
                   (GIL_BCraw['Stage 3 Reason']=="Restructured") ]

    values = ['NPL','IPL','IPL R&R', 'IPL R&R']
    GIL_BCraw['PL IPL IPL R&R NPL'] = np.select(conditions, values)
    GIL_BCfinal = GIL_BCraw[['GCIF #','PL IPL IPL R&R NPL']]  
    masterbb =master.merge(GIL_BCfinal,how='left',left_on="GCIF",right_on='GCIF #')
    masterbb['PL IPL IPL R&R NPL']= masterbb['PL IPL IPL R&R NPL'].replace(np.nan,'PL')
    masterbb.drop(columns=['GCIF #'],inplace= True)

    return masterbb
# %%
def lb_fund(LB_Funded,NOB_Code,masterbb):
    LB_Funded1= LB_Funded[['M_Cus_No','NOB']]
    LB_Funded1['Broad Code']=(np.floor(LB_Funded1['NOB']/1000))*1000
    LB_Funded1 =LB_Funded1.merge(NOB_Code,how='left',left_on='NOB',right_on='NOB Code')
    LB_Funded2 = LB_Funded1[['M_Cus_No','NOB','Broad Code','NOB Desc','Sub Sector Desc']].copy()
    LB_Funded2 =LB_Funded2.merge(NOB_Code,how='left',left_on='Broad Code',right_on='NOB Code')
    LB_Fundedfinal = LB_Funded2[['M_Cus_No','NOB','Broad Code','NOB Desc_x','Sub Sector Desc_x','NOB Desc_y']].copy()
    LB_Fundedfinal.rename({'NOB Desc_x':'NOB Desc','Sub Sector Desc_x':'Subsector','NOB Desc_y': 'Broad Sector'},axis='columns',inplace=True)
    
    return LB_Fundedfinal
# %%
def lb_nfund(LB_NFunded,NOB_Code,masterbb):
    LB_NFunded1= LB_NFunded[['M_Cus_No','Nature_of_Business']]
    # LB_NFunded1['Broad Code']=(np.floor(LB_NFunded1['Nature_of_Business']/1000))*1000
    # LB_NFunded2 =LB_NFunded2.merge(NOB_Code,how='left',left_on='Broad Code',right_on='NOB Code')
    # LB_NFundedfinal = LB_NFunded2[['M_Cus_No','Nature_of_Business','Broad Code','NOB Desc_x','Sub Sector Desc_x','NOB Desc_y']].copy()
    # LB_NFundedfinal.rename({'Nature_of_Business':'NOB','NOB Desc_x':'NOB Desc','Sub Sector Desc_x':'Subsector','NOB Desc_y': 'Broad Sector'},axis='columns',inplace=True)

    return LB_NFunded1

masterbb= gil_bc(GIL_BCraw,master)

LB_NFundedfinal = lb_fund(LB_NFunded,NOB_Code,masterbb)
LB_NFundedfinal.head()
# %%
LB_Fundedfinal = lb_fund(LB_Funded,NOB_Code,masterbb)
LB_Fundedfinal.head()
# %%
