Pet project for IT2School students

Integrate tasks solving with python into SC2 campaign missions via SC2Bot API.
Players connect to webserver, running on host machine, and get tasks. 
Solving tasks, players get resources -- money/energy, which could be spent on units production.
Interaction with SC2 engine is going via redis db -- webserver push commands into storage, sc2 bot read them and send into game chat.
Custom map has chat commands handlers for moving and spawning units.