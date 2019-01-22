1.0

Developed By Kyle Meade

Instructions:
	Open "Main.py" (Double click)

Requirements:
	Python 2.7 32bit(Not 2.6, not 2.8, definitely not 3.1)
	Link: https://www.python.org/download/releases/2.7/

	pygame-1.9.1.win32-py2.7.msi (Make sure the 'py2.7' is in the title)
	Link: http://www.pygame.org/download.shtml

	Minimum computer specification: A dedicated graphics card

How to play:
	Run around and shoot zombies, don't get close to them or they will lunge to you.
	Kill all the zombies that spawn from the spawners to progress to the next room.
	As you progress through the rooms, more zombies will spawn and they game will
	progressively get challenging. As you shoot zombies you will accumulate score,
	which you can use to upgrade your player, buy bullet types, items or ammo.
	Survive as long as you can to accumulate the highest total accumulated score.

Controls:

	Movement:
	[W]: Move player up
	[S]: Move player down
	[A]: Move player left
	[D]: Move player right
	[Space]: Sprint

	Shooting:
	Move mouse and the player will rotate to it.
	Left click to shoot a bullet to the direction of where the character is facing.
	(There is also a random inaccuracy value)

	Menu:
	[F] Open items Menu 
	Button 1: Player traits(health, agility, accuracy, max ammo)
	Button 2: Bullet Types(bouncy, explosive, spray, flame)
	Button 3: Items(Distraction Orb, Grenade, Spinning Blade, Freeze Block)
	Button 4: Ammo(1 Mag, 2 Mags, 4 Mags, 8 Mags)

	Name Toggle (name will be changable):
	[E]: Toggle name on/off
	
	Use Items:
	[Z]: Place distraction orb at mouse location tile (can't place on tiles or spawners)
	[X]: Throw grenade in direction to mouse from player (accurate)
	[C]: Place spinning blade at mouse location tile (can't place on tiles or spawners)
	[V]: Place freezing block at mouse location tile (can't place on tiles or spawners)

	Toggle Bullet Types:
	(Bullet types keys show up when their bought on the bottom right)
	[1]: Normal
	[2]: Bouncy
	[3]: Explosive
	[4]: Spray
	[5]: Flame

	Other:
	[Q]: Close game

Current Bugs:
	- zombie's are as stupid as zombies
	- Bounce bullet types are canceling out when shot between 2 blocks (they are bouncing off collided sides)
	- manual reloading doesn't work, math is incorrect and you can just spam it.

Changelog:
	Alpha 1.0: Main Build
	Alpha 1.1: Gameplay adjustments, (Little too hard off the bat):
		   Increased player base speed. Greatly increased based health. Greatly increased Max health.
		   Made freeze blocks freeze zombies forever, made blades do 2 damage/1second, instead of 1damage/1second.
		   Added Stronger inaccuracy for spray bullets. Reduced Max radius for explosive bullets.
		   Reduced existence length for flame tiles. Increased max starting ammo
		   Decreased zombie evolution speed, GREATLY decreased zombie spawned/room progression.
		   Huge grenade nerf, reduced explosion radius. Decreased Damage from 10 per zombie to 3.
		   Gave player's 1 of each item off the bat.
	Beta 1.0:
		Added menus, splash screen, death screen, options, difficulties, adjusted
		gameplay, store prices, player names, high score saving, high score organizing
		and displaying in the high score screen. Significantly more levels. Sound effects
		and background music. Resolution adjuster. Scaling Graphics.
		Vector coordinates to percentages. Significantly optimized games
