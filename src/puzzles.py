from Polyomino import Polyomino, tetrominos, letters
from PolyominoProblem import PolyominoProblem, abdec

puzzles = {
  '1': PolyominoProblem(
    abdec('a'),
    Polyomino.fromString(
      '''
      .O
      OO
      '''
    ),
  ),

  '2': PolyominoProblem(
    abdec('b'),
    Polyomino.fromString(
      '''
      .O
      OO
      .OO
      '''
    ),
  ),

  '3': PolyominoProblem(
    abdec('ab'),
    Polyomino.fromString(
      '''
      ....O
      OO.OO
      .OOO
      ..O
      '''
    ),
  ),

  '4': PolyominoProblem(
    abdec('aabb'),
    Polyomino.fromString(
      '''
      .OOO
      OOO.
      O.OO
      .OOO
      '''
    ),
  ),

  '5': PolyominoProblem(
    abdec('bbbbb'),
    Polyomino.fromString(
      '''
      OOOOO
      .OOOO
      OO.OO
      .OOOO
      '''
    ),
  ),

  '6': PolyominoProblem(
    abdec('a'),
    Polyomino.fromString(
      '''
      OOO
      O*O
      **O
      '''
    ),
  ),

  '7': PolyominoProblem(
    abdec('bb'),
    Polyomino.fromString(
      '''
      OOO
      O*O
      O.O
      '''
    ),
  ),

  '8': PolyominoProblem(
    abdec('aaab'),
    Polyomino.fromString(
      '''
      .OOO
      OOOO*
      OOOO
      ...*
      '''
    ),
  ),

  '9': PolyominoProblem(
    abdec('aabbb'),
    Polyomino.fromString(
      '''
      ..OO
      .OOOO
      .O.OOO
      *O*O
      ..OO
      ..*
      '''
    ),
  ),

  '10': PolyominoProblem(
    abdec('a'),
    Polyomino.fromString(
      '''
      .aOO
      .O.O
      OO
      '''
    ),
  ),

  '11': PolyominoProblem(
    abdec('bb'),
    Polyomino.fromString(
      '''
      OObObOO
      '''
    ),
  ),

  '12': PolyominoProblem(
    abdec('bb'),
    Polyomino.fromString(
      '''
      OOOOObO
      OOObOOO
      '''
    ),
  ),

  '13': PolyominoProblem(
    abdec('ab'),
    Polyomino.fromString(
      '''
      OaO
      O.O
      OOO
      ..O
      '''
    ),
  ),

  '14': PolyominoProblem(
    abdec('aaaa'),
    Polyomino.fromString(
      '''
      OO.O*
      OOaOO
      OOOOO
      OO*OO
      '''
    ),
  ),

  '15': PolyominoProblem(
    abdec('aaabbb'),
    Polyomino.fromString(
      '''
      OObOO
      OOOOO
      OOOOOa
      .OOOOO
      ..O*OO
      ..OOa
      '''
    ),
  ),

  '16': PolyominoProblem(
    abdec('bbbbbbb'),
    Polyomino.fromString(
      '''
      O
      OOOO*O
      O.OO.O
      OOOOOO
      .O.OO
      .OOOO
      .ObbO
      '''
    ),
  ),

  '17': PolyominoProblem(
    abdec('ac'),
    Polyomino.fromString(
      '''
      .OO
      OaO
      .O
      '''
    ),
  ),

  '18': PolyominoProblem(
    abdec('aabcc'),
    Polyomino.fromString(
      '''
      OOOO
      cOOO
      OOOO
      OOOc
      '''
    ),
  ),

  '19': PolyominoProblem(
    abdec('aabbc'),
    Polyomino.fromString(
      '''
      .O
      O*
      *O*O*O
      .*.O.O
      .*.*.O
      '''
    ),
  ),

  '20': PolyominoProblem(
    abdec('abccccc'),
    Polyomino.fromString(
      '''
      OO*OO
      OOOOc
      OObOO
      O.OOO
      '''
    ),
  ),

  '21': PolyominoProblem(
    abdec('bbbbccc'),
    Polyomino.fromString(
      '''
      OOOOO
      OOOOO
      OOOOO
      OOOOa
      '''
    )
  ),

  '22': PolyominoProblem(
    abdec('ccccccccccccc'),
    Polyomino.fromString(
      '''
      OOOO
      *OaOO
      OaOaO
      OOaOO
      .OO*O
      '''
    )
  ),

  '23': PolyominoProblem(
    abdec('ab'),
    Polyomino.fromString(
      '''
      .OO
      OOOO
      Od
      O
      '''
    )
  ),

  '24': PolyominoProblem(
    abdec('d'),
    Polyomino.fromString(
      '''
      ..O
      *O*
      *OO
      .O
      '''
    )
  ),

  '25': PolyominoProblem(
    abdec('bbcd'),
    Polyomino.fromString(
      '''
      OOOO*
      OOOOO
      OOdOO
      OcOOO
      OO*OO
      '''
    )
  ),

  'cat_1': PolyominoProblem(
    abdec('aade'),
    Polyomino.fromString(
      '''
      OOOaOOOO
      OOOOOeOO
      OOOOOOO*OO
      O*O*OOOOOO
      OO*OOOO*eO
      OOOOOOOOOO
      O*OOOO*OOO
      OOOO
      '''
    )
  ),

  'blaz_1': PolyominoProblem(
    abdec('cccccc'),
    Polyomino.fromString(
      '''
      aOOOOOOOOO
      OOOOOOaOOOO
      OOOOOOOOOaO
      OOOOOOOOOOO
      OOOOOOOOOO
      OOOOaOOOOO
      OOOOOOOOOO
      OOOOOOOOOO
      OOOOOOOOOO
      OOOOOOOOOa
      '''
    )
  ),

  'blaz_2': PolyominoProblem(
    abdec('cccccc'),
    Polyomino.fromString(
      '''
      aOOOOOOOOOOO
      OOOOOOOOOObO
      OOOOOOOOOOOO
      OOOOOObOOO
      OOOOOOOOOO
      OOOOOOOOOO
      OOOOOOOOOO
      OOOOOOOOOO
      OOOOOOOOOO
      OOOOOOOOOa
      '''
    )
  ),

  # 'test': PolyominoProblem(
  #   abdec('accc'),
  #   Polyomino.fromString(
  #     '''
  #     .aOa
  #     OOOOO
  #     '''
  #   )
  # ),

  '26': PolyominoProblem(
    abdec('abbbdd'),
    Polyomino.fromString(
      '''
      OOOOO
      OOO.O
      OOOOO
      OO.O
      OO.O
      OOOO
      '''
    )
  ),

  '27': PolyominoProblem(
    abdec('aabb'),
    Polyomino.fromString(
      '''
      OOOOO
      OO*O*
      OOOdO
      O*OOO
      OOOdO
      '''
    )
  ),

  '28': PolyominoProblem(
    abdec('a'),
    Polyomino.fromString(
      '''
      OOOOOO
      OOOOOO
      OOO***
      OO****
      OO**OO
      *O**OO
      '''
    )
  ),

  '29': PolyominoProblem(
    abdec('ac'),
    Polyomino.fromString(
      '''
      *OOO
      OOOO
      OOO*
      O*O
      '''
    )
  ),

  '30': PolyominoProblem(
    abdec('ac'),
    Polyomino.fromString(
      '''
      OOO*
      OOOO
      OO*O
      *O*
      '''
    ),
  ),

  '31': PolyominoProblem(
    abdec('bbbb'),
    Polyomino.fromString(
      '''
      OOOOOO
      OOOOOO
      OObbOO
      '''
    ),
  ),

  '32': PolyominoProblem(
    abdec('cccc'),
    Polyomino.fromString(
      '''
      OOOOOO
      OO*O*O
      OOOdOO
      OO*OOO
      OOOOOO
      *O..OO
      '''
    ),
  ),

  '33': PolyominoProblem(
    abdec('aaaaaaaab'),
    Polyomino.fromString(
      '''
      ..O
      OOOOO
      OOO*O
      OOOOO
      OO*Oa
      OOOOO
      OOO*O
      OOOOO
      '''
    ),
  ),

  '34': PolyominoProblem(
    abdec('bccd'),
    Polyomino.fromString(
      '''
      OOOcO*O
      OOOcOOO
      ObOOOOO
      OOOOOOO
      ..OOO
      ..*O*
      '''
    ),
  ),

  '35': PolyominoProblem(
    abdec('bbbbc'),
    Polyomino.fromString(
      '''
      eOeeOe
      eOeOeO
      ....OO
      ....ee
      '''
    ),
  ),

  '35E': PolyominoProblem(
    abdec('bbbbc'),
    Polyomino.fromString(
      '''
      EOEEOE
      EOEOEO
      ....OO
      ....EE
      '''
    ),
  ),

  '36': PolyominoProblem(
    abdec('abe'),
    Polyomino.fromString(
      '''
      ..eO*O*O
      *OOOOOO*
      .OOOOOOO
      ..OOO*O*
      '''
    ),
  ),

  '36E': PolyominoProblem(
    abdec('abE'),
    Polyomino.fromString(
      '''
      ..EO*O*O
      *OOOOOO*
      .OOOOOOO
      ..OOO*O*
      '''
    ),
  ),

  '37': PolyominoProblem(
    abdec('ace'),
    Polyomino.fromString(
      '''
      OO..Oc
      OOO*OO
      O*OOO*
      OOO*OO
      OO..OO
      '''
    ),
  ),

  '37E': PolyominoProblem(
    abdec('acE'),
    Polyomino.fromString(
      '''
      OO..Oc
      OOO*OO
      O*OOO*
      OOO*OO
      OO..OO
      '''
    ),
  ),

  '38': PolyominoProblem(
    abdec('aaac'),
    Polyomino.fromString(
      '''
      OO.eO
      OOOOO
      OOOOO
      OOOOO
      OOOO.
      OeOOO
      '''
    ),
  ),

  '39': PolyominoProblem(
    abdec('b'),
    Polyomino.fromString(
      '''
      OOOO
      O*OO
      OO*O
      OOOO
      '''
    ),
  ),

  '40': PolyominoProblem(
    abdec('aaac'),
    Polyomino.fromString(
      '''
      aO
      OOOOa
      .OOO.
      .OO..
      .a...
      '''
    ),
  ),

  '41': PolyominoProblem(
    abdec('aaa'),
    Polyomino.fromString(
      '''
      .*OOOO*
      .OOOOOO
      .OOOOOO
      OOOOOOOO
      OaOOOOaO
      .OO..OO.
      '''
    ),
  ),

  '42': PolyominoProblem(
    abdec('aabc'),
    Polyomino.fromString(
      '''
      OOOb
      O*OO
      O*OO
      O**O
      O**O
      OOOc
      '''
    ),
  ),

  '43': PolyominoProblem(
    abdec('bcde'), #bcde
    Polyomino.fromString(
      '''
      .OOOOOOOO*
      OOOOOOOObO
      OOOOOOOOOO
      OOOOOcOO*O
      OOOOOOOOOO
      OO*OO*O
      O*O*OOO
      .OOOOOO
      '''
    ),
  ),

  '44': PolyominoProblem(
    abdec('abcd'),
    Polyomino.fromString(
      '''
      OOOOOO
      OaO*OO
      cOOOOO
      OOOOdO
      OObOOO
      ObO*OO
      OOOOOO
      '''
    ),
  ),

  'tyzone_1': PolyominoProblem(
    abdec('cy'),
    Polyomino.fromString(
      '''
      OOOOOO
      OOOOOO
      OO**OO
      OO**OO
      OOOOOO
      OOOOOO
      '''
    ),
  ),

  # 'iq': PolyominoProblem(
  #   abdec('abcdefghijkl'),
  #   Polyomino.fromString(
  #     '''
  #     ***********
  #     ***********
  #     ***********
  #     ***********
  #     ***********
  #     '''
  #   ),

  # ),

  # 'iq2': PolyominoProblem(
  #   abdec('abcdefghijkl'),
  #   Polyomino.fromString(
  #     '''
  #     OOOOOOOOOOO
  #     OOOOOOOOOOO
  #     OOOOOOOOOOO
  #     OOOOOOOOOOO
  #     OOOOOOOOOOO
  #     '''
  #   ),

  # ),

  'advent1': PolyominoProblem(
    abdec('abd'),
    Polyomino.fromString(
      '''
      ..OO
      *OOOOO
      OOOO*O
      OOOOO
      OOO*aO
      .*OOOO
      .OO*OO
      .OO
      '''
    ),
  ),

  'advent2': PolyominoProblem(
    abdec('abd'),
    Polyomino.fromString(
      '''
      ..OO
      *OOOOO
      OOOO*O
      OOOOOOO*
      OOOdOOOO
      OdOO*OOO
      OOOOOOOO
      ..OO
      '''
    ),
  ),

  'advent3': PolyominoProblem(
    abdec('abd'),
    Polyomino.fromString(
      '''
      ..OOOO
      OOdOOO
      OOOObO
      OOOOOOO*
      OOOOOOOO
      OO*O*OOO
      OOOOOOOO
      ..OO
      '''
    ),
  ),

  'advent3_meta': PolyominoProblem(
    abdec('FGHJ'),
    Polyomino.fromString(
      '''
      OOOOOO
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      '''
    ),
  ),

  'advent3_meta': PolyominoProblem(
    abdec('FGHJ'),
    Polyomino.fromString(
      '''
      OOOOOO
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      '''
    ),
  ),

  'advent3_meta2': PolyominoProblem(
    abdec('FGHJ'),
    Polyomino.fromString(
      '''
      OOOOOO
      OOOOOO
      OOOOOO
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      .OOOOOOO
      '''
    ),
  ),

  'advent3_A': PolyominoProblem(
    abdec('abd'),
    Polyomino.fromString(
      '''
      OO*OOO
      OOOOOb
      O*OOO
      OOOOd.OO
      OOO.OOOO
      OObO*OOO
      OOOOOOO
      ..OOOOO
      '''
    ),
  ),

  'advent3_B': PolyominoProblem(
    abdec('abd'),
    Polyomino.fromString(
      '''
      OOOOOO
      OObOO
      OOOOO
      OdOOO*O
      .OOO.OOO
      *OOOObOO
      OO*OOOO
      OOOOOOO
      '''
    ),
  ),

  'advent3_C': PolyominoProblem(
    abdec('abd'),
    Polyomino.fromString(
      '''
      ..OOOO
      OOdOOO
      OOOObO
      OOOOO*O
      ..OOOOOO
      *OOOObOO
      OO*OOOO
      OOOOOOO
      '''
    ),
  ),

  'advent3_D': PolyominoProblem(
    abdec('abd'),
    Polyomino.fromString(
      '''
      OOO*O
      OObOOO
      OO.bOOOO
      OdOOOOOO
      .OOOOOOO
      *OOOOOO
      OO*OOOO
      OOOO
      '''
    ),
  ),

  'advent3_E': PolyominoProblem(
    abdec('abd'),
    Polyomino.fromString(
      '''
      ..OOOO
      OOdOOO
      OOOObO
      OOOOOO
      OOOOOOOO
      OObO*O*O
      OOOOOOOO
      ..OO.*OO
      '''
    ),
  ),

  'advent3_F': PolyominoProblem(
    abdec('abd'),
    Polyomino.fromString(
      '''
      ..OOOO
      OOdOOO
      OOOObO
      OOOOOOO*
      OOOOOOOO
      OObO*O*O
      OOOOOOOO
      ..OO...O
      '''
    ),
  ),

  'advent3_meta3': PolyominoProblem(
    abdec('FGHJ'),
    Polyomino.fromString(
      '''
      .OOOOOO.
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      .OOOOOO.
      '''
    ),
  ),

  'advent3_meta4': PolyominoProblem(
    abdec('fghj'),
    Polyomino.fromString(
      '''
      .OOOOOO.
      OOOOOOOO
      OOOOOOOO
      OOO.OOOO
      OOOOOOOO
      OOOOOOOO
      OOOOOOOO
      .OOOOOO.
      '''
    ),
  ),

  'advent3_meta4_C': PolyominoProblem(
    abdec('abd'),
    Polyomino.fromString(
      '''
      .O..OOO.
      *OOOObOO
      OOO*OOOO
      OaO.OOOO
      OOOOOOOO
      OOOOOOOO
      .ObOOO.O
      .OOOO...
      '''
    ),
  ),

  'advent3_letibus': PolyominoProblem(
    abdec('aabbccde'),
    Polyomino.fromString(
      '''
      .OaOOOOOOOOO
      OOOOOOOOOOOOO
      O*O*O*O*O*O*O
      OOOOOOOOOOaOOO
      OObOOOOOOOOOOO
      .OO........OO.
      '''
    ),
  ),

  'advent3_letibus2': PolyominoProblem(
    abdec('aabbccde'),
    Polyomino.fromString(
      '''
      .OaOOOOOOOOO
      OOOOOOOOOOOOO
      .O*OO*OO*OO*O
      OOOOOOOOOOOObO
      OObOOOOOOOOOOO
      .OO........OO.
      '''
    ),
  ),

  'advent3_letibus3': PolyominoProblem(
    abdec('aabcde'),
    Polyomino.fromString(
      '''
      .OaOOOOOOOOO
      OO*O*O*O*O*OO
      .OOOOOOOOOOOO
      O*O*O*OOOOd*OO
      OObOOOOOOOOOOO
      .OO........OO.
      '''
    ),
  ),

  'advent3_letibus4': PolyominoProblem(
    abdec('abbdec'),
    Polyomino.fromString(
      '''
      .ObOOOOOOOOO
      ..OOO*O*O*.*.
      .OOOOOOOOe.OO
      O*O*O*O*O*OOOO
      OObOOOOOOOOOOO
      .OO........OO.
      '''
    ),
  ),

  'advent3_letibus4_adult': PolyominoProblem(
    abdec('bbde'),
    Polyomino.fromString(
      '''
      .ObOOOOOOOO.
      ..OOOOOOOO.O.
      .OOOOOOOOe.OO
      O.OOOOOOOOOOOO
      .ObOOOOOOOOOOO
      .OO........OO.
      '''
    ),
  ),

  'advent3_meta4_A': PolyominoProblem(
    abdec('abd'),
    Polyomino.fromString(
      '''
      .OOOO*O.
      OOObOOOO
      ..OOOObO
      OOO.OOOO
      OaOOOOO.
      OOOOOOOO
      OO*OOOOO
      .O...OO.
      '''
    ),
  ),

  'advent3_meta4_B': PolyominoProblem(
    abdec('abd'),
    Polyomino.fromString(
      '''
      .O..OO..
      *OOOOOOO
      OOOOOOOO
      OaO.OOOO
      OOOOObOO
      OOO*OOOO
      .ObOOOOO
      .OOOO...
      '''
    ),
  ),

  'advent_hohoho_T': PolyominoProblem(
    abdec('hihihi'),
    Polyomino.fromString(
      '''
      OOhOOOi*
      hOO**OOO
      OO*OOO.O
      O*O*OOOi
      OOOOhOOO
      .O*OOO*O
      ..OO
      '''
    ),
  ),

  'herb': PolyominoProblem(
    abdec('herb'),
    Polyomino.fromString(
      '''
      OOOOOh
      OO*OOOOO
      OOOOOOOO
      OOOOO*O
      ..OOOOOO
      '''
    ),
  ),

  'herb2': PolyominoProblem(
    abdec('her'),
    Polyomino.fromString(
      '''
      OOOOOO
      hOOOOO
      OOOO
      OOOO
      '''
    ),
  ),

  'advent_hohoho_L': PolyominoProblem(
    abdec('hIhIhI'),
    Polyomino.fromString(
      '''
      OOhOOOI*
      hOO**OOO
      OO*OOO.O
      O*O*OOOI
      OOOOhOOO
      .O*OOO*O
      ..OO
      '''
    ),
  ),

  'lokdec1': PolyominoProblem(
    abdec('bee'),
    Polyomino.fromString(
      '''
      OOOOOOOOO
      OOO*OOOOO
      bOOOOOOOO
      bOOOOOOOO
      .OOOOOOOO
      eOOOOOO*O
      OeOOOOOOO
      OOOOOOOOO
      OOOOOOOOO
      OOOOOOOOO
      OOO
      '''
    ),
  ),

  'abdecfhr': PolyominoProblem(
    abdec('abdecfhr'),
    Polyomino.fromString(
      '''
      OO*OaOOO
      OOOOOOOO
      OOOOOOOO
      dOOO*OOO
      OOO*OOOb
      OOOOOOOO
      OOOOOOOO
      OOOeOOOO
      '''
    ),
  ),
  
}