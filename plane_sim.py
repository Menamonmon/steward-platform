import numpy as np
from matplotlib import pyplot as plt
from vector_operations import R_v, pairwise_batch_cosine_sim_cal

# plane will 4 points representing 
	
class TopPlane:
	def __init__(self, arm_length, hand_length, plane_height, plane_radius, initial_plane_orientation=np.array([0, 0, 1])):
		self.arm_length = arm_length
		self.hand_length = hand_length
		self.plane_radius = plane_radius
		self.plane_height = plane_height
		self.reinit(initial_plane_orientation)

	def get_plane_joints(self):
		a, _, c = self.orientation

		h1 = np.array([c, 0, -a]) # vector perpendicular to the plane on positive x axis

		self.h_vec = self.plane_height * np.array([0, 0, 1])
		h1 = self.plane_radius * h1 / np.linalg.norm(h1)
		planar_directions = np.array([R_v(self.orientation, h1, i * np.pi/2) for i in range(4)])
		plane_joints = np.array([x + self.h_vec for x in planar_directions])
		# normalize planar direction
		planar_directions = np.array([x / np.linalg.norm(x) for x in planar_directions])
		return plane_joints, planar_directions

	def reinit(self, orientation):
		orientation_mag = np.linalg.norm(orientation)

		# Normalized normal vector representing the orientation of the plane
		self.orientation = orientation / orientation_mag
		self.plane_joints, self.planar_directions = self.get_plane_joints()
	
	def get_hand_ends(self):
		return self.plane_joints + self.get_isolated_hands()
	
	def get_hand_starts(self):
		return self.plane_joints

	def get_isolated_hands(self):
		return self.hand_length * self.planar_directions
	
	def update_orientation(self, goal_orientation, base):
		plane = self
		plane.reinit(goal_orientation)
		g = plane.get_hand_starts() - base.get_horn_pivots()
		hd = plane.get_isolated_hands()
		D = g + hd
		x = np.arccos(np.diag(pairwise_batch_cosine_sim_cal(g, D)))
		D_scal = np.linalg.norm(D, axis=1)
		b, a, c = np.repeat(base.servo_horn, D.shape[0]), np.repeat(plane.arm_length, D.shape[0]), D_scal
		A = np.arccos(((b**2 + c**2 - a**2) / (2*b*c)))
		m = np.repeat(np.array([[0, 0, 1]]), g.shape[0], axis=0)
		g_offset = np.arccos(np.diag(pairwise_batch_cosine_sim_cal(m, g)))
		alphas_prime = A + x + g_offset 
		alpha = np.pi/2 - alphas_prime
		return alpha


	def plot_plane_and_vectors(self, plane_joints=False, ref_plane=None):
		normal_vector = self.orientation

		# Function to generate points on a plane
		def generate_plane_points(normal):
			xx, yy = np.meshgrid(range(-self.plane_radius, self.plane_radius + 1), range(-self.plane_radius, self.plane_radius + 1))

			z = ((-normal[0] * xx - normal[1] * yy) * 1. /normal[2]) + self.plane_height
			return xx, yy, z

		# Generate data for a plane with a given normal vector
		xx, yy, z = generate_plane_points(normal_vector)

		# Generate data for four random 3D vectors
		random_vectors = self.plane_joints

		# Plotting
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		lim = self.plane_radius + self.hand_length + 3
		ax.set_xlim(-lim, lim)
		ax.set_ylim(-lim, lim)
		ax.set_zlim(-lim, lim)

		# Plot plane points
		ax.plot_surface(xx, yy, z, alpha=0.5)

		if ref_plane is not None:
			xx, yy, z = generate_plane_points(ref_plane)
			ax.plot_surface(xx, yy, z, alpha=0.3, color='g')

		if plane_joints:
			for v in random_vectors:
				ax.quiver(0, 0, 0, v[0], v[1], v[2], color='r', label='Random Vectors')


		# Set labels and legend
		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')
		ax.legend()

		plt.title('Plane and Random Vectors in 3D')
		return ax, plt, fig



# plane = TopPlane(plane_height=3, plane_radius=3, arm_length=0.5, hand_length=0.5, initial_plane_orientation=np.array([0.1, 0.1, 1]))
# plane.plot_plane_and_vectors()