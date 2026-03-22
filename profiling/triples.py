# run with python -m cProfile profiling/triples.py
# profiling/triples.py
def calc_triples(mx):
    triples = []
    for a in range(1, mx + 1):
        for b in range(a, mx + 1):
            hypotenuse = calc_hypotenuse(a, b)
            if is_int(hypotenuse):
                triples.append((a, b, int(hypotenuse)))
    return triples
#def calc_hypotenuse(a, b):
 #   return (a**2 + b**2) ** .5
def calc_hypotenuse(a, b):
    return (a*a + b*b) ** .5
def is_int(n):  # n is expected to be a float
    return n.is_integer()
def for_loop():
    for i in triples:
        for k in i:
            print(k)
def iter_loop():
    new_iter_obj = iter(triples)
    print(*new_iter_obj)
triples = calc_triples(10000)

def list_comp():
    new_list = [k for i in triples for k in i]
    print(*new_list,sep='\n')

#for_loop()
#iter_loop()
list_comp()
