import logging
import pandas as pd

logger = logging.getLogger("AnnotationCheck")

def import_from_google_sheets(sheet_url_templ: str):
    logger.info("importing data from " + sheet_url_templ)
    annot_dfs = {}
    sheet_id = ['1660345856', '1399166433', '823487049']
    sheet_name = ['lex_rel', 'sense', 'lemma']
    for sheet, gid in zip(sheet_name, sheet_id):
        url = sheet_url_templ.format(gid=gid)
        df = pd.read_csv(url, dtype='str').dropna()
        annot_dfs[sheet] = df
    
    ok_flag = False
    return annot_dfs, ok_flag