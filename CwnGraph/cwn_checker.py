from functools import reduce
from .cwn_graph_utils import CwnGraphUtils
from .cwn_types import *

class CwnChecker:
    def __init__(self, V, E):
        self.cgu = CwnGraphUtils(V, E)
        self.suggestions = []

    def check_synset_definitions(self):
        def collect_def(old, new):
            new_id = new[0]
            new_data = new[1]
            old.setdefault(new_data["def"], []).append(new_id)
            return old
        sense_iter = filter(lambda x: x[1]["node_type"]=="sense", self.cgu.V.items())
        synonym_maps = reduce(collect_def, sense_iter, {})

        for sense_def, sense_ids in synonym_maps.items():
            #TODO: to be implemenetedP
            pass
            
        return sense_iter

    def check_inverse_relations(self, rel: CwnRelationType, rel_inv: CwnRelationType):
        pass

    def check_synset_consistency(self):
        pass

