from .cwn_graph_utils import CwnGraphUtils
from .cwn_types import *

class CwnChecker:
    def __init__(self, V, E):
        self.cgu = CwnGraphUtils(V, E)
    
    def check_synset_definitions(self):
        pass

    def check_inverse_relations(self, rel: CwnRelationType, rel_inv: CwnRelationType):
        pass

    def check_synset_consistency(self):
        pass

