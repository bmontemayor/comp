class FuncDirectory(object):
    def __init__(self):
        self.functions = {}
        self.program_name = "p"
    
    def decFunction(self, name, type, scope):
        self.functions[name] = {"type" : type, "scope" : scope, "name" : name}
        self.functions[name]['var_table'] = [[], [], [], [[], [], []]]
        self.functions[name]['param_order'] = []


#{
 # "name": {
 #   "type": "data"
 #   "scope": "data"
 #   "name": "data"
 #   "var_table": {
 #      "id": {
 #      }
#       "type":{
#       }
#       "virtualAddress":{
#       }
#       "arrays":{ dir0 = isArray
#               dir1 = size
#               dir2 = virtualAddIndexes
#       }
 #  }
 # }
#}