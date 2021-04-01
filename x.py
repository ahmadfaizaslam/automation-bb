from my_files import *
from my_classes import *

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

print(lb_fm.head())
