from functools import reduce
from itertools import groupby
from enum import Enum
from .cwn_graph_utils import CwnGraphUtils
from .cwn_types import *

class CwnCheckerSuggestion(Enum):
    MISSING_SYNSET = 1
csg = CwnCheckerSuggestion

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
            senses = map(lambda sid: CwnSense(sid, self.cgu), sense_ids)
            senses = sorted(senses, key=lambda x: x.synset.id if x.synset else "<None>")
            grp_iter = groupby(senses, lambda x: x.synset)
            syn_groups = [(grp_id, list(members)) for grp_id, members in grp_iter]
            no_synsets = [x for x in syn_groups if not x[0]]
            with_synsets = [x for x in syn_groups if x[0]]
            syn_groups = sorted(with_synsets, key=lambda x: len(x[1]), reverse=True) + no_synsets
            if len(syn_groups) > 1:
                dom_synset = syn_groups[0][0]
                for grp_id, members in syn_groups[1:]:
                    for mem_x in members:
                        if not dom_synset:                            
                            self.suggestions.append((csg.NO_SYNNSET, mem_x.id))
                        self.suggestions.append((
                            csg.MISSING_SYNSET,
                            (mem_x.id, dom_synset.id, CwnRelationType.is_synset)))        

    def check_inverse_relations(self, rel: CwnRelationType, rel_inv: CwnRelationType):
        pass

    def check_synset_consistency(self):
        synset_iter = filter(lambda x: x[1]["node_type"]=="synset", self.cgu.V.items())
        for synset_id, synset_data in synset_iter:
            synset_x = CwnSynset(synset_id, self.cgu)
            senses = synset_x.senses
            if not senses:
                self.suggestions.append(csg.SYN_NO_SENSE, synset_x.id)
            
            try:
                senses = sorted(senses, key=lambda x: x.definition)
            except:
                breakpoint()
            grp_iter = groupby(senses, lambda x: x.definition)
            def_groups = [(grp_id, list(members)) for grp_id, members in grp_iter]
            def_groups = sorted(def_groups, key=lambda x: len(x[1]), reverse=True)
            for grp_id, members in def_groups:
                for mem_x in members:
                    if grp_id != mem_x.definition:
                        self.suggestions.append((
                            csg.SYN_WRONT_DEF, (mem_x.id, grp_id)
                        ))
        



