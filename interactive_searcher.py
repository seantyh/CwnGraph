import re
import pprint

def searchByLemma(q, cwn, exact=True, printExamples=True, printSense=True, printLemma=True):
    """
    Search by lemma, can use regex in `q`.
    Prints out the hierarchy from lemma to senses to examples.
      `exact=True`: whether to perform exact (i.e., not regex) search. 
         Set `exact=False` to search with regex.
      `print*=True`: whether to print examples, sense, or lemma.
    """
    if exact: 
        q = f"^{q}$"
    
    lemmas = cwn.find_lemma(q)
    for i, lemma in enumerate(lemmas):
        print()
        if printLemma:
            print(f"{i+1}.", lemma.lemma, lemma.id,  end="\n")
        for j, sense in enumerate(lemma.senses):
            if printSense:
                print("\t" * printLemma, end="")
                print(f"{j+1:>3}) {sense.id:<10} pos: {sense.pos:<8} def: {sense.definition}")
                #print(f"{j+1:>3}) {lemma.ljust(4, '　')} id: {sense.id:<10} pos: {sense.pos:<8} def: {sense.definition}")
            for s, sent in enumerate(sense.examples):
                if printExamples:
                    print("\t" * sum([printSense, printLemma]), end="")
                    print(f"{s+1}) {sent}")
            print()


def compareLemma(l1, l2, cwn):
    """
    Compare all senses of two lemmas by showing their senses side-by-side.
    The lemma with more senses is printed on the left.
      `l1`: str. lemma 1
      `l2`: str. lemma 2
    """
    l1 = f"^{l1}$"
    l2 = f"^{l2}$"
    
    l1_lst = [str(li).replace('<CwnSense', '').replace('>', '').replace('(', '').replace(')', '') for li in cwn.find_senses(lemma=l1)]
    l2_lst = [str(li).replace('<CwnSense', '').replace('>', '').replace('(', '').replace(')', '') for li in cwn.find_senses(lemma=l2)]
    
    if len(l1_lst) < len(l2_lst):
        zip_lst = zip(l2_lst, l1_lst)
        long = l2_lst
        short = l1_lst
    else:
        zip_lst = zip(l1_lst, l2_lst)
        long = l1_lst
        short = l2_lst
    
    # Print paired list
    for i, (a, b) in enumerate(zip_lst):
        #print(f"{a:50}{b:>50}")
        print(f"{i+1:>3} {a.ljust(45, '　')}{b}")  # 使用全形空白
    # Print remaining list
    if len(long) > len(short):
        for item in long[len(list(zip_lst)):]:
            i += 1
            print(f"{i+1:>3} {item}")

              
def exploreSense(q, cwn, type="definition", printExamples=False):
    """
    Exploratory searching definition or examples.
    Can use regex in `q`.
    The matched string in the definition or examples will be wrapped in【】.
      `type`: where to perform the search. Must be "definition" or "examples".
    """
    if type == "definition":
        senses = cwn.find_senses(definition=q)
    else:
        senses = cwn.find_senses(examples=q)
    
    pat = re.compile(f"({q})")
    for j, sense in enumerate(senses):
        lemma = re.search("\((\w+)\)", str(sense)).group(1)
        # Label searched term in definition
        sense.definition = pat.sub("【\\1】", sense.definition) if type == "definition" else sense.definition
        print(f"{j+1:>3}) {lemma.ljust(4, '　')} id: {sense.id:<10} pos: {sense.pos:<8} def: {sense.definition}")
        for s, sent in enumerate(sense.examples):
            if printExamples:
                print("\t", end="")
                # Label searched term in definition
                sent = pat.sub("【\\1】", sent) if type == "examples" else sent
                print(f"{s+1}) {sent}")
        print()


def sense_id(id, cwn):
    """
    Show all info about a cwn sense.
    """
    sense = cwn.V[id]
    sense['id'] = id
    pprint.pprint(sense) 
