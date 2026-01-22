import numpy as np
import time
import copy

def solveProblems(problems, return_all_solutions=False, is_auto = False):
  solutions = []
  if not is_auto:
    print("All problem recipes:")
    for p in problems:
      print([x.name for x in p['recipe']])
    # input()
  for p in problems:
    tmp_auto = False
    if not is_auto:
      print("Trying with recipe:")
      [print(piece.name, piece.coords) for piece in p['recipe']]
      keyword = input("Press Enter to resume solving, or type 'cancel' to cancel the solving process for this recipe.")
      if keyword == "cancel":
        continue
      elif keyword == "auto":
        tmp_auto = True
    newSolutions, _ = solve(p['recipe'], p['matrix'], evaluated_solution=[], essentials = [], base_essentiality=p['base_essentiality'], return_all_solutions=return_all_solutions, is_auto = is_auto or tmp_auto)
    solutions.extend([[p['recipe'], ns] for ns in newSolutions])
    if len(solutions) > 0 and not return_all_solutions:
      return solutions

  
  return solutions

def solve(recipe, matrix, evaluated_solution=[], essentials = [], base_essentiality=0, return_all_solutions=False, is_auto = False, exploredRows = None):

  # time.sleep(1)
  # More quickwin/quickloss checks here

  solutions = []
  if not exploredRows:
    exploredRows = []

  # print(matrix.shape)

  # print("Comparisons")
  # print(sum(matrix[0, :]))
  # print(essentiality)
  # print("Matrix size")
  # print(matrix.shape)
  depth = len(evaluated_solution)
  # if depth < 3:
  #   print("." * (depth + 1) + str(len(exploredRows)) + str(matrix.shape))

  total_essentiality = sum(matrix[0, :])
  earned_essentiality = sum(matrix[0, essentials])
  essentiality = base_essentiality + earned_essentiality

  # print(f"Essentiality = {sum(matrix[0, essentials])} + {base_essentiality} = {essentiality}")

  #Checking if we have enough remaining options to obtain the necessary essentiality
  # if matrix.shape[0] > 2:
  #   essential_columns = np.where(matrix[0, :] > 0)
  #   impossible_columns = np.where(np.max(matrix[2:, :], axis=0) < 1)
  #   both = np.intersect1d(essential_columns, impossible_columns)
  #   impossible_essentiality = np.sum(matrix[0, both])
  #   needed_essentiality = total_essentiality - essentiality
  #   remaining_essentiality = total_essentiality - impossible_essentiality

  #   # print("matrix")
  #   # print(matrix)

  #   print("essentials",essential_columns)
  #   print("impossible",impossible_columns)
  #   print("both",both)

  #   print(f"Essentiality: {essentiality} / {total_essentiality} ({impossible_essentiality} impossible)")

  #   print("remaining",remaining_essentiality,"needed",needed_essentiality)
  #   # input()

  #   if remaining_essentiality < needed_essentiality:
  #     print("Not enough essentiality to go around. Returning")
  #     return [], False


  if not is_auto:
    print("Depth:", depth)
    # print("Matrix")
    # print(matrix)
    print(f" Essentiality: {essentiality} / {sum(matrix[0,:])}")
    keyword = input("Press Enter to resume solving, or type 'cancel' to cancel the solving process for this recipe.")
    if keyword == "cancel":
      return [], True
    elif keyword == "auto":
      is_auto = True

  #Check that none of the remaining columns are essential
  # print("Essentials covered:",len(essentials))
  # print("Sum of essentials:",sum(matrix[0,:]))
  if np.isclose(sum(matrix[0,:]), essentiality):
    print("Found a solution!")
    # print([e.tolist()[0] for e in evaluated_solution])
    # print("Returning")
    # print(evaluated_solution)
    return [[e for e in evaluated_solution]], False #For some reason I'll lose refs to those elements in the solutions array if I don't recreate it here.
  elif matrix.shape[0] == 2:
    # print("Found no solution here.")
    return [], False

  #Remove header
  matrixNh = matrix[2:, :]
  matrixH = matrix[0:2, :].copy() #Header only
  matrixH[0, essentials] = 0 #Disregard essential columns that were already validated

  #set essential to 0 where the column has no 1 entry (the essential element is no longer attainable and shouldn't be picked for the search)
  # print(np.max(matrixNh, axis = 0) < 1)
  # print(np.where(np.max(matrixNh, axis = 0) < 1))
  matrixH[0, np.where(np.max(matrixNh, axis = 0) < 1)] = 0
  # print(matrixH)
  # time.sleep(2)
  # print(matrixH)
  matrixH = 10e5 * (matrixH == 0) #Adds 10000 to non-essential columns so they aren't returned by the min column search
  # print(matrixH)

  # print("H1",matrixH)
  # print("Essentials:",essentials)

  # for e in essentials:
  #   matrixH[e] = 10e5
  
  # print("H2",matrixH)

  # essentialMatrix = np.append(np.reshape(matrixH, (2, matrixH.shape[0])), matrixNh, axis = 0)
  essentialMatrix = np.append(np.atleast_2d(matrixH[0, :]), np.minimum(matrixNh, 1), axis = 0)

  #Index of the ESSENTIAL column with the fewest options.
  # print(f"Depth: {len(evaluated_solution) + 1}")
  # print(f"Matrix dimensions: {matrix.shape}")
  # print(np.sum(essentialMatrix, axis=0))
  # print("ESMAT")
  # print(essentialMatrix)
  # time.sleep(10)
  # print(np.sum(essentialMatrix, axis=0))
  c = np.argmin(np.sum(essentialMatrix, axis=0))
  # print("Min column index:", c)
  # print(len(evaluated_solution[0] if len(evaluated_solution) else 0))
  # if len(evaluated_solution) == 1:
  #   time.sleep(10)
  # if len(evaluated_solution) == 0:
  #   time.sleep(10)

  choices = int(np.sum(matrix[:, c]) - 1)
  # print(f"Smallest column: {c} ({choices} possible choices)")
  # print(matrix[:, c])

  if choices == 0:
    # print("An essential piece/tile has no covering options. Returning")
    return [], False
  
  exploredMatrix = matrix

  # print("EXPMAT??")
  # print(exploredMatrix)
  fullrange = np.transpose(np.where(matrix[2:, c] > 0))

  for kk, kc in enumerate(reversed(fullrange)):
    # if depth < 3:
    #   print(f"{kk + 1} / {choices}")
    candidateRow = exploredMatrix[kc + 2, :]
    if not is_auto:
      print("Matrix")
      print(matrix)
      print("exploredMatrix")
      print("Candidate row:")
      print(np.vstack([matrix[[0,1],:], candidateRow]))

      print("Explored rows:")
      for r in exploredRows:
        print(r)
    
    # if candidateRow[0, 6] and candidateRow[0, 12] and candidateRow[0, 13] and candidateRow[0, 14]:
    #   print("AS WE PRACTICED (top)")
    #   time.sleep(5)
    #   input("go on")
    
    # if candidateRow[0, 10] and candidateRow[0, 11] and candidateRow[0, 15]:
    #   print("AS WE PRACTICED (bottom)")
    #   time.sleep(5)
    #   input("go on")

    alreadyExplored = False
    # print(len(recipe))
    for r in exploredRows:
      # print(candidateRow[0, len(recipe):])
      # print(r[0, len(recipe):])
      if np.max(np.abs(candidateRow[0, len(recipe):] - r[0, len(recipe):])) < .001:
        # print("I've already explored this row! Ignoring!")
        # print(candidateRow[0, :len(recipe)])
        # print(r[0, :len(recipe)])
        piece1 = recipe[next(i for i,v in enumerate(candidateRow[0,:len(recipe)]) if v > 0)]
        piece2 = recipe[next(i for i,v in enumerate(r[0,:len(recipe)]) if v > 0)]
        # print(piece1.name, piece1.blueprint, piece2.name, piece2.blueprint)
        if piece1.blueprint == piece2.blueprint:
          alreadyExplored = True
          break
        else:
          # print("Identical positions found but for different blueprints")
          pass

    if alreadyExplored:
      # print("Ignored")
      continue

    # print("That's a fresh row.")
    # input()
    exploredRows.append(candidateRow)
    # time.sleep(2)
    # print()
    # print(candidateRow)
    # print(candidateRow.tolist()[0])
    evaluated_solution.append(candidateRow.tolist()[0])
    subMatrix, newEssentials = reduceMatrix(exploredMatrix, kc, is_auto=is_auto)
    newSolutions, cancel = solve(recipe, subMatrix, evaluated_solution, essentials + newEssentials, base_essentiality, return_all_solutions = return_all_solutions, is_auto = is_auto, exploredRows = copy.copy(exploredRows))
    solutions.extend(newSolutions)
    if cancel == True:
      return solutions, True
    # print(f"Returned. Solutions: {len(solutions)}")
    if len(solutions) > 0 and not return_all_solutions:
      return solutions, False
    evaluated_solution.pop()

    exploredMatrix = np.delete(exploredMatrix, kc + 2, axis=0) #TODO UNCOMMENT??

  depth = len(evaluated_solution)
  if not is_auto:
    print(f"Depth {depth} -> {depth - 1}")
  return solutions, False

def reduceMatrix(matrix, kc, is_auto=True):

  #Remove header
  matrixNh = matrix[2:, :]
  matrixH = matrix[0:2, :] #Header only

  # print("Reducing matrix with vector:")
  # print(matrix[kc + 1, :])
  if not is_auto:
    print("Reducing matrix with vector:")
    print(matrix[kc + 2, :])

  # print("From:")
  # print(matrixNh)

  mulMatrix = np.tile(matrix[kc + 2, :], (matrixNh.shape[0], 1))
  
  # Indices will be 1 if both rows have a 1 on the same index;
  # 0 if one of them had a 0,
  # 0.3 if one of them was 1 and the other was 0.3,
  # and a lower value otherwise.
  prodMatrix = np.multiply(matrixNh, mulMatrix)

  # print("To:")
  # print(prodMatrix)

  # Find the highest value in each row
  highestProdPerRow = np.max(prodMatrix, axis=1)

  #We'll remove any row that has a value geq 0.3 (adding back the header row)
  # reducedMatrix = np.append(np.reshape(matrixH, (1, matrixH.shape[0])), matrixNh[np.where(highestProdPerRow < 0.3)], axis = 0)
  reducedMatrix = np.append(matrixH, matrixNh[np.where(highestProdPerRow < 0.2)], axis = 0)

  if not is_auto:
    print("Reducing matrix with vector:")
    print(matrix[kc + 2, :])
    # print("Reduced matrix:")
    # print(reducedMatrix)

  # print("Essentials check")
  # print(matrix[kc + 1, :])
  # print(matrixH)
  # print(np.multiply(matrix[kc + 1, :], matrixH))
  # print(np.where(np.multiply(matrix[kc + 1, :], matrixH) == 1)[0].tolist())

  # print("Essential coords")
  # print(np.where(np.multiply(matrix[kc + 2, :], matrixH[0, :]) == 1)[1])
  # print("Essential coords 2")
  # print(np.where(matrix[kc + 2, :] == 1)[1])
  # print(np.where(matrixH[0, :] > 0)[0])
  # print(np.intersect1d(np.where(matrix[kc + 2, :] == 1)[1], np.where(matrixH[0, :] > 0)[0]))

  essentials = np.intersect1d(np.where(matrix[kc + 2, :] >= 1)[1], np.where(matrixH[0, :] > 0)[0]).tolist()

  # print("Essentials")
  # print(essentials)

  return reducedMatrix, essentials

def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols

def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)

def trim_duplicate_solutions(solutions):
  unique_solutions = []
  for solution in solutions:
    nbPieces1 = len(solution[0])
    valid = True
    for other_solution in unique_solutions:
      any_difference = False
      nbPieces2 = len(other_solution[0])
      # print("Nb pieces:")
      # print(nbPieces1, nbPieces2)
      # print(solutions)
      recipe1 = solution[0]
      for s in solution[1]:
        if s[nbPieces1:] not in [o[nbPieces2:] for o in other_solution]:
          any_difference = True
          break
      
      if not any_difference:
        valid = False
    
    if valid: #This solution has no duplicate for now
      unique_solutions.append(solution)
  
  return unique_solutions

