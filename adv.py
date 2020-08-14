from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# Stack
class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


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
# we need to go into a room & mark it as visited
# we also need to log the room num with the direction for the previous room as well as vise versa
# if a room doesn't have '?' anymore it's the end & we need to backtrack using backtrack
# if every room has no '?'s we end the path

# s = Stack()
# visited = set()
# s.push([starting_vertex])

# while s.size() > 0:
#     current = s.pop()
#     vert = current[-1]
#     if vert == destination_vertex:
#         return current
#     if vert not in visited:
#         visited.add(vert)
#     for neighbor in self.get_neighbors(vert):
#         s.push(current + [neighbor])

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
s = Stack()
visited = set()
# when hitting dead ends we'll need to backtrack through the opposite direction
opposite_directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

# while rooms we went to are less than all in graph...
# get the exits & setup a path
while len(visited) < len(world.rooms):
    exits = player.current_room.get_exits()
    path = []

    # for each exit, if there is an exit with a room not yet visited we append it to the path
    for exit in exits:
        if exit is not None and player.current_room.get_room_in_direction(exit) not in visited:
            path.append(exit)

    # put the current room in our visited set
    visited.add(player.current_room)

    # if there is still a path of unvisited rooms, we push the next one from the path
    # to the stack & then the player travels to that next unvisited room which gets
    # appended to the ultimate trans_path
    if len(path) > 0:
        # next_room chooses an index of the path at random to go to next
        next_room = random.randint(0, len(path) - 1)
        s.push(path[next_room])
        player.travel(path[next_room])
        traversal_path.append(path[next_room])
    else:
        # if the path of unvisited rooms is empty but the total visited rooms is still less than entire graph,
        # we hit a dead end & the player has to backtrack
        backtrack = s.pop()
        player.travel(opposite_directions[backtrack])
        traversal_path.append(opposite_directions[backtrack])


# TRAVERSAL TEST - DO NOT MODIFY
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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
