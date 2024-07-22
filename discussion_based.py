def discussion_based(G , threshhold) :
  n = G.number_of_nodes()
  nodes = list(G.nodes())
  zeros = [0 for _ in range(n)]
  pred = [list(G.predecessors(i)) for i in G.nodes()]
  step = [len(l) for l in pred]
  mat = []
  mat.append(step)

  index = 1
  while( (not (step == zeros)) and index <= threshhold) :
    index = index +1  
    dis = [[] for _ in range(n)]
    
    for i in range(n) :
      for j in pred[i] :
        for k in list(G.predecessors(j)) :
          dis[i].append( k )
          dis[i] = list(set(dis[i]))

    if index % 2 == 0 :
      step =  [-len(l) for l in dis]
    else :
      step =  [len(l) for l in dis]

    mat.append(step)
    pred = dis

  scores = list(zip(*mat))
  nodes_scores = list(zip(nodes ,  scores ))

  sorted_nodes = sorted(nodes_scores, key=lambda x: x[1:], reverse=False)
  sorted_nodes = [x[0] for x in sorted_nodes]

  # Create ranking string
  rank_string = ""
  previous_value = None
  equal_group = []

  for i, node in enumerate(sorted_nodes):
      current_value = [score for n, score in nodes_scores if n == node][0]
      if previous_value is None:
          equal_group.append(node)
      elif current_value == previous_value:
          equal_group.append(node)
      else:
          if equal_group:
              rank_string += " , ".join(equal_group) + " > "
          equal_group = [node]
      previous_value = current_value

  if equal_group:
      rank_string += " , ".join(equal_group)

  #affichage console
  print("nodes scores", nodes_scores)
  print("sorted nodes", sorted_nodes)
  print("ranking string", rank_string)

  return rank_string
