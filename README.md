## Programming Paradigms Final Project
#### created by Ashley Towne and John Rocha


####The Inspiration
Our project was inspired by the game FTL, a top-down spaceship simulator in which you fight enemies while maintaining your ship and
exploring the galaxy. Our twist on the popular game is adding multiplayer so that two users can fight each other with their own 
spaceships. The core gameplay consists of selecting a weapon on your ship and choosing where to fire it on the other ship. 

#### Game setup
The program consists of a server and two clients. First, the server needs to be run on the student02 machine with the command `python
server.py`

Each client can then connect to this server on a local machine by running the command `python main.py 40084` for player 1 or `python
main.py 40092` to connect as player 2. 

Upon startup, the clients are presented with the main menu, and they can click the "Play" option to move forward to ship selection. 
Similarly, click the name of the desired ship to be loaded into the game with it. Once a ship is selected, the game screen is displayed
with your ship on it. Other sprites on-screen include the green health blocks above the ship, the blue shield nodes right below them, and 
a weapon icon underneath the ship. The player waits here until the other client selects a ship, at which time both will appear on the screen and 
the real-time action can begin. 

#### Gameplay
Once the other player is loaded in, it's a free-for-all. To fire at the enemy, select the weapon icon below your ship and click a room on
the enemy ship that you would like to fire at. Luckily, if you get the ships confused, you won't be allowed to fire on yourself. Each hit taken
reduces the amount of hitpoints a ship has. Of course, once a ship runs out of health, it has been defeated and both players are notified of the 
winning player. As of right now, player 1 is always on the left and player 2 is always on the right. Also, weapons need time to charge up
so that they don't overheat. Thus, the current implementation is such that you can only have one laser blast from your ship on the screen at a time.
To start the fun from the beginning again, simply restart the server and clients!
