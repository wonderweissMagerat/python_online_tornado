#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#########################################################################
# File Name: process.py
# Author: NLP_zhaozhenyu
# Mail: zhaozhenyu_tx@126.com
# Created Time: 15:41:54 2019-01-25
#########################################################################
import sys
import re


def get_word_dict(words):
    pat = '(\.|\?|-|:|&|/)'
    res = {}
    for word in words:
        for span in re.split(pat,word):
            if span != '' and span!= ' ':
                try:
                    int(span)
                    continue
                except:
                    if span in res:
                        res[span] +=1
                    else:
                        res[span] = 1

    return res

def is_in_ngram(words,dic):
    res = set()
    cur = 0
    while cur < len(words):
        word = words[cur]
        if word in dic:
            flag = True
            for j in range(len(dic[word])):
                if j+cur+1 <len(data):
                    if data[j+cur+1]!=ngram[word][j]:
                        flag = False
                        break
                else:
                    flag = False
                    break
            if flag:
                res.add((word+' '+' '.join(dic[word])).strip())
                cur = cur+1+len(dic[word])
            else:
                cur +=1
        else:
            cur +=1
    return cur


def preprocess(content,forbidden_strict,forbidden_nostrict):
    '''
    preprocessing content
    return:
        word_dict: key is the word,value is num
        keywords_dict:{'strict':{}} where value is also a set type
    '''
    words = content.lower().split(' ')
    word_dict = get_word_dict(words)
    keywords_dict = {'strict':is_in_ngram(words,forbidden_strict),'nostrict':is_in_gram(words,forbidden_nostrict)}
    return word_dict,keywords_dict



def precess(model,idf_dict,embedding,dim,content,category,title,url,forbidden_strict,forbidden_nostrict,cate_dict):
    '''
    main processing function：
    idf_dict:idf weighting，dict
    embedding:glove embedding，dict，300d
    dim : 300 default
    content: string, splited by blanket
    category: text_category, dict
    title: string
    url:url string
    forbidden_strict: keywords that are serious,dict,key is firstword ,value is list of rest words{porn:[videos,pic]}
    forbidden_nostrict: keywords that may have relation with sex,dict
    '''
    #preprocess for is_in keywords,counts
    content_words,content_keywords = preprocess(content,forbidden_strict,forbidden_nostrict)
    title_words,title_keywords = preprocess(title,forbidden_strict,forbidden_nostrict)
    url_words,url_keywords = preprocess(url,forbidden_strict,forbidden_nostrict)
    
    input_x = []
    input_x.extend(get_embedding_feature(content_words,embedding,idf_dict))
    input_x.extend(get_embedding_feature(title_words,embedding,idf_dict))
    input_x.extend(get_embedding_feature(url_words,embedding,idf_dict))
    
    input_x.extend(get_category_onehot(category,cate_dict))

    keywords_flag = get_keywords_flag(content_keywords,title_keywords)

    #predict
    py = model.predict_proba([input_x])[0][1]

    label = judge(keywords_flag,py)
    #
    res = {'label':label,'score':0.0,'keywords':[]}


