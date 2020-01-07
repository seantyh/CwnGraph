import re
from CwnGraph import CwnSense

# Lexical relations
#https://docs.google.com/spreadsheets/d/1vzDlokmrsXMdGBaoSFR9lC1F9BlN8qHR6b5YDMMvv7Y/export?format=csv&gid=1660345856

# New sense
#https://docs.google.com/spreadsheets/d/1vzDlokmrsXMdGBaoSFR9lC1F9BlN8qHR6b5YDMMvv7Y/export?format=csv&gid=1399166433

# New lemma
#https://docs.google.com/spreadsheets/d/1vzDlokmrsXMdGBaoSFR9lC1F9BlN8qHR6b5YDMMvv7Y/export?format=csv&gid=823487049

# Check duplicated rows
def find_duplicates(df, cols=['sid_src', 'sid_tgt']):
    dup_idx = df.duplicated(subset=cols, keep=False)
    return(df[dup_idx])

def is_cwn_sid(id):
    if re.match("[0-9]{8}", id):
        return True
    
    return False

# Check synonym has same def
def check_synonym_def(df_lex_rel, df_sense, cwn):
    # Get synonym rows
    df_lex_rel = df_lex_rel[(df_lex_rel['relation_type'] == "synonym") & (df_lex_rel['action'] == "add")]
    df_sense = df_sense[df_sense['action'] == "add"]
    
    invalid_row_idx = []
    for idx, row in df_lex_rel.iterrows():
        src, tgt = row['sid_src'], row['sid_tgt']
        # Get sense definitions
            # Case 1  tgt: CWN, src: CWN
            # Case 2  tgt: new, src: CWN
            # Case 3  tgt: CWN, src: new
            # Case 4  tgt: new, src: new
        src_def = CwnSense(src, cwn).definition if is_cwn_sid(src) else df_sense[df_sense['sid'] == src]['sense_def'].values[0]
        tgt_def = CwnSense(tgt, cwn).definition if is_cwn_sid(tgt) else df_sense[df_sense['sid'] == tgt]['sense_def'].values[0]
        # Case 1 (two old senses, new relations)
        # Deal with: Adding Synonym  & Modifying Sense Definition at the same time
        if is_cwn_sid(src) and is_cwn_sid(tgt) and (src in df_sense['sid'].values or tgt in df_sense['sid'].values):
            df_newSynonym = df_sense[(df_sense['sid'] == src) | (df_sense['sid'] == tgt)]
            if df_newSynonym.shape[0] == 2:  # num of rows
                src_def = df_newSynonym[df_newSynonym['sid'] == src]['sense_def'].values[0]
                tgt_def = df_newSynonym[df_newSynonym['sid'] == tgt]['sense_def'].values[0]
            elif df_newSynonym.shape[0] == 1:
                if df_newSynonym['sid'].values[0] == src:
                    src_def = df_newSynonym[df_newSynonym['sid'] == src]['sense_def'].values[0]
                elif df_newSynonym['sid'].values[0] == tgt:
                    tgt_def = df_newSynonym[df_newSynonym['sid'] == tgt]['sense_def'].values[0]
                else:
                    print(f'沒想過的 bug1: 同時 修改既有之sense definition & 並增加 Synonym {idx}, {row}')
            else:
                print(f'沒想過的 bug2: 同時 修改既有之sense definition & 並增加 Synonym {idx}, {row}')

        # Check src_def == tgt_def
        if src_def != tgt_def:
            invalid_row_idx.append(idx)

    return(df_lex_rel.loc[invalid_row_idx])

"""
def has_diffDef(senses):
    all_defs = [sense.definition for sense in senses]
    unique_defs = set(all_defs)
    return(len(unique_defs) > 1)
"""