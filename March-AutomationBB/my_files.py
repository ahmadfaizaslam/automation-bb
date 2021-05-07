import os
import pandas as pd
import numpy as np


class file:
    dir_path = r"C:\\Users\\faiza\\Desktop\\March-AutomationBB\\Master BB Mar'21"

    my_path = os.path.dirname(
        os.path.realpath(__file__)
    )  # where the code is located, where the log file will be generated

    master = pd.read_csv(
        dir_path + r"\\REDW\bb.txt",
        delimiter="\t",
        header=0,
        na_values="?",
        engine="python",
        dtype={
            "Account_Num": str,  # used to be str
            "Balance": float,
            "Party_Id": str,
            "RISK_ADJ_BRR": str,
        },
    ).rename(columns={"Party_Id": "GCIF", "RISK_ADJ_BRR": "BRR"})

    task_f = pd.read_excel(dir_path + r"\Code and reference\TF03.xlsx",
                           sheet_name="Sheet1", dtype={"GCIF": str})
    task_f1 = task_f[["GCIF", "Status"]]

    limit_borr = pd.read_excel(dir_path + r"\MIS\2021-03 Limit EXCO Mar 2021 A.xlsx",
                               sheet_name="FINAL (2)", dtype={"Cus_No": str})
    limit_borr1 = limit_borr[['Cus_No', 'OD', 'ODCRBAL', 'STRCTB']].rename(columns={
                                                                           "Cus_No": "GCIF"})
    limit_borr2 = limit_borr[['Cus_No', 'TL']].rename(
        columns={"Cus_No": "GCIF"})

    limit_tl = pd.read_excel(dir_path + r"\Daniel\2021-03 BB TL (for Yan May).xlsx",
                             sheet_name="Sheet1", dtype={"Cus No": str})
    limit_tl = limit_tl.groupby(["Cus No"])["M Approved Limit SUM"].sum()
    limit_tl = limit_tl.rename(
        {"Cus No": "GCIF", "M Approved Limit SUM": "TL"})

    limit_tl_final = pd.concat([limit_borr2, limit_tl], sort=False).drop_duplicates(
        subset="GCIF"
    )

    usd_tl = pd.read_excel(dir_path + r"\Daniel\2021-03 BB USD TL (for Yan May).xlsx", sheet_name="Sheet1", dtype={
                           "Cus No": str}).rename(columns={"Cus No": "GCIF", "M Approved Limit Myr SUM": "USD TL Limit"}).drop_duplicates(subset="GCIF")
    usd_tl = usd_tl.groupby(["GCIF"])["USD TL Limit"].sum()

    crrs = pd.read_excel(dir_path + r"\CRRS @Mar 2021.xlsx",
                         sheet_name="corporate", dtype={"GCIF_NUM": str})
    crrs = crrs[['GCIF_NUM', 'AA_NUM', 'SCORECARDS']].rename(
        columns={"GCIF_NUM": "GCIF"}).drop_duplicates(subset="GCIF")

    borr_group = pd.read_excel(dir_path + r"\List of BB Group (6,988) Limit @Dec20.xlsx",
                               sheet_name="Group List (6,988)", dtype={"Cus_No": str})
    borr_group = borr_group[['Cus_No', 'Group Name']].rename(
        columns={"Cus_No": "GCIF"}).drop_duplicates(subset="GCIF")

    oaad = pd.read_excel(dir_path + r"\OAAD_Mar 2021.xlsx",
                         sheet_name="OAADLST", dtype={"CIF_NUM": str})
    oaad = oaad[['CIF_NUM', 'FINAL_APPROVER_LEVEL']].rename(
        columns={"CIF_NUM": "GCIF"}).drop_duplicates(subset="GCIF")

    code_ref = pd.read_excel(
        dir_path + r"\\Code and reference\\MASTER - Codes.xls",
        sheet_name="Cust Class & BRR & Risk Cat",
        nrows=26,
        usecols=[3, 4],
        skiprows=1,
        dtype={
            "BRR": str,
            "Risk CAT": str,
        },
    ).drop_duplicates()

    """dictionaries should not have duplicate keys.... if needed, do a list in dictionaries"""
    validation = {
        "odtl1": {
            "filename": "ODTL FY 1112 SMF Product table",
            "sheet": "OD",
            "merge_on": "Account_No",
            "check_on": "M_Bnm_Balance_SUM1",
        },
        "odtl2": {
            "filename": "ODTL FY 1112 SMF Product table",
            "sheet": "TL",
            "merge_on": "M_Account_No",
            "check_on": "M_Bnm_Balance",
        },
        "od": {
            "filename": "OD Cr Bal 1011 product table",
            "sheet": "Recovered_Sheet1",
            "merge_on": "Account_No",
            "check_on": "M_Bnm_Balance_SUM1",
        },
        "strc_bc": {
            "filename": "STRC FY 1112 product table",
            "sheet": "STRC_BB_monthly_4",
            "merge_on": "M_Cus_No",
            "check_on": "M_Bnm_Balance_SUM",
        },
        "trade_nf": {
            "filename": "TRADE FY1112 product table (Non Funded)",
            "sheet": "Trade_BB_monthly",
            "merge_on": "Account No",
            "check_on": "M Bnm Balance SUM",
        },
        "trade_f": {
            "filename": "TRADE FY1112 product table Funded",
            "sheet": "Trade_BB_monthly",
            "merge_on": "M_Cus_No",
            "check_on": "M_Bnm_Balance_SUM",
        },
    }

    preparation = {
        "gil": {
            "filename": "GIL by BC Mar21",
            "sheet": "GILMar21",
            "merge_on": "GCIF #",
            "check_on": "Stage 3 Reason",
            "skiprow": 3,
        },
        "lb_f": {
            "filename": "LB Mar21",
            "sheet": "Funded",
            "skiprow": 2,
            "merge_on": "NOB",
            "check_on": "M_Cus_No",
        },
        "lb_uf": {
            "filename": "LB Mar21",
            "sheet": "Unfunded",
            "skiprow": "0",
            "merge_on": "",
            "check_on": "M_Cus_No",
        },
        "nob": {
            "filename": "NOB Code Value Chain (Jan 2017)",
            "sheet": "Latest aftr Renew. Energy Align",
            "skiprow": 2,
            "merge_on": "",
            "check_on": "",
        },
    }

    taggings = {
        "NPL Flag Y": "NPL",
        "Impairment Status Y": "IPL",
        "Rescheduled": "IPL R&R",
        "Restructured": "IPL R&R",
        "Cross default by HP": "IPL",
        "Cross default by credit card": "IPL",
        "Bankruptcy Flag Y": "PL",
    }

    funded_nfunded = {
        "Non-Funded Tradebills": "Non Funded",
        "FEC (10%)": "Non Funded",
        "Term Loan": "Funded",
        "STRC": "Funded",
        "Funded Tradebills": "Funded",
        "OD": "Funded",
    }

    pl_npl = {"Y": "NPL", "N": "PL"}
