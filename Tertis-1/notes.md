General:
	* Your prject lacks a README.md.
	* Commenting is atrocious.
	* Purely iterative style of programming will lead to problems later when changes are needed.
	* Tertis uses 100% of a single CPU. Maybe add a frametime / FPS counter?
	* Actually make use of Git. "Add files via upload" is not a helpful commit message.
	* Add me as contributor to your repository so I can contribute easily.
	* Work in smaller increments, include a polishing and cleanup step in each increment and commit accordingly.

Line 23-32:
	Take care not to define a global variable if not strictly necessary.
	All the global variables defined here could also and maybe more appropriately
	implemented as default values in a Grid or maybe Game class.

Line 156:
	Why does a "Piece" need a score?
	
Line 162:
	Python gotcha. Never use the primitives [], {} as default objects, use None instead.
	https://stackoverflow.com/questions/26320899/why-is-the-empty-dictionary-a-dangerous-default-value-in-python

Line 275:
	"comicsans" is not a valid font choice on my system. Maybe include a royalty free font as static asset?

Line 289:
	Most of the contents of main() should probably be encapsulated in a `class Game()` object

Line 296:
Line 385:
	Instead of using a variable to control execution flow, break out of the loop directly, i.e.
	
	```
	if event.type == pygame.QUIT:
		run = False  # This is not controlled
	```

	```
	if event.type == pygame.QUIT:
		break  # This is more controlled
	```

	```
	def quit_menu():
		# Do stuff to clean up
		...

		pygame.quit()

	if event.type == pygame.QUIT:
		quit_menu()  # Even better
	
	```

Line 303:
	What does 0.27 represent? Pixel/ms? This is a case of a magic value and should be documented.

Line 307:
	Make better use of clock.tick() to control the game's framerate.
	https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.tick

Line 323-349:
	Undoing changes to the current_piece based on the outcome of `valid_space` seems prone to error. Better to find an
	implementation that allows for collision checking before making changes. I think this could become part of a 
	`class Grid` object.
	
Line 323-349:
	All interactions with `current_piece` should be implemented in the `class Piece` itself, for example
	
	```
	class Piece:
		…

		def move_left():
			…

		def move_right():
			…

		def drop():
			…

		def rotate():
			…
	```
	

Line 360:
	Your use of Booleans to control execution flow reminds me of GOTO's. Can be avoided by encapsulated game objects
	with attached methods to control execution.

Line 379:
	Aggressive towards the player. Would not make me want to pick up the game another time...
