# APODE

Este documento muestra la funcionalidad actual del paquete apode. El mismo provee una clase que hereda (pendiente) de la clase DataFrame.

Esta clase dispone de varios métodos que calculan medidas y generan gráficos en los siguuinetes temas:

* Pobreza
* Desigualdad
* Bienestar
* Polarización
* Concentración

Otros temas serán agregados más adelante.

Al momento los algoritmos no han sido testeados y es escasa la documentación. 

# Clase IneqMeasure

Los objetos se crean mediante:

    df = IneqMeasure(data, varx=None, weight=None, issorted=False):
    
Métodos para acceder/modificar atributos:

    df.data
    df.varx
    df.weight
    df.issorted
    df.sort()
    
Métodos sobre el dataframe:

    df.describe()
    df.columns()
    df.ndim()
    df.shape()
    df.size()
    df.display()

Metodos que calculan indicadores:
   
    df.poverty(method,*args)    
    df.tip(*args)
    df.ineq(method,*args)
    df.lorenz(*args)
    df.welfare(method,*args) 
    df.polar(method,*args)
    df.conc(method,*args)
 




```python
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import pandas as pd

from apode import IneqMeasure # clase
from apode import distribution_examples,joinpar # test
```

# Generar datos

* Los datos pueden generarse manualmente o mediante simuación. Estan contenidos en un DataFrame
* Los datos pueden estar agrupados. En este caso una variable contiene las frecuencias.
* Pueden existir otras variables categóricas que permiten aplicar los indicadores por grupos (groupby)
* Un parámetros indica si los datos están ordenados (por defecto no)

    

## Carga manual

Se puede crear objeto desde un DataFrame o desde un argumento válido de la funcion DataFrame. La función *binning* se puede usar para agrupar datos.


```python
# dr1a y dr1b son equivalentes
x = [23, 10, 12, 21, 4, 8, 19, 15, 11, 9]
dr1a = IneqMeasure(x) 

df1 = pd.DataFrame({'x':x})
dr1b = IneqMeasure(df1) 

dr1b.display()
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>23</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10</td>
    </tr>
    <tr>
      <th>2</th>
      <td>12</td>
    </tr>
    <tr>
      <th>3</th>
      <td>21</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
    </tr>
    <tr>
      <th>5</th>
      <td>8</td>
    </tr>
    <tr>
      <th>6</th>
      <td>19</td>
    </tr>
    <tr>
      <th>7</th>
      <td>15</td>
    </tr>
    <tr>
      <th>8</th>
      <td>11</td>
    </tr>
    <tr>
      <th>9</th>
      <td>9</td>
    </tr>
  </tbody>
</table>
</div>


## Lectura desde la web

Falta de implementar. 

## Simulación 

La función *distribution_examples* brinda algunos ejemplos de distribuciones usuales para modelar la distribución del ingreso.

Se generan dos objetos (datos agrupados y no agrupados) que serán utilizados más adelante para mostrar la aplicación de diferentes medidas (muchos de las medidas aún no estan implementadas para datos agrupados).

### Datos no agregados


```python
# Generar datos
n = 1000 # observaciones
j_d = 6  # elegir distribción
listd = ['uniform','lognormal','exponential','pareto','chisquare','gamma','weibull']
fdistr = listd[j_d]
df2 = distribution_examples(fdistr,n)

# Crear objeto (sin agrupamiento)
dr2 = IneqMeasure(df2) 

# Graficar distribución
sns.distplot(df2).set_title(fdistr)
plt.show()
```


![png](output_6_0.png)


### Datos agregados


```python
# Generar datos con agrupamiento
nbins = 10 # maximo, se descartan NAN
df3 = distribution_examples(fdistr,n,nbins)

# Crear objeto
dr3 = IneqMeasure(df3,varx = 'x',weight='weight')  

dr3.display()
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>weight</th>
      <th>x</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>181</td>
      <td>18.911842</td>
    </tr>
    <tr>
      <th>1</th>
      <td>257</td>
      <td>51.151646</td>
    </tr>
    <tr>
      <th>2</th>
      <td>213</td>
      <td>84.566546</td>
    </tr>
    <tr>
      <th>3</th>
      <td>155</td>
      <td>118.095719</td>
    </tr>
    <tr>
      <th>4</th>
      <td>88</td>
      <td>153.008449</td>
    </tr>
    <tr>
      <th>5</th>
      <td>47</td>
      <td>182.722287</td>
    </tr>
    <tr>
      <th>6</th>
      <td>31</td>
      <td>220.953474</td>
    </tr>
    <tr>
      <th>7</th>
      <td>16</td>
      <td>257.621040</td>
    </tr>
    <tr>
      <th>8</th>
      <td>8</td>
      <td>279.644214</td>
    </tr>
    <tr>
      <th>9</th>
      <td>4</td>
      <td>328.825513</td>
    </tr>
  </tbody>
</table>
</div>


La variable x y el ponderador se pueden modificar luego de crear el objeto (mientras estén presentes en el dataframe)

# Data description

El método **describe** extiende la función describe de DataFrame, para incluir parámetros y tratar el caso de datos agrupados


```python
dr1b.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>weight</th>
      <td>False</td>
    </tr>
    <tr>
      <th>bins</th>
      <td>10</td>
    </tr>
    <tr>
      <th>sorted</th>
      <td>False</td>
    </tr>
    <tr>
      <th>count</th>
      <td>10</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>13.2</td>
    </tr>
    <tr>
      <th>std</th>
      <td>6.14275</td>
    </tr>
    <tr>
      <th>min</th>
      <td>4</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>9.25</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>11.5</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>18</td>
    </tr>
    <tr>
      <th>max</th>
      <td>23</td>
    </tr>
  </tbody>
</table>
</div>




```python
dr3.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>weight</th>
      <td>True</td>
    </tr>
    <tr>
      <th>bins</th>
      <td>10</td>
    </tr>
    <tr>
      <th>sorted</th>
      <td>False</td>
    </tr>
    <tr>
      <th>count</th>
      <td>1000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>89.4632</td>
    </tr>
    <tr>
      <th>min</th>
      <td>18.9118</td>
    </tr>
    <tr>
      <th>max</th>
      <td>328.826</td>
    </tr>
  </tbody>
</table>
</div>



Otros métodos:


```python
dr3.columns()
```




    ['weight', 'x']




```python
dr3.shape(),dr3.ndim(),dr3.size()  # requieren parentesis en la invocacion
```




    ((10, 2), 2, 20)



# Poverty

EStán implementados 11 medidas de pobreza y la curva TIP (permite comparar gráficamente la pobreza entre distribuciones)


```python
pline = 50 # Poverty line
# Evaluar un método - datos sin agrupar
p = dr2.poverty('fgt0',pline)
p
```




    0.294




```python
# Evaluar un método - datos agrupados
p = dr3.poverty('fgt0',pline)
p
```




    0.181




```python
# Evaluar un listado de métodos
mlist_p = ['fgt0','fgt1','fgt2',['fgt',1.5],'sen','sst','watts',['cuh',0],['cuh',0.5],'takayama','kakwani','thon',['bd',2],'hagenaars',['chakravarty',0.5 ]]
mlist_p2 = [joinpar(x,pline) for x in mlist_p ]
table = []
for elem in mlist_p2:   
    table.append(dr2.poverty(elem[0],*elem[1:]))
df_outp =  pd.DataFrame(mlist_p2,columns = ['method','pline','par'])  
df_outp['poverty_measure'] = table
df_outp
```

    D:\GitHub\apode\apode\poverty.py:76: RuntimeWarning: overflow encountered in int_scalars
      p = (q/(n*pline*a))*u
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>method</th>
      <th>pline</th>
      <th>par</th>
      <th>poverty_measure</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>fgt0</td>
      <td>50</td>
      <td>NaN</td>
      <td>0.294000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>fgt1</td>
      <td>50</td>
      <td>NaN</td>
      <td>0.132876</td>
    </tr>
    <tr>
      <th>2</th>
      <td>fgt2</td>
      <td>50</td>
      <td>NaN</td>
      <td>0.078541</td>
    </tr>
    <tr>
      <th>3</th>
      <td>fgt</td>
      <td>50</td>
      <td>1.5</td>
      <td>0.100014</td>
    </tr>
    <tr>
      <th>4</th>
      <td>sen</td>
      <td>50</td>
      <td>NaN</td>
      <td>0.174214</td>
    </tr>
    <tr>
      <th>5</th>
      <td>sst</td>
      <td>50</td>
      <td>NaN</td>
      <td>0.049088</td>
    </tr>
    <tr>
      <th>6</th>
      <td>watts</td>
      <td>50</td>
      <td>NaN</td>
      <td>0.223284</td>
    </tr>
    <tr>
      <th>7</th>
      <td>cuh</td>
      <td>50</td>
      <td>0.0</td>
      <td>0.205619</td>
    </tr>
    <tr>
      <th>8</th>
      <td>cuh</td>
      <td>50</td>
      <td>0.5</td>
      <td>0.160156</td>
    </tr>
    <tr>
      <th>9</th>
      <td>takayama</td>
      <td>50</td>
      <td>NaN</td>
      <td>0.120573</td>
    </tr>
    <tr>
      <th>10</th>
      <td>kakwani</td>
      <td>50</td>
      <td>NaN</td>
      <td>133.524319</td>
    </tr>
    <tr>
      <th>11</th>
      <td>thon</td>
      <td>50</td>
      <td>NaN</td>
      <td>0.239322</td>
    </tr>
    <tr>
      <th>12</th>
      <td>bd</td>
      <td>50</td>
      <td>2.0</td>
      <td>-796.161273</td>
    </tr>
    <tr>
      <th>13</th>
      <td>hagenaars</td>
      <td>50</td>
      <td>NaN</td>
      <td>0.057076</td>
    </tr>
    <tr>
      <th>14</th>
      <td>chakravarty</td>
      <td>50</td>
      <td>0.5</td>
      <td>0.083570</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Curva TIP
df_tip = dr2.tip(pline)
```


![png](output_20_0.png)


# Inequality

Están implementadas 12 medidas de desigualdad y la Curva de Lorenz (permite comparar gráficamente la desigualdad entre distribuciones)


```python
# Evaluar un método - datos sin agrupar
q = dr2.ineq('gini')
q
```




    0.37306848835818096




```python
# Evaluar un método - datos agrupados
q = dr3.ineq('rr')
q
```




    3.4641481722739518




```python
# Evaluar una lista de métodos
list_i = ['rr','dmr','cv','dslog','gini','merhan','piesch','bonferroni',['kolm',0.5],['ratio',0.05],['ratio',0.2], \
          ['entropy',0],['entropy',1],['entropy',2],['atkinson',0.5],['atkinson',1],['atkinson',2]]
list_i = [[elem] if not isinstance(elem,list) else elem for elem in list_i]
table = []
for elem in list_i:   
    table.append(dr2.ineq(*elem))
dz_i =  pd.DataFrame(list_i,columns = ['method','par'])  
dz_i['ineq_measure'] = table
dz_i
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>method</th>
      <th>par</th>
      <th>ineq_measure</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>rr</td>
      <td>NaN</td>
      <td>4.720396</td>
    </tr>
    <tr>
      <th>1</th>
      <td>dmr</td>
      <td>NaN</td>
      <td>0.271119</td>
    </tr>
    <tr>
      <th>2</th>
      <td>cv</td>
      <td>NaN</td>
      <td>0.692086</td>
    </tr>
    <tr>
      <th>3</th>
      <td>dslog</td>
      <td>NaN</td>
      <td>0.900626</td>
    </tr>
    <tr>
      <th>4</th>
      <td>gini</td>
      <td>NaN</td>
      <td>0.373068</td>
    </tr>
    <tr>
      <th>5</th>
      <td>merhan</td>
      <td>NaN</td>
      <td>0.523238</td>
    </tr>
    <tr>
      <th>6</th>
      <td>piesch</td>
      <td>NaN</td>
      <td>0.297987</td>
    </tr>
    <tr>
      <th>7</th>
      <td>bonferroni</td>
      <td>NaN</td>
      <td>0.519042</td>
    </tr>
    <tr>
      <th>8</th>
      <td>kolm</td>
      <td>0.50</td>
      <td>78.258822</td>
    </tr>
    <tr>
      <th>9</th>
      <td>ratio</td>
      <td>0.05</td>
      <td>0.033960</td>
    </tr>
    <tr>
      <th>10</th>
      <td>ratio</td>
      <td>0.20</td>
      <td>0.109733</td>
    </tr>
    <tr>
      <th>11</th>
      <td>entropy</td>
      <td>0.00</td>
      <td>0.287383</td>
    </tr>
    <tr>
      <th>12</th>
      <td>entropy</td>
      <td>1.00</td>
      <td>0.229951</td>
    </tr>
    <tr>
      <th>13</th>
      <td>entropy</td>
      <td>2.00</td>
      <td>0.239492</td>
    </tr>
    <tr>
      <th>14</th>
      <td>atkinson</td>
      <td>0.50</td>
      <td>-79104.684217</td>
    </tr>
    <tr>
      <th>15</th>
      <td>atkinson</td>
      <td>1.00</td>
      <td>-67399.687185</td>
    </tr>
    <tr>
      <th>16</th>
      <td>atkinson</td>
      <td>2.00</td>
      <td>-40205.624705</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Curva de Lorenz
df_lor = dr2.lorenz()
```


![png](output_25_0.png)


# Welfare

Están implementadas 5 funciones de bienestar social.


```python
# Evaluar un método - datos sin agrupar
w = dr2.welfare('sen')
w
```




    56.3243476802907




```python
# Evaluar un método - datos agrupados
w = dr3.welfare('utilitarian')
w
```




    89.46316830250787




```python
# Lista de indicadores
list_w = ['utilitarian','rawlsian','sen','theill','theilt',['isoelastic',0],['isoelastic',1],['isoelastic',2],['isoelastic',np.Inf]]
list_w = [[elem] if not isinstance(elem,list) else elem for elem in list_w]
table = []
for elem in list_w:   
    table.append(dr2.welfare(*elem))
dz_w =  pd.DataFrame(list_w,columns = ['method','par'])  
dz_w['welfare_measure'] = table
dz_w     
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>method</th>
      <th>par</th>
      <th>welfare_measure</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>utilitarian</td>
      <td>NaN</td>
      <td>89.840736</td>
    </tr>
    <tr>
      <th>1</th>
      <td>rawlsian</td>
      <td>NaN</td>
      <td>0.619402</td>
    </tr>
    <tr>
      <th>2</th>
      <td>sen</td>
      <td>NaN</td>
      <td>56.324348</td>
    </tr>
    <tr>
      <th>3</th>
      <td>theill</td>
      <td>NaN</td>
      <td>67.400687</td>
    </tr>
    <tr>
      <th>4</th>
      <td>theilt</td>
      <td>NaN</td>
      <td>71.385011</td>
    </tr>
    <tr>
      <th>5</th>
      <td>isoelastic</td>
      <td>0.0</td>
      <td>89.840736</td>
    </tr>
    <tr>
      <th>6</th>
      <td>isoelastic</td>
      <td>1.0</td>
      <td>4.210655</td>
    </tr>
    <tr>
      <th>7</th>
      <td>isoelastic</td>
      <td>2.0</td>
      <td>-0.024872</td>
    </tr>
    <tr>
      <th>8</th>
      <td>isoelastic</td>
      <td>inf</td>
      <td>0.619402</td>
    </tr>
  </tbody>
</table>
</div>



# Polarization 

Están implementados 2 medidas de polarización.


```python
# Evaluar un método - datos sin agrupar
p = dr2.polar('er')
p
```




    0.06739213923133214




```python
# lista de indicadores
list_pz = ['er','wlf']
table = []
for elem in list_pz:   
    table.append(dr2.polar(elem))
dz_pz =  pd.DataFrame(list_pz,columns = ['method'])  
dz_pz['polarization_measure'] = table
dz_pz
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>method</th>
      <th>polarization_measure</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>er</td>
      <td>0.067392</td>
    </tr>
    <tr>
      <th>1</th>
      <td>wlf</td>
      <td>-0.127073</td>
    </tr>
  </tbody>
</table>
</div>



# Concentration

Están implementadas 4 medidas de concentración (de uso comun para analizar la concentración industrial).


```python
# Evaluar un método - datos sin agrupar
c = dr2.conc('hhi')
c
```




    0.0014789830846348713




```python
# lista de indicadores
list_c = ['hhi','hhin','rosenbluth',['cr',1],['cr',5]]
list_c = [[elem] if not isinstance(elem,list) else elem for elem in list_c]
table = []
for elem in list_c:   
    table.append(dr2.conc(*elem))
dz_c =  pd.DataFrame(list_c,columns = ['method','par'])  
dz_c['concentration_measure'] = table
dz_c     
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>method</th>
      <th>par</th>
      <th>concentration_measure</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>hhi</td>
      <td>NaN</td>
      <td>0.001479</td>
    </tr>
    <tr>
      <th>1</th>
      <td>hhin</td>
      <td>NaN</td>
      <td>0.000479</td>
    </tr>
    <tr>
      <th>2</th>
      <td>rosenbluth</td>
      <td>NaN</td>
      <td>0.001595</td>
    </tr>
    <tr>
      <th>3</th>
      <td>cr</td>
      <td>1.0</td>
      <td>0.004727</td>
    </tr>
    <tr>
      <th>4</th>
      <td>cr</td>
      <td>5.0</td>
      <td>0.019833</td>
    </tr>
  </tbody>
</table>
</div>



# Decomposition

Los medidas pueden aplicarse por subrgrupos de acuerdo a cierta categoría. Por ejemplo:


```python
x = [23, 10, 12, 21, 4, 8, 19, 15, 5, 7]
y = [10,10,20,10,10,20,20,20,10,10] 
w = np.arange(1,11)
dfa = pd.DataFrame({'x':x,'y':y,'w':w})
dra = IneqMeasure(dfa,varx='x',weight='w')  
dra.display()
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x</th>
      <th>y</th>
      <th>w</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>23</td>
      <td>10</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10</td>
      <td>10</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>12</td>
      <td>20</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>21</td>
      <td>10</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>10</td>
      <td>5</td>
    </tr>
    <tr>
      <th>5</th>
      <td>8</td>
      <td>20</td>
      <td>6</td>
    </tr>
    <tr>
      <th>6</th>
      <td>19</td>
      <td>20</td>
      <td>7</td>
    </tr>
    <tr>
      <th>7</th>
      <td>15</td>
      <td>20</td>
      <td>8</td>
    </tr>
    <tr>
      <th>8</th>
      <td>5</td>
      <td>10</td>
      <td>9</td>
    </tr>
    <tr>
      <th>9</th>
      <td>7</td>
      <td>10</td>
      <td>10</td>
    </tr>
  </tbody>
</table>
</div>



```python
# calculo simple
pline = 11
p1 = dra.poverty('fgt0',pline)
p1
```




    0.5818181818181818




```python
# calculo por grupos según variable "y"
p2 = dra.poverty('fgt0',pline,gby='y')
p2
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x_measure</th>
      <th>x_weight</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>10</th>
      <td>0.83871</td>
      <td>31</td>
    </tr>
    <tr>
      <th>20</th>
      <td>0.25000</td>
      <td>24</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Si el indicador es descomponible se obtiene el mismo resultado:
p2_p = sum(p2['x_measure']*p2['x_weight']/sum(p2['x_weight']))
p2_p
```




    0.5818181818181818



# Pendiente


**En algoritmos falta (implementación):**

* Tamaño nulo del dataframe
* Division por cero (/log(1))
* overflow
* Tratamiento de missings
* implementación eficiente (algunos son lentos: polarizacion)
* mejorar algunos nombres
* Hay metodos que tienen varios nombres o que pueden estar en diferentes categorías. Ver si agregar redundancia.
* Curva de lorenz generalizada
* random (cambiar generador)


**En algoritmos (análisis):**

* Intervalos de confianza
* comparación de distribuciones (impacto de políticas, etc)


**En test:**

* Comparar resultados con librerias de R

# Otras Implementaciones

Relevantes para el dearrollo de los test.

**Python**

- http://www.poorcity.richcity.org/oei/  (algoritmos)
- https://github.com/mmngreco/IneqPy
- https://pythonhosted.org/IneqPy/ineqpy.html
- https://github.com/open-risk/concentrationMetrics

**R**

- https://cran.r-project.org/web/packages/ineq/ineq.pdf
- https://cran.r-project.org/web/packages/affluenceIndex/affluenceIndex.pdf
- https://cran.r-project.org/web/packages/dineq/dineq.pdf
- https://github.com/PABalland/EconGeo
- https://cran.r-project.org/web/packages/rtip/rtip.pdf

**Stata**

- https://www.stata.com/manuals/rinequality.pdf
- http://dasp.ecn.ulaval.ca/dmodules/madds20.htm


# Referencias

* F A Cowell: Measuring Inequality, 1995 Prentice Hall
* Handbook on Poverty and Inequality. https://openknowledge.worldbank.org/bitstream/handle/10986/11985/9780821376133.pdf
* POBREZA Y DESIGUALDAD EN AMÉRICA LATINA. https://www.cedlas.econo.unlp.edu.ar/wp/wp-content/uploads/Pobreza_desigualdad_-America_Latina.pdf
* https://www.cepal.org/es/publicaciones/4740-enfoques-la-medicion-la-pobreza-breve-revision-la-literatura
* https://www.cepal.org/es/publicaciones/4788-consideraciones-indice-gini-medir-la-concentracion-ingreso



