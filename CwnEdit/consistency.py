import logging
import pandas as pd
from CwnGraph import CwnBase

logger = logging.getLogger("ConsistencyCheck")

def check_consistency(cwn: CwnBase, annot_df: pd.DataFrame):
    logger.info("In consistency check")
    V = {}
    E = {}
    cwn_data = (V, E)
    
    #  2c. synset, 同義詞的連結一致 (AnnotationData -> CwnGraphData)
    #      hyper/hypo, hyper/tropo, holo/mero
    
    # 2c.1 Synset identification
    # 2c.1.1 All synsets have the same definition
    # 2c.1.2 All senses having the same definitions are synsets
    
    # 2c.2 Synset check
    # 2c.2.1 All synsets have the same semantic relations
    # 2c.2.2 All senses in a synset have same semantic relations with other senses

    # 2c.3 inverse relations
    # 2c.3.1 All hypernymy noun sense pairs are also hyponymy pairs in reversed direction.
    # 2c.3.2 All hypernyny verb sense pairs are also troponymy pairs in reversed direction.
    # 2c.3.4 All holonymy sense pairs are meronymy pairs in reverse direction.
    

    
    check_flag = False
    return cwn_data, check_flag