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

    master_BC_GCIF.info()
    master_BC_Acc.info()
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
