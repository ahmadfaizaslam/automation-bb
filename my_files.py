import os
import pandas as pd

class file():
    dir_path = os.path.dirname(os.path.realpath(__file__)) #"Z:\BB RISK\BB DATA\\2020\8. Aug 2020
    
    master =  pd.read_csv(dir_path + r"\bb.txt",
                           delimiter = "\t",
                           header =0,
                           na_values='?',
                           engine='python',
                           dtype={'Account_Num':str,"Balance":int})
    
    validation = {  #dictionaries should not have duplicate keys.... if needed, do a list in dictionaries
        'odtl1' :{
            'filename' : 'ODTL FY 1112 SMF Product table',
            'sheet'    : 'OD',
            'merge_on' : 'Account_No',
            'check_on' : 'M_Bnm_Balance_SUM1' 
        },
        'odtl2' :{
            'filename' : 'ODTL FY 1112 SMF Product table',
            'sheet'    : 'TL',
            'merge_on' : 'M_Account_No',
            'check_on' : 'M_Bnm_Balance' 
        },
        'strc_bc' :{
            'filename' : 'STRC FY 1112 product table 1',
            'sheet'    : 'STRC_BB_monthly_4',
            'merge_on' : 'M_Cus_No',
            'check_on' : 'M_Bnm_Balance_SUM' 
        },
        'od' :{
            'filename' : 'OD Cr Bal 1011 product table',
            'sheet'    : 'Recovered_Sheet1',
            'merge_on' : 'Account_No',
            'check_on' : 'M_Bnm_Balance_SUM1' 
        },
        'trade_f' :{
            'filename' : 'TRADE FY1112 product table Funded',
            'sheet'    : 'Trade_BB_monthly',
            'merge_on' : 'M_Cus_No',
            'check_on' : 'M_Bnm_Balance_SUM' 
        },
        'trade_nf' :{
            'filename' : 'TRADE FY1112 product table (Non Funded)',
            'sheet'    : 'Trade_BB_monthly',
            'merge_on' : 'Account No',
            'check_on' : 'M Bnm Balance SUM' 
        }
    }
    
    preparation = {
        'gil' :{
            'filename' : 'GIL by BC Dec20',
            'sheet'    : 'GILDec20',
            'merge_on' : 'GCIF #',
            'check_on' : 'Stage 3 Reason',
            'skiprow' : '3'
         },
        'lb_f' :{
            'filename' : 'LB Dec20',
            'sheet'    : 'Funded',
            'skiprow'  : '2',
            'merge_on' : '',
            'check_on' : 'M_Cus_No'
        }
        # 'lb_uf' :{
        #     'filename' : 'LB Dec20',
        #     'sheet'    : 'Unfunded',
        #     'skiprow' : '0',
        #     'merge_on' : '',
        #     'check_on' : 'M_Cus_No'
        # },
        # 'nob' :{
        #     'filename' : 'NOB Code Value Chain (Jan 2017)',
        #     'sheet'    : 'Latest aftr Renew. Energy Align',
        #     'skiprow' : '2',
        #     'merge_on' : '',
        #     'check_on' : ''
        # }
    }

    taggings = {
        "NPL Flag Y"            : "NPL",
        "Impairment Status Y"   : "IPL",
        "Rescheduled"           : "IPL R&R",
        "Restructured"          : "IPL R&R",
        "Bankruptcy Flag "      :  "PL"
    }
