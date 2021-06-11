Pet project for IT2School students

Integrates tasks solving with python into SC2 campaign missions via SC2Bot API.
Players connect to webserver, running on host machine, and get tasks. 
Solving tasks, players get resources -- money/energy, which could be spent on units production.
Interaction with SC2 engine is going via redis db -- webserver pushes commands into storage, sc2 bot reads them and send into game chat.
Custom map chat handlers reads and execute commands.