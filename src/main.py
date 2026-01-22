import sys
sys.dont_write_bytecode = True

from Polyomino import Polyomino, tetrominos, letters
from PolyominoProblem import PolyominoProblem
import time
import numpy as np
import sys
import os
from shapeprint import print_polyomino, print_solution
from puzzles import puzzles

np.set_printoptions(suppress=True,linewidth=np.nan,threshold=sys.maxsize)
os.system('cls')

is_auto = input("Auto solve? Y/N").lower() == 'y'

t00 = time.time()
for puzzle_name, problem in puzzles.items():
  if puzzle_name != 'lokdec1':
    continue
  print("SOLVING PUZZLE",puzzle_name)

  problem.allow_crafting = True
  problem.allow_formatting = True
  problem.allow_flipping = True

  t0 = time.time()
  solutions = problem.solve(is_auto=is_auto, return_all_solutions = True) #convertToDlx; solveProblems; trim_duplicate_solutions; interpret; return sets of pieces
  t1 = time.time()
  print(f"Solutions: {len(solutions)} (took {t1 - t0} seconds.)")

  # assert(len(solutions) == 1)

  for k, solution in enumerate(solutions):
    print(f"---SOLUTION {k + 1}---")
    print(len(solution))
    for p in solution:
      print(p.region)
      print(p.coords)
    print_solution(problem.regions, solution)
    input()

  # print("Time taken:",t1 - t0)
  print()
  
  # input()
  # assert(len(solutions) == 1)

t11 = time.time()
print(f"Total time: {t11 - t00} seconds.")