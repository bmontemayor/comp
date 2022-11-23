class Virtual_Memory(object):
    def __init__(self):
        self.glob = [1000, 4000, 7000]
        self.local = [10000, 14000, 17000]
        self.temporal = [20000, 24000, 27000]
        self.constant = [30000, 34000, 37000]

    #global 1000 - 9999
        #int    1000 - 3999
        #float  4000 - 6999
        #string 7000 - 9999
    #local  10000 - 19999
        #int    10000 - 13999
        #float  14000 - 16999
        #string 17000 - 19999
    #temporal 20000 - 29999
        #int    20000 - 23999
        #float  24000 - 26999
        #string 27000 - 29999
    #constants 30000 - 39999
        #int    30000 - 33999
        #float  34000 - 36999
        #string 37000 - 39999


    def clear(self):
        self.local = [10000, 14000, 17000]
        self.temporal = [20000, 24000, 27000]
    

#asigna una direccion virtual a una variable dependiendo de su scope
    def assign(self, scope, type):
        if(scope == 'global'):
            if(type == 'int'):
                virtual_add = self.glob[0]
                self.glob[0] +=1
                return virtual_add
            elif(type == 'float'):
                virtual_add = self.glob[1]
                self.glob[1] +=1
                return virtual_add
            else:
                virtual_add = self.glob[2]
                self.glob[2] +=1
                return virtual_add
        if(scope == 'local'):
            if(type == 'int'):
                virtual_add = self.local[0]
                self.local[0] +=1
                return virtual_add
            elif(type == 'float'):
                virtual_add = self.local[1]
                self.local[1] +=1
                return virtual_add
            else:
                virtual_add = self.local[2]
                self.local[2] +=1
                return virtual_add
        if(scope == 'temporal'):
            if(type == 'int'):
                virtual_add = self.temporal[0]
                self.temporal[0] +=1
                return virtual_add
            elif(type == 'float'):
                virtual_add = self.temporal[1]
                self.temporal[1] +=1
                return virtual_add
            else:
                virtual_add = self.temporal[2]
                self.temporal[2] +=1
                return virtual_add
        if(scope == 'constant'):
            if(type == 'int'):
                virtual_add = self.constant[0]
                self.constant[0] +=1
                return virtual_add
            elif(type == 'float'):
                virtual_add = self.constant[1]
                self.constant[1] +=1
                return virtual_add
            else:
                virtual_add = self.constant[2]
                self.constant[2] +=1
                return virtual_add
