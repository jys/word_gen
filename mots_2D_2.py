#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import numpy as np
from numpy.random import choice, seed
seed(1)
import codecs
import os

def process(lang, codec):
    filepath = os.path.join("words", "%s.txt" % lang)
    outfile = os.path.join("outputs", "%s.txt" % lang)
    probafile = os.path.join("counts", "%s.bin" % lang)

    dico = []
    with codecs.open(filepath, "r", "ISO-8859-1") as lines:
        for l in  lines:
            dico.append(l[:-1])
        
    count = np.fromfile(probafile, dtype="int32").reshape(256,256,256)

    s = count.sum(axis=2)
    st = np.tile(s.T, (256,1,1)).T
    p = count.astype('float') / st
    p[np.isnan(p)] = 0

    #%%
    with codecs.open(outfile, "w", codec) as f:
        K = 100
        for TGT in range(12,13):

        #K = 100
        #for TGT in range(4,11):
            total = 0
            while total < 100:
                i = 0
                j = 0
                res = u''
                while not j==10:
                    k=choice(range(256),1,p=p[i,j,:])[0]
                    #res = res + chr(k)
                    res = res + unichr(k)
                    i = j
                    j = k
                if len(res) == 1 + TGT:
                    x = res[:-1]
                    if res[:-1] in dico:
                        x = res[:-1] + "*"
                    total += 1
                    print(x)
                    f.write(x + "\n")

@click.command()
@click.option('--lang', default="FR", help='Language')
@click.option('--codec', default="ISO-8859-1", help='Codec')
def main(lang, codec):
    process(lang, codec)

if __name__ == '__main__':
    main()
