from room import Room
from player import Player
from world import World
from util import Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
walking_player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

"""
 You are provided with a pre-generated graph consisting of 500 rooms. You are responsible for filling `traversal_path` with directions that, when walked in order, will visit every room on the map at least once.

* World generation code. Do not modify this!
* An incomplete list of directions. Your task is to fill this with valid traversal directions.
* Test code. Run the tests by typing `python3 adv.py` in your terminal.
* REPL code. You can uncomment this and run `python3 adv.py` to walk around the map.


You may find the commands `player.current_room.id`, `player.current_room.get_exits()` and `player.travel(direction)` useful.

To solve this path, you'll want to construct your own traversal graph. You start in room `0`, which contains exits `['n', 's', 'w', 'e']`. Your starting graph should look something like this:

```
{
  0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}
}
```
#1 Depth first traversal will give every possible room

#2 If player.current_room.get_exits() is not none, for item 

#####
#                                        #
#      017       002       014           #
#       |         |         |            #
#       |         |         |            #
#      016--015--001--012--013           #
#                 |                      #
#                 |                      #
#      008--007--000--003--004           #
#       |         |                      #
#       |         |                      #
#      009       005                     #
#       |         |                      #
#       |         |                      #
#      010--011--006                     #
#                                        #

# depth first to a dead end - could just by a while loop?
# using that path, bfs back to closest unexplored node

#####
3
{0: {'n': 1}}
{0: {'n': 1, 's': 5}}
{0: {'n': 1, 's': 5, 'w': 7}}
{0: {'n': 1, 's': 5, 'w': 7, 'e': 3}}

-------------------                                                                                                                                    1 ↵
#####
#                                        #
#      017       002       014           #
#       |         |         |            #
#       |         |         |            #
#      016--015--001--012--013           #
#                 |                      #
#                 |                      #
#      008--007--000--003--004           #
#       |         |                      #
#       |         |                      #
#      009       005                     #
#       |         |                      #
#       |         |                      #
#      010--011--006                     #
#                                        #
"""


def traversal(visited=None, previous=None, came_from=None):
    current_room = player.current_room.id
    exits = player.current_room.get_exits()
    reverse = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

    # redeclaring visited every time as to not cause issues with carrying over values with multiple function calls
    if visited is None:  # don't want to redefine this if we're being passed and updated value
        visited = {}

    if current_room not in visited:
        # have to instantiate an object before you can assign values in a nested object
        visited[current_room] = {}

    # if we're not on the first node, there will always be a previous otherwise
    if previous:
        # what direction did we go to get to the current room?
        # i.e. 0: { 'n': 1 }, north from 0 = 1
        visited[previous][came_from] = current_room
        # what direction would we have to go to get back?
        # i.e. 1: { 's': 0  } south from 1 = 0
        visited[current_room][reverse[came_from]] = previous

    for direction in exits:
        if direction not in visited[current_room]:
            traversal_path.append(direction)
            player.travel(direction)
            # for each viable direction in every single node, we're repeating this for loop
            traversal(visited, previous=current_room, came_from=direction)

    # we hit this case when the direction IS in visited, but we haven't touched all of the nodes yet
    if len(visited) < len(room_graph):
        # retracing steps until we get to a point where
        retrace = reverse[came_from]
        player.travel(retrace)
        traversal_path.append(retrace)

    # print(visited)
    # print(traversal_path)


traversal()

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# walking_player.current_room.print_room_description(walking_player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
