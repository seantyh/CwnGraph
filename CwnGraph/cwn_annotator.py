import os
import json
from datetime import datetime
from . import cwnio
from . import annot_merger
from .cwn_types import *
from typing import List, Dict, Tuple, Union
from .cwn_graph_utils import CwnGraphUtils

class CwnAnnotator:
    def __init__(self, cgu:CwnGraphUtils, label):
        self.label = label
        self.V = cgu.V.copy()
        self.E = cgu.E.copy()
        self.tape: List[AnnotRecord] = []
        self.meta = {
            "label": label,
            "timestamp": datetime.now().strftime("%y%m%d%H%M%S"),
            "serial": 0
        }        
    
    def __repr__(self):
        n_edit = sum(1 for x in self.tape if x.annot_action == AnnotAction.Edit)
        n_delete = sum(1 for x in self.tape if x.annot_action == AnnotAction.Delete)
        return f"<CwnAnnotator: {self.label}> ({n_edit} Edits, {n_delete} Deletes)"

    def load(self, fpath):

        if os.path.exists(fpath):
            print("loading saved session from ", fpath)

            self.meta, self.V, self.E = \
                cwnio.load_annot_json(fpath)
            return True

        else:
            print("cannot find ", fpath)
            return False

    def save(self, fpath):
        label = self.meta["label"]        
        cwnio.ensure_dir("annot")        
        cwnio.dump_annot_json(self.meta, self.V, self.E, fpath)
        with open(fpath, "wb") as fout:
            pickle.dump((self.V, self.E, self.meta), fout)

    def new_node_id(self):
        serial = self.meta.get("serial", 0) + 1
        label = self.meta.get("label", "")
        self.meta["serial"] = serial
        return f"{label}_{serial:06d}"

    def get_id(self, raw_id: Union[str, Tuple[str]]):
        if isinstance(raw_id, str):
            ids = [raw_id]
        else:
            ids = raw_id
        
        annot_ids = []
        for id_x in ids:
            annot_id = self.map_to_annot_id(id_x)
            annot_ids.append(annot_ids)
        return annot_ids if len(annot_ids) > 1 else annot_ids[0]

    def map_to_annot_id(self, raw_id: str):
        iter_rec = filter(lambda x: x.raw_id == raw_id, self.tape)
        recs = list(iter_rec)
        if len(recs) == 0:
            return raw_id
        elif len(recs) == 1:
            return recs[0].annot_id
        else:
            raise ValueError(f"More than one annot_id found for {raw_id}")

    def create_lemma(self, lemma):
        node_id = self.new_node_id()
        new_lemma = CwnLemma(node_id, self)
        new_lemma.lemma = lemma
        self.set_lemma(new_lemma)
        return new_lemma

    def create_sense(self, definition):
        node_id = self.new_node_id()
        new_sense = CwnSense(node_id, self)
        new_sense.definition = definition
        self.set_sense(new_sense)
        return new_sense

    def create_relation(self, src_id, tgt_id, rel_type):
        if not self.get_node_data(src_id):
            raise ValueError(f"{src_id} not found")
        if not self.get_node_data(tgt_id):
            raise ValueError(f"{tgt_id} not found")
        edge_id = (src_id, tgt_id)
        new_rel = CwnRelation(edge_id, self)
        new_rel.relation_type = rel_type
        self.set_relation(new_rel)
        return new_rel

    def set_lemma(self, cwn_lemma):
        self.V[cwn_lemma.id] = cwn_lemma.data()

    def set_sense(self, cwn_sense):
        self.V[cwn_sense.id] = cwn_sense.data()

    def set_relation(self, cwn_relation):
        self.E[cwn_relation.id] = cwn_relation.data()

    def remove_lemma(self, cwn_lemma):
        if cwn_lemma.id in self.V:
            del self.V[cwn_lemma.id]
            return True
        else:
            return False

    def remove_sense(self, cwn_sense):
        if cwn_sense.id in self.V:
            del self.V[cwn_sense.id]
            return True
        else:
            return False

    def remove_relation(self, cwn_relation):
        if cwn_relation.id in self.E:
            del self.E[cwn_relation.id]
            return True
        else:
            return False

    def get_node_data(self, node_id):
        node_data = self.V.get(node_id, {})
        return node_data

    def get_edge_data(self, edge_id):
        edge_data = self.E.get(edge_id, {})

        return edge_data




