import pandas as pd
import check
from datetime import datetime
from CwnGraph import CwnBase, CwnAnnotator, CwnSense
from CwnGraph import CwnRelationType
cwn = CwnBase()

import logging

logger = logging.getLogger("AnnotationCheck")

######### Import annotation spreadsheet ########
dfs = dict()
sheet_id = ['1660345856', '1399166433', '823487049']
sheet_name = ['lex_rel', 'sense', 'lemma']
for sheet, gid in zip(sheet_name, sheet_id):
    url = f"https://docs.google.com/spreadsheets/d/1vzDlokmrsXMdGBaoSFR9lC1F9BlN8qHR6b5YDMMvv7Y/export?format=csv&gid={gid}"
    df = pd.read_csv(url, dtype='str').dropna()
    dfs[sheet] = df


########## Initialize checking ##################
now = datetime.today()
with open(f"log_check_conflict_{str(now)[:10]}.txt", 'w', encoding='utf-8') as f:
    f.write(f"Annotation Conflict Check\t Time: {str(now)[:19]}\n")
    f.write("======================================================\n\n")

    #####################  Check: Duplicated rows  #########################
    f.write("## Duplicated rows\n\n")
    for key, cols in zip(['lex_rel', 'sense', 'lemma'], [ ['sid_src', 'sid_tgt'], 'sid', 'lid' ]):
        dup_df = check.find_duplicates(dfs[key], cols)
        if dup_df.shape[0] > 0:
            # Write duplicated df to log
            f.write(f"  Sheet: `{key}`\n")
            for row in dup_df.to_string().split('\n'):
                f.write(f"    {row}\n")
            f.write("\n\n")
    
    ############# Check: synonym must have same sense defs ##################
    f.write("## Synonyms have different definitions\n\n")
    syn_diff_df = check.check_synonym_def(dfs['lex_rel'], dfs['sense'], cwn)
    if syn_diff_df.shape[0] > 0:
        # write to problematic rows in lex_rel to log
        f.write(f"  Sheet: `lex_rel`\n")
        for row in syn_diff_df.to_string().split('\n'):
            f.write(f"    {row}\n")
        f.write("\n\n")
