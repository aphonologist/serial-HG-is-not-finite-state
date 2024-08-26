def harmony(x):
  h = 0
  # ident, dep, STOP, *ab, maxC, *caa, *baca, maxA, maxB
  ws = [5,   5,    4,   4,    5,    2,     1,    1,    1]
  for i in range(9):
    h += ws[i] * x[i]
  return h

def stop(x):
  v = 0
  if x[:2] == 'ac':
      v += 1
  if x[-2:] == 'ca':
      v += 1
  if x[:5] == 'aacab':
      v += 1
  if x[-5:] == 'bacaa':
      v += 1
  return v

def ab(x):
  v = 0
  for i in range(len(x)):
    if x[i:i+2] in {'ab', 'ba'}:
      v += 1
  return v

def caa(x):
  v = 0
  for i in range(len(x)):
    if x[i:i+3] in {'caa', 'aac', 'cbb', 'bbc'}:
      v += 1
  return v

def baca(x):
  v = 0
  for i in range(len(x)):
    if x[i:i+4] in {'baca','acba','abcb','bcab'}:
      v += 1
  return v

# memoization to save time
memo = {}

for m in range(1,50):
  for n in range(1,50):
    # sanity printing
    if m == n:
      print(m,n)
      continue

  ur = 'aabb' * (m+1) + 'aacaa' + 'bbaa' * (n+1)
  input = ur
  if m > n:
    expected = 'aabb' * (m-n) + 'aacaa'
  if m < n:
    expected = 'aacaa' + 'bbaa' * (n-m)

  # collect intermediate representations to memoize
  irs = set()

  while True:
    irs.add(input)
    # faithful candidate
    best_cand = input
    # ident, dep, STOP, *ab, maxC, *caa, *baca, maxA, maxB
    vios = [0,0,stop(best_cand),ab(best_cand),0,caa(best_cand),baca(best_cand),0,0]
    best_harm = harmony(vios)

    # make one change
    for i in range(len(input)):
      for seg in 'abc':
        new_cand = input[:i] + seg + input[i+1:]
        # ident, dep, STOP, *ab, maxC, *caa, *baca, maxA, maxB
        new_vios = [1,0,stop(new_cand),ab(new_cand),0,caa(new_cand),baca(new_cand),0,0]
        new_harm = harmony(new_vios)
        if new_harm < best_harm:
          best_cand = new_cand
          best_harm = new_harm

    # insert one segment
    for i in range(len(input)):
      for seg in 'abc':
        new_cand = input[:i] + seg + input[i:]
        # ident, dep, STOP, *ab, maxC, *caa, *baca, maxA, maxB
        new_vios = [0,1,stop(new_cand),ab(new_cand),0,caa(new_cand),baca(new_cand),0,0]
        new_harm = harmony(new_vios)
        if new_harm < best_harm:
          best_cand = new_cand
          best_harm = new_harm

    # delete one segment
    for i in range(len(input)):
      deleted = input[i]
      new_cand = input[:i] + input[i+1:]
      # ident, dep, STOP, *ab, maxC, *caa, *baca, maxA, maxB
      new_vios = [0,0,stop(new_cand),ab(new_cand),0,caa(new_cand),baca(new_cand),0,0]
      if deleted == 'c':
        new_vios[4] = 1
      elif deleted == 'a':
        new_vios[7] = 1
      else:
        new_vios[8] = 1
      new_harm = harmony(new_vios)
      if new_harm < best_harm:
        best_cand = new_cand
        best_harm = new_harm

    # check for convergence
    if input == best_cand:
      break

    # optimal candidate is new input
    input = best_cand
    
    # check for previously computed
    if input in memo:
      best_cand = memo[input]
      break

  # print if there's an unexpected surface form
  sr = best_cand
  if not sr == expected:
    print(m, n, ur, expected, sr)
  
  # update memoization
  for ir in irs:
    if ir not in memo:
      memo[ir] = sr
