# vim: sta:et:sw=2:ts=2:sts=2
"""
##  Hypothesis Testing expertiments
##  Courtesy : https://github.com/timm
"""
from __future__ import division
import sys, random, math
sys.dont_write_bytecode = True
from scipy.stats import chi2
from copy import deepcopy

class o:
  def __init__(i,**d) : i.add(**d)
  def has(i): return i.__dict__
  def add(i,**d) : i.has().update(**d); return i
  def __setitem__(i,k,v): i.has()[k] = v
  def __getitem__(i,k)  : return i.has()[k]
  def __repr__(i) :
     f = lambda z: z.__class__.__name__ == 'function'
     name = lambda z: z.__name__ if f(z) else z
     public = lambda z: not "_" is z[0]
     d    = i.has()
     show = [':%s=%s' % (k,name(d[k])) 
             for k in sorted(d.keys()) if public(k)]
     return '{'+' '.join(show)+'}'

  
  
"""
Misc funcs
"""
rand = random.random
any = random.choice
seed = random.seed
exp = lambda n: math.e**n
log = lambda n: math.log(n, math.e)
g = lambda n: round(n, 2)

def probit( p ):
    """
    Refer http://home.online.no/~pjacklam/notes/invnorm/impl/field/ltqnorm.txt
    for details
    """
    if p <= 0 or p >= 1:
        # The original perl code exits here, we'll throw an exception instead
        raise ValueError( "Argument to probit %f must be in open interval (0,1)" % p )
    # Coefficients in rational approximations.
    a = (-3.969683028665376e+01,  2.209460984245205e+02, \
         -2.759285104469687e+02,  1.383577518672690e+02, \
         -3.066479806614716e+01,  2.506628277459239e+00)
    b = (-5.447609879822406e+01,  1.615858368580409e+02, \
         -1.556989798598866e+02,  6.680131188771972e+01, \
         -1.328068155288572e+01 )
    c = (-7.784894002430293e-03, -3.223964580411365e-01, \
         -2.400758277161838e+00, -2.549732539343734e+00, \
          4.374664141464968e+00,  2.938163982698783e+00)
    d = ( 7.784695709041462e-03,  3.224671290700398e-01, \
          2.445134137142996e+00,  3.754408661907416e+00)
    # Define break-points.
    plow  = 0.02425
    phigh = 1 - plow
    # Rational approximation for lower region:
    if p < plow:
       q  = math.sqrt(-2*math.log(p))
       return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    # Rational approximation for upper region:
    if phigh < p:
       q  = math.sqrt(-2*math.log(1-p))
       return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    # Rational approximation for central region:
    q = p - 0.5
    r = q*q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
           (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)


def median(lst, ordered=False):
  if not ordered: lst = sorted(lst)
  n = len(lst)
  p = n//2
  if n % 2: return lst[p]
  q = p - 1
  q = max(0, min(q, n))
  return (lst[p] + lst[q])/2

def median_IQR(lst):
  "Assumes lst is ordered."
  n   = len(lst)
  a   = int(0.25 * n)  
  b1  = int(0.50 * n) ; b2 = max(b1 - 1,0)
  c   = int(0.75 * n)
  iqr = lst[c] - lst[a]
  mid = lst[b1] if n % 2 else ((lst[b1] + lst[b2]) / 2) 
  return mid, iqr

def msecs(f):
  import time
  t1 = time.time()
  f()
  return (time.time() - t1) * 1000

  
def pairs(lst):
  "Return all pairs of items i,i+1 from a list."
  last=lst[0]
  for i in lst[1:]:
    yield last, i
    last = i


def xtile(lst,lo=0,hi=100,width=40,
       chops=[0.1 ,0.3,0.5,0.7,0.9],
       #chops=[0.25,0.5,0.75],
       marks=[" ","-","-"," "],
       #marks=["-","-"],
       bar="|",star="*",show=" %3.0f", showQuartiles=True):
  """The function _xtile_ takes a list of (possibly)
  unsorted numbers and presents them as a horizontal
  xtile chart (in ascii format). The default is a 
  contracted _quintile_ that shows the 
  10,30,50,70,90 breaks in the data (but this can be 
  changed- see the optional flags of the function).
  """
  def pos(p)   : return ordered[int(len(ordered)*p)]
  def place(x) : 
    return int(width*float((x - lo))/(hi - lo+0.00001))
  def pretty(lst) : 
    return ', '.join([show % x for x in lst])
  ordered = sorted(lst)
  #lo      = min(lo,ordered[0])
  #hi      = max(hi,ordered[-1])
  what    = [pos(p)   for p in chops]
  where   = [place(n) for n in  what]
  out     = [" "] * width
  for one,two in pairs(where):
    for i in range(one,two):
      if i<len(out):
        out[i] = marks[0]
    marks = marks[1:]
  out[int(width/2)]    = bar
  out[place(pos(0.5))] = star
  #print(lst)
  if not showQuartiles:
    return '('+''.join(out) +  "),"
  return '('+''.join(out) +  ")," +  pretty(what)

def lastIndex(lst, item):
  return max(i for i, val in enumerate(lst) if val == item)

"""

### Standard Accumulator for Numbers

Note the _lt_ method: this accumulator can be sorted by median values.

Warning: this accumulator keeps _all_ numbers. Might be better to use
a bounded cache.

"""
class Num:
  "An Accumulator for numbers"
  def __init__(i,name,inits=[]): 
    i.n = i.m2 = i.mu = 0.0
    i.all=[]
    i._median=None
    i.name = name
    i.rank = 0
    i.blom = None
    for x in inits: i.add(x)
  def s(i)       : return (i.m2/(i.n - 1))**0.5
  def add(i,x):
    i._median=None
    i.n   += 1   
    i.all += [x]
    delta  = x - i.mu
    i.mu  += delta*1.0/i.n
    i.m2  += delta*(x - i.mu)
  def __add__(i,j):
    return Num(i.name + j.name,i.all + j.all)
  def quartiles(i):
    def p(x) : return int(100*g(xs[x]))
    i.median()
    xs = i.all
    n  = int(len(xs)*0.25)
    return p(n) , p(2*n) , p(3*n)
  def median(i):
    if not i._median:
      i.all = sorted(i.all)
      i._median=median(i.all)
    return i._median
  def __lt__(i,j):
    return i.median() < j.median() 
  def spread(i):
    i.all=sorted(i.all)
    n1=i.n*0.25
    n2=i.n*0.75
    if len(i.all) <= 1:
      return 0
    if len(i.all) == 2:
      return i.all[1] - i.all[0]
    else:
      return i.all[int(n2)] - i.all[int(n1)]
  def setBlom(i, mus):
    rank = (mus.index(i.median()) + lastIndex(mus, i.median()))/2 + 1
    i.blom = probit((rank - 0.375)/(len(mus)+0.25))
"""
### The A12 Effect Size Test 
"""

def a12(lst1,lst2):
  "how often is x in lst1 more than y in lst2?"
  def loop(t,t1,t2): 
    while t1.j < t1.n and t2.j < t2.n:
      h1 = t1.l[t1.j]
      h2 = t2.l[t2.j]
      h3 = t2.l[t2.j+1] if t2.j+1 < t2.n else None 
      if h1>  h2:
        t1.j  += 1; t1.gt += t2.n - t2.j
      elif h1 == h2:
        if h3 and h1 > h3 :
            t1.gt += t2.n - t2.j  - 1
        t1.j  += 1; t1.eq += 1; t2.eq += 1
      else:
        t2,t1  = t1,t2
    return t.gt*1.0, t.eq*1.0
  #--------------------------
  lst1 = sorted(lst1, reverse=True)
  lst2 = sorted(lst2, reverse=True)
  n1   = len(lst1)
  n2   = len(lst2)
  t1   = o(l=lst1,j=0,eq=0,gt=0,n=n1)
  t2   = o(l=lst2,j=0,eq=0,gt=0,n=n2)
  gt,eq= loop(t1, t1, t2)
  return gt/(n1*n2) + eq/2/(n1*n2)


"""
## Non-Parametric Hypothesis Testing

The following _bootstrap_ method was introduced in
1979 by Bradley Efron at Stanford University. It
was inspired by earlier work on the
jackknife.
Improved estimates of the variance were [developed later][efron01].  

[efron01]: http://goo.gl/14n8Wf "Bradley Efron and R.J. Tibshirani. An Introduction to the Bootstrap (Chapman & Hall/CRC Monographs on Statistics & Applied Probability), 1993"

To check if two populations _(y0,z0)_
are different, many times sample with replacement
from both to generate _(y1,z1), (y2,z2), (y3,z3)_.. etc.
"""
def sampleWithReplacement(lst):
  "returns a list same size as list"
  def any(n)  : return random.uniform(0,n)
  def one(lst): return lst[ int(any(len(lst))) ]
  return [one(lst) for _ in lst]

"""
Then, for all those samples,
 check if some *testStatistic* in the original pair
hold for all the other pairs. If it does more than (say) 99%
of the time, then we are 99% confident in that the
populations are the same.

In such a _bootstrap_ hypothesis test, the *some property*
is the difference between the two populations, muted by the
joint standard deviation of the populations.
"""
def testStatistic(y,z): 
    """Checks if two means are different, tempered
     by the sample size of 'y' and 'z'"""
    tmp1 = tmp2 = 0
    for y1 in y.all: tmp1 += (y1 - y.mu)**2 
    for z1 in z.all: tmp2 += (z1 - z.mu)**2
    s1 = (float(tmp1)/(y.n - 1))**0.5
    s2 = (float(tmp2)/(z.n - 1))**0.5
    delta = z.mu - y.mu
    if s1+s2:
      delta = delta/((s1/y.n + s2/z.n)**0.5)
    return delta
"""

The rest is just details:

+ Efron advises
  to make the mean of the populations the same (see
  the _yhat,zhat_ stuff shown below).
+ The class _total_ is a just a quick and dirty accumulation class.
+ For more details see [the Efron text][efron01].  

"""
def bootstrap(y0,z0,conf=0.01,b=1000):
  """The bootstrap hypothesis test from
     p220 to 223 of Efron's book 'An
    introduction to the boostrap."""
  class total():
    "quick and dirty data collector"
    def __init__(i,some=[]):
      i.sum = i.n = i.mu = 0 ; i.all=[]
      for one in some: i.put(one)
    def put(i,x):
      i.all.append(x);
      i.sum +=x; i.n += 1; i.mu = float(i.sum)/i.n
    def __add__(i1,i2): return total(i1.all + i2.all)
  y, z   = total(y0), total(z0)
  x      = y + z
  tobs   = testStatistic(y,z)
  yhat   = [y1 - y.mu + x.mu for y1 in y.all]
  zhat   = [z1 - z.mu + x.mu for z1 in z.all]
  bigger = 0.0
  for i in range(b):
    if testStatistic(total(sampleWithReplacement(yhat)),
                     total(sampleWithReplacement(zhat))) > tobs:
      bigger += 1
  return bigger / b < conf




def different(l1,l2, mode="a12"):
  #return bootstrap(l1,l2) and a12(l2,l1)
  if mode == "a12":
    # hack to make it faster
    return a12(l2,l1) and bootstrap(l1,l2)
  elif mode == "cliffs":
    return cliffsDelta(l1,l2)
  elif mode == "cliffs_bs":
    return cliffsDelta(l1,l2) and bootstrap(l1,l2)

"""

## Saner Hypothesis Testing

The following code, which you should use verbatim does the following:


+ All treatments are clustered into _ranks_. In practice, dozens
  of treatments end up generating just a handful of ranks.
+ The numbers of calls to the hypothesis tests are minimized:
    + Treatments are sorted by their median value.
    + Treatments are divided into two groups such that the
      expected value of the mean values _after_ the split is minimized;
    + Hypothesis tests are called to test if the two groups are truly difference.
          + All hypothesis tests are non-parametric and include (1) effect size tests
            and (2) tests for statistically significant numbers;
          + Slow bootstraps are executed  if the faster _A12_ tests are passed;

In practice, this means that the hypothesis tests (with confidence of say, 95%)
are called on only a logarithmic number of times. So...

+ With this method, 16 treatments can be studied using less than _&sum;<sub>1,2,4,8,16</sub>log<sub>2</sub>i =15_ hypothesis tests  and confidence _0.99<sup>15</sup>=0.86_.
+ But if did this with the 120 all-pairs comparisons of the 16 treatments, we would have total confidence _0.99<sup>120</sup>=0.30.

For examples on using this code, see _rdivDemo_ (below).

"""
def scottknott(data,cohen=0.3,small=3, test=None,epsilon=0.01):
  """Recursively split data, maximizing delta of
  the expected value of the mean before and 
  after the splits. 
  Reject splits with under 3 items"""
  if test == "anova":
    return rdiv_anova(data)
  elif test == "linear_cliffs":
    return ranked(data)
  all  = reduce(lambda x,y:x+y,data)
  same = lambda l,r: abs(l.median() - r.median()) <= all.s()*cohen
  if test: 
    same = lambda l, r:   not different(l.all,r.all,test) 
  big  = lambda    n: n > small    
  return rdiv(data,all,minMu,big,same,epsilon)


def rankInList(item, lst, delta=0.01):
  start,end = 0,0
  for i, val in enumerate(sorted(lst)):
    if start!=0 and val >= item:
      start = i+1
    if val > (item + delta):
      end = i
      break
  return (start+end)/2
  
  
def rdiv_anova(data, epsilon=0.01): # a list of class Nums
  data = sorted(data)
  def recurse(parts, rank=0):
    all = reduce(lambda x,y:x+y,parts)
    cut, left, right = minChi(parts, all)
    if cut: 
        # if cut, rank "right" higher than "left"
        rank = recurse(left,rank) + 1
        rank = recurse(right,rank)
    else: 
      # if no cut, then all get same rank
      for part in parts: 
        part.rank = rank
    return rank
  recurse(data)
  data = sorted(data, key=lambda i: (i.median(),i.rank))
  return data

def computeBlom(data, all):
  rank = rankInList(data.median(), all.all)
  data.blom = probit((rank - 0.375)/(all.n+0.25))

def minChi(parts, all):
  pi=math.pi
  def meanBlom(tests):
    return sum([test.blom for test in tests])/len(tests)
  def SSE(tests):
    return sum([test.blom**2 for test in tests])
  for part in parts:
    computeBlom(part, all)
  k = parts[0].n
  cut, left, right = None, None, None
  bestError = 0
  if len(parts) == 1:
    return cut, left, right
  totalError = meanBlom(parts)
  for i in range(1,len(parts)):
      lParts, rParts = parts[:i], parts[i:]
      error = k*(len(lParts)*((meanBlom(lParts) - totalError)**2) + len(rParts)*((meanBlom(rParts) - totalError)**2))
      if (error > bestError):
        bestError, cut, left, right = error, i, lParts, rParts
  v = k/(pi-2)
  lamda = (pi/(2*(pi-2)))*bestError/(SSE(parts)/v)
  chi = chi2.ppf(0.99, v)
  if lamda > chi:
    return cut, left, right
  return None, None, None

def rdiv(data,  # a list of class Nums
         all,   # all the data combined into one num
         div,   # function: find the best split
         big,   # function: rejects small splits
         same, # function: rejects similar splits
         epsilon): # small enough to split two parts
  """Looks for ways to split sorted data, 
  Recurses into each split. Assigns a 'rank' number
  to all the leaf splits found in this way. 
  """
  def recurse(parts,all,rank=0):
    "Split, then recurse on each part."
    cut,left,right = maybeIgnore(div(parts,all,big,epsilon),
                                 same,parts)
    if cut: 
      # if cut, rank "right" higher than "left"
      rank = recurse(parts[:cut],left,rank) + 1
      rank = recurse(parts[cut:],right,rank)
    else: 
      # if no cut, then all get same rank
      for part in parts: 
        part.rank = rank
    return rank
  recurse(sorted(data),all)
  return data

def maybeIgnore((cut,left,right), same,parts):
  if cut:
    if same(sum(parts[:cut],Num('upto')),
            sum(parts[cut:],Num('above'))):    
      cut = left = right = None
  return cut,left,right

def minMu(parts,all,big,epsilon):
  """Find a cut in the parts that maximizes
  the expected value of the difference in
  the mean before and after the cut.
  Reject splits that are insignificantly
  different or that generate very small subsets.
  """
  cut,left,right = None,None,None
  before, mu     =  0, all.mu
  for i,l,r in leftRight(parts,epsilon):
    if big(l.n) and big(r.n):
      n   = all.n * 1.0
      now = l.n/n*(mu- l.mu)**2 + r.n/n*(mu- r.mu)**2  
      if now > before:
        before,cut,left,right = now,i,l,r
  return cut,left,right

def leftRight(parts,epsilon=0.01):
  """Iterator. For all items in 'parts',
  return everything to the left and everything
  from here to the end. For reasons of
  efficiency, take a first pass over the data
  to pre-compute and cache right-hand-sides
  """
  rights = {}
  n = j = len(parts) - 1
  while j > 0:
    rights[j] = parts[j]
    if j < n: rights[j] += rights[j+1]
    j -=1
  left = parts[0]
  for i,one in enumerate(parts):
    if i> 0: 
      if parts[i]._median - parts[i-1]._median > epsilon:
        yield i,left,rights[i]
      left += one
      
"""
## Cliff's Delta
Checking if the two lists of numbers are
different by an interesting amount.
""" 
def runs(lst):
  for j,two in enumerate(lst):
    if j == 0:
      one,i = two,0
    if one!=two:
      yield j - i,one
      i = j
    one=two
  yield j - i + 1,two

def ntiles(lst,tiles):
  thing = lambda z: lst[ int(len(lst)*z)  ]
  return [ thing(tile) for tile in tiles ]
  
  
def cliffsDelta(lst1, lst2, dull=0.147):
  m, n = len(lst1), len(lst2)
  lst2 = sorted(lst2)
  j = more = less = 0
  for repeats,x in runs(sorted(lst1)):
    while j <= (n - 1) and lst2[j] <  x: 
      j += 1
    more += j*repeats
    while j <= (n - 1) and lst2[j] == x: 
      j += 1
    less += (n - j)*repeats
  d= (more - less) / (m*n + 0.000001) 
  return abs(d)  > dull      

"""
Linear Cliffs Delta
Take a dictionary of values representing
different treatments. Return a list
of the values, sorted on their median,
ranked by Cliff's Delta.
"""
def ranked(rx,tiles=None,trivial=None, doPrint=True):
  "Returns a ranked list."
  def kill_outliers(lst, median):
    return [x for x in lst if x < 4*median]
  tiles = tiles or [0.25, 0.5, 0.75 ]
  tiny = trivial or 0.01
  def prep(key):
    nums  = sorted( rx[key] )
    med,iqr = median_IQR(nums)
    return o(rank  = 1,
             name  = key,
             _nums = nums,
             median= med,
             iqr   = iqr,
             tiles = ntiles(nums, tiles))
  lsts = sorted([prep(k) for k in rx],
                key = lambda z: z.median)
  rank, pool = 1, lsts[0]._nums
  b4,_ = median_IQR(pool)
  for x in lsts[1:]:
    if abs(x.median - b4) > tiny \
       and cliffsDelta(x._nums, pool):
      rank += 1
      pool  = x._nums
      b4    = x.median
    else:
      pool  += x._nums
      b4,_   = median_IQR(sorted(pool))
    x.rank = rank
    
  data = []
  for lst in lsts:
    num = Num(lst.name, sorted(rx[lst.name]))
    num.rank = lst.rank
    data.append(num)
  ranks, maxMedian =[],-1
  for x in data:
    maxMedian = max(maxMedian, x.median())
    ranks += [(x.rank,x.median(),x)]
  if not doPrint:
    return ranks
  
  all=[]
  for _,__,x in sorted(ranks): all += x.all
  
  all = kill_outliers(sorted(all),maxMedian)
  lo, hi = all[0], all[-1]
  line = "----------------------------------------------------"
  last = None
  print  ('%4s , %16s ,    %s   , %4s ' % \
               ('rank', 'name', 'med', 'iqr'))+ "\n"+ line
  for _,__,x in ranks:
    q1,q2,q3 = x.quartiles()
    #xtile(x.all,lo=lo,hi=hi,width=30,show="%5.2f")
    print  ('%1s , %16s , %4s , %4s ' % \
                 (x.rank, x.name, q2, q3 - q1))  + \
              xtile(x.all,lo=lo,hi=hi,width=30,show="%5.2f")
    last = x.rank 

"""
## Putting it All Together

Driver for the demos:

"""
def rdivDemo(data, test="a12"):
  def z(x):
    return int(100 * (x - lo) / (hi - lo + 0.00001))
  def kill_outliers(lst, median):
    return [x for x in lst if x < 4*median]
  data = map(lambda lst:Num(lst[0],lst[1:]),
             data)
  ranks=[]
  maxMedian = -1
  for x in scottknott(data, test=test):
    maxMedian = max(maxMedian, x.median())
    ranks += [(x.rank,x.median(),x)]
  all=[]
  for _,__,x in sorted(ranks): all += x.all
  #all = sorted(all)
  all = kill_outliers(sorted(all),maxMedian)
  lo, hi = all[0], all[-1]
  line = "----------------------------------------------------"
  last = None
  print  ('%4s , %16s ,    %s   , %4s ' % \
               ('rank', 'name', 'med', 'iqr'))+ "\n"+ line
  for _,__,x in sorted(ranks):
    q1,q2,q3 = x.quartiles()
    #xtile(x.all,lo=lo,hi=hi,width=30,show="%5.2f")
    print  ('%1s , %16s , %4s , %4s ' % \
                 (x.rank+1, x.name, q2, q3 - q1))  + \
              xtile(x.all,lo=lo,hi=hi,width=30,show="%5.2f")
    last = x.rank 

    
def rankDemo(data, tests=None):
  
  def updateRankObj(rankObj, ranks, test):
    for rank,_,x in ranks:
      rankObj[x.name][test] = rank
    
  def kill_outliers(lst, median):
    return [x for x in lst if x < 6*median]
  if not tests:
    tests = ["anova", "cliffs", "cliffs_bs", "a12", "linear_cd"]
  rankObj = {}
  for row in data:
    testObj = {}
    for test in tests:
      testObj[test]=0
    rankObj[row[0]] = testObj
  
  data = map(lambda lst:Num(lst[0],lst[1:]),
             data)
  maxMedian = -1
  for test in tests:
    ranks = []
    datacp = deepcopy(data)
    if test == "linear_cd":
      rx = dict()
      for n in datacp:
        rx[n.name] = n.all
      ranks = ranked(rx, doPrint=False)
    else :
      for x in scottknott(datacp, test=test):
        maxMedian = max(x.median(), maxMedian)
        ranks += [(x.rank+1, x.median(), x)]
    updateRankObj(rankObj, ranks, test)
  
  all=[]
  for _,__,x in sorted(ranks): all += x.all
  all = kill_outliers(sorted(all),maxMedian)
  #all = sorted(all)
  lo, hi = all[0], all[-1]
  line = "-"*100
  last = None
  testsF = "".join(["%10s, "]*len(sorted(tests)))
  print "%15s, "%"Method" + testsF%tuple(sorted(tests)) + ", %5s %5s"%("med","iqr") + "\n" + line
  for _,__,x in sorted(ranks, key= lambda z:(z[0],z[2].quartiles()[1])):
    q1,q2,q3 = x.quartiles()
    keys = sorted(rankObj[x.name].keys())
    vals = [rankObj[x.name][key] for key in keys]
    print "%15s, " % x.name + testsF % tuple(vals) + ", %5s %5s"%(q2, q3-q1) + ", " + xtile(x.all,lo=lo,hi=hi,width=30,show="%5.2f", showQuartiles=False)
  
  
  
  
  
  