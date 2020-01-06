from typing import Dict
from CwnGraph import CwnAnnotator
import pandas as pd

def transform_dataframe(annot: CwnAnnotator, annot_dfs: Dict[str, pd.DataFrame]):
    import_lemmas(annot, annot_dfs.get("lemma", pd.DataFrame()))
    import_senses(annot, annot_dfs.get("sense", pd.DataFrame()))
    import_relations(annot, annot_dfs.get("lex_rel", pd.DataFrame()))

def import_lemmas(annot: CwnAnnotator, lemma_df: pd.DataFrame):
    for idx, lemma_x in lemma_df.iterrows():
        breakpoint()

def import_senses(annot: CwnAnnotator, sense_df: pd.DataFrame):
    pass

def import_relations(annot: CwnAnnotator, rel_df:pd.DataFrame):
    pass