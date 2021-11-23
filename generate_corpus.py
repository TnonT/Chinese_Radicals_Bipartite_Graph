# -*- coding: utf-8 -*-

"""
@project: chinese_radicals_bipartite_graph
@author: heibai
@file: generate_corpus.py
@ide: PyCharm
@time 2021/11/23 20:54
"""
import json
import pickle
import pandas as pd
from typing import List


def save_as_json(data, fpath):
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_as_plk(data, fpath):
    with open(fpath, 'rb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

def generate_n_gram(s: str, n: int) -> List:
    l = len(s)
    if l < n:
        return []
    grams = []
    i = 0
    while i + n <= l:
        grams.append(s[i: i + n])
        i += 1
    return grams


def build_chinese_stroke_adjacency_matrix(cid_2_ngram_strokes, strokes_2_sid):
    m, n = len(cid_2_ngram_strokes), len(strokes_2_sid)
    matrix = [[0] * m  for _ in range(m)]

    for cid, strokes in  cid_2_ngram_strokes.iterms():
        for stroke in strokes:
            sid = strokes_2_sid[stroke]
            matrix[cid - 1][sid - 1] = 1

    return adjacency_matrix


def generate_corpus(fpath: str, n_gram: List):
    cid_2_chinese = {}
    chinese_2_cid = {}
    cid_2_n_grams_strokes = {}
    n_grams_strokes = set()


    df = pd.read_csv(DATA_PATH, use_cols=["ID", "汉字", "笔画数", "笔顺"])
    for _, row in df.iterrows():
        cid = row['ID']
        chinese = row['汉字']
        cnt = row['笔画数']
        stroke_order = row['笔顺']

        cid_2_chinese[cid] = chinese
        chinese_2_cid[chinese] = cid

        n_gram_stroke = []
        for gram in n_gram:
            grams = generate_n_gram(stroke_order, gram)
            n_gram_stroke.extend(grams)
        cid_2_n_grams_strokes[cid] = n_gram_stroke
        n_grams_strokes.update(n_grams_stroke)

    sid_2_strokes = {}
    strokes_2_sid = {}
    for idx, stroke in enumerate(n_grams_strokes):
        sid_2_strokes[idx + 1] = stroke
        strokes_2_sid[stroke] = idx + 1

    adjacency_matrix = build_chinese_stroke_adjacency_matrix(cid_2_ngrams_strokes, strokes_2_sid)


    save_as_json("data/processed_data/cid_2_chinese.json", cid_2_chinese)
    save_as_json("data/processed_data/chinese_2_cid.json", chinese_2_cid)
    save_as_json("data/processed_data/sid_2_strokes.json", sid_2_strokes)
    save_as_json("data/processed_data/strokes_2_sid.json", strokes_2_sid)
    save_as_plk("data/processed_data/adjacency_matrix.pkl", adjacency_matrix)


if __name__ == "__main__":
    DATA_PATH = "data/raw_data/T_hz.csv"









