import base_sim
import plane_sim
import numpy as np
from numpy import linalg as la
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from vector_operations import pairwise_batch_cosine_sim_cal

def full_sim():

	def find_alpha(plane: plane_sim.TopPlane, base: base_sim.Base, goal_orientation: np.array, res = None):
		plane.update_orientation(goal_orientation, base)
		g = plane.get_hand_starts() - base.get_horn_pivots()
		hd = plane.get_isolated_hands()
		# D = np.sqrt(g_scal**2 + hd_scal**2 - 2*g_scal*hd_scal*cosbeta) # the 4 distances one for each corner
		D = g + hd
		
		D_scal = np.linalg.norm(D, axis=1)
		b, a, c = np.repeat(base.servo_horn, D.shape[0]), np.repeat(plane.arm_length, D.shape[0]), D_scal
		if not res:
			ax, p, fig = plane.plot_plane_and_vectors(ref_plane=np.array([0, 0, 1]))
		else:
			ax, p, fig = res
			# clear fig
			fig.clf()

		if not res:
			ax.quiver(*plane.get_hand_starts().T, *plane.get_isolated_hands().T, color='r')
			ax.quiver(*base.get_horn_pivots().T, *g.T, color='g')
			ax.quiver(*base.get_horn_pivots().T, *D.T, color='b')
		
		# let x be angle between g and D
		print(a, b, c)
		# check triangle inequality for our triangles with the variable arms and hand lengths
		# assert (a + b > c).all(), "Triangle inequality violated"
		x = np.arccos(np.diag(pairwise_batch_cosine_sim_cal(g, D)))
		print(x)

		A = np.arccos(((b**2 + c**2 - a**2) / (2*b*c)))
		print(A)
		# rotate every element vector in g by alpha_prime and normalize it 
		# find angle between g and 0, 0, 1
		# create a matrix that's a 4 repeat of 0, 0, 1
		m = np.repeat(np.array([[0, 0, 1]]), g.shape[0], axis=0)
		g_offset = np.arccos(np.diag(pairwise_batch_cosine_sim_cal(m, g)))

		alphas_prime = A + x + g_offset 
		print(alphas_prime)
		alpha = np.pi/2 - alphas_prime
		print(alpha)
		base.rotate_servos(*alpha)
		
		# find vectors going from horn ends to head end
		legv = plane.get_hand_ends() - base.get_horn_ends()
		print(la.norm(legv, axis=1))
		base.vis_servos(ax);
		# ax.quiver(0, 0, 0, *base.get_horn_ends().T, color='y')
		if not res:
			ax.quiver(*base.get_horn_ends().T, *legv.T, color='m')
		
		# add a slider for roll and pitch and translate that to a new goal_orientation
		if not res:
			# p.ion()
			p.show()
		else:
			pass
			# p.draw_idle()
		return ax, p, fig
		# TODO: find a way to paralelize the change in the angles so that they all run at the same time, load signal and send to 4 simeltaneously


	plane = plane_sim.TopPlane(arm_length=5, hand_length=3, plane_height=5, plane_radius=7, initial_plane_orientation=np.array([0.1, 0.1, 0.1]))
	base = base_sim.Base(6, 3, 3)
	xslider = Slider(plt.axes([0.1, 0.01, 0.8, 0.02]), 'X', -np.pi, np.pi, valinit=0)
	yslider = Slider(plt.axes([0.1, 0.04, 0.8, 0.02]), 'Y', -np.pi, np.pi, valinit=0)
	zslider = Slider(plt.axes([0.1, 0.07, 0.8, 0.02]), 'Z', -np.pi, np.pi, valinit=1)
	goal_orientation = np.array([0, 0, 1])
	fig = [None]
	def updater(val=None):
		res = find_alpha(plane, base, np.array([xslider.val, yslider.val, zslider.val]), fig[0])
		fig[0] = res

	xslider.on_changed(updater)
	yslider.on_changed(updater)
	zslider.on_changed(updater)
	updater()

full_sim()
