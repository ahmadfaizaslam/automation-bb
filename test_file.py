import pandas as pd
from pandas.core.reshape.concat import concat
from my_classes import *
from my_files import *

master_BC_GCIF = []
master_BC_Acc = []
bullet = 1
master = file.master
code_ref = file.code_ref


print("\n Master file loaded. \n")

if __name__ == "__main__":

    # for validating MIS with the bb.txt file
    for classname, elements in file.validation.items():
        x = classname
        files, frame = file.validation[classname], classname
        classname = my_validation(
            files["filename"], files["sheet"], files["merge_on"], files["check_on"]
        )
        print(f"{bullet} . {files['filename']},{files['sheet']} is loaded")
        try:
            dfs = my_validation.series(classname)
            dfs = dfs[["Account_No", "BC_NAME", "REGION"]]
            if x == "strc_bc" or x == "trade_f" or x == "trade_nf":
                master_BC_GCIF.append(dfs)
            else:
                master_BC_Acc.append(dfs)

            merged = my_validation.comparison(
                classname, master, "Account_Num", "Account_No"
            )
            my_validation.odtl_check(merged, "Balance", "M_Bnm_Balance")

        except Exception as e:
            print(
                f"        File {files['filename']} is not compatible \n        !! {e} is not found"
            )
            pass
        bullet = bullet + 1

    master_BC_GCIF = pd.concat(master_BC_GCIF, sort=False).drop_duplicates(
        subset="Account_No"
    )
    master_BC_GCIF[["BC_NAME"]] = (
        master_BC_GCIF[["BC_NAME"]]
        .replace({"JOHOR BARU BC": "JOHOR BAHRU BC"})
        .replace({"SUBANG": "SUBANG BC"})
    )

    master_BC_Acc = pd.concat(master_BC_Acc, sort=False)
    master_BC_Acc[["BC_NAME"]] = (
        master_BC_Acc[["BC_NAME"]]
        .replace({"JOHOR BARU BC": "JOHOR BAHRU BC"})
        .replace({"SUBANG": "SUBANG BC"})
    )

    print(
        "================================================================================================"
    )

    for x, j in file.preparation.items():
        classname = x
        files = file.preparation[classname]
        classname = my_transformation(
            files["filename"],
            files["sheet"],
            files["merge_on"],
            files["check_on"],
            files["skiprow"],
        )
        print(f"{bullet} . {files['filename']}, {files['sheet']} is loaded")
        print(f"        Dimension : {classname.shape}")
        bullet = bullet + 1

        if x == "gil":
            gil = my_transformation.create_column(classname, "PL+GIL", "PL")
            gil = my_transformation.tag(
                gil, "Stage 3 Reason", "PL IPL IPL R&R NPL", file.taggings
            )
            gil = my_transformation.get_gil(
                gil, "GCIF #", "PL IPL IPL R&R NPL", "PL+GIL"
            )
        elif x == "lb_f" or x == "lb_uf":
            if x == "lb_f":
                lb_f = my_transformation.calculation(
                    classname, "Broad Code", "M_Cus_No", "NOB"
                )
            else:
                lb_uf = my_transformation.calculation(
                    classname, "Broad Code", "M_Cus_No", "Nature_of_Business"
                )  # renames Nature of business to NOB
                lb_uf["NOB"] = lb_uf["NOB"].astype(str)
        elif x == "nob":
            nob = my_transformation.get_nob(
                classname, "NOB Code", "Sub Sector Desc", "NOB Desc"
            )

    """merge gil with master(bb.txt)"""
    masterbb = (
        my_transformation.do_merge(master, gil, "GCIF", "GCIF #")
        .drop(columns=["GCIF #"])
        .drop_duplicates()
    )  # ok
    masterbb["PL IPL IPL R&R NPL"] = masterbb["PL IPL IPL R&R NPL"].replace(
        np.nan, "PL"
    )  # ok
    masterbb["PL+GIL"] = masterbb["PL+GIL"].replace(np.nan, "PL")  # ok

    """merge lb funded with nob"""
    lb_fm = my_transformation.do_merge(lb_f, nob, "NOB", "NOB Code").dropna(how="all")
    lb_fm = lb_fm[["Broad Code", "M_Cus_No", "NOB", "NOB Desc", "Sub Sector Desc"]]
    lb_fm2 = my_transformation.do_merge(lb_fm, nob, "Broad Code", "NOB Code")  # ok
    lb_fm2 = lb_fm2[
        [
            "M_Cus_No",
            "NOB",
            "Broad Code",
            "NOB Desc_x",
            "Sub Sector Desc_x",
            "NOB Desc_y",
        ]
    ].rename(
        columns={
            "NOB Desc_x": "NOB Desc",
            "Sub Sector Desc_x": "Subsector",
            "NOB Desc_y": "Broad Sector",
        }
    )
    """merge lb notfunded with nob"""
    lb_ufm = my_transformation.do_merge(lb_uf, nob, "NOB", "NOB Code").dropna(
        how="all"
    )  # ok
    lb_ufm = lb_ufm[["Broad Code", "M_Cus_No", "NOB", "NOB Desc", "Sub Sector Desc"]]
    lb_ufm2 = my_transformation.do_merge(lb_ufm, nob, "Broad Code", "NOB Code")  # ok
    lb_ufm2 = lb_ufm2[
        [
            "M_Cus_No",
            "NOB",
            "Broad Code",
            "NOB Desc_x",
            "Sub Sector Desc_x",
            "NOB Desc_y",
        ]
    ].rename(
        columns={
            "NOB Desc_x": "NOB Desc",
            "Sub Sector Desc_x": "Subsector",
            "NOB Desc_y": "Broad Sector",
        }
    )

    lb_fnf = pd.concat([lb_fm2, lb_ufm2], sort=True).drop_duplicates(
        subset="M_Cus_No"
    )  # ok

    masterbb1 = my_transformation.do_merge(masterbb, lb_fnf, "GCIF", "M_Cus_No")

    masterbb2 = my_transformation.do_merge(
        masterbb1, master_BC_GCIF, "GCIF", "Account_No"
    )
    masterbb2 = my_transformation.do_merge(
        masterbb2, master_BC_Acc, "Account_Num", "Account_No"
    )

    # problem bc name and region
    masterbb2 = my_transformation.copy_value(masterbb2, "BC_NAME_x", "BC_NAME_y")
    masterbb2 = (
        my_transformation.copy_value(masterbb2, "REGION_x", "REGION_y")
        .drop(
            columns=[
                "M_Cus_No",
                "Account_No_x",
                "Account_No_y",
                "BC_NAME_x",
                "REGION_x",
            ]
        )
        .rename(
            columns={
                "BC_NAME_y": "BC_NAME",
                "REGION_y": "Region",
                "NOB_y": "NOB Code",
                "NOB_x": "NOB Sector",
            }
        )
    )

    masterbb3 = my_transformation.do_merge(masterbb2, code_ref, "BRR", "BRR")
    for new in [("Risk Cat CRD"), ("Risk Cat GCMC")]:
        masterbb3 = my_transformation.colummn_create(
            masterbb3, new, masterbb3["Risk CAT"]
        )
    masterbb3 = my_transformation.conditional_copy(
        masterbb3, "PL+GIL", "Risk Cat CRD", "GIL", "GIL"
    )

    for x in [("REPORT_DATE"), ("RISK_RATG_DT")]:
        masterbb3[x] = pd.to_datetime(masterbb3[x])

    # masterbb3 = my_transformation.ageing(masterbb3,'REPORT_DATE','RISK_RATG_DT','Ageing')
    masterbb3["days"] = (masterbb3["REPORT_DATE"] - masterbb3["RISK_RATG_DT"]).dt.days
    masterbb3["Ageing"] = masterbb3["days"]
    masterbb3.loc[masterbb3["days"] > 335, "Ageing"] = "Stale"
    masterbb3.loc[masterbb3["days"] <= 335, "Ageing"] = "Current"
    masterbb3["Ageing"].fillna("Stale", inplace=True)

    masterbb3 = my_transformation.tag(
        masterbb3, "Facility_Level_2", "Funded Non Funded", file.funded_nfunded
    ).drop(columns=["days"])
    masterbb3 = my_transformation.tag(masterbb3, "NPL_Indicator", "PL NPL", file.pl_npl)
    masterbb3["PL NPL"] = masterbb3["PL NPL"].replace("", "PL")
    masterbb3["FRR"] = masterbb3["FAC_RISK_RATG"]
    masterbb3["FRR"] = masterbb3["FRR"].fillna("Unrated")
    masterbb3["RM Mil"] = masterbb3["Balance"] / 1000000
    idx = masterbb3.groupby(["GCIF"])["Balance"].transform(max) == masterbb3["Balance"]
    masterbb3 = my_transformation.sconditional_copy(masterbb3, idx, "BC Max", "x")
    masterbb3["BC Max"] = masterbb3["BC Max"].replace(np.nan, "y").astype(object)

    masterbb3 = my_transformation.conditional_copy(
        masterbb3, "BC Max", "BC_Borr", "x", masterbb3["BC_NAME"]
    )
    masterbbprep = masterbb3.drop_duplicates(subset="GCIF")
    masterbbprep = my_transformation.conditional_copy(
        masterbbprep, "BC Max", "BC_Borr", "y", masterbbprep["BC_NAME"]
    )
    masterbbprep = masterbbprep.drop(columns=["BC_NAME", "BC Max"])
    masterbbprep = masterbbprep[["GCIF", "BC_Borr"]]

    masterbb4 = masterbb3.groupby(["GCIF"], as_index=False)["Balance"].sum()
    masterbb5 = masterbb3[
        [
            "GCIF",
            "REPORT_DATE",
            "Customer_Class",
            "Cust_Type",
            "Org_Name",
            "MBB_Sub_Market_Segment_Desc",
            "MISC_Cd",
            "MISC_Desc",
            "NOB Sector",
            "BRR",
            "SPRTER_ADJ_RATG",
            "RISK_RATG_DT",
            "PL+GIL",
            "Broad Code",
            "Broad Sector",
            "NOB Code",
            "NOB Desc",
            "Subsector",
            "BC_NAME",
            "Region",
            "Risk CAT",
            "Risk Cat CRD",
            "Funded Non Funded",
            "FRR",
        ]
    ]
    masterbb5 = masterbb5.drop_duplicates(subset="GCIF")
    masterbb_borr = masterbb4.merge(
        masterbb5, how="left", left_on="GCIF", right_on="GCIF"
    )
    masterbb_borr.loc[
        masterbb_borr["Funded Non Funded"] == "Funded", "Funded Balance"
    ] = masterbb_borr["Balance"]
    masterbb_borr.loc[
        masterbb_borr["Funded Non Funded"] == "Non Funded", "Non Funded Balance"
    ] = masterbb_borr["Balance"]

    masterbb_borr1 = masterbb_borr.merge(
        masterbbprep, how="left", left_on="GCIF", right_on="GCIF"
    )
    # masterbb_borr1.to_excel(
    #     path + r"\\MasterbbBORR_final.xlsx", engine="openpyxl", index=False
    # )
    print(masterbb_borr1.info())