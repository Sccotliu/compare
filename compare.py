from copy import copy
import json


def path_string(path):
  return ' > '.join(path)


def compare(ob1, ob2, path=[]):
  if not (isinstance(ob1, dict) and isinstance(ob1, dict)):
    if ob1 != ob2:
      if (isinstance(ob1, list) and isinstance(ob1, list)):
        # COMPARE as lists
        difference = {'ob1': [], 'ob2': [], 'positions':[]}
        m = max(len(ob1), len(ob2))
        for i in range(0, m):
          if i < len(ob2) and i < len(ob1):
            childpath = copy(path)
            childpath.append(str(i))
            different = compare(ob1[i], ob2[i], childpath)
            if different:
              difference['ob1'].append(ob1[i])
              difference['ob2'].append(ob2[i])
          else:
            if i >= len(ob1):
              difference['ob1'].append('<not present>')
              difference['ob2'].append(ob2[i])
            else:
              difference['ob1'].append(ob1[i])
              difference['ob2'].append('<not present>')
            difference['positions'].append(str(i))
        print "{path} lists differed at positions: {positions}\n{ob1}\n{ob2}\n\n".format(
          path=path_string(path),
          positions=','.join(difference['positions']),
          ob1=difference['ob1'],
          ob2=difference['ob2'])
        if difference['ob1']:
          return difference
        else:
          return False
      else:
        return True
    else:
      return False
  # COMPARE as dicts
  keys = list(set(ob1.keys()) | set(ob2.keys()))
  difference = {'ob1':[], 'ob2':[]}
  for key in keys:
    path_str = path_string(path)
    if key not in ob2:
      print "{} > '{}'   in ob1, value={}\n{}\n\n".format(path_str, key, ob1[key], path_str)
      continue
    if key not in ob1:
      print "{} > '{}'   in ob2, value={}\n{}\n\n".format(path_str, key, ob2[key], path_str)
      continue
    childpath = copy(path)
    childpath.append("'"+str(key)+"'")
    different = compare(ob1[key], ob2[key], childpath)
    if different:
      if not isinstance(different, dict):
        print "'{}' was different:\n{}\n{}\n\n".format(key, ob1[key], ob2[key])
  return False


if __name__ == '__main__':
  ob1 = {'a':{'b':[1,{'c':1,'d':2,'nested_e':['some val']},2],'f':3},'g':3}
  ob2 = {'a':{'b':[1,{'c':1,'nested_e':['some val', 'something']},2,3],'f':3},'g':4}
  print 'Comparing two objects: \n{}\n{}\n\n'.format(ob1, ob2)
  compare(ob1, ob2)

  l1 = [1,3,5,7]
  l2 = [2,4,6,]
  print 'Comparing two simple list: \n{}\n{}\n\n'.format(l1, l2)
  compare(l1, l2)