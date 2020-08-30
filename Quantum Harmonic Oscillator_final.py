'''
Created by: Uday Sankar Manoj
            Student SCS NISER,Bhubaneswar,India 
'''

import matplotlib.pyplot as plt
import numpy as np
from math import exp

def F(u,e):#using the equation ddpsi=(u^2-epsilon)*psi
    return u**2-e

def Numrov(x,q0,q1,psi1,f1,dx,eps):# function implementing numerov's algorith
    q2=(dx**2)*f1*psi1+2*q1-q0
    f2=F(x,eps)
    psi2=q2/(1-f2*dx**2/12)
    return q2,f2,psi2

def Numrov2(x,q2,q1,psi1,f1,dx,eps):# function implementing numerov's algorith
    q2=(dx**2)*f1*psi1+2*q1-q0
    f2=F(x,eps)
    psi2=q2/(1-f2*dx**2/12)
    return q2,f2,psi2

def run_eq(X,q,f,psi,eps):#function to find all the psi values
    #print(eps)
    for i in range(len(X)-2):
        x=X[i+1]
        f1=f[-1]
        psi1=psi[-1]
        q1=q[-1]
        q0=q[-2]
        dx=X[i+1]-X[i]
        q2,f2,psi2=Numrov(x,q0,q1,psi1,f1,dx,eps)
        q.append(q2)
        f.append(f2)
        psi.append(psi2)

def run_mult(range_eps):
    data=[]
    for eps in range_eps:
        X,psi,f,q=initials(eps)
        run_eq(X,q,f,psi,eps)
        data.append([X,psi])
    return data


def initials(eps=1,Xmin=-5,Xmax=5,psi_0=1e-30,psi_1=1e-30,div=10**4):
    '''
    Xmin,Xmax=minimum and maximum of the range
    div denotes the number of divisions for X
    '''
    X=np.linspace(Xmin,Xmax,div)
    dx=X[1]-X[0]
    f_0=(X[0]**2-eps)
    f_1=(X[1]**2-eps)
    q_0=psi_0*(1-dx**2*f_0/12)
    q_1=psi_1*(1-dx**2*f_1/12)
    psi=[psi_0,psi_1]
    f=[f_0,f_1]
    q=[q_0,q_1]
    return X,psi,f,q

def initialsBk(eps=1,Xmin=-5,Xmax=5,psi_0=1e-30,psi_1=1e-30,div=10**5):
    '''
    Xmin,Xmax=minimum and maximum of the range
    div denotes the number of divisions for X
    '''
    X=np.linspace(Xmin,Xmax,div)
    X=X[::-1]
    dx=X[1]-X[0]
    f_0=(X[0]**2-eps)
    f_1=(X[1]**2-eps)
    q_0=psi_0*(1-dx**2*f_0/12)
    q_1=psi_1*(1-dx**2*f_1/12)
    psi=[psi_0,psi_1]
    f=[f_0,f_1]
    q=[q_0,q_1]
    return X,psi,f,q

def Eigen_finder2(eps_init,num_steps,div=.1):
    '''
    starts with an eigen values
    in all epsilon corresponding to non iegen energies the psi goes to infinty after 
    the origin.Then find the  fractional difference between the higest point near origin and last value of psi
    Then this function tries to minimize this fractional difference by changing the epsilon. 
    i,e it tries to find a psi which has least value near the end of our range(this our boundary condition)
    '''
    for i in range(num_steps):# an arbitary number of steps
        E_range=[eps_init-div,eps_init,eps_init+div]#Our epsilon range 3 psi values for which we try the plotting
        d=run_mult(E_range)#getting the values
        X=d[0][0]#X is same for all 
        imin=np.where((X>-2) & (X<-1.9))[0][0]# getting the range of indices near origin
        imax=np.where((X>2)&(X<2.1))[0][0]#here our range is (-2,2)
        Grad=[]#array to store the fractional difference
        '''
        Method:
        1) find the fractional differencees for 3 epsilon values
        2)fins the minimum amoung the fractional differences
        3) I .Shifts the epsilon ranges toward the epsilon which gave minimum difference
          II .If the difference is less for the current epsilon the epsilon range 
          is futher divided into more finer intervales
        '''
        for i in range(len(E_range)):
            Y=d[i][1]#psi values are diffrent for different epsilons
            max_psi=max(Y[imin:imax])# The maximum ner origin
            min_psi=abs(min(Y[imin:imax]))
            if min_psi>max_psi:
                max_psi=min_psi
            g=abs(Y[-1]/max_psi)# the maximum
            Grad.append(g)
        if Grad[2]<Grad[0]:# comparing the fractional difference between different epsilons
            if Grad[2]<Grad[1]:# if the fractional difference is lesser for the higher epsilon 
                eps_init=eps_init+div#then shifts epsilon range to higer epsilon
            else:
                div=div/2# if its lest for current epsilon the range is further divided into finer intervals
        else:
            if Grad[0]<Grad[1]:
                eps_init=eps_init-div
            else:
                div=div/2
    return eps_init

def Eigen_Helper(min_e,max_e,int_gap):
    '''
    In this method we divide an interval and get many points in between the interval.
    Then optimize the values to get eigen energies
    '''
    Eps=[]#denotes the array to store possible eigen epsilons
    
    M_ra=np.linspace(min_e,max_e,int_gap)#the main range
    for i in range(len(M_ra)):
        print("Initail Guess->",M_ra[i])
        C=True
        eps=Eigen_finder2(M_ra[i],15)#optimizing to get eigen epsilons
        eps=round(eps,2)
        for j in range(len(Eps)):# to avoid repetition of eigen values
            if Eps[j]==eps:
                C=False
        if C:
            Eps.append(eps)
        print("Correct eigen value after optimizing->",eps)
    return Eps

def Normalize(x,y,norml_Val=1):#function to normalize the function
    '''
    UDX->uniformly descretized x axis
    this means that x axis is uniformly divided hence the interval between any 2 consecutieve points 
    in X axis is same.
    '''
    A=0
    for i in range(len(x)-1):
        dx=(x[i+1]-x[i])
        a=abs(dx*(y[i]+y[i+1])/2)
        A=A+a
    norm_y=y/A
    return norm_y

def Run_both(eps=1,Xmin=-10,Xmax=10,psi_0=1e-30,psi_1=1e-30,div=10**4):
    '''
    This function splirts the x axis into two and runs two function one from negative till x=0
    another from positive.
    xmin has to be a negatieve number and Xmax a positieve number, othewise this step donot work
    This gives a functiojn which satisfies boundary condition irrespective of the eigen value
    So FOR SOLVING EIGEN VALUES THIS FUNCTION SHOULD NOT BE USED
    '''
    X,psi,f,q=initials(eps,Xmin,Xmax,psi_0,psi_1,div)
    X_b,psi_b,f_b,q_b=initialsBk(eps,Xmin,Xmax,psi_0,psi_1,div)
    run_eq(X,q,f,psi,eps)
    run_eq(X_b,q_b,f_b,psi_b,eps)
    N_psi=Merger(X,psi,X_b,psi_b)
    return X,N_psi
   
def Merger(X,psi,X_b,psi_b):
    '''
    Given the both forward and backward solution this function merges both of them together.
    An explotion near the end of the forward. othewise this tep is not needed 
    X_b starts from 10 till -10(towards negatieve direction)
    '''
    psi_b=np.copy(psi_b[::-1])
    psi_m=np.copy(psi)# the final merged psi 
    last_min=0#stores the postion of last minimum in the psi array this indicates the minimum before the explotion
    for p in range(len(psi)-2):
        if abs(psi_m[p])>abs(psi_m[p+1]):  
            if abs(psi_m[p+1])<abs(psi_m[p+2]):
                last_min=p+1   
    psi_m[last_min:]=psi_b[last_min:]#merging both of them
    psi_n=Normalize(X,psi_m)
    return psi_n

def Plot_Eq(E_range,Xmin=-10,Xmax=10):
    print(E_range)
    for e in E_range:
        x,Psi=Run_both(e,Xmin,Xmax)
        plt.legend()
        print(e)
        ax.plot(x,Psi+e,label=e)

int_gap=10
EPS=Eigen_Helper(1,10,int_gap)

X=np.linspace(-10,10,10**3)
fig=plt.figure()
ax=plt.axes(ylim=(0,12))
ax.set_title("Solution for Quantum Harmonic Oscilator")
ax.plot(X,F(X,0))
Plot_Eq(EPS)
ax.legend()
plt.show()

h=6.63e-34
w=1
i=1
for e in EPS:
    print(f"Eigent energy {i}=",e*h*w/2)
    i+=1
