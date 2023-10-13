# -*- coding: utf-8 -*-
"""LL(1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CcM2IJteVuRjiaYPA2r0fR7prziWn1df
"""

import re
import pandas as pd

"""**CFG**"""

#grammar = {
#   'S':['E'],
#   'E':['E + T','T'],
#   'T':['`T * F', 'F'],
#   'F':['(E)','id'],
#}

productions = {
    "S": {"aA", "bB", "dC"},
    "A": {"aA", "bA", "d"},
    "B": {"bB", "d"},
    "C": {"d"}
}

start = "S"

"""PARSER"""

def parse(user_input, start_symbol, parsingTable):
  flag = 0 #indicate whether input string is accepted or not

  user_input = user_input + "$" #$ to signify end of input

  #making of the stack
  stack = []
  stack.append("$")
  stack.append(start_symbol)

  input_len = len(user_input)
  index = 0

  while len(stack)>0 and index < input_len:
    top = stack[-1]
    print("Top =>", top)

    current_input = user_input[index]
    print("Current Input =>", current_input)

    if top == current_input:
      stack.pop()
      index = index + 1
    else:
      key = top, current_input
      print(key)

      if key not in parsingTable:
        flag = 1
        break

      value = parsingTable[key]
      if value != '@':
        value = value[::-1]
        value = list(value)

        stack.pop()

        for element in value:
          stack.append(element)
      else:
        stack.pop()

  if flag == 0:
    print("String accepted!")
  else:
    print("String not accepted!")

def ll1(follow, productions):
  print("\nParsing Table\n")

  table = {}
  for key in productions:
    for value in productions[key]:
      if value != '@':
        for element in first(value, productions):
          table[key, element]=value
      else:
        for element in follow[key]:
          table[key, element] = value

  for key, val in table.items():
    print(key, "=>", val)

  new_table = {}
  for pair in table:
    new_table[pair[1]]={}
  for pair in table:
    new_table[pair[1]][pair[0]] = table[pair]

  print("\n\nTable\n")
  print(pd.DataFrame(new_table).fillna('-'))
  print("\n")

  return table

"""FOLLOW FUNCTION"""

def follow(s, productions,ans):
  if len(s) != 1:
    return{}
  for key in productions:
    for value in productions[key]:
      f = value.find(s)
      if f != -1:
        if f == (len(value) - 1):
          if key != s:
            if key in ans:
              temp = ans[key]
            else:
              ans = follow(key, productions, ans)
              temp = ans[key]
            ans[s] = ans[s].union(temp)

        else:
          first_of_next = first(value[f+1:], productions)
          if '@' in first_of_next:
            if key != s:
              if key in ans:
                temp = ans[key]
              else:
                ans = follow(key, productions, ans)
                temp = ans[key]
              ans[s]= ans[s].union(temp)
              ans[s]= ans[s].union(first_of_next) - {'@'}
          else:
            ans[s] = ans[s].union(first_of_next)


  return ans

"""FIRST FUNCTION"""

#def first(s, productions):
 # c = s[0]
  #ans = set()
 # if c.isupper():
  #  for st in productions[c]:
   #   if st == '@':
    #    if len(s) != 1:
     #     ans = ans.union(first(s[1:], productions))
      #  else:
     #     ans = ans.union('@')
     # else:
      #  f = first(st, productions)
       # ans = ans.union(x for x in f)
#  else:
 #   ans = ans.union(c)
  #return ans

def first(s, productions, computed=None):
    if computed is None:
        computed = set()

    ans = set()
    if not s:
        ans.add('@')  # An empty string can derive epsilon
    else:
        c = s[0]
        if c.isupper():
            if c not in computed:
                for st in productions[c]:
                    if st != c:
                        f = first(st + s[1:], productions, computed)
                        ans.update(f)
                computed.add(c)
        else:
            ans.add(c)
    return ans

"""Working with grammar"""

if __name__ == "__main__":
  productions = dict()
  first_dict = dict()
  follow_dict = dict ()

  flag =1
  for line in productions:
        l = re.split("( |->|\n|\||)*", line)
        lhs = l[0]
        rhs = set(l[1:-1]) - {''}
        if flag:
            flag = 0
            start = lhs
        productions[lhs] = rhs

  print('\nFirst\n')

  for lhs in productions:
    first_dict[lhs] = first(lhs, productions)
  for f in first_dict:
    print(str(f) + " : " + str(first_dict[f]))
  print("")

  print('\nFollow\n')

  for lhs in productions:
    follow_dict[lhs] = set()

  follow_dict[start] = follow_dict[start].union('$')

  for lhs in productions:
    follow_dict = follow(lhs, productions, follow_dict)

  for lhs in productions:
    follow_dict = follow(lhs, productions, follow_dict)

  for f in follow_dict:
    print(str(f) + " : " + str(follow_dict[f]))

  ll1Table = ll1(follow_dict, productions)

  parse("aabd", start, ll1Table)