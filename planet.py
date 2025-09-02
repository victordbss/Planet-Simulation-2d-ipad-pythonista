from scene import *
import math
import email

class Planet(ShapeNode):
	
	AU = 149.6e6 * 1000
	G = 6.67428e-11
	SCALE = 250 / AU  # 1AU = 100 pixels
	
	def __init__(self, position, radius, color, mass, vel_x, vel_y, name, canmove = True):
		
		self.radius = radius
		self.mass = mass
		self.canmove = canmove
		self.name = name
		self.vel_x = vel_x
		self.vel_y = vel_y
		self.x = position[0]
		self.y = position[1]
		self.position = (self.x * self.SCALE, self.y * self.SCALE)
		
		self.createvelocityline()
	
		self.createplanetdesign(radius, color)
		self.createlabel(radius)
		
	def createvelocityline(self):
		vect_x = Rect(0,0,1,10, fill_color="white")
		
	
		
	def createplanetdesign(self, radius, color):
		path = ui.Path.oval(0,0,radius,radius)
		super().__init__(path, fill_color=color, stroke_color = color)
	
	def createlabel(self, radius):
		self.label = LabelNode(text=self.name, font=("Helvetica", 12), color="white")
		self.label.position = (0, -radius - 10)
		self.add_child(self.label)
	
	def attraction(self, other):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
		
		force = self.G * other.mass * self.mass / distance ** 2
		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force
		return force_x, force_y	

	
	def updateplanet(self, planetslist, timestep):
		if self.canmove:
			totalfx = totalfy = 0
			
			for planet in planetslist:
				if planet.name != self.name:
			
					fx, fy = self.attraction(planet)
					totalfx += fx
					totalfy += fy
			
			self.vel_x += totalfx / self.mass * timestep
			self.vel_y += totalfy / self.mass * timestep
			self.x += self.vel_x * timestep
			self.y += self.vel_y * timestep

		
	def updatedesign(self):
		self.position = (self.x * self.SCALE, self.y * self.SCALE)
