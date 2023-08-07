#======================Bibliotecas Necessárias====================================================
import numpy as np
import sympy as sy
from sympy import solve,log
import math as mt
from scipy.special import lambertw
import numpy as np
import pandas as pd
import streamlit as st
sy.init_printing(scale=0.1,forecolor='black')
r = sy.Symbol('r')
x = sy.Symbol("x")

#======================Definindo Funções do Problema===============================================
#Definindo Potencial 
def pot_ef(r,M,l):
    p = -6.00*M/(pow(r,3))
    V = (1.00 - (2.00*M)/r)*((l*(l+1.00)/(pow(r,2))) + p) 
    return V
#Coordenada Tortoise
def Turtle(r,M):
    return r+2.00*M*sy.log(r/(2*M)-1.00)
#Inversa de r 
def inv(x,M):
    eq = Turtle(r,M)-x
    resultado = solve(eq,r)[1]
    resultado = sy.simplify(resultado)
    return resultado
#Potencial Definido em r*
def pot_ef_Turtose(inversa,M,l,x):
    r_t = inversa
    Valor_Pot = pot_ef(r_t,M,l)
    return sy.simplify(Valor_Pot)

#=======================Definindo Funções para Cálculo de Derivada======================================
def DerivadaPrimeira(Potencial,x):
    return sy.diff(Potencial,x,1)
def DerivadaSegunda(Potencial,x):
    return sy.diff(Potencial,x,2)
def DerivadaTerceira(Potencial,x):
    return sy.diff(Potencial,x,3)
def DerivadaQuarta(Potencial,x):
    return sy.diff(Potencial,x,4)
def DerivadaQuinta(Potencial,x):
    return sy.diff(Potencial,x,5)
def DerivadaSexta(Potencial,x):
    return sy.diff(Potencial,x,6)

#==========================Definindo Funções para o Cálculo dos Modos====================================
def Delta(r,M,l,dr4,dr2,dr3,n):
    alpha = n + 0.5
    P_1_1 = dr4/dr2
    P_1_2 = 0.25 + pow(alpha,2)
    Parcela_1 = (1/8)*(P_1_1)*(P_1_2)
    P_2_1 = pow(dr3/dr2,2)
    P_2_2 = 7.00+60.00*(pow(alpha,2))
    Parcela_2 = (1/288)*(P_2_1)*(P_2_2)
    Delta_valor = Parcela_1-Parcela_2
    return  Delta_valor
def Omega(r,M,l,dr2,dr3,dr4,dr5,dr6,n):
    alpha = n + 0.5
    #Calculando componentes do Omega
    p_1_1 = pow(dr3/dr2,4)
    p_1_2 = 77.00+188.00*(pow(alpha,2))
    Parcela_1 =  (5/6912)*(p_1_1)*(p_1_1)
    p_2_1 = pow(dr3,2)
    p_2_2 = pow(dr2,3)
    p_2_3 = 51.00 + 100.00*pow(alpha,2)
    Parcela_2 = (1/384)*((dr4*p_2_1)/(p_2_2))*(p_2_3)
    p_3_1 = pow(dr4/dr2,2)
    p_3_2 = 65.00 +68.00*pow(alpha,2)
    Parcela_3 = (1/2304)*(p_3_1)*(p_3_2)
    p_4_1 = dr3*dr5
    p_4_2 = pow(dr2,2)
    p_4_3 = 19.00 + 28.00*pow(alpha,2)
    Parcela_4 = (1/288)*(p_4_1/(p_4_2))*(p_4_3)
    p_5_1 = dr6/dr2
    p_5_2 = 5.00 + 4.00*pow(alpha,2)
    Parcela_5 = (1/288)*(p_5_1)*(p_5_2)
    Omega_1 = 1/(-2.00*dr2)
    Valor_Omega = (Omega_1)*(Parcela_1-Parcela_2+Parcela_3 + Parcela_4-Parcela_5)
    return Valor_Omega
def ModosQuaseNormais(Potencial1,x0,n,l,Delta1,Omega1,dr2_1):
    alpha = n + 0.5
    Potencial_0 = Potencial1
    Parte_1_1 = pow(-2.00*dr2_1,0.5)
    Parte_1 = Potencial_0 + Delta1
    Parte_2_1 = pow(-2.00*dr2_1,0.5) 
    Parte_2 = -1j*(alpha)*(Parte_2_1)*(1.00+Omega1)
    Frequencia = np.array([Parte_1.subs(x,x0),Parte_2.subs(x,x0)])
    return Frequencia  
#Definindo Função Principal para Determinar Módulos
def Main(n,l,M):
    Potencial = pot_ef(r,M,l)
    Derivada_primeira = DerivadaPrimeira(Potencial,r)
    pontos_criticos = solve(Derivada_primeira,r)
    ponto_max = pontos_criticos[1]
    x0  = Turtle(r,M).subs(r,ponto_max)
    inversa = inv(x,M)
    Potencial = pot_ef_Turtose(inversa,M,l,x)
    Potencial1 = (pot_ef_Turtose(inversa,M,l,x)).subs(x,x0)
    #Calculando derivada no ponto dado
    dr1 = (DerivadaPrimeira(Potencial,x))
    dr2 =  (DerivadaSegunda(Potencial,x))
    dr3 = (DerivadaTerceira(Potencial,x))
    dr4 = (DerivadaQuarta(Potencial,x))
    dr5 = (DerivadaQuinta(Potencial,x))
    dr6 = (DerivadaSexta(Potencial,x))
    dr22 = (DerivadaSegunda(Potencial,x)).subs(x,x0)
    Omega1 = (Omega(x,M,l,dr2,dr3,dr4,dr5,dr6,n))
    Delta1 =(Delta(x,M,l,dr4,dr2,dr3,n))
    w =  (ModosQuaseNormais(Potencial1,x0,n,l,Delta1,Omega1,dr2))
    a = w[0]
    b = w[1]
    if type(a) is sy.core.numbers.Float:
        b = w[1]/1j
    else:
        a = w[0]/1j
    modulo = ((a**2)+(b**2))**(0.5)
    cosseno = a/modulo
    sen = b/modulo
    tg = b/a
    theta = mt.atan(tg)
    w1 = (modulo**0.5)*(np.cos(0.5*theta)+ 1j*np.sin(0.5*theta))
    return w1

#Input do Método 
st.header("APLICAÇÃO WEB PARA CÁLCULO DE MODOS QUASINORMAIS DE BURACOS NEGROS")
M = st.number_input('Digite o Valor da Massa do Buraco Negro : ')
n = st.slider("Selecione a quantidade de valores de n desejada : ")
Modos_Trabalho = pd.DataFrame()
indice_n = []
indice_l = []
indice_z = []
coluna1 = []
coluna_2 = []
if n  is not 0:
    st.write("A Quantidade de valores de n é ", n)
    for q in range(0,n):
        indice_n.append(q)
l = st.slider("Selecione a quantidade de valores de l desejada : ")
if l is not  0:
    st.write("A Quantidade de valores de l é ", l)
    for p in range(2,l+2):
        indice_l.append(p)
    for i in indice_n:
        for j in indice_l:
            coluna1.append(i)
            coluna2.apppend(j)
            indice_z.append(Main(i,j,M))
    Modos_Trabalho['n'] =  coluna1
    Modos_Trabalho['l'] =  coluna2
    #Modos_Trabalho['z'] = [indice_z]
if len(Modos_Trabalho)!=0:
    st.dataframe(Modos_Trabalho) 
    






