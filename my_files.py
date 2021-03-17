import os
import pandas as pd

class file():
    #path = "Z:\BB RISK\BB DATA\\2020\8. Aug 2020\MIS"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    master =  pd.read_csv(dir_path + r"\bb.txt",
                           delimiter = "\t",
                           header =0,
                           na_values='?',
                           engine='python',)
    
    
    validation = {
        'ODTL FY 1112 SMF Product table'   :   'OD',
        'STRC FY 1112 product table 1'     :   'STRC_BB_monthly_4',
        'OD Cr Bal 1011 product table'     :   'Recovered_Sheet1'
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



