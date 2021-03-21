import os
import pandas as pd

class file():
    #path = "Z:\BB RISK\BB DATA\\2020\8. Aug 2020\MIS"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    master =  pd.read_csv(dir_path + r"\bb.txt",
                           delimiter = "\t",
                           header =0,
                           na_values='?',
                           engine='python',
                           dtype={'Account_Num':str,"Balance":int})
    
    
  
    validation = {
        'ODTL1' :{
            'filename' : 'ODTL FY 1112 SMF Product table',
            'sheet'    : 'OD',
            'merge_on' : 'Account_No',
            'check_on' : 'M_Bnm_Balance_SUM1' 
        },
        'ODTL2' :{
            'filename' : 'ODTL FY 1112 SMF Product table',
            'sheet'    : 'TL',
            'merge_on' : 'M_Account_No',
            'check_on' : 'M_Bnm_Balance' 
        },
        'STRC_BC' :{
            'filename' : 'STRC FY 1112 product table 1',
            'sheet'    : 'STRC_BB_monthly_4',
            'merge_on' : 'M_Cus_No',
            'check_on' : 'M_Bnm_Balance_SUM' 
        },
        'OD' :{
            'filename' : 'OD Cr Bal 1011 product table',
            'sheet'    : 'Recovered_Sheet1',
            'merge_on' : 'Account_No',
            'check_on' : 'M_Bnm_Balance_SUM1' 
        },
        'Trade_F' :{
            'filename' : 'TRADE FY1112 product table Funded',
            'sheet'    : 'Trade_BB_monthly',
            'merge_on' : 'M_Cus_No',
            'check_on' : 'M_Bnm_Balance_SUM' 
        },
        'Trade_NF' :{
            'filename' : 'TRADE FY1112 product table (Non Funded)',
            'sheet'    : 'Trade_BB_monthly',
            'merge_on' : 'Account No',
            'check_on' : 'M Bnm Balance SUM' 
        }
    }
    
    
    

    preparation = {
        'GIL' :{
            'filename' : 'GIL by BC Dec20',
            'sheet'    : 'GILDec20',
            'skiprows' : '3'
        },
        'LB' :{
            'filename' : 'LB Dec20',
            'sheet'    : 'Funded',
            'skiprows' : '2'
        },
        'LB' :{
            'filename' : 'LB Dec20',
            'sheet'    : 'Unfunded',
            'skiprows' : '0'
        },
        'NOB' :{
            'filename' : 'NOB Code Value Chain (Jan 2017)',
            'sheet'    : 'Latest aftr Renew. Energy Align',
            'skiprows' : '2'
        },
    }

