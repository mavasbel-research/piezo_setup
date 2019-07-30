import matlab.engine
import numpy as np

eng = matlab.engine.connect_matlab()

# Examples
# Executing function
tf = eng.isprime(37) 
print(tf)
# eng.run('CreateWeightFunc.m', nargout=0)

# Access variable from workspace
# ans = eng.workspace['ans']
# weightFun = eng.workspace['weightFunc']

#Create variable in workspace
# eng.workspace['testVar'] = [[1,2,3,4,5,6],[2,3,4,5,6,7]]

pass