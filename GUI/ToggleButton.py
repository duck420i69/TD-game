import pygame

from typing import Callable
from GUI.Button import Button, ButtonSprites


class ToggleButton(Button):
	def __init__(self,
				 sprites: ButtonSprites,
				 name: str,
				 rect: pygame.Rect = None,
				 is_icon: bool = False,
				 on_press: Callable[[], None] = None,
				 on_release: Callable[[], None] = None,
				 on_toggle: Callable[[bool], None] = None,
				 toggled: bool = False):
		super().__init__(sprites, name, rect, is_icon, on_press, on_release)
		self.toggled = toggled
		self.on_toggle = on_toggle
		self._render()

	def press(self):
		if self.hold:
			self.pressed = False
			if self.hover:
				self.toggled = not self.toggled
				if self.on_toggle is not None:
					try:
						self.on_toggle(self.toggled)
					except Exception:
						pass
				if self.on_release is not None:
					self.on_release()
		self.hold = False
		self._render()

	def set_toggled(self, value: bool):
		if self.toggled != value:
			self.toggled = value
			self._render()

	def _render(self):
		super()._render()
		# draw a small indicator when toggled
		try:
			if self.toggled:
				surf = self.image
				r = max(3, int(min(surf.get_width(), surf.get_height()) * 0.07))
				margin = r + 3
				pos = (surf.get_width() - margin, margin)
				pygame.draw.circle(surf, (0, 200, 0), pos, r)
		except Exception:
			pass

