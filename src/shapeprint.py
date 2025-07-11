

color_formats = {
  'red': "\033[91m",
  'green': "\033[92m",
  'yellow': "\033[93m",
  'blue': "\033[94m",
  'purple': "\033[95m",
  'lightblue': "\033[96m"
}

colors = ['red', 'green', 'yellow', 'blue', 'purple', 'lightblue']

def cprint(color, msg, *args, **kwargs):
  if color in color_formats:
    print(f"{color_formats[color]}{msg}\033[00m", *args, **kwargs)
  else:
    print(*args, **kwargs)

def print_polyomino(p):
  x0, y0 = p.getSmallestX(), p.getSmallestY()
  x1, y1 = p.getLargestX(), p.getLargestY()

  msg = ''

  for y in range(y0 - 1, y1 + 2):
    if y > y0 - 1:
      msg += '\n'
    for x in range(x0 - 1, x1 + 2):
      if p.containsCoordinate([x, y]):
        msg += 'O'
      else:
        msg += '.'
  
  print(msg)


indicators = [str(k) for k in range(1,10)] + ['A', 'B', 'C', 'D', 'E', 'F']

def print_solution(regions, pieces):

  for kr, r in enumerate(regions):
    x0, y0 = r.getSmallestX(), r.getSmallestY()
    x1, y1 = r.getLargestX(), r.getLargestY()

    msg = ''
    print(r.dx,",", r.dy,"/",r.ox)

    for y in range(y0 - 1, y1 + 2):
      if y > y0 - 1:
        print()
      for x in range(x0 - 1, x1 + 2):
        if not r.containsCoordinate([x, y]):
          print('.', end='')
          continue
        
        foundPiece = False
        for k, p in enumerate(pieces):
          if p.region != r and not (p.region is None and kr == 0):
            continue
          if p.containsCoordinate([x, y]):
            foundPiece = True
            cprint(colors[k % len(colors)], indicators[k], end='')
            break
        
        if not foundPiece:
          print('O', end='')
    
    print("\n")