from .cwn_annotator import CwnAnnotator
from .cwn_types import *
from typing import List, Dict, Tuple, Union
from .cwn_graph_utils import CwnGraphUtils

class CwnSuggestionAnnotator(CwnAnnotator):
    def __init__(self, cgu: CwnGraphUtils, suggestions: List[SuggestionData]):
        super(CwnSuggestionAnnotator, self).__init__(cgu, "auto_sug")
        self.suggestions = suggestions

    def annotate(self):
        # MISSING_SYNSET = auto()
        # NO_SYNSET = auto()
        # SYN_NO_SENSE = auto()
        # SYN_WRONG_DEF = auto()
        # SYN_MISSING_REL = auto()
        # SYN_REL_DIFF = auto()
        # INVERSE_ERROR = auto()
        # INVERSE_NOT_EXISTS = auto()
        pass