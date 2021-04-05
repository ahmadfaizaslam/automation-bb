from my_files import *
from my_classes import *
import datetime as dt

my_path = file.my_path
bullet = 1

master_BC_GCIF = []
master_BC_Acc = []
bullet = 1
master = file.master
code_ref = file.code_ref


if __name__ == "__main__":

    for classname, elements in file.validation.items():
        x = classname
        files, frame = file.validation[classname], classname
        classname = my_validation(
            files["filename"], files["sheet"], files["merge_on"], files["check_on"]
        )
        print(f"{bullet} . {files['filename']},{files['sheet']} is loaded")
        try:
            classframe = my_validation.series(classname)
            dfs = classframe[["Account_No", "BC_NAME", "REGION"]]
            if x == "strc_bc" or x == "trade_f" or x == "trade_nf":
                master_BC_GCIF.append(dfs)
            else:
                master_BC_Acc.append(dfs)
            merged = my_validation.comparison(
                classname, master, "Account_Num", "Account_No", x
            )
            my_validation.odtl_check(merged, "Balance", "M_Bnm_Balance", x)

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
            gil = my_transformation.create_column(classname, "PL+GIL", "GIL")
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
                classname, "NOB Code", "NOB Desc", "Sub Sector Desc"
            )
            broad_sectors = (
                my_transformation.get_broad_sector(nob, "NOB Code")
                .rename(columns={"NOB Desc": "Broad Sector"})
                .drop(columns={"Sub Sector Desc"})
            )
            nob_desc = my_transformation.get_nob_sec(nob, "NOB Code")

    masterbb = (
        my_transformation.do_merge(master, gil, "GCIF", "GCIF #")
        .drop(columns=["GCIF #"])
        .drop_duplicates()
    )
    masterbb["PL IPL IPL R&R NPL"] = masterbb["PL IPL IPL R&R NPL"].replace(
        np.nan, "PL"
    )  # ok
    masterbb["PL+GIL"] = masterbb["PL+GIL"].replace(np.nan, "PL")

    lb_fm = (
        my_transformation.do_merge(lb_f, nob_desc, "NOB", "NOB Code")
        .dropna(how="all")
        .drop(columns=["NOB Code"])
    )
    lb_fm = my_transformation.do_merge(
        lb_fm, broad_sectors, "Broad Code", "NOB Code"
    ).drop(columns=["NOB Code"])

    lb_ufm = (
        my_transformation.do_merge(lb_uf, nob_desc, "NOB", "NOB Code")
        .dropna(how="all")
        .drop(columns=["NOB Code"])
    )
    lb_ufm = my_transformation.do_merge(
        lb_ufm, broad_sectors, "Broad Code", "NOB Code"
    ).drop(columns=["NOB Code"])

    lb_fnf = pd.concat([lb_fm, lb_ufm], sort=True).drop_duplicates(subset="M_Cus_No")

    masterbb1 = my_transformation.do_merge(masterbb, lb_fnf, "GCIF", "M_Cus_No")

    masterbb2 = my_transformation.do_merge(
        masterbb1, master_BC_GCIF, "GCIF", "Account_No"
    )
    masterbb2 = my_transformation.do_merge(
        masterbb2, master_BC_Acc, "Account_Num", "Account_No"
    )
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
    masterbb3 = my_transformation.conditional_copy(
        masterbb3, "PL+GIL", "Risk Cat CRD", "GIL", "GIL"
    )

    for new in [("Risk Cat CRD"), ("Risk Cat GCMC")]:
        masterbb3 = my_transformation.colummn_create(
            masterbb3, new, masterbb3["Risk CAT"]
        )

    masterbb3 = my_transformation.conditional_copy(
        masterbb3, "PL IPL IPL R&R NPL", "Risk Cat GCMC", "IPL", "IPL"
    )
    masterbb3 = my_transformation.conditional_copy(
        masterbb3, "PL IPL IPL R&R NPL", "Risk Cat GCMC", "IPL R&R", "IPL R&R"
    )
    masterbb3 = my_transformation.conditional_copy(
        masterbb3, "PL IPL IPL R&R NPL", "Risk Cat GCMC", "NPL", "NPL"
    )

    masterbb3["days"] = (
        pd.to_datetime(masterbb3["REPORT_DATE"])
        - pd.to_datetime(masterbb3["RISK_RATG_DT"])
    ).dt.days
    masterbb3.loc[masterbb3["days"] > 335, "Ageing"] = "Stale"
    masterbb3.loc[masterbb3["days"] <= 335, "Ageing"] = "Current"
    masterbb3["Ageing"] = masterbb3["Ageing"].fillna("Stale")
    masterbb3 = masterbb3.drop(columns={"days"})

    masterbb3 = my_transformation.tag(
        masterbb3, "Facility_Level_2", "Funded Non Funded", file.funded_nfunded
    )
    masterbb3 = my_transformation.tag(
        masterbb3, "NPL_Indicator", "PL NPL", file.pl_npl
    ).replace("", "PL")
    masterbb3["FRR"] = masterbb3["FAC_RISK_RATG"].fillna("Unrated")
    masterbb3["RM Mil"] = masterbb3["Balance"] / 1000000
    masterbb3.to_excel(
        my_path + r"\masterbb_account_level.xlsx", engine="openpyxl", index=False
    )
    masterbb3["Balance"] = masterbb3["Balance"].astype(float)
    idx = (
        masterbb3.groupby(["GCIF"])["Balance"].transform(max).astype(float)
        == masterbb3["Balance"]
    )
    masterbb3 = my_transformation.conditional_copy2(masterbb3, idx, "BC Max", 1).fillna(
        0
    )
    masterbb3 = my_transformation.conditional_copy(
        masterbb3, "BC Max", "BC_Borr", 1, masterbb3["BC_NAME"]
    )
    masterbbprep = masterbb3.drop_duplicates(subset="GCIF")

    masterbbprep = my_transformation.conditional_copy(
        masterbbprep, "BC Max", "BC_Borr", 0, masterbbprep["BC_NAME"]
    )
    masterbbprep.drop(columns=["BC_NAME", "BC Max"])
    masterbbprep = masterbbprep[["GCIF", "BC_Borr"]]
    #     """

    #     """
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
            "Sub Sector Desc",
            "BC_NAME",
            "Region",
            "Risk CAT",
            "Risk Cat CRD",
            "Funded Non Funded",
            "FRR",
        ]
    ]

    masterbb5 = masterbb5.drop_duplicates(subset="GCIF")
    masterborr = my_transformation.do_merge(masterbb4, masterbb5, "GCIF", "GCIF")

    masterborr = my_transformation.conditional_copy(
        masterborr,
        "Funded Non Funded",
        "Funded Balance",
        "Funded",
        masterborr["Balance"],
    ).fillna(0)

    masterborr = my_transformation.conditional_copy(
        masterborr,
        "Funded Non Funded",
        "Non Funded Balance",
        "Non Funded",
        masterborr["Balance"],
    ).fillna(0)

    final_frame = my_transformation.do_merge(masterborr, masterbbprep, "GCIF", "GCIF")


final_frame.to_excel(
    my_path + r"\masterBB_borrower_level.xlsx", engine="openpyxl", index=False
)
