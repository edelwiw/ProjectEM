import numpy as np 
import math 
import matplotlib.pyplot as plt


# charges = [[[-3, -3], -6], [[-3, 3], 3], [[3, 3], -3], [[2, -3], 3], [[0, 0], 4]]
charges = [[[2, 3], 5], [[2, -3], 3]]
epsilon = 1


x_min = -8
x_max = 8
y_min = -8
y_max = 8

# cast to required format 
for i in range(len(charges)):
    charges[i] = [np.array(charges[i][0]), charges[i][1]]


def vector_from_points(point1, point2):
    return point2 - point1


def vector_length(vec):
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2)


def F(pos): # Coulombs force 
    k = 1 / epsilon 
    force = np.array([0.0, 0.0])

    for i in range(len(charges)): # sum force from each charge 
        x, y, charge = charges[i][0][0], charges[i][0][1], charges[i][1]
        R = vector_from_points(charges[i][0], pos) # vector from charge to test charge 
        if(not vector_length(R)): return np.array([0.0, 0.0]) # to avoid division by zero if point and charge at the same place 
        force += k * charge * R / vector_length(R) ** 3 # Coloumbs law 
    return force 


def pot(pos, charges):
    phi = 0 
    k = 1 / epsilon 
    for i in range(len(charges)): # sum potentian from each charge 
        x, y, charge = charges[i][0][0], charges[i][0][1], charges[i][1]
        R = vector_from_points(charges[i][0], pos) # vector from charge to test charge 
        if(not vector_length(R)): return 0
        phi += k / (4 * 3.14) * charge / vector_length(R)
    return phi


# configure canvas 
figure = plt.figure() 
ax = plt.gca()
ax.set_xlim([x_min, x_max])
ax.set_ylim([y_min, y_max])
ax.set_aspect('equal')

# draw field lines 
for charge in charges: 
    x, y = charge[0] 
    R = 0.01
    for alpha in range(-180, 180, 15): # arrange start point around charge 
        xcurr, ycurr = x + R * math.cos(math.radians(alpha)), y + R * math.sin(math.radians(alpha)) # line start point 
        xpath, ypath = [], []
        for i in range(10000): 
            xpath.append(xcurr)
            ypath.append(ycurr)

            force = F(np.array([xcurr, ycurr])) # find force at point 
            # gradient descent
            xcurr, ycurr = (force / vector_length(force) if vector_length(force) != 0 else 0) * 0.01 + np.array([xcurr, ycurr]) 
        plt.plot(xpath, ypath, color="#d9b555") # draw field line 


xx, yy = np.arange(x_min, x_max, 0.1), np.arange(y_min, y_max, 0.1)
z = np.zeros(shape=(len(yy), len(xx)), dtype=np.double)

# calculate potential at each point 
for i in range(len(xx)):
    for j in range(len(yy)):
        z[j][i] = pot(np.array([xx[i], yy[j]]), charges) 


# plot equipotential lines 
plt.contourf(xx, yy, z, levels=np.linspace(-1, 1, 20)) 

# plot charges 
for charge in charges: 
    x, y = charge[0]
    plt.plot(x, y,'o', color="#FF0000" if charge[1] > 0 else "#0000FF") 


plt.show()