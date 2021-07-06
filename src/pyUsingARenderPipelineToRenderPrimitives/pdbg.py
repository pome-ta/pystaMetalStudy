from pprint import pprint

def __pPass():
  print('Pass')
  

def state(obj):
  print('# --- name______')
  try:
    pprint(obj)
  except:
    __pPass()
  print('# --- vars( )______')
  try:
    pprint(vars(obj))
  except:
    __pPass()
  print('# --- dir( )______')
  try:
    pprint(dir(obj))
  except:
    __pPass()

def mthd(obj):
  # todo: 落ちる時は落ちる
  print('# --- ivarDescription')
  try:
    #pass
    pprint(obj._ivarDescription())
  except:
    __pPass()
  print('# --- shortMethodDescription')
  try:
    pprint(obj._shortMethodDescription())
  except:
    __pPass()
  print('# --- methodDescription')
  try:
    pprint(obj._methodDescription())
  except:
    __pPass()
  
  print('# --- recursiveDescription')
  try:
    pprint(obj.recursiveDescription())
  except:
    __pPass()
  print('# --- autolayoutTrace')
  try:
    pprint(obj._autolayoutTrace())
  except:
    __pPass()
    
def all(obj):
  state(obj)
  mthd(obj)

