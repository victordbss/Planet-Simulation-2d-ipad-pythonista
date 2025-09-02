from scene import *
from planet import *
from trajectory import *
from gameui import *
 
import sound
import random
import math
import time

A = Action

	

class MyScene (Scene):
	def setup(self):
		self.background_color = "black"
		self.last_touch_position = None
		self.scale_factor = 1.0
		self.time_scale_list = [1,2,4,10,50, 100, 500, 1000, 5000,10000,50000, 100000,500000,1000000, 5000000, 10000000, 50000000]
		self.time_scale = self.time_scale_list[0]
		self.focus_planet = None
		self.trajectory_points = []
		
		
		self.soleil = Planet(position=(0 * Planet.AU, 0), radius = 60, color = "yellow", mass = 1.989e30, vel_x = 0, vel_y = 0, name="Soleil", canmove = True)
		
		self.terre = Planet(position=(1 * Planet.AU, 0), radius = 20, color = "blue", mass = 6e24, vel_x = 0, vel_y = 30000, name="Terre", canmove = True)
		
		self.mars = Planet(position=(1.34 * Planet.AU, 0), radius = 15, color = "red", mass = 6e23, vel_x = 0, vel_y = 25000, name="Mars", canmove = True)
		
		self.venus = Planet(position=(0.72 * Planet.AU, 0), radius = 15, color = "orange", mass = 4.8e24, vel_x = 0, vel_y = 35000, name="Venus", canmove = True)
		
		self.mercure = Planet(position=(0.388 * Planet.AU, 0), radius = 10, color = "darkgrey", mass = 3.2e23, vel_x = 0, vel_y = 47200, name="Mercure", canmove = True)

		self.ingameui = GameUI(self)
		
		self.planetslist = [self.soleil, self.terre, self.mars, self.venus, self.mercure]
		
		
		for planet in self.planetslist:
			self.add_child(planet)
		
	def did_change_size(self):
		pass
	
	def update(self):
		self.ingameui.update(self)
		
		print("Objects : " + str(len(self.children)))
		dt = self.dt * self.time_scale 
		for planet in self.planetslist:
			planet.updateplanet(self.planetslist, dt)
			planet.updatedesign()
			
			point = TrajectoryPoint(position = (planet.x, planet.y), radius = planet.radius * 0.2, duration= 1)
			self.add_child(point)
			self.trajectory_points.append(point)
			
		
		for point in list(self.trajectory_points):
			point.update()
			if point.parent is None:
				self.trajectory_points.remove(point)	
			
			
		self.center_planet()
		
		
		
	
	def touch_began(self, touch):
		self.ingameui.on_click(touch, self)
		
		self.last_touch_position = touch.location
		if len(self.touches) == 1:
			
			
			
			for planet in self.planetslist:
				touch_x, touch_y = touch.location
				distance = math.sqrt((touch_x * (1 / self.scale_factor)  - planet.position[0]) ** 2 + (touch_y * (1 / self.scale_factor) - planet.position[1]))
				
				if distance <= planet.radius:
					self.focus_planet = planet
					break
					
		
	
	def touch_moved(self, touch):
		
		
		if len(self.touches) == 2:
			touches = list(self.touches.values())
			prev_distance = math.sqrt((touches[0].prev_location.x - touches[1].prev_location.x) ** 2 + (touches[0].prev_location.y - touches[1].prev_location.y) ** 2)
			curr_distance = math.sqrt((touches[0].location.x - touches[1].location.x) ** 2 + (touches[0].location.y - touches[1].location.y) ** 2)

			zoom_speed = 0.005
			self.scale_factor += zoom_speed * (curr_distance - prev_distance)
			self.scale_factor = max(0.1, min(self.scale_factor, 5.0))
			self.scale = self.scale_factor
			


		elif self.last_touch_position and len(self.touches) == 1 and not self.focus_planet:
			dx = (touch.location.x - self.last_touch_position.x)
			dy = (touch.location.y - self.last_touch_position.y) 
			
			
			for planet in self.planetslist:
				planet.x += dx * 1e9
				planet.y += dy * 1e9
			
			for point in self.trajectory_points:
				point.pos_x += dx  * 1e9 
				point.pos_y += dy * 1e9 
			
			self.last_touch_position = touch.location
	
	def touch_ended(self, touch):
		self.last_touch_position = None
	
	
	def center_planet(self):
		if self.focus_planet:
			screen_x = 2.3 * self.focus_planet.AU * (1/self.scale_factor)
			screen_y = 1.5 * self.focus_planet.AU * (1/self.scale_factor)
			
			dx = self.focus_planet.x - screen_x
			dy = self.focus_planet.y - screen_y
			for planet in self.planetslist:
				planet.x -= dx * 0.5
				planet.y -= dy * 0.5
	


if __name__ == '__main__':
	run(MyScene(), show_fps=True)
