'''
Created on 3 janv. 2018

@author: Sergey
'''
a=0.75
b=0.025
c=0.54
d=0.011

X=c/d
Y=a/b

h=0.01
N=int(90/h)

x=lievres[0]
y=lynx[0]
EulerX=[x]
EulerY=[y]

for k in range(N):
    aux=(1+a*h)*x-b*h*x*y
    y=(1-c*h)*y+d*h*x*y
    x=aux
    EulerX.append(x)
    EulerY.append(y)

Abs=[1845+k*h for k in range(9001)]
pl.plot(Abs,EulerX,color='orange',linewidth=3,label=r"$(t_n,x_n)$ pour $n\in[|0,N|]$")
pl.plot(Abs,EulerY,color='purple',linewidth=3,label=r"$(t_n,y_n)$ pour $n\in[|0,N|]$")
labels=[1845+k for k in range(0,92,2)]
pl.xticks(temps[::2],labels,rotation=45,fontsize=8)

pl.legend(fontsize=12)
pl.title(r"Courbes approchees",fontsize=14)
pl.ylabel("Nombre d'animaux en milliers",fontsize=14)
pl.xlabel("Années",fontsize=14)

pl.figure()
pl.plot(EulerX,EulerY,color="orange",linewidth=2,label=r"Portrait de phase approche de pas $h='+str(h)+'$")
pl.legend(fontsize=12)

pl.plot([X],[Y],'o',color="red",markersize=8)
pl.xlabel("$x(t)$ en milliers",fontsize=14)
pl.ylabel("$x(t)$ en milliers",fontsize=14)
pl.axis("equal")