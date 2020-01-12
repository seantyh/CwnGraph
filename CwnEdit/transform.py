import logging
from typing import Dict
from CwnGraph import CwnAnnotator, CwnRelationType
from CwnGraph import CwnLemma, CwnSense, CwnRelation
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
        
        if lemma_data.action == "add":
            lemma_x = annot.create_lemma(lemma)        
            lemma_x.sno = lemma_data.lemma_sno
            lemma_x.zhuyin = lemma_data.zhuyin
            lemma_x.author = lemma_data["annot."]        
            annot.set_lemma(lemma_x)
            logger.info(lemma_x)    
        elif lemma_data.action == "remove":
            lemma_x = CwnLemma(lemma_data.lid, annot.cgu)
            annot.remove_lemma(lemma_x)
            
    return ret_flag

def import_senses(annot: CwnAnnotator, sense_df: pd.DataFrame):
    ret_flag = True
    for idx, sense_data in sense_df.iterrows():
        if not sense_data.definition or \
            not sense_data.lid:
            logger.warning(f"Incomplete sense data in {sense_data.sid}")
        if sense_data.action == "add":
            sense_x = annot.create_sense(sense_data.defintion)
            sense_def = sense_data.definition
            lid = annot.get_id(sense_data.lid)
            sid = annot.get_id(sense_data.sid)
            annot.create_relation(lid, sid, CwnRelationType.has_sense)

            sense_x.examples = sense_data.examples.split("\n")
            sense_x.pos = sense_data
            sense_x.author = sense_data["annot."]
            annot.set_sense(sense_x)

        elif sense_data.action == "delete":
            sense_x = CwnSense(sense_data.sid, annot.cgu)
            annot.remove_sense(sid)

def import_relations(annot: CwnAnnotator, rel_df:pd.DataFrame):
    ret_flag = True
    for idx, rel_data in rel_df.iterrows():
        sid_src = rel_data.sid_src
        sid_tgt = rel_data.sid_tgt
        rel_type = rel_data.relation_type
        if not rel_data.sid_src or \
            not rel_data.sid_tgt or \
            not rel_data.relation_type:
            logger.warning(f"Incomplete relation data in {rel_data.sid}")
        
        annot.get_
        if rel_data.action == "add":
            rel_x = annot.create_relation(sid_src, sid_tgt, rel_type)
            rel_x.author = rel_data["annot."]
            annot.set_relation(rel_x)

        elif rel_data.action == "delete":
            rel_x = CwnRelation(sid_src, sid_tgt, rel_type)
            annot.remove_sense(rel_x)