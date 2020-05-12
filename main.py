#    IV = (0xface, 0xe961, 0x041d) 
# IV = convert_hash2str((0xface, 0xe961, 0x041d))

from db_handler import *
import sys
import bobcatModule
from igraph import *
import math
import random

num_of_ints = 2
### hash value to sql int
### this will convert a tuble of 3 ints to a string of fixed size
def convert_hash2str(h):
    result = ""
    for i in range(num_of_ints):
        result += format(h[i], '04x')
    for i in range(num_of_ints, 3):
        result += format(0, '04x')
    return result

def str_to_binary(s):
    return [ord(char) for char in s]

def convert_hash2ints(s):
    #every 4 chars is a one byte hexadicimal
    #each int will be a word of 2 bytes.
    #we always have 3 ints but we are ignoring some depends on num_of_ints
    return [int(s[i:i + 4],16) for i in range(0,12,4)]

#IV is string...for simplicity
def hash(IV, msg):
    msg = str_to_binary(msg)
    IV = convert_hash2ints(IV)
    while len(msg) % 8 != 0:
        #appending spaces
        msg.append(32)
    blocks = [msg[i:i + 8] for i in range(0,len(msg), 8)]
    for m in blocks:
        IV = bobcatModule.bobcatIV(IV, m)
    return convert_hash2str(IV)



#IV is string...for simplicity
def hash16bit(IV, msg):
    msg = str_to_binary(msg)
    IV = convert_hash2ints(IV)
    IV= (IV[0],IV[1],0)
    while len(msg) % 8 != 0:
        #appending spaces
        msg.append(32)
    blocks = [msg[i:i + 8] for i in range(0,len(msg), 8)]
    for m in blocks:
        IV = bobcatModule.bobcatIV(IV, m)
    return convert_hash2str((IV[0],IV[1]))


white_spaces = [9, 10, 11, 12, 13, 32, 133, 160,
5760, 8192, 8193, 8194, 8195, 8196, 8197, 8198,
8199, 8200, 8201, 8202, 8232, 8233, 8239, 8287,
12288]

def guesses_per_line(IV, TAG,guess_max_len, num_of_guesses):
    for _ in range(0,num_of_guesses):
        msg_len = random.randrange(1,guess_max_len,8)
        guess = ""
        for j in range(msg_len):
            guess = guess + chr(random.choice(white_spaces))
        hash_val = hash(IV, guess)
        db_collisions = get_collisions(hash_val)
        is_collision = False
        inline_collision = False
        for collision in db_collisions:
            if collision[1] == TAG:
                #collisoin on the same line ignore this guess/msg
                inline_collision = True 
                break 
            else:
                is_collision = True
                #there should be no more collisions!
                break
        #Ignore this msg/guess it's a collision inline
        if inline_collision:
            continue
        elif is_collision:
            print("***Found a collision***\n")
            insert_collision(guess, hash_val, TAG)
        else:
            insert_hash(hash_val, guess, TAG)
        #if we are here means no collision we need to save a new msg

def look_collisions(IV, guess_max_len, num_of_guesses):
    counter = 0
    print("started guessing messages -- searching for collisions")
    for _ in range(0,num_of_guesses):
        TAG = 0 #TAG is used for Nastradamus attack, so set it to 0
        msg_len = random.randrange(8,guess_max_len,8)
        guess = ""
        for j in range(msg_len):
            guess = guess + chr(random.choice(white_spaces))
        hash_val = hash(IV, guess)
        db_collisions = get_collisions(hash_val)
        is_collision = False
        for collision in db_collisions:
            print("***Found a collision: {}***\n")
            is_collision= True
            insert_collision(guess, hash_val, TAG)
            #there should be no more collisions
            break
        if is_collision: continue
        insert_hash(hash_val, guess, TAG)
        counter += 1
        if counter > 10000:
            print("generated {} hashes".format(counter))  
            counter = 0
        #if we are here means no collision we need to save a new msg

#height must be power(2,n). height is number of leaves
def generate_graph_datastructure(height):
    #depth of the tree or just the log(number of leaves)!!
    depth = int(math.log(height,2))
    return [ list(range(2**(p-1)-1,2**p-1)) for p in range(depth  , 0, -1)]


#msgs is the first leaves of messages
def generate_onelevel(hashes, guess_max_len, attempts_per_line):
    for i, hash_val in enumerate(hashes):
        guesses_per_line(hash_val, i, guess_max_len, attempts_per_line)
        print("------------------\n")
        print("Finished generating guesses for line {}\n".format(i))


def load_msgs_from_file(file_name):
    with open(file_name) as f:
        return list(f) 



generate_diamond(IV, msgs, guess_max_len, attempts_per_line):
    init_db()
    graph = generate_graph_datastructure(len(msg))
    level[0] = msgs
    for level in graph:
        is_level_incomplete=False
        while(is_level_incomplete):
            hashes = map(lambda x: hash(IV, x), msgs)
            generate_one_level(hashes, guess_max_len, attempts_per_line)
            collisions = get_found_collisions()
            for c in collisions:  
                int(c[0]) 

                ###I'm done no more work on this
            
###TESTING
init_db()
IV = convert_hash2str((0xface, 0xe961, 0x041d))
#m = load_msgs_from_file("msgs.txt")
#generate_onelevel(IV, m,16*4, 1000)
look_collisions(IV, 16*4, int(sys.argv[1]))

