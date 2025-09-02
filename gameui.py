from scene import *
import ui

class GameUI(ShapeNode):
	def __init__(self, scene):
		self.time_scale_label = LabelNode(text = "Vitesse de la simulation : ", font=('Anonymous Pro', 18), color="white")
		self.time_scale_label.position = (170,770)
		self.time_scale_label.z_position = 1
		
		scene.add_child(self.time_scale_label)
		self.subbutton, self.subbuttontext = self.creation_bouton_time_wrap(scene, (100, 720), -1, "-")
		scene.add_child(self.subbutton)
		scene.add_child(self.subbuttontext)
		
		scene.add_child(self.time_scale_label)
		self.addbutton, self.addbuttontext = self.creation_bouton_time_wrap(scene, (300, 720), 1, "+")
		scene.add_child(self.addbutton)
		scene.add_child(self.addbuttontext)
		
		self.endfocusbutton, self.endofocusbuttontext = self.createbutton((1000,50), (100,40), "white", "End Focus", "black")
		
		scene.add_child(self.endfocusbutton)
		scene.add_child(self.endofocusbuttontext)
		
		self.sceneref = scene
		
	
	def createbutton(self, buttonposition, button_scale, button_color, label_text, label_color, label_font = ("Helvetica", 12), button_var = None):
		
		button = ShapeNode(ui.Path.rect(100,100,button_scale[0], button_scale[1]), fill_color= button_color, stroke_color = button_color)
		button.position = buttonposition
		if not button_var:
			button.var = button_var
		
		buttontext = LabelNode(text = label_text, font= label_font, color = label_color)
		buttontext.position = buttonposition
		
		return button, buttontext
	
	
	def creation_bouton_time_wrap(self, scene, position, adder, btext):
		button = ShapeNode(ui.Path.rect(100,100,100,30), fill_color = "grey", stroke_color = "grey")
		button.position = position
		button.adder = adder
		
		buttontext = LabelNode(text = btext, font=("Helvetica", 18), color="black")
		buttontext.position = button.position
		
		
		return button, buttontext
		
	
	def update(self, sceneref):
#		 self.scale = 1 / sceneref.scale_factor
		
		self.time_scale_label.text = f"Vitesse de la simulation : {sceneref.time_scale} x"
		if sceneref.focus_planet == None:
			self.endfocusbutton.alpha = 0
			self.endofocusbuttontext.alpha = 0
		else:
			self.endfocusbutton.alpha = 1
			self.endofocusbuttontext.alpha = 1
	
	def on_click(self, touch, scene):
		if self.addbutton.frame.contains_point(touch.location):
			self.sceneref.time_scale = self.sceneref.time_scale_list[self.sceneref.time_scale_list.index(self.sceneref.time_scale) + 1]
		
		if self.subbutton.frame.contains_point(touch.location):
			self.sceneref.time_scale = self.sceneref.time_scale_list[self.sceneref.time_scale_list.index(self.sceneref.time_scale) - 1]
		
		if self.endfocusbutton.frame.contains_point(touch.location):
			scene.focus_planet = None
			
