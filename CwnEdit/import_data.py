import logging
import pandas as pd
from CwnEdit import check

logger = logging.getLogger("AnnotationCheck")
pd.set_option('display.max_colwidth', 18)

def import_from_google_sheets(sheet_url_templ: str, cwn):
    ok_flag = True

    logger.info("importing data from " + sheet_url_templ)
    annot_dfs = {}
    sheet_id = ['1660345856', '1399166433', '823487049']
    sheet_name = ['lex_rel', 'sense', 'lemma']
    for sheet, gid in zip(sheet_name, sheet_id):
        url = sheet_url_templ.format(gid=gid)
        try:
            df = pd.read_csv(url, dtype='str').dropna(how='all')
        except:
            logger.critical(f"Failed to retrieve data from google sheet.\nURL: {url}")
            ok_flag = False
            annot_dfs = {'lex_rel': None, 'sense': None, 'lemma': None}
            return annot_dfs, ok_flag
        logger.info(f"retrieved {df.shape[0]} rows from {sheet}")
        annot_dfs[sheet] = df
    
    #------------------- Check: duplicated rows -----------------#
    for key, cols in zip(['lex_rel', 'sense', 'lemma'], [ ['sid_src', 'sid_tgt'], 'sid', 'lid' ]):
        dup_df = check.find_duplicates(annot_dfs[key], cols)
        if dup_df.shape[0] > 0:
            logging.warning(f"Duplicated rows\nSheet: `{key}`\n{dup_df.iloc[:,0:5].to_string()}")
            ok_flag = False
    
    #------------ Check: synonyms must have the same sense definition ------------#
    syn_diff_df = check.check_synonym_def(annot_dfs['lex_rel'], annot_dfs['sense'], cwn)
    if syn_diff_df.shape[0] > 0:
        logging.warning(f"Different definitions for synonyms\nSheet: `lex_rel`\n{syn_diff_df.to_string()}")
        ok_flag = False
    
    #----------------- Check: valid relation typos -----------------#
    invalid_rel_df = check.check_rel_type(annot_dfs['lex_rel'])
    if invalid_rel_df:
        logging.warning(f"Invalid relation types (typo?) \nSheet: `lex_rel`\n{invalid_rel_df.to_string()}")
        ok_flag = False
    
    return annot_dfs, ok_flag
