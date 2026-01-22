_rotations = [
  lambda c: [c[0], c[1]],
  lambda c: [-c[1], c[0]],
  lambda c: [-c[0], -c[1]],
  lambda c: [c[1], -c[0]]
]

_reflect = lambda c: [-c[0], c[1]]

_getx = lambda c: c[0]
_gety = lambda c: c[1]

class Polyomino:

  def __init__(self, coords, name='', critters=[], clues=[], blueprint=None):
    if type(coords) == map:
      coords = list(coords)
    if type(critters) == map:
      critters = list(critters)
    if type(clues) == map:
      clues = list(clues)
    
    self.coords = coords
    self.critters = critters if len(critters) else []
    self.clues = clues if len(clues) > 0 else []
    self.name = name
    self.regionIdx = 0
    self.baseName = name[0] if len(name) > 0 else ''
    self.region = None
    self.blueprint = blueprint

    #Used in the definition of virtual grids (which indicate the placement of tilted pieces)
    self.dx = 1
    self.dy = 0
    self.ox = 0

    #Shortcut in regions to find the column of their first tile
    self.col = 0

  def fromString(msg):
    coords = []
    critters = []
    clues = []
    rows = msg.split('\n')
    kx, ky = 0, 0
    for r in rows:
      kx = 0
      for c in r:
        if c in ['O', '*', 'a', 'b', 'c', 'd', 'e', 'E', 'h', 'i', 'I']:
          coords.append([kx, ky])
          if c == '*':
            critters.append([[kx, ky], False])
          elif c != 'O':
            clues.append([[kx, ky], c, False])
        
        kx += 1
      ky += 1
    
    poly = Polyomino(coords, '_Region', critters, clues)
    
    return poly

  def clone(self):
    clone_poly = Polyomino(self.coords, self.name, self.critters, self.clues)
    clone_poly.setRegion(self.region)
    clone_poly.col = self.col
    clone_poly.blueprint = self.blueprint
    return clone_poly

  # Return an translated version with smallest possible non-negative coordinates
  # and coordinates sorted by ascending x then ascending y
  def normalize(self):
    smallestX = min(map(_getx, self.coords))
    smallestY = min(map(_gety, self.coords))
    p = self.translate(-smallestX, -smallestY)
    coords = sorted(p.coords)
    return Polyomino(coords, self.name, p.critters, p.clues, blueprint = self.blueprint)
  
  def setRegion(self, region):
    self.region = region
    self.dx = region.dx if region else 0
    self.dy = region.dy if region else 0
    self.ox = region.ox if region else 0

  # Strict comparison; i.e. the coordinates are identical as lists.
  def equals(self, p):
    return (len(self.coords) == len(p.coords)) and all(self.coords[k] == p.coords[k] for k in range(len(self.coords)))

  def isEmpty(self):
    return len(self.coords) == 0

  # Rotates n*90 degrees counter-clockwise
  def rotate(self, n):
    angle = n % 4
    return Polyomino(map(_rotations[angle], self.coords), self.name, blueprint = self.blueprint)

  def reflect(self):
    return Polyomino(map(_reflect, self.coords), self.name, blueprint = self.blueprint)

  def translate(self, dx, dy):
    t = lambda c: [c[0] + dx, c[1] + dy]
    t2 = lambda c: [[c[0][0] + dx, c[0][1] + dy], c[1]]
    t3 = lambda c: [[c[0][0] + dx, c[0][1] + dy], c[1], c[2]]
    return Polyomino(map(t, self.coords), self.name, map(t2, self.critters), map(t3, self.clues), blueprint = self.blueprint)

  def isDisjointFrom(self, other):
    for mine in coords:
        for theirs in other.coords:
            if mine[0] == theirs[0] and mine[1] == theirs[1]:
              return False
    return True
  
  def getAdjacentCoords(self):
    adjacent = []
    for c in self.coords:
      for offset in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
        newC = [c[0] + offset[0], c[1] + offset[1]]
        if newC not in adjacent and newC not in self.coords:
          adjacent.append(newC)

    return adjacent

  def getWidth(self):
    xs = list(map(_getx, self.coords))
    return max(xs) - min(xs) + 1
  
  def scale(self, mult):
    assert(mult == int(mult), "Scale multiplier must be an integer")
    
    new_coords = []
    for c in self.coords:
      for sx in range(mult):
        for sy in range(mult):
          new_coords.append([c[0] * mult + sx, c[1] * mult + sy])
    
    return Polyomino(new_coords, self.name + (f"*{mult}" if mult > 1 else ""), self.critters, self.clues)

  def getHeight(self):
      ys = list(map(_gety, self.coords))
      return max(ys) - min(ys) + 1

  def getSize(self):
    return max(self.getWidth(), self.getHeight())

  def getSmallestX(self):
    return min(map(_getx, self.coords))

  def getSmallestY(self):
    return min(map(_gety, self.coords))

  def getLargestX(self):
    return max(map(_getx, self.coords))

  def getLargestY(self):
    return max(map(_gety, self.coords))

  def containsCoordinate(self, c):
    return ([c[0], c[1]] in self.coords)

tetrominos = {
    'I': Polyomino([[0, 0], [0, 1], [0, 2], [0, 3]], 'I'),
    'O': Polyomino([[0, 0], [0, 1], [1, 1], [1, 0]], 'O'),
    'T': Polyomino([[0, 1], [1, 1], [1, 0], [2, 1]], 'T'),
    'J': Polyomino([[0, 0], [1, 0], [1, 1], [1, 2]], 'J'),
    'L': Polyomino([[0, 2], [0, 1], [0, 0], [1, 0]], 'L'),
    'S': Polyomino([[0, 0], [1, 0], [1, 1], [2, 1]], 'S'),
    'Z': Polyomino([[0, 1], [1, 1], [1, 0], [2, 0]], 'Z')
}

letters = {
    'a': Polyomino([[0, 0], [0, 1], [1, 0]], 'a'),
    'b': Polyomino([[0, 0], [0, 1], [0, 2]], 'b'),
    'c': Polyomino([[0, 0]], 'c'),
    'd': Polyomino([[0, 0], [0, 1], [0, 2], [1, 1], [1, 2], [2, 1]], 'd'),
    'e': Polyomino([[0, 0], [0, 3], [1, 0], [1, 1], [1, 2], [1, 3], [2, 3], [3, 2], [3, 3], [4, 2], [4, 3], [5, 2], [5, 3]], 'e'),
    'E': Polyomino([[0, 0], [0, 1], [0, 2], [1, 0]], 'E'),
    'y': Polyomino([[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]], 'y'),
    'F': Polyomino([[0, 0], [1, 0], [2, 0], [3, 0], [-1, 1], [0, 1], [1, 1], [2, 1], [3, 1], [2, 2], [3, 2]], 'F'),
    'G': Polyomino([[0, 0], [0, 1], [1, 1], [2, 1], [3, 1], [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [2, 3], [3, 3], [4, 3]], 'G'),
    'H': Polyomino([[0, 0], [1, 0], [0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [2, 3], [3, 3]], 'H'),
    'J': Polyomino([[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1], [0, 2], [1, 2], [2, 2], [0, 3], [1, 3], [2, 3], [0, 4]], 'J'),
    # 'f': Polyomino([[0, 0], [1, 0], [2, 0], [3, 0], [-1, 1], [0, 1], [1, 1], [2, 1], [3, 1], [2, 2], [3, 2]], 'F'), #backpack
    'g': Polyomino([[0, 0], [0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [2, 3], [3, 3]], 'G'), #fat italy
    # 'h': Polyomino([[0, 0], [1, 0], [0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [1, 3], [2, 3], [3, 3]], 'H'), #fat crewmate
    'j': Polyomino([[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1], [0, 2], [1, 2], [2, 2], [0, 3], [1, 3], [2, 3], [0, 4], [1, -1]], 'J'), #rando2

    'h': Polyomino([[0, 0], [1, 0], [0, 1], [1, 1], [0, 2]], 'h'), #herd h
    'i': Polyomino([[0, 1], [1, 1], [1, 0], [2, 1]], 'i'), #rose o aka T-tetromino (hohoho)
    'I': Polyomino([[0, 2], [0, 1], [0, 0], [1, 0]], 'I'), #rose fake o aka L-tetromino (hohoho)
    'r': Polyomino([[0, 0], [1, 0]], 'r'), #herd r,
    'f': Polyomino([[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [2, 1]], 'f')

}

fake_letters = {
  'a': Polyomino([[0, 0], [0, 1], [1, 0], [1, 1], [2, 1]], 'a'),
  'b': Polyomino([[0, 0], [1, 0], [1, 1], [2, 0], [3, 0]], 'b'),
  'c': Polyomino([[0, 0], [1, 0], [0, 1], [2, 0], [2, 1]], 'c'),
  'd': Polyomino([[0, 0], [1, 0], [1, 1], [2, 1], [2, 2]], 'd'),
  'e': Polyomino([[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]], 'e'),
  'f': Polyomino([[0, 0], [1, 0], [1, 1], [2, 1], [1, 2]], 'f'),
  'g': Polyomino([[0, 0], [1, 0], [2, 0], [2, 1]], 'g'),
  'h': Polyomino([[0, 0], [1, 0], [1, 1], [2, 1], [3, 1]], 'h'),
  'i': Polyomino([[0, 0], [1, 0], [1, 1], [2, 1]], 'i'),
  'j': Polyomino([[0, 0], [1, 0], [1, 1]], 'j'),
  'k': Polyomino([[0, 0], [1, 0], [1, 1], [2, 0]], 'k'),
  'l': Polyomino([[0, 0], [1, 0], [0,1], [0, 2], [0, 3]], 'l'),
  'E': Polyomino([[0,0]], 'E'),
  'y': Polyomino([[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]], 'y')
}


all_blueprints = {
  'a': ['ccc'],
  'b': ['ccc'],
  'c': [],
  'd': ['ab', 'ccc', 'hc'],
  'e': ['bbbbc', 'aaac'],
  'E': ['bbbbc'],
  'a*2': ['aaaa'],
  'b*2': ['bbbb'],
  'h*2': ['her', 'br', 'cc', 'ar'],
  'i': [],
  'I': []
  # 'd*2': ['ccc']
}