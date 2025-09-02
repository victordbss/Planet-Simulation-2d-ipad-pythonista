from scene import *
import math
import time


class TrajectoryPoint(ShapeNode):
	AU = 149.6e6 * 1000
	SCALE = 250 / AU  # 1AU = 100 pixels
	
	def __init__(self, position, radius = 5, color="lightgrey", duration = 1):
			
		path = ui.Path.oval(0, 0, radius, radius)
		super().__init__(path, fill_color=color, stroke_color=color)
			
		self.lifetime = duration
		self.creationtime = time.time()
		self.z_position = -1
		self.pos_x = position[0]
		self.pos_y = position[1]
		self.position = (self.pos_x * self.SCALE, self.pos_y * self.SCALE)
			
	def update(self):
		self.position = (self.pos_x * self.SCALE, self.pos_y * self.SCALE)
		elapsed_time = time.time() - self.creationtime
			
		if elapsed_time >= self.lifetime:
			self.remove_from_parent()
		else:
			opacity = max(0, 1 - elapsed_time / self.lifetime)
			self.alpha = opacity

