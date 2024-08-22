from collections import deque
def selectsort(x):
    n=len(x)
    for i in range(0,n-2):
        min_index = i
        for j in range(i+1,n-1):
            if x[j]<x[min_index]:
                min_index = j
        print("x[i]:",x[i]," x[min_index]:",x[min_index])
        x[i],x[min_index]=x[min_index],x[i]
def function(N,A):
    #N = int(input()) 
    #A es un arreglo de tamaño N 
    #A = tuple(map(int, input().split())) 
    i = 0 
    j = 2 
    x = 0 
    while i < 4: 
        k = i 
        while k < N: 
            x += A[k] 
            k += j 
        j += 1 
        i += 1 
        print(x)
def anotherfunction(N,X):
    #N = int(input()) 
    #X es una pila de tamaño N 
    #X = deque(map(int, input().split()))
    N=N
    X=deque(X)
    Y = deque() 
    i = 1 
    while len(X) > 0: 
        e = X.pop() 
        if i % 3 != 0: 
            Y.append(e) #push
            print("e:",e)
        i += 1 
    j = 1 
    while len(Y) > 0: 
        e = Y.pop() 
        if j % 2 != 0: 
            print(e) 
        j += 1
def binfunction(x):
    f=len(x)-1
    i=0
    xi=x[i]
    if len(x)==1:
        return xi
    if x[i]<x[f]:
        return x[f]

    while i<f:
        m=(i+f)//2
        if x[m]>x[m+1]:
            return x[m]
            
        elif x[m]<x[m-1]:
            return x[m-1]
            
        elif x[m]>xi:
            i=m+1
        else:
            f=m-1
    

def randomfunction(X,N):
    N=N
    X=X
    suma = 0 
    contador = 0 
    while len(X) > 0: 
        elemento = X.popleft() #Hace un pop al inicio de la lista 
        contador += 1 
        if contador % N != 0:
            X.append(elemento)
        else:
            print(elemento)
            print(contador) 
        suma += elemento 
    print(suma)

from bisect import bisect_left
import heapq
a=[24,36,15,36,41,24,24]
b=[24,36,15,36,41,24,24]
heapq.heapify(b)
n=len(a)
a.sort()
for j in range(n):
    z=heapq.heappop(b)
    print(bisect_left(a,z))   