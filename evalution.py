"""
Original code from https://github.com/ChuanMeng/QPP4CS/blob/main/evaluation_retrieval.py
Modified by: Sajad Ebrahimi
"""

import argparse
import json
import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau


def evaluation(ap_path=None, pp_path=None, target_metric: str = "mrr@10"):
    ap = {}
    with open(ap_path, 'r') as r:
        ap_bank = json.loads(r.read())

    for qid in ap_bank.keys():
        ap[qid] = float(ap_bank[qid][target_metric])

    pp = {}
    with open(pp_path, 'r') as r:
        for line in r:
            qid, pp_value = line.rstrip().split()
            pp[qid] = float(pp_value)

    ap_list = []
    pp_list = []

    for qid in ap.keys():
        ap_list.append(ap[qid])
        pp_list.append(pp[qid])

    print(f'sanity check for {target_metric}: {round(np.mean(ap_list), 3)}')
    print(f"len_ap: {len(ap)}, len_pp: {len(pp)}")
    print(f"ap's first 5 {ap_list[:5]}")
    print(f"pp's first 5 {pp_list[:5]}")

    pearson_coefficient, pearson_pvalue = pearsonr(ap_list, pp_list)
    kendall_coefficient, kendall_pvalue = kendalltau(ap_list, pp_list)
    spearman_coefficient, spearman_pvalue = spearmanr(ap_list, pp_list)

    result_dict = {"Pearson": round(pearson_coefficient, 3), "Kendall": round(kendall_coefficient, 3),
                   "Spearman": round(spearman_coefficient, 3), "len_ap": len(ap), "len_pp": len(pp)}

    print(result_dict)

    return result_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ap_path", type=str)
    parser.add_argument("--pp_path", type=str)
    parser.add_argument("--target_metric", type=str, default="mrr@10")
    args = parser.parse_args()

    result = evaluation(args.ap_path, args.pp_path, target_metric=args.target_metric)
