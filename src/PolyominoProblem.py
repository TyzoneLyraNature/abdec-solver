from Polyomino import Polyomino, all_blueprints, letters
import numpy as np
import math
import time
from shapeprint import print_polyomino, print_solution
from AlgorithmX import solveProblems, trim_duplicate_solutions
import copy

def abdec(s):
  return [letters[c].clone() for c in s]

class PolyominoProblem:

  def __init__(self, pieces, region, allow_crafting = True, allow_formatting = True, allow_flipping = True):
      self.pieces = list(map(lambda x: x.normalize(), pieces))
      self.region = region.normalize()
      self.regions = [self.region]
      self.allow_crafting = allow_crafting
      self.allow_formatting = allow_formatting
      self.allow_flipping = allow_flipping

      # Extremal bounds
      self.width = self.region.getWidth()
      self.height = self.region.getHeight()

  def _fits(self, piece):
    #Quick check
    region = piece.region if piece.region is not None else self.region
    if piece.getWidth() > region.getWidth() or piece.getHeight() > region.getHeight():
      return False
    
    return all(region.containsCoordinate(c) for c in piece.coords)

  def to_grid(self, c, dx, dy, ox):
    basis = self.invert_basis(dx, dy)
    result = np.matmul(basis, np.array([[[c[0] - ox], [c[1]]]])).tolist()
    result = [result[0][0][0], result[0][1][0]]
    return result

  def invert_basis(self, dx, dy):
    denom = dx**2 + dy**2
    return np.array([[dx, dy], [-dy, dx]]) / denom
  
  def from_grid(self, c, dx, dy, ox):
    basis = np.array([[dx, -dy], [dy, dx]])
    result = np.matmul(basis, np.array([[[c[0]], [c[1]]]])).tolist()[0]
    return [result[0][0] + ox, result[1][0]]

  def _getOverlappingCoords(self, c, r1, r2, split_partially_covered=False):
    x, y = c[0], c[1]
    o_vertices = [[x, y], [x + 1, y], [x + 1, y + 1], [x, y + 1], [x + .5, y + .5]]

    dx1, dy1, ox1 = r1.dx, r1.dy, r1.ox
    dx2, dy2, ox2 = r2.dx, r2.dy, r2.ox
    vertices = [self.to_grid(self.from_grid(v, dx1, dy1, ox1), dx2, dy2, ox2) for v in o_vertices] #Convert from grid 1 to world, then to grid 2
    x1, x2 = math.floor(min(v[0] for v in vertices)), math.ceil(max(v[0] for v in vertices))
    y1, y2 = math.floor(min(v[1] for v in vertices)), math.ceil(max(v[1] for v in vertices))

    tot_overlapping, part_overlapping = [], []
    for xx in range(x1, x2):
      for yy in range(y1, y2):
        o_vertices2 = [[xx, yy], [xx + 1, yy], [xx + 1, yy + 1], [xx, yy + 1], [xx + .5, yy + .5]]
        vertices2 = [self.to_grid(self.from_grid(v, dx2, dy2, ox2), dx1, dy1, ox1) for v in o_vertices2] #Convert back from grid 2 to grid 1
        some_overlap, all_overlap = False, True

        #Point is strictly within the other tile (there is definite overlap)
        e0 = .001 #epsilon for float imprecision
        expr1 = [x + e0 < vv[0] < x + 1 - e0 and y + e0 < vv[1] < y + 1 - e0 for vv in vertices2]
        expr2 = [xx + e0 < p[0] < xx + 1 - e0 and yy + e0 < p[1] < yy + 1 - e0 for p in vertices]
        expr = [e1 or e2 for e1, e2 in zip(expr1, expr2)]

        some_overlap = any(expr)

        if not some_overlap:
          all_overlap = False
        elif split_partially_covered:
          #Point is out of the shape
          expr1b = [not (x - e0 < vv[0] < x + 1 + e0 and y - e0 < vv[1] < y + 1 + e0) for vv in vertices2]

          all_overlap = not any(expr1b) # or not any (expr2b)
        else:
          all_overlap = True
        
        if all_overlap:
          tot_overlapping.append([xx, yy])
        elif some_overlap:
          part_overlapping.append([xx, yy])

    return tot_overlapping, part_overlapping

  def _generateVirtualRegions(self):
    N = 3 #TODO 3
    regionArea = len(self.region.coords)

    for dx in range(1, N + 1):
      for dy in range(1, N + 1):
        if np.gcd(dx, dy) > 1: #This grid already exists at a smaller scale. Ignore
          continue
        
        for ox in range(dx**2 + dy**2):
        
          r2 = Polyomino([])
          r2.dx = dx
          r2.dy = dy
          r2.ox = ox
          t0 = time.time()
          for c in self.region.coords:
            overlapping, _ = self._getOverlappingCoords(c, self.region, r2)
            for o in overlapping:
              #not actually covering all cases but we move
              o_base1 = self.from_grid(o, dx, dy, ox)
              o_base2 = self.from_grid([o[0] + 1, o[1] + 1], dx, dy, ox)
              # print(o, dx, dy, ox, o_base1,  o_base2)
              if o_base1[0] < self.region.getSmallestX() or o_base2[0] > self.region.getLargestX() + 1:
                continue
              if o_base1[1] < self.region.getSmallestY() or o_base2[1] > self.region.getLargestY() + 1:
                continue
              if o not in r2.coords:
                r2.coords.append(o)
          t1 = time.time()
          
          new_coords = []
          for c in r2.coords:
            overlapping, _ = self._getOverlappingCoords(c, r2, self.region)
            if all(cc in self.region.coords for cc in overlapping):
              new_coords.append(c)
          t2 = time.time()

          r2.coords = new_coords

          changed = True
          while changed:
            changed = False
            for c in self.region.critters:
              overlapping, _ = self._getOverlappingCoords(c[0], self.region, r2) #Including cells not in the virtual grid

              critter_overlap = [o in r2.coords for o in overlapping]

              if any(critter_overlap) and not all(critter_overlap):
                #This virtual grid only partially covers a critter. You should never attempt to place anything there as it would invalide the solution immediately.
                #In fact, let's just discard that coordinate entirely, so we don't get tempted to use it later on.
                r2.coords = [cc for cc in r2.coords if cc not in overlapping]
                changed = True

            if len(r2.coords) == 0:
              break

            for c in self.region.clues:
              overlapping, _ = self._getOverlappingCoords(c[0], self.region, r2) #Including cells not in the virtual grid

              clue_overlap = [o in r2.coords for o in overlapping]

              if any(clue_overlap) and not all(clue_overlap):
                #This virtual grid only partially covers a critter. You should never attempt to place anything there as it would invalide the solution immediately.
                #In fact, let's just discard that coordinate entirely, so we don't get tempted to use it later on.
                r2.coords = [cc for cc in r2.coords if cc not in overlapping]
                changed = True
          t3 = time.time()
          # print(t1 - t0, t2 - t1, t3 - t2)
          if len(r2.coords) == 0:
            continue
          
          r2.col = self.regions[-1].col + len(self.regions[-1].coords)

          r2.coords.sort(key = lambda c: c[::-1])
          
          self.regions.append(r2)
    
    #All regions have been generated. Now to create an overlap matrix.
    nbCoords = sum([len(r.coords) for r in self.regions])
    self.overlapMatrix = np.identity(nbCoords)

    t5 = time.time()
    for k1, r1 in enumerate(self.regions):
      oc1 = sum([len(r.coords) for r in self.regions[:k1]])

      for k2, r2 in enumerate(self.regions[k1 + 1:]):
        oc2 = sum([len(r.coords) for r in self.regions[:k1 + 1 + k2]])

        for kc1, c1 in enumerate(r1.coords):
          for kc2, c2 in enumerate(r2.coords):
            ic1 = oc1 + kc1
            ic2 = oc2 + kc2

            assert(ic1 != ic2)

            tot_overlap, part_overlap = self._getOverlappingCoords(c1, r1, r2, split_partially_covered=False)

            #TODO MAYBE overlap = 1 if ...
            overlap = .2 if c2 in tot_overlap else (.2 if c2 in part_overlap else 0)

            self.overlapMatrix[ic1, ic2] = overlap
            self.overlapMatrix[ic2, ic1] = overlap

  def _canCraftBlueprint(self, pieces, blueprint):
    used_pieces = []
    for c in blueprint:
      found_piece = False
      for p in pieces:
        if p.name == c and p not in used_pieces:
          used_pieces.append(p)
          found_piece = True
          break
      
      if not found_piece:
        return False, None
    
    return True, used_pieces

  def _generateAllPossibleRecipes(self, pieces, recipePieces=[], available_blueprints = all_blueprints, maxScales = None):
    maxScale = 8
    recipes = []
    regionArea = len(self.region.coords)

    if not maxScales:
      maxScales = {}
      for p in pieces:
        if p.baseName not in maxScales:
          maxScales[p.baseName] = maxScale

    # print("Pieces")
    # print([p.name for p in pieces])
    # print("Recipe pieces")
    # print([p.name for p in recipePieces])
    # print("Max scales")
    # print(maxScales)
    # input()

    if self.allow_crafting:
      for output, blueprints in available_blueprints.items():

        #Crafted letters are only ever useful when covering a letter clue.
        #If no clue exists for that letter, don't even bother crafting.
        if not any([c[1] == output[0] for c in self.region.clues]):
          continue
        for b in blueprints:
          is_craftable, used_pieces = self._canCraftBlueprint(pieces, b)
          # print([p.name for p in pieces], output, b, is_craftable, used_pieces)
          # input()
          if is_craftable:
            # print("Crafting piece",output,"with blueprint",b)
            crafted_piece = letters[output[0]].clone()
            if len(output) == 3: #scaled name:
              crafted_piece = crafted_piece.scale(int(output[2]))
            crafted_piece.blueprint = b
            new_pieces = [crafted_piece] + [p for p in pieces if p not in used_pieces]
            sub_blueprints = {k:v for k,v in available_blueprints.items() if k >= output}
            # print("New pieces")
            # print([p.name for p in new_pieces])
            recipes.extend(self._generateAllPossibleRecipes(new_pieces, available_blueprints = sub_blueprints))

    # print("Scaling piece with name",pieces[0].name)
    # print("Max scale:",maxScales[pieces[0].baseName])
    for mult in range(1, maxScales[pieces[0].baseName] + 1):
      othersArea = sum(len(p.coords) for p in pieces[1:]) + sum(len(p.coords) for p in recipePieces)
      myArea = len(pieces[0].coords)
      if othersArea + myArea * mult * mult > regionArea:
        break
      
      newPiece = pieces[0].scale(mult)
      newPiece.blueprint = pieces[0].blueprint

      subMaxScales = copy.copy(maxScales)
      subMaxScales[pieces[0].baseName] = mult
      # print("Current scale",mult)
      
      if len(pieces) > 1:
        recipes.extend(self._generateAllPossibleRecipes(pieces[1:], recipePieces + [newPiece], maxScales=subMaxScales, available_blueprints = {}))
      else:
        recipes.extend([recipePieces + [newPiece]])
    
    # print("Returning recipes")
    # for r in recipes:
    #   print([p.name for p in r])
    # print()
    # input()
    return recipes

  # Oh boy, that's where the Abdec magic happens.
  # This will include scaling and crafting, making multiple matrices if need be...
  # If formatting is added, there may even be gimmicks with interacting virtual grids...
  def _generateAllPossibleConfigurations(self, piece):
    places = []
    uniqueConfigs = []

    for rotation in [0, 1, 2, 3]:
      for reflected in ([False, True] if self.allow_flipping else [False]):
        config = piece.rotate(rotation)
        if reflected:
          config = config.reflect()
        config = config.normalize()

        # Account for symmetries
        # Two configs are the same iff their normalizations are equal
        if any(c.equals(config) for c in uniqueConfigs):
          continue

        uniqueConfigs.append(config)

        for r in self.regions:

          for dx in range(r.getSmallestX(), r.getLargestX() + 1):
            for dy in range(r.getSmallestY(), r.getLargestY() + 1):
              place = config.translate(dx, dy)
              place.setRegion(r)
              if (self._fits(place)):
                places.append(place)

    return places

  def convertToDlx(self):

    totalPieceCoords = sum(len(p.coords) for p in self.pieces)
    regionArea = len(self.region.coords)

    t0 = time.time()

    if self.allow_formatting:
      self._generateVirtualRegions()
    else:
      self.overlapMatrix = np.identity(len(self.region.coords))

    subproblems = []
    # print("regions",time.time() - t0)

    t0 = time.time()

    recipes = self._generateAllPossibleRecipes(self.pieces)

    # print("Recipes",time.time() - t0)

    all_configs = {}

    t1 = time.time()
    for recipe in recipes:

      for c in self.region.critters:
        c[1] = False
      
      for c in self.region.clues:
        c[2] = False

      piece_names = [p.name for p in recipe]

      # Columns are indexed by pieces followed by region coordinates:
      # p_1 p_2 p_3 ... p_n | (x0, y0) (x1, y1) (x2, y2) ... (xk, yk)

      # Each row will assert that piece p_i may exist at certain coordinates in the region, which
      # is indicated by placing a 1 at column p_i and 1's at the columns of the coordinates it occupies.
      # A solution is then a subset of rows so that 1 appears exactly once in each column.

      recipe.sort(key = lambda p: -len(p.coords))

      # The first row is a sort of metadata that indicates if this column is essential or not.
      # All piece-columns are essential (because all pieces must be placed).
      # Tile-columns are only essential if they must be covered (critters, letter-clues).
      # The solving algorithm doesn't halt when the submatrix is empty, but rather, when none of the remaining columns are essential.

      #The second row is an index for the type of column. 0 = Column piece, 1 = Main region, 2+ = Virtual regions.
      headerRow1 = [1] * len(recipe)
      headerRow2 = [0] * len(recipe)
      for k, r in enumerate(self.regions):
        headerRow1 += [0] * len(r.coords)
        headerRow2 += [k + 1] * len(r.coords)
      
      rowSize = len(headerRow1)

      for c in self.region.critters:
        tileIndex = self.region.coords.index(c[0])
        headerRow1[tileIndex + len(recipe)] = 1

        for k, r in enumerate(self.regions[1:]): #Increment essentiality of overlapping tiles in virtual regions (Jessie what the fuck are you talking about?)
          virtual_overlaps = np.where(self.overlapMatrix[r.col:r.col + len(r.coords),tileIndex] == 0.2)[0]
          if len(virtual_overlaps) > 0:
            overlapping, _ = self._getOverlappingCoords(c[0], self.region, r) #Including cells not in the virtual grid, so different from virtual_overlaps.
            for v in virtual_overlaps:
              headerRow1[r.col + v + len(recipe)] += 1 / len(overlapping)
              r.critters.append([r.coords[v], True])

      for c in self.region.clues:
        tileIndex = self.region.coords.index(c[0])
        headerRow1[tileIndex + len(recipe)] = 1

        for k, r in enumerate(self.regions[1:]): #Increment essentiality of overlapping tiles in virtual regions (Jessie what the fuck are you talking about?)
          virtual_overlaps = np.where(self.overlapMatrix[r.col:r.col + len(r.coords),tileIndex] == 0.2)[0]
          if len(virtual_overlaps) > 0:
            overlapping, _ = self._getOverlappingCoords(c[0], self.region, r)
            for v in virtual_overlaps:
              headerRow1[r.col + v + len(recipe)] += 1 / len(overlapping)
              r.clues.append([r.coords[v], c[1], True])

      self.matrix = [headerRow1, headerRow2]

      validRecipe = True
      for clue in self.region.clues:
        print(clue, [p.baseName for p in recipe])
        if not any(p.baseName == clue[1] for p in recipe):
          print("Impossible to match the letter clues with this recipe. Ignoring.")
          validRecipe = False
          break
      
      print("a")
      
      if not validRecipe:
        continue

      print("testing recipe")

      for k, piece in enumerate(recipe):

        print(k, piece)

        config_datas = all_configs.get(piece.name)

        if not config_datas:
          configs = self._generateAllPossibleConfigurations(piece)
          # print(f"Found {len(configs)} possible placements of piece number {k + 1} ({piece.name}).")
          # input()

          if len(configs) == 0:
            # print("Invalid recipe. Ignoring.")
            validRecipe = False
            break

          final_configs = []

          for config in configs:

            clued = False
            adjacent = []
            #A config will be discarded if it's adjacent to a letter-clue, or if it overlaps a clue of the wrong letter.
            #If the config overlaps a correct clue, its adjacent tiles will be set to 0.3 in its matrix row.
            if len(config.region.clues) > 0:
              adjacent = config.getAdjacentCoords()

              valid = True

              for clue in config.region.clues:
                #If you're in the main region and adjacent to a clue, discard
                if clue[0] in adjacent and config.region == self.region:
                  valid = False
                  break
                
                if clue[0] in config.coords:
                  if clue[1] == config.baseName:
                    #If you're in the main region and adjacent to a critter while clued, discard
                    # print("I am clued")
                    # print(self.region.critters)
                    # print(adjacent)
                    # print([critter in adjacent for critter in config.region.critters])
                    # input()
                    if config.region == self.region and any([critter[0] in adjacent for critter in config.region.critters]):
                      valid = False
                    else:
                      clued = True
                  else: #If you're in any region and overlapping a clue of a different letter, discard
                    valid = False
                    break

              
              if not valid:
                continue #Discard this piece placement

              #Crafted letters are only ever useful when covering a letter clue.
              #If a letter is crafted, disregard any placement where it isn't clued.
              if config.blueprint is not None and not clued:
                continue
            
            final_configs.append({'config': config, 'clued': clued, 'adjacent': adjacent})
          
          config_datas = final_configs
          all_configs[piece.name] = config_datas

        for config_data in config_datas:

          config = config_data['config']
          clued = config_data['clued']
            
          #Some critters/clues still haven't been covered by a config. They all need to be coverable for this subproblem to be solvable.
          uncovered_critters = [c for c in self.region.critters if not c[1]]
          uncovered_clues = [c for c in self.region.clues if not c[2]]
          if len(uncovered_critters + uncovered_clues):
            # print("Uncovering")
            # print(uncovered_critters, uncovered_clues)
            for c in config.coords:
              changed = False
              overlap = [c]
              if config.region != self.region:
                overlap, _ = self._getOverlappingCoords(c, config.region, self.region)
              
              # if len(config.coords) == 12:
              # print([p.name for p in recipe])
              # print(config.coords)
              # print(overlap)
              # print(uncovered_clues)
              # input()

              # print(overlap, uncovered_critters)
              for cc in uncovered_critters:
                if cc[0] in overlap:
                  # print("Bap")
                  # input()
                  cc[1] = True
                  changed = True
              for cc in uncovered_clues:
                if cc[0] in overlap:
                  # print("Yippee")
                  cc[2] = True
                  changed = True
                  # print(uncovered_clues)
                  # print(self.region.clues)
              
              if changed:
                uncovered_critters = [cc for cc in self.region.critters if not cc[1]]
                uncovered_clues = [cc for cc in self.region.clues if not cc[2]]
                if not len(uncovered_critters + uncovered_clues):
                  break

          row = [0] * rowSize

          regionIdx = self.regions.index(config.region)
          offset = len(recipe) + sum([len(r.coords) for r in self.regions[:regionIdx]])

          for c in config.coords:
            ind = config.region.coords.index(c)
            row[offset + ind] = 1

          row[k] = regionIdx + 1 #Piece index

          row_mult = np.matmul(self.overlapMatrix, row[len(recipe):]).tolist()

          for kk,v in enumerate(row_mult):
            if v != 0 and row[kk + len(recipe)] != 1:
              row_mult[kk] = .3

          row = row[:len(recipe)] + row_mult
          
          if clued:
            for a in config_data['adjacent']:
              if a in config.region.coords:
                tileIndex = config.region.coords.index(a)
                regionIdx = self.regions.index(config.region)
                offset = len(recipe) + sum([len(r.coords) for r in self.regions[:regionIdx]])
                row[tileIndex + offset] = 0.2

          self.matrix.append(row)

      # print([p.name for p in recipe])
      # print([len(p.coords) for p in recipe])
      # print(self.region.critters)
      # print(self.region.clues)
      impossible_critters = [c for c in self.region.critters if not c[1]]
      if len(impossible_critters):
        # print("These critters cannot ever be covered by a shape, so no solution exists. Returning")
        # print(impossible_critters)
        validRecipe = False

      impossible_clues = [c for c in self.region.clues if not c[2]]
      if len(impossible_clues):
        # print("These clues cannot ever be covered by a shape, so no solution exists. Returning")
        # print(impossible_clues)
        validRecipe = False
      
      if not validRecipe:
        continue

      self.matrix = np.vstack(self.matrix)

      #Serves as an offset for all the virtual essentiality we added in the virtual regions' columns.
      base_essentiality = np.sum(self.matrix[0,len(recipe) + len(self.region.coords):])

      subproblems.append({'matrix': self.matrix, 'recipe': recipe, 'base_essentiality': base_essentiality})

    # print("b",time.time() - t1)

    def findOneIndices(arr):
      return [k for k,v in enumerate(arr) if v == 1]

    # In our case, some indices are 0<x<1, to account for Abdec's adjacency rules.
    def findPositiveIndices(arr):
      return [k for k,v in enumerate(arr) if v > 0]

    #This takes the solution rows and turns them back into (placed) shapes.
    def interpreter(solution_data):
      if solution_data == []:
        # print("No solution was found for this puzzle.")
        return
      
      recipe, solution = solution_data
      pieces = []
      
      for row in solution:
        regionIndex = next(p for p in row if p >= 1)
        pieceIndex = next(i for i,p in enumerate(row) if p > 0)
        region = self.regions[int(regionIndex) - 1]
        pieceCoordsIndices = [k for k, v in enumerate(row[len(solution) + region.col : len(solution) + region.col + len(region.coords)]) if v == 1]
        pieceCoords = [region.coords[k] for k in pieceCoordsIndices]

        offset = 0
        
        piece = Polyomino(pieceCoords, recipe[pieceIndex].name, blueprint = recipe[pieceIndex].blueprint)
        piece.setRegion(region)
        pieces.append(piece)

      return pieces

    return {'problems': subproblems, 'interpreter': interpreter}
  
  def solve(self, is_auto=True, return_all_solutions=True):

    t0 = time.time()
    
    convertedProblem = self.convertToDlx()
    t1 = time.time()

    # print("Regions")
    # for r in self.regions:
    #   print(r.dx, r.dy, r.ox, len(r.coords))
    
    # input()

    solutions = solveProblems(convertedProblem['problems'], return_all_solutions=return_all_solutions, is_auto = is_auto)
    solutions = trim_duplicate_solutions(solutions)
    t2 = time.time()
    # print(t1 - t0)
    # print(t2 - t1)
    print("Solutions")
    for solution in solutions:
      for s in solution:
        print(s)
      
    solutions = [convertedProblem['interpreter'](solution) for solution in solutions]

    complete_solutions = []

    for solution in solutions:
      craft_solutions = []
      for p in solution:
        if p.blueprint is None: #p is actally "crafted" with subpieces! Recursively solve for their placements.
          if len(craft_solutions):
            craft_solutions = [c + [p] for c in craft_solutions]
          else:
            craft_solutions = [[p]]
        else:
          subproblem = PolyominoProblem(
            abdec(p.blueprint),
            p.clone(),
            allow_formatting = False,
            allow_crafting = False,
            allow_flipping = True
          )

          for c in subproblem.region.coords:
            subproblem.region.critters.append([c, True])

          #The piece's coords will be normalized, keep track of their current offset.
          x0 = min(p.coords)[0]
          y0 = min(p.coords, key = lambda x: x[1])[1]

          sub_solutions = subproblem.solve()
          sub_solutions = [[pp.translate(x0, y0) for pp in sub_solution] for sub_solution in sub_solutions]
          [[pp.setRegion(p.region) for pp in sub_solution] for sub_solution in sub_solutions]
          if len(craft_solutions):
            craft_solutions = [c + sub_solution for c in craft_solutions for sub_solution in sub_solutions]
          else:
            craft_solutions = sub_solutions

      complete_solutions.extend(craft_solutions)
    
    return complete_solutions


