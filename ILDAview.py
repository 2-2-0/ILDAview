#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ILDAview.py
#  by 220 @ WKH
#  initial release
#  
#  Copyright 2015 220 <220@WKH>
#
#  requires pygame and ILDA.py, by Micah Dowty
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#


import ILDA
import pygame, math, time, sys

init_filename = "o-t1.ild"

def previewFrame (surface, f, scale, show_trace=True, show_hidden=False, show_nodes=False):
	lx = 0
	ly = 0
	
	visible_lines = 0
	hidden_lines = 0
	
	for p in f.iterPoints():
		dx = (p.x*scale)+400
		dy = (p.y*-scale)+300
		
		if show_nodes: pygame.draw.circle (surface, (255, 255, 255), (int (dx), int (dy)), 4, 1)
		if (lx!=0 and ly!=0):
			if (p.blanking):
				c = (127, 127, 127)
				hidden_lines+= 1
				if show_hidden: pygame.draw.line (surface, c, (dx, dy), (lx, ly))
			else:
				c = (255, 127, 0)
				visible_lines+= 1
				if show_trace: pygame.draw.line (surface, c, (dx, dy), (lx, ly))

		lx = dx;
		ly = dy;
		
	pygame.display.update ()
	return (visible_lines, hidden_lines)


def loadILD (fname):
	fstream = open (fname, 'rb')
	return ILDA.read (fstream)


def main ():
	print "ILDAview, by 220 @ WKH"
	print "initial release"
	
	screen = pygame.display.set_mode ((800, 600))
	pygame.display.set_caption ("ILDAview")
	pygame.init ()
	pygame.font.init ()
	sfont = pygame.font.SysFont ("monospace", 14, False, False)
	
	
	current_frame = 0
	total_count = 0
	preview = False
	show_hidden = False
	show_nodes = False
	show_trace = True
	pscale = 290
	
	ild_filename = ""
	frames = loadILD (init_filename)
	ild_filename = init_filename
	
	
	
	tables = []
	for f in frames:
		print f
		tables.append (f)

	total_count = tables [0].total
	print (total_count)
	
	done = False
	while (not done):
		
		for event in pygame.event.get ():
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_ESCAPE:
					done = True
				if event.key==pygame.K_LEFT:
					if current_frame>0: 
						preview = False
						current_frame-=1
						print (str (current_frame)+" / "+str (total_count))
				if event.key==pygame.K_RIGHT:
					if current_frame<total_count-1: 
						preview = False
						current_frame+=1
						print (str (current_frame)+" / "+str (total_count))
						
				if event.key==pygame.K_UP:
					pscale+= 10
				if event.key==pygame.K_DOWN:
					pscale-= 10
						
				if event.key==pygame.K_HOME:
					current_frame = 0
				if event.key==pygame.K_END:
					current_frame = total_count-1
					
				if event.key==pygame.K_SPACE:
					preview = not preview
				if event.key==pygame.K_i:
					fn = raw_input ("open ILD filename>")
					frames = loadILD (fn)
					ild_filename = fn
					
					tables = []	
					for f in frames:
						tables.append (f)

					total_count = tables [0].total
					current_frame = 0
					preview = False
				
				if event.key==pygame.K_h:
					show_hidden = not show_hidden
				if event.key==pygame.K_t:
					show_trace = not show_trace
				if event.key==pygame.K_n:
					show_nodes = not show_nodes


		screen.fill ((0, 0, 0))
		if preview:
			if (current_frame<total_count-1): current_frame+= 1
			else: current_frame = 0
			time.sleep (0.05)

		frame = tables [current_frame]

		info = previewFrame (screen, frame, pscale, show_trace, show_hidden, show_nodes)
		
		s = "filename: " + ild_filename
		label = sfont.render (s, True, (255, 127, 255))
		screen.blit (label, (5, 6))
		
		s = str (current_frame+1) + " / " + str (total_count)
		label = sfont.render (s, True, (255, 127, 255))
		screen.blit (label, (5, 18))
		
		s = "points: " + str (frame.length)
		label = sfont.render (s, False, (255, 127, 255))
		screen.blit (label, (5, 30))
		
		s = "visible lines: " + str (info [0])
		label = sfont.render (s, False, (255, 127, 255))
		screen.blit (label, (5, 42))
		
		s = "hidden lines: " + str (info [1])
		label = sfont.render (s, False, (255, 127, 255))
		screen.blit (label, (5, 54))
		
		s = "proj scale:  " + str (pscale)
		label = sfont.render (s, True, (255, 127, 255))
		screen.blit (label, (5, 66))
		
		s = "format:  " + str (999)
		label = sfont.render (s, True, (255, 127, 255))
		screen.blit (label, (5, 78))
		
		s = "name:  " + str (frame.name)
		label = sfont.render (s, True, (255, 127, 255))
		screen.blit (label, (5, 90))
		

		pygame.display.update ()		
	
	pygame.font.quit ()
	pygame.quit ()
	print "succesful logout"
	return 0

if __name__ == "__main__":
	main ()
