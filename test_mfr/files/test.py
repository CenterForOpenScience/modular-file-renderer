import collections

from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction


def nCk(n, k):
    return int(reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1))


t = int(input())
for testcase in range(t):
    n = int(input())
    arr = collections.Counter(int(x) for x in raw_input().split(" "))
    print sum(nCk(x, 2) for x in arr.values() if x>1)*2
