from typing import Tuple, Dict
import pandas as pd

NodeId = str
EdgeId = Tuple[NodeId, NodeId]
V = Dict[NodeId, any]
E = Dict[EdgeId, any]
CwnGraphData = Tuple[V, E]
AnnotationData: Dict[str, pd.DataFrame]
CheckResult = bool
MergeResult = Tuple[CwnGraphData, CheckResult]