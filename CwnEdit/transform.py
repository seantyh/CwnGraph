import logging
from typing import Dict
from CwnGraph import CwnAnnotator
import pandas as pd

logger = logging.getLogger("AnnnotationCheck.Transform")
logger.info("test log")
def transform_dataframe(annot: CwnAnnotator, annot_dfs: Dict[str, pd.DataFrame]):
    import_lemmas(annot, annot_dfs.get("lemma", pd.DataFrame()))
    import_senses(annot, annot_dfs.get("sense", pd.DataFrame()))
    import_relations(annot, annot_dfs.get("lex_rel", pd.DataFrame()))

def import_lemmas(annot: CwnAnnotator, lemma_df: pd.DataFrame):
    ret_flag = True
    for idx, lemma_data in lemma_df.iterrows():
        lemma = lemma_data.lemma        
        if not lemma or pd.isna(lemma):
            logger.warning(f"Empty lemma in {lemma_data.lid}")
            ret_flag = False
            continue
        lemma_x = annot.create_lemma(lemma)        
        lemma_x.sno = lemma_data.lemma_sno
        lemma_x.zhuyin = lemma_data.zhuyin
        lemma_x.author = lemma_data["annot."]        
        logger.info(lemma_x)        
    
    return ret_flag

def import_senses(annot: CwnAnnotator, sense_df: pd.DataFrame):
    pass

def import_relations(annot: CwnAnnotator, rel_df:pd.DataFrame):
    pass