import logging
from functools import reduce
from itertools import groupby, combinations
from enum import Enum, auto
from typing import List, Tuple, Dict
from .cwn_graph_utils import CwnGraphUtils
from .cwn_types import *

logger = logging.getLogger("CwnGraph.CwnChecker")

class CwnCheckerSuggestion(Enum):
    MISSING_SYNSET = auto()
    NO_SYNSET = auto()
    SYN_NO_SENSE = auto()
    SYN_WRONG_DEF = auto()
    SYN_MISSING_REL = auto()
    SYN_REL_DIFF = auto()
    INVERSE_ERROR = auto()
    INVERSE_NOT_EXISTS = auto()
csg = CwnCheckerSuggestion

SuggestionData = Tuple[CwnCheckerSuggestion, any]

class CwnCheckerBase:
    def check(self):
        raise NotImplementedError("implement check() in the inherited class")

    def suggestions(self):
        raise NotImplementedError("implement suggestions in the inherited class")

class CwnChecker:
    def __init__(self, V, E):
        self.V, self.E = V, E
        self.checkers_cls = []

    def add_checker(self, checker: CwnCheckerBase):
        if issubclass(checker, CwnCheckerBase):
            self.checkers_cls.append(checker)
        
    def check(self) -> Dict[CwnCheckerSuggestion, SuggestionData]:
        suggestions = []
        for checker_cls in self.checkers_cls:
            checker_x = checker_cls(self.V, self.E)
            sugg = checker_x.check()
            suggestions.extend(sugg)
        ret_suggestions = self.group_suggestions(suggestions)
        return ret_suggestions
    
    def group_suggestions(self, suggestions):
        suggestions = sorted(suggestions, key=lambda x: x[0])
        sug_grp_iter = groupby(suggestions, key=lambda x: x[0])
        sugg_map = {grp_id: list(members) for grp_id, members in sug_grp_iter}
        
        return sugg_map


class CwnCheckerSynset(CwnChecker):
    """
    Check consistency among synset/sense relations (AnnotationData -> CwnGraphData)
    
    1. Synset identification
        1.1. All synsets have the same definition
        1.2. All senses having the same definitions are synsets

    2. Synset check
        2.1. All synsets have the same semantic relations with its member senses
        2.2. All senses in a synset have same semantic relations with other senses

    3. inverse relations
        3.1. All hypernymy noun sense pairs are also hyponymy pairs in reversed direction.
        3.2. All hypernyny verb sense pairs are also troponymy pairs in reversed direction.
        3.3. All holonymy sense pairs are meronymy pairs in reverse direction.  
    """
    def __init__(self, V, E):
        self.cgu = CwnGraphUtils(V, E)
        self._suggestions = []

    def check(self) -> SuggestionData:
        self.check_synset_definitions()
        self.check_synset_consistency()
        self.check_inverse_relations()

        return self.suggestions

    def suggestions(self):
        return self._suggestions

    def suggests(self, suggest_type: CwnCheckerSuggestion, supp_data: any):
        self._suggestions.append(
            (suggest_type, supp_data)
        )
    
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
                            self.suggests(csg.NO_SYNSET, mem_x.id)
                        self.suggests(
                            csg.MISSING_SYNSET,
                            (mem_x.id, dom_synset.id, CwnRelationType.is_synset))      

    def check_inverse_relations(self):
        for edge_id, edge_data in self.cgu.E.items():
            rel_type_str = edge_data.get("edge_type", None)
            if not rel_type_str:
                continue
            rel_type = CwnRelationType[rel_type_str]
            rev_rel_type = rel_type.inverse()

            if rev_rel_type:
                rev_id = (edge_id[1], edge_id[0])
                if rev_rel_type != rel_type.inverse():
                    self.suggests(csg.INVERSE_ERROR, 
                        (rev_id[0], rev_id[1], rev_rel_type.name))
                else:
                    self.suggests(csg.INVERSE_NOT_EXISTS, 
                        (rev_id[0], rev_id[1], rev_rel_type.name))
            else:
                pass


    def check_synset_consistency(self):
        synset_iter = filter(lambda x: x[1]["node_type"]=="synset", self.cgu.V.items())
        for synset_id, synset_data in synset_iter:
            synset_x = CwnSynset(synset_id, self.cgu)
            senses = synset_x.senses
            syn_relations = synset_x.semantic_relations
            if not senses:
                self.suggests(csg.SYN_NO_SENSE, synset_x.id)
            
            try:
                senses = sorted(senses, key=lambda x: x.definition)
            except Exception as ex:
                logger.Error(ex)

            grp_iter = groupby(senses, lambda x: x.definition)
            def_groups = [(grp_id, list(members)) for grp_id, members in grp_iter]
            def_groups = sorted(def_groups, key=lambda x: len(x[1]), reverse=True)

            for grp_def, members in def_groups:
                if grp_def != synset_x.definition:
                    for mem_x in members:                    
                        # the sense definition is different than the synset's
                        self.suggests(
                            csg.SYN_WRONG_DEF, (mem_x.id, synset_x.definition)
                        )
                else:
                    # sense definition is the same, then check the synset's relations
                    self.check_synset_relations(synset_x, members)
                    self.check_sense_relations_within_synset(synset_x, members)

    def check_synset_relations(self, synset: CwnSynset, synset_members: List[CwnSense]):
        """
        Check all senses in a synset share the same relations with parenting synset

        Parameters
        -----------

        synset: CwnSynset
            the synset node to be considered
        synset_members: List[CwnSense]
            the sense nodes belonged to the ``synset``
        """
        
        synset_relations = set(synset.semantic_relations)
        suggest_rel = set()
        for mem_x in synset_members:
            rel_x = set(mem_x.semantic_relations)
            if rel_x == synset_relations:
                continue
            diff_syn_rel = synset_relations.difference(rel_x)
            diff_rel_x = rel_x.difference(synset_relations)
            
            for rel_x in diff_syn_rel:
                self.suggests(csg.SYN_MISSING_REL, 
                    (synset.id, rel_x[1], rel_x[0]))

            for rel_x in diff_rel_x:
                self.suggests(csg.SYN_MISSING_REL,
                    (mem_x.id, rel_x[1], rel_x[0]))
            
    def check_sense_relations_within_synset(
            self, synset: CwnSynset, synset_members: List[CwnSense]):
        """
        Check senses in a synset have the same relations with other senses

        Parameters
        -----------

        synset: CwnSynset
            the synset node to be considered
        synset_members: List[CwnSense]
            the sense nodes belonged to the ``synset``
        """
        
        for sense_x, sense_y in combinations(synset_members, 2):
            rel_set_x = set(sense_x.relations)
            rel_set_y = set(sense_y.relations)

            # relations exist in sense_x but not in sense_y
            diff_x = rel_set_x.difference(rel_set_y)
            for rel_x in diff_x:
                self.suggests(csg.SYN_REL_DIFF, 
                    (sense_y.id, rel_x[1], rel_x[0]))
            
            diff_y = rel_set_y.difference(rel_set_x)
            for rel_y in diff_x:
                self.suggests(csg.SYN_REL_DIFF, 
                    (sense_x.id, rel_y[1], rel_y[0]))
            




