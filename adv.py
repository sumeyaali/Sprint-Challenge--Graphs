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
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

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


# building the visited graph

def traverse_map(starting_room, direction=None):

    starting_room = player.current_room.id

    s = Stack()
    s.push([starting_room])

    # get room id 
    #player.current_room.id

    visited = {}
    reverse = {
        'n': 's',
        's': 'n',
        'e': 'w',
        'w': 'e'
    }

    while len(visited) < len(world.rooms):
        path = s.pop()
        visited[path[-1]] = traversal_path
        # iterate through exits 
        for room_exit in player.current_room.get_exits():
            current_room = world.rooms[starting_room]
            # we are checking to see of an exit and room has been visited, of not we add them to the visited's list
            if room_exit == '?' and player.current_room.id not in visited:
                print('Lone',room_exit)
                # if exit has not been in visited, travel to that exit and add visited {}
                visited[current_room] = traversal_path

                for next_room in player.current_room.get_room_in_direction(direction):
                    if next_room not in visited:
                        visited[next_room] = traversal_path          
                        new_path = traverse_map(next_room, visited)
                        if new_path:
                            return new_path



    return traversal_path


#   while s.size() > 0:
#             #create the path 
#             path = s.pop()
#             #Once we dequeue, we check to see if the last number in the list has been visited
#             if path[-1] not in visited:
#             #DO THE THING
#                 print(path[-1])
#                 visited.add(path[-1])

#                 for next_edge in self.get_neighbors(path[-1]):
#                     new_path = list(path)
#                     new_path.append(next_edge)
#                     s.push(new_path)








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
