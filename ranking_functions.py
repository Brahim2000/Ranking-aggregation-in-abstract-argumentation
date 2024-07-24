from Alpha_Burden_based_semantic import alpha_burden_based
from Burden_based_semantic import burden_based
from catergriser_based import categoriser_based_ranking as categoriser_based_ranking_func
from discussion_based import discussion_based
from matt_and_toni import mt_ranking
from tuple_based import tuple_based
from scoring_aggregation.borda_count_aggregation import borda_count_aggregation

def alpha_burden_based_ranking(G, alpha_value):
    return alpha_burden_based(G, alpha_value)

def burden_based_ranking(G, n):
    return burden_based(G, n)

def categoriser_based_ranking(G):
    return categoriser_based_ranking_func(G)

def discussion_based_ranking(G, n):
    return discussion_based(G, n)

def mt_ranking_func(G):
    return mt_ranking(G)

def tuple_based_ranking(G):
    return tuple_based(G)

def borda_count_aggregation_rankings(rankings):
    return borda_count_aggregation(rankings)
