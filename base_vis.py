from base import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

base = Base(3,2,1)

ax = plt.figure().add_subplot(projection='3d')

ax.set_xlim(-5,5)
ax.set_ylim(-5,5)
ax.set_zlim(-5,5)

plt.title("Base Simulation")

for servo in base.get_servos():
    ax.quiver(0,0,0, servo.radius[0], servo.radius[1], servo.radius[2], color = "b")
    ax.quiver(servo.radius[0], servo.radius[1], servo.radius[2], servo.height[0], servo.height[1], servo.height[2], color = "g")

    start1 = servo.radius[0] + servo.height[0]
    start2 = servo.radius[1] + servo.height[1]
    start3 = servo.radius[2] + servo.height[2]
    ax.quiver(start1, start2, start3, servo.horn[0], servo.horn[1], servo.horn[2], color = "orange")


plt.show()
