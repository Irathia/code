# -*- coding: utf-8 -*-
import operator
import sys

import time

q_max = []
time_limit = 0
time_start = 0
number_of_colors = 0

def reenumenate(edges, new_en):
    new_edges = {}
    sort_edges_keys = list(edges.keys())
    sort_edges_keys.sort()
    for i in edges.keys():
        new_v = new_en[sort_edges_keys.index(i)]
        new_edges[new_v] = []
        for v in edges[i]:
            new_edges[new_v].append(new_en[sort_edges_keys.index(v)])

    return new_edges


def find_new_enumeration(edges):
    new_en = []
    st = []#степень
    sort_edges_keys = list(edges.keys())
    sort_edges_keys.sort()
    for v in sort_edges_keys:
        st.append(len(edges[v]))

    indexes = sorted(range(len(st)), key=lambda k : st[k], reverse=True)
    return [sort_edges_keys[i] for i in indexes]

def read_dimacs(name):
    file = open(name, 'r')
    s = file.readline()
    while s[0] == "c":#пропускаем строки с коментариями в DIMACS файлахони начинаются с c
        s = file.readline()

    edges = {}

    for line in file.readlines():# бежим по каждой строчке, там написано e вершина1 вершина2.
        tmp, a, b = line.split(" ")#получаем индексы вершин
        b = int(b)
        a = int(a)
        if a not in edges.keys():#если вершины a еще не было
            edges[a] = [b]#добавляем ее и добавляем ей, вершину b, как соседа
        else:
            edges[a].append(b)#добавляем ей, вершину b, как соседа

        if b not in edges.keys():#если вершины b еще не было
            edges[b] = [a]#добавляем ее и добавляем ей, вершину a, как соседа
        else:
            edges[b].append(a)#добавляем ей, вершину a, как соседа

    file.close()

    return edges#возвращаем словарь вершин и их соседей


def find_candidates(edges, q):#поиск кандидатов

    max_v = max(q)
    candidates = set(edges[q[0]])#
    for v in q[1:]:
        candidates = candidates & set(edges[v])#берем только тех, кто является соседями всех вершин из q

    return [x for x in candidates if x > max_v]#берем только большего индекса, чтобы не повторяться



def BandB(edges, q):
    if time.clock() - time_start > time_limit:
        return -1
    global q_max
    if len(q) > len(q_max):# если нашли больше, чем есть, то сохраняем
        #print("Found clique of bigger size", q)
        q_max = q.copy()

    if len(q_max) == number_of_colors:
        return

    candidates = find_candidates(edges, q)#ищем кандидатов на добавление

    if len(q) + len(candidates) < len(q_max):# проверяем верхнюю границу
        return#если она меньше, чем у нас есть, то выходим

    candidates.sort()
    for v in candidates:#берем каждую вершину из кандидатов
        q.append(v)#добавляем ее
        BandB(edges, q)#снова запускаем метод ветвей и границ, рекурсивно
        q.pop()#убираем кандидата
    return


def color(edges):
    colors = [0 for i in range(len(edges))]
    sort_edges_keys = list(edges.keys())
    sort_edges_keys.sort()
    n_colors = 1
    for i in range(len(sort_edges_keys)):
        colors_of_neigboors = set([colors[sort_edges_keys.index(x)] for x in edges[sort_edges_keys[i]]])
        colors[i] = min(set(list(range(1,n_colors+2)))-colors_of_neigboors)
        if colors[i] > n_colors:
            n_colors += 1
        #print(colors)

    return n_colors

def solve(edges):
    global time_start, number_of_colors
    time_start = time.clock()
    #new_en = find_new_enumeration(edges)
    #print(new_en)
    #edges = reenumenate(edges,new_en)
    sort_edges_keys = list(edges.keys())
    sort_edges_keys.sort()
    number_of_colors = color(edges)
    print("Colors =",number_of_colors)
    for v in sort_edges_keys:#для каждой вершины запускаем метод ветвей и границ
        rv = BandB(edges, [v])
        if rv == -1:
            break
    if rv != -1:
        print(len(q_max), " ".join([str(x) for x in q_max]),time.clock() - time_start, sep = ";")
        #print("Maximum clique -",q_max,"size =", len(q_max), 'time',time.clock() - time_start)
    else:
        print('0',  " ".join([str(x) for x in q_max]),time_limit, sep = ";")
        #print("Maximum clique -",q_max,"size =", 0,'time',time_limit)



if __name__ == "__main__":
    filename = sys.argv[1]
    time_limit = int(sys.argv[2])
    #print(filename)
    edges = read_dimacs(filename)#считываем
    # for x in edges.keys():
    #     print(x, "-", edges[x])
    solve(edges)#решаем





