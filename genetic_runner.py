import sys
from population import Population
if len(sys.argv) == 2:
    file = open(str(sys.argv[1]))
    p = Population(100, file, 450, 80000, 3000)
    p.run()
else:
    print("You need to provide a file name...")
