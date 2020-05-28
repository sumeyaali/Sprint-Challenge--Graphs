from room import Room
from player import Player
from world import World

from util import Stack

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
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

'''
previous_room: None  needs to be updated
current room: 1 needs to be updated
direction: None

get the id
get the exits for that room [direction]
traverse/iterate  the exits

move to unvisited exit [have we moved in this direction yet, if not we can move in this direction]

1. iterate through the rooms
2. iterate through the exits
3. updated the visited{} when you move


Always update the visited list everytime we move

what condition in my previous is changed when my visited is updated

if direction = south: return north or opposite direction 


dft:
path variable = []  keeps track of the direction you move in 


finished: indicated by the length of the path array

When i'm in a room, im initializing the exits with '?'



'''
# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

'''
What am I keep track of?
the path= keeps track of the direction you move in 
where i have visited

also reverse of directions for when I hit a dead end
'''

reverse = {
    'n': 's',
    's': 'n',
    'w': 'e',
    'e': 'w'
}

def map_traversal(starting_room, visited=[]):
    # keeps track of the direction you move in 
    path = []

    for direction in player.current_room.get_exits():
        # player moves in this direction
        player.travel(direction)

        # if the current room has already been visited, go back
        if player.current_room.id in visited:
            player.travel(reverse[direction])
        else:
            # else add this room to visited, and directions you took to your path list
            visited.append(player.current_room.id)
            path.append(direction)
            path = path + map_traversal(player.current_room.id, visited)
            player.travel(reverse[direction])
            path.append(reverse[direction])
    
    return path


traversal_path = map_traversal(player.current_room.id)




# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
