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
        'GIL by BC Dec20'                  : 'GILDec20',
        'LB Dec20'                         : 'Funded',
        'LB Dec20'                         : 'Unfunded',
        'NOB Code Value Chain (Jan 2017)'  : 'Latest aftr Renew. Energy Align'
}


