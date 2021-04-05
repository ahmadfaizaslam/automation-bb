from my_files import *
from my_classes import *
import datetime as dt

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
            if x == "strc_bc":
                try:
                    my_validation.strc_check(dfs)
                    master_BC_GCIF.append(dfs)
                else:
                    print("Unab")
            elif x == "trade_f":
                master_BC_GCIF.append(dfs)
            elif x == "trade_nf":
                master_BC_GCIF.append(dfs)
            elif x == "od":
                
            else:
                master_BC_Acc.append(dfs)

            merged = my_validation.comparison(
                classname, master, "Account_Num", "Account_No"
            )
            print(merged.shape)
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

    print(master_BC_Acc.info())
    print(master_BC_GCIF.info())