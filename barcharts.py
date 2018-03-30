from lingpy import *
from collections import defaultdict
from matplotlib import pyplot as plt
import colorsys

wl = Wordlist('ALL_Borrowings.tsv')

langs = csv2list('dogon-languages.tsv')

# make dictionary to get the groups quickly from a language name
lang2group = {k[3]: k[1] for k in langs[1:]}

patterns = {l: [] for l in lang2group}
allpats = defaultdict(list)

etd = wl.get_etymdict(ref='cogid')
for k, vals in etd.items():
    idxs = [v[0] for v in vals if v and wl[v[0], 'doculect'] in lang2group]
    lngs = [wl[idx, 'doculect'] for idx in idxs]
    groups = defaultdict(list)
    for idx, lng in zip(idxs, lngs):
        groups[lang2group[lng]] += [lng]
    gstruc = ' '.join(['{0}:{1}'.format(y, len(groups[y])) for y in
        sorted(groups)])
    for idx, lng in zip(idxs, lngs):
        patterns[lng] += [(gstruc, idx)]
    allpats[gstruc] += [k]

bars = [0, 0, 0, 0, 0]
bars2 = [0, 0, 0, 0, 0]
bars3 = [0, 0, 0, 0, 0]
bars4 = [0, 0, 0, 0, 0]
bars5 = [0, 0, 0, 0, 0]

with open('patterns.tsv', 'w') as f:
    f.write('PATTERN\tAtlantic\tBangime\tDogon\tMande\tSonghai\tExamples\tCOGIDS\n')
    for k, v in allpats.items():
        nums = ['0', '0', '0', '0', '0']
        grps = ['Atlantic', 'Bangime', 'Dogon', 'Mande', 'Songhai']
        cncs = [wl[[y[0] for y in etd[cogid] if y][0], 'concept'] for cogid in
                v]
        for key in k.split():
            a, b = key.split(':')
            kidx = grps.index(a)
            nums[kidx] = b
        f.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(k, '\t'.join(nums),
            len(v), ' '.join([str(x) for x in
            v]), ', '.join(cncs)))
        if 'Bangime' in k:
            nums = [int(x) for x in nums]
            if nums.count(0) == 3:
                for i, (a, b) in enumerate(zip(grps, nums)):
                    if b > 0 and a != 'Bangime':
                        this_lng = a
                        bars[i] += len(v)
            elif nums.count(0) == 4:
                bars[1] += len(v)
        if 'Atlantic' in k:
            nums = [int(x) for x in nums]
            if nums.count(0) == 3:
                for i, (a, b) in enumerate(zip(grps, nums)):
                    if b > 0 and a != 'Atlantic':
                        this_lng = a
                        bars2[i] += len(v)
            elif nums.count(0) == 4:
                bars2[0] += len(v)

        if 'Dogon' in k:
            nums = [int(x) for x in nums]
            if nums.count(0) == 3:
                for i, (a, b) in enumerate(zip(grps, nums)):
                    if b > 0 and a != 'Dogon':
                        this_lng = a
                        bars3[i] += len(v)
            elif nums.count(0) == 4:
                bars3[2] += len(v)
        if 'Mande' in k:
            nums = [int(x) for x in nums]
            if nums.count(0) == 3:
                for i, (a, b) in enumerate(zip(grps, nums)):
                    if b > 0 and a != 'Mande':
                        this_lng = a
                        bars4[i] += len(v)
            elif nums.count(0) == 4:
                bars4[3] += len(v)

        if 'Songhai' in k:
            nums = [int(x) for x in nums]
            if nums.count(0) == 3:
                for i, (a, b) in enumerate(zip(grps, nums)):
                    if b > 0 and a != 'Mande':
                        this_lng = a
                        bars5[i] += len(v)
            elif nums.count(0) == 4:
                bars5[4] += len(v)




plt.clf()
labels = grps
explode = [0.2, 0.0, 0.0, 0.2, 0.2]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgray']
plt.pie(bars, explode=explode, labels=labels, colors=colors, shadow=True,
        startangle=140, autopct='%1.1f%%')
plt.axis('equal')
plt.savefig('bangime.pdf')
plt.clf()
labels = grps
explode = [0.2, 0.0, 0.0, 0.2, 0.2]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgray']
plt.pie(bars2, explode=explode, labels=labels, colors=colors, shadow=True,
        startangle=140, autopct='%1.1f%%')
plt.axis('equal')
plt.savefig('atlantic.pdf')
plt.clf()
explode = [0.2, 0.0, 0.0, 0.2, 0.2]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgray']
plt.pie(bars3, explode=explode, labels=labels, colors=colors, shadow=True,
        startangle=140, autopct='%1.1f%%')
plt.axis('equal')
plt.savefig('dogon.pdf')
plt.clf()
explode = [0.2, 0.0, 0.0, 0.2, 0.2]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgray']
plt.pie(bars4, explode=explode, labels=labels, colors=colors, shadow=True,
        startangle=140, autopct='%1.1f%%')
plt.axis('equal')
plt.savefig('mande.pdf')
plt.clf()
explode = [0.2, 0.0, 0.0, 0.2, 0.2]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgray']
plt.pie(bars5, explode=explode, labels=labels, colors=colors, shadow=True,
        startangle=140, autopct='%1.1f%%')
plt.axis('equal')
plt.savefig('songhai.pdf')


pies = {}
alls = defaultdict(int)
for l in patterns:
    pies[l] = defaultdict(list)
    for pattern, cogid in patterns[l]:
        name = '-'.join([x.split(':')[0] for x in pattern.split()])
        pies[l][name] += [cogid]
        alls[name] += 1
print(len(alls))

pattern_order = sorted(alls, key=lambda x: alls[x], reverse=True)


from matplotlib import gridspec
from lingpy.convert.html import colorRange

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

crange = colorRange(len(patterns))
#crange = [hex_to_rgb(x) for x in crange]

import numpy as np
import random
from matplotlib import cm
cs1=cm.tab20(np.arange(20)/20.)
cs2=cm.tab20b(np.arange(20)/20.)
cs = list(cs1)+list(cs2)
#random.shuffle(cs)

gs = gridspec.GridSpec(6, 2)
plt.clf()
fig = plt.Figure()
for i, l in enumerate(sorted(patterns)):
    sp = plt.subplot(gs[i])
    # assemble the pie chart
    bars = []
    colors = []
    for i, (pattern, color) in enumerate(zip(pattern_order, cs)):
        if len(pies[l][pattern]) > 5:
            bars += [len(pies[l][pattern])]
            colors += [color]
    print(bars, colors)
    sp.pie(bars, colors=colors)
    sp.set_autoscale_on(False)
    plt.ylim(-1, 1)
    plt.xlim(-1, 1)
    sp.set_aspect('equal')
    sp.set_title(l)
    #sp.title(l)

for color, pattern in zip(cs, pattern_order):
    plt.plot(-10, -10, 'o', color=color, label=pattern)
plt.legend()
plt.savefig('patterns.pdf')
