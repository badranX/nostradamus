f= open("msgs.txt","w+")
for i in range(2**6):
   f.write("At the end of the talk, we will have {} students\n".format(i)) 
f.close()
