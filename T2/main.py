import sys
from MVC.Views.View import run

grid_size = 10
if len(sys.argv) > 1:
    grid_size = int(sys.argv[1])
    print("Running with grid size of " + str(grid_size) + ".")
else:
    print("No grid size given, running with 10 by default")
run(grid_size)
