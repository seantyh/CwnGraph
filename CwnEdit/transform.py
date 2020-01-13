import logging
from typing import Dict
from CwnGraph import CwnAnnotator, CwnRelationType
from CwnGraph import CwnLemma, CwnSense, CwnRelation
from CwnGraph import CwnIdNotFoundError
import pandas as pd

logger = logging.getLogger("AnnnotationCheck.Transform")
def transform_dataframe(annot: CwnAnnotator, annot_dfs: Dict[str, pd.DataFrame]):
    ret_flag = True
    ret_flag &= import_lemmas(annot, annot_dfs.get("lemma", pd.DataFrame()))
    ret_flag &= import_senses(annot, annot_dfs.get("sense", pd.DataFrame()))
    ret_flag &= import_relations(annot, annot_dfs.get("lex_rel", pd.DataFrame()))
    return ret_flag

def import_lemmas(annot: CwnAnnotator, lemma_df: pd.DataFrame):
    ret_flag = True
    for idx, lemma_data in lemma_df.iterrows():
        lemma = lemma_data.lemma
        if not lemma or pd.isna(lemma):
            logger.warning(f"Empty lemma in {lemma_data.lid}")
            ret_flag = False
            continue

        if lemma_data.action == "add":
            lemma_x = annot.create_lemma(lemma, lemma_data.lid)
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
        if not sense_data.sense_def or \
            not sense_data.lid:
            logger.warning(f"Incomplete sense data in {sense_data.sid}")
            ret_flag = False

        if sense_data.action == "add":            
            sense_x = annot.create_sense(sense_data.sense_def, sense_data.sid)            
            
            if not pd.isna(sense_data.examples):
                sense_x.examples = sense_data.examples.split("\n")
            sense_x.pos = sense_data.pos_tag
            sense_x.author = sense_data["annot."]
            annot.set_sense(sense_x)

            try:                
                annot.create_relation(
                    sense_data.lid, sense_data.sid,
                    CwnRelationType.has_sense)
            except CwnIdNotFoundError as ex:
                logger.error(ex)
                ret_flag = False

        elif sense_data.action == "delete":
            sense_x = CwnSense(sense_data.sid, annot.cgu)
            annot.remove_sense(sense_data.sid)
    
    return ret_flag

def import_relations(annot: CwnAnnotator, rel_df:pd.DataFrame):
    ret_flag = True
    for idx, rel_data in rel_df.iterrows():
        sid_src = rel_data.sid_src
        sid_tgt = rel_data.sid_tgt
        rel_type = CwnRelationType[rel_data.relation_type]
        if not rel_data.sid_src or \
            not rel_data.sid_tgt or \
            not rel_data.relation_type:
            logger.warning(f"Incomplete relation data in {rel_data.sid}")
            ret_flag = False

        if rel_data.action == "add":
            try:
                rel_x = annot.create_relation(sid_src, sid_tgt, rel_type)
                rel_x.author = rel_data["annot."]
            except CwnIdNotFoundError as ex:
                logger.error(ex)
                ret_flag = False
            
            annot.set_relation(rel_x)

        elif rel_data.action == "delete":
            rel_x = CwnRelation(sid_src, sid_tgt, rel_type)
            annot.remove_relation(rel_x)
    return ret_flag