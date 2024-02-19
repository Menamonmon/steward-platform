from vector_operations import *

class Servo:
	def __init__(self, servo_angle, servo_radius, servo_height, servo_horn):
		self.servo_angle = servo_angle
		self.servo_radius = servo_radius
		self.servo_height = servo_height
		self.servo_horn = servo_horn

		self.radius = np.array([self.servo_radius, 0, 0])
		self.radius = R_z(self.radius, self.servo_angle)

		self.height = np.array([0, 0, self.servo_height])
		self.horn = np.array([self.servo_horn, 0, 0])
		self.horn = R_z(self.horn, self.servo_angle)

		self.horn_end = self.radius + self.height + self.horn

	def rotate(self, alpha):
		self.horn = np.array([self.servo_horn, 0, 0])
		self.horn = R_z(self.horn, self.servo_angle)
		if self.servo_angle == 0:
			self.horn = R_y(self.horn, -alpha)
		elif self.servo_angle == np.pi/2:
			self.horn = R_x(self.horn, alpha)
		elif self.servo_angle == np.pi:
			self.horn = R_y(self.horn, alpha)
		elif self.servo_angle == 3*np.pi/2:
			self.horn = R_x(self.horn, -alpha)

		self.horn_end = self.radius + self.height + self.horn


	def get_horn_end(self):
		return self.horn_end
	
	def get_horn_pivot(self):
		return self.radius + self.height

   
class Base: 
	def __init__(self, servo_radius, servo_height, servo_horn):
		self.servo_radius = servo_radius
		self.servo_height = servo_height
		self.servo_horn = servo_horn
		self.servos_list = []
		for i in range(4):
			self.servos_list.append(Servo(i*(np.pi/2), self.servo_radius, self.servo_height, self.servo_horn))

	def get_servos(self):
		return self.servos_list

	def rotate_servos(self, alpha_0, alpha_1, alpha_2, alpha_3):
		angles = [alpha_0, alpha_1, alpha_2, alpha_3]
		for i in range(len(self.servos_list)):
			self.servos_list[i].rotate(angles[i])

	def get_horn_ends(self):
		positions = []
		for i in self.servos_list:
			positions.append(i.get_horn_end())
		return np.array(positions)

	def get_horn_pivots(self):
		positions = []
		for i in self.servos_list:
			positions.append(i.get_horn_pivot())
		return np.array(positions)


	def vis_servos(self, ax):
		for servo in self.servos_list:
			ax.quiver(0, 0, 0, *servo.radius, color='r')
			ax.quiver(*servo.radius, *servo.height, color='g')
			ax.quiver(*servo.get_horn_pivot(), *servo.horn, color='y')
