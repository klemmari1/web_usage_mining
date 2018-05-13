# -*- encoding: utf8 -*-

import pandas as pd
from collections import Counter


def genereateRules(frequentItemsets, supports, minConfidence):
    for itemset in frequentItemsets:
        for subset in itemset:
            if(len(itemset) > 1):
                newset = set(itemset)
                newset.remove(subset)
                newset = frozenset(newset)
                if(supports[itemset] / supports[newset] >= minConfidence):
                    print(str(set(newset)) + " => " + subset + ", confidence: " + str(supports[itemset] / supports[newset]) + ", support: " + str(supports[itemset]))

def frequentItems(transactions, support):
    counter = Counter()
    for trans in transactions:
        counter.update(frozenset([t]) for t in trans)
    return set(item for item in counter if counter[item]/len(transactions) >= support), counter
 
def generateCandidates(L, k):
    candidates = set()
    for a in L:
        for b in L:
            union = a | b
            if len(union) == k and a != b:
                candidates.add(union)
    return candidates

def filterCandidates(transactions, itemsets, support):
    counter = Counter()
    for trans in transactions:
        subsets = [itemset for itemset in itemsets if itemset.issubset(trans)]
        counter.update(subsets)
    return set(item for item in counter if counter[item]/len(transactions) >= support), counter

def apriori(transactions, support):
    result = list()
    resultc = Counter()
    candidates, counter = frequentItems(transactions, support)
    result += candidates
    resultc += counter
    k = 2
    while candidates:
        candidates = generateCandidates(candidates, k)
        candidates,counter = filterCandidates(transactions, candidates, support)
        result += candidates
        resultc += counter
        k += 1
    resultc = {item:(resultc[item]/len(transactions)) for item in resultc}
    return result, resultc

# dataset preprocessing
clicks = pd.read_csv('wum_dataset_hw/clicks.csv')
visitors = pd.read_csv('wum_dataset_hw/visitors.csv')
dataset = []
data_row = []
visit_id = None
for index, row in clicks.iterrows():
    if (visit_id and visit_id != row.VisitID):
        dataset.append(data_row)
        visit_id = None
        data_row = []
    visitor_row = visitors[visitors.VisitID == row.VisitID]
    if(len(visitor_row.Length_seconds) == 1):
        visit_length = visitor_row.Length_seconds.item()
        #Continue if visit length is longer than 0 seconds.
        if(visit_length > 0):
            visit_id = row.VisitID
            # Save all PageNames the user visited during their session
            data_row.append(row.PageName)
# If there is still data in data_row after the loop
if (visit_id):
    dataset.append(data_row)
frequentItemsets, supports = apriori(dataset, 0.05)
print("Rules for PageNames:")
genereateRules(frequentItemsets, supports, 0.5)
