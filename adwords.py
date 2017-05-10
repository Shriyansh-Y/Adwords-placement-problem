import sys
import csv
import math
import random
import collections
import numpy as np

if len(sys.argv)!=2:
  exit(1)
m=sys.argv[1]

def greedy():
  s=[]
  selected=[]
  for l in l2:
    s.append(l[2])
  
  for l in l2:
    if l[2]==max(s):
      selected=l
  return selected

def msvv():
  highest=0.0
  selected=[]
  for l in l2:
    numerator=initial_budgets[l[0]]-budgets[l[0]]
    denominator=initial_budgets[l[0]]
    xu=numerator/denominator
    phi_xu=1-math.exp(xu-1)
    if highest<(float(l[2])*phi_xu):
      highest=(float(l[2])*phi_xu)
      selected=l
  return selected

def balance():
  highest=0.0
  selected=[]
  for l in l2:
    if highest<budgets[l[0]]:
      highest=budgets[l[0]]
      selected=l
  return selected


with open('bidder_dataset.csv','rb') as f:
  reader = csv.reader(f)
  adv = list(reader)

budgets={}
for b in adv[1:]:
  if(b[3]):
    try:
      value=float(b[3])
    except ValueError:
      break
    budgets[b[0]] = value

budgets=collections.OrderedDict(sorted(budgets.items()))


initial_budgets=budgets.copy()
opt = sum(budgets.values())
#print opt
#print budgets
revenue=0.0

query_list=[]
f=open('queries.txt')
for data in f:
  query_list.append(data.rstrip('\n'))
#print query_list

for q in query_list:
  l1=[]
  l2=[]
  for a in adv:
    if a[1]==q:
      l1.append(a)

  for l in l1:
    if(budgets[l[0]]>=float(l[2])):
      l2.append(l) 
#  print l2

  if m=="greedy":
    selected=greedy()
  if m=="msvv":
    selected=msvv()
  if m=="balance":
    selected=balance()
  if len(selected)!=0:
    t=float(selected[2])
    revenue=revenue+t
    budgets[selected[0]]-=t
 
print "Revenue : "+str(revenue)
 
random.seed(0)
z=[]
for i in range(100):
  random.shuffle(query_list)
  for q in query_list:
    select=[]
    l1=[]
    l2=[]
    for a in adv:
      if a[1]==q:
        l1.append(a)

    for l in l1:
      if(budgets[l[0]]>=float(l[2])):
        l2.append(l) 
    #print l2

    if m=="greedy":
      select=greedy()
    if m=="msvv":
      select=msvv()
    if m=="balance":
      select=balance()
    if len(select)!=0:
      t=float(select[2])
      revenue=revenue+t
      budgets[select[0]]-=t
      z.append(revenue)

x = min(float(s) for s in z)
ratio=x/opt
#ratio=(sum(z)/len(z))/opt
print "Competitive Ratio : "+str(round(ratio,2))
