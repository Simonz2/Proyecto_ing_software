from math import pow
pedf=0.99
pf=1/100000
pnf=1-pf
pnednf=0.995
pednf=1-pnednf
pfde=pedf*pf/((pedf*pf)+(pednf*pnf))
pnedf=1-pedf
pnfdne=pnednf*pnf/((pnednf*pnf)+(pnedf*pf))
print(pfde)
print(pnfdne)
