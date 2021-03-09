
    
print('1. Loading Files...\n')
master_file =  pd.read_csv(dir_path + r"\bb.txt",
                           delimiter = "\t",
                           header =0,
                           na_values='?',
                           engine='python',
                           parse_dates=['NPL_Date','RISK_RATG_DT'],
                           dtype={'Party_Id':object,'SPL_MENTION_ACCT_IND':object})
print('Master file loaded completed.')