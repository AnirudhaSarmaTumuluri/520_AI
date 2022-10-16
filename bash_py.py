fp = open("bash.sh", "w")
fp.write("")
fp.close()
fp = open("bash.sh", "a")
for i in range(1, 101):
    fp.write("python3 Generator_maze.py " + str(i) + "\n")
fp.close()