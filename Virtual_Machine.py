#objeto para almacenar memoria; valor y direccion virtual
import matplotlib.pyplot as plt
from statistics import mean, median, mode

class Memory(object):
    def __init__(self):
        self.int = [[], []]
        self.float = [[], []]
        self.string = [[], []]




class Virtual_Machine(object):
    def __init__(self):
        self.pointer = 0
        self.quads = []
        self.global_mem = Memory()
        self.local_mem = []
        self.temporal_mem = [Memory()]
        self.funcdir = None
        self.constant = []
        self.program_name = ''
        self.function_stack = []
        self.gosub_stack = []
        self.gosub_pointer_stack = []
        self.parameters_stack = []
        self.recursion_counter = 0
        self.pointer_array = [[], []]



    def start(self):
        while(self.pointer < len(self.quads)):
            self.do()

    def do(self):
        quad = self.quads[self.pointer]
        operation = quad[0]

        if(operation == 'WRITE'):
            write = quad[3]
            if(write in self.pointer_array[0]):
                index = self.pointer_array[0].index(write)
                write = self.pointer_array[1][index]

            print(self.find(write))
            self.pointer += 1

        elif(operation == 'GOTO'):
            self.pointer = int(quad[3])
        
        elif(operation == 'GOTOF'):
            left_op = int(self.find(quad[1]))

            if(left_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(left_op)
                left_op = self.pointer_array[1][index]
            if(left_op == 0):
                self.pointer = int(quad[3])
            else:
                self.pointer += 1
        elif(operation == 'GOTOT'):
            if(int(self.find(quad[1]) > 0)):
                self.pointer = int(quad[3])
            else:
                self.pointer += 1

        elif(operation == 'ERA'):
            #creacion de memoria para la funcion
            name = quad[3]
            self.function_stack.append(name)
            self.local_mem.append(Memory())
            self.temporal_mem.append(Memory())
            
            #registrar las variables de la funcion en la memoria
            for i in self.funcdir[name]['var_table'][2]:
                self.register(i)
            

            self.pointer +=1 
        
        #busca el dato en la memoria y le asigna su valor
        elif(operation == 'PARAMETER'):
            #agrega elvalor e los parametros al stack de parametros
            if int(quad[3]) == 0:
                self.parameters_stack.append([])
            self.parameters_stack[self.recursion_counter].append(self.find_parameters(int(quad[1])))
            self.pointer += 1

        #agregar el siguiente quadruplo para regresar cuando acabe la funcion y ir a la funcion
        elif(operation == 'GOSUB'):
            type = self.funcdir[quad[1]]['type']

            #guarda el siguiente cuadruplo para cuando salga de la funcion
            self.gosub_pointer_stack.append(self.pointer + 1)

            #asigna el valor de los parametros del scope anterior para no perder esos valores
            j = 0
            for i in self.parameters_stack[self.recursion_counter]:
                self.assign(self.funcdir[self.function_stack[-1]]['var_table'][2][j], i)
                j += 1
            
            self.recursion_counter += 1
            
            
            #si tiene un return, guarda la direccion de la funcion para asignar su valor
            if(type != 'void'):
                next = self.quads[self.pointer + 1]
                virtual_add = int(next[1])
                self.gosub_stack.append(virtual_add)    


            self.pointer = int(quad[3])
        
        #asigna el valor de retorno a la funcion y pop a las memorias
        elif(operation == "RETURN"):

            self.parameters_stack.pop()
            
            return_value = self.find(int(quad[3]))
            return_address = self.gosub_stack.pop()

            self.temporal_mem.pop()
            self.local_mem.pop()
            self.function_stack.pop()

            #asigna el valor que regresa la funcion a la direccion virtual guardada anteriormente
            self.assign(return_address, return_value)

            self.pointer = self.gosub_pointer_stack.pop()
            self.recursion_counter -= 1

        #pop a las memorias al terminar una funcion
        elif(operation == 'ENDFunc'):
            self.parameters_stack.pop()
            self.temporal_mem.pop()
            self.local_mem.pop()
            self.function_stack.pop()

        #regresa al quad donde se quedo en el programa
            self.pointer = self.gosub_pointer_stack.pop()
            self.recursion_counter -= 1

        elif(operation == '+'):
            left_op = int(quad[1])
            right_op = int(quad[2])
            temporal = int(quad[3])

            if(left_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(left_op)
                left_op = self.pointer_array[1][index]
            if(right_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(right_op)
                right_op = self.pointer_array[1][index]

            self.register(left_op)
            self.register(right_op)
            self.register(temporal)

            result = self.find(left_op) + self.find(right_op)
            self.assign(temporal, result)
            self.pointer += 1
        
        elif(operation == '-'):
            left_op = int(quad[1])
            right_op = int(quad[2])
            temporal = int(quad[3])
            
            if(left_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(left_op)
                left_op = self.pointer_array[1][index]
            if(right_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(right_op)
                right_op = self.pointer_array[1][index]

            self.register(left_op)
            self.register(right_op)
            self.register(temporal)

            result = self.find(left_op) - self.find(right_op)
            self.assign(temporal, result)
            self.pointer += 1
        

        elif(operation == '*'):
            left_op = int(quad[1])
            right_op = int(quad[2])
            temporal = int(quad[3])

            if(left_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(left_op)
                left_op = self.pointer_array[1][index]
            if(right_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(right_op)
                right_op = self.pointer_array[1][index]

            self.register(left_op)
            self.register(right_op)
            self.register(temporal)

            result = self.find(left_op) * self.find(right_op)
            self.assign(temporal, result)
            self.pointer += 1
        
        elif(operation == '/'):
            left_op = int(quad[1])
            right_op = int(quad[2])
            temporal = int(quad[3])

            if(left_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(left_op)
                left_op = self.pointer_array[1][index]
            if(right_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(right_op)
                right_op = self.pointer_array[1][index]

            self.register(left_op)
            self.register(right_op)
            self.register(temporal)

            result = int(self.find(left_op) / self.find(right_op))
            self.assign(temporal, result)
            self.pointer += 1
        
        elif(operation == '='):
            var = int(quad[1])
            assignator = int(quad[3])

            if(var in self.pointer_array[0]):
                index = self.pointer_array[0].index(var)
                var = self.pointer_array[1][index]
            if(assignator in self.pointer_array[0]):
                index = self.pointer_array[0].index(assignator)
                assignator = self.pointer_array[1][index]

            self.register(var)
            self.register(assignator)
            self.assign(assignator, self.find(var))
            self.pointer += 1
        
        
        elif(operation == '>'):
            left_op = int(quad[1])
            right_op = int(quad[2])
            temporal = int(quad[3])

            if(left_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(left_op)
                left_op = self.pointer_array[1][index]
            if(right_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(right_op)
                right_op = self.pointer_array[1][index]

            self.register(left_op)
            self.register(right_op)
            self.register(temporal)
            if(self.find(left_op) > self.find(right_op)):
                result = 1
            else:
                result = 0
            self.pointer += 1
            self.assign(temporal, result)
        
        elif(operation == '>='):
            left_op = int(quad[1])
            right_op = int(quad[2])
            temporal = int(quad[3])

            if(left_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(left_op)
                left_op = self.pointer_array[1][index]
            if(right_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(right_op)
                right_op = self.pointer_array[1][index]

            self.register(left_op)
            self.register(right_op)
            self.register(temporal)
            if(self.find(left_op) >= self.find(right_op)):
                result = 1
            else:
                result = 0
            self.pointer += 1
            self.assign(temporal, result)
        
        elif(operation == '<'):
            left_op = int(quad[1])
            right_op = int(quad[2])
            temporal = int(quad[3])

            if(left_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(left_op)
                left_op = self.pointer_array[1][index]
            if(right_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(right_op)
                right_op = self.pointer_array[1][index]

            self.register(left_op)
            self.register(right_op)
            self.register(temporal)
            if(self.find(left_op) < self.find(right_op)):
                result = 1
            else:
                result = 0
            self.pointer += 1
            self.assign(temporal, result)
        
        elif(operation == '<='):
            left_op = int(quad[1])
            right_op = int(quad[2])
            temporal = int(quad[3])

            if(left_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(left_op)
                left_op = self.pointer_array[1][index]
            if(right_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(right_op)
                right_op = self.pointer_array[1][index]

            self.register(left_op)
            self.register(right_op)
            self.register(temporal)
            if(self.find(left_op) <= self.find(right_op)):
                result = 1
            else:
                result = 0
            self.pointer += 1
            self.assign(temporal, result)
        
        elif(operation == '=='):
            left_op = int(quad[1])
            right_op = int(quad[2])
            temporal = int(quad[3])

            if(left_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(left_op)
                left_op = self.pointer_array[1][index]
            if(right_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(right_op)
                right_op = self.pointer_array[1][index]

            self.register(left_op)
            self.register(right_op)
            self.register(temporal)
            if(self.find(left_op) == self.find(right_op)):
                result = 1
            else:
                result = 0
            self.pointer += 1
            self.assign(temporal, result)

        elif(operation == '!='):
            left_op = int(quad[1])
            right_op = int(quad[2])
            temporal = int(quad[3])

            if(left_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(left_op)
                left_op = self.pointer_array[1][index]
            if(right_op in self.pointer_array[0]):
                index = self.pointer_array[0].index(right_op)
                right_op = self.pointer_array[1][index]

            
            self.register(left_op)
            self.register(right_op)
            self.register(temporal)
            if(self.find(left_op) != self.find(right_op)):
                result = 1
            else:
                result = 0
            self.pointer += 1
            self.assign(temporal, result)

        #crea el apuntador hacia la casilla de un arreglo
        elif(operation == "GET"):
            left_op = int(quad[1])
            right_op = int(quad[2])
            temporal = int(quad[3])

            self.register(left_op)
            self.register(right_op)
            self.register(temporal)
            
            #busca la direccion exacta de la casilla del arreglo
            add = self.find(left_op) + right_op

            #si el temporal no es apuntador lo convierte en uno
            if(temporal not in self.pointer_array[0]):
                self.pointer_array[0].append(temporal)
                self.pointer_array[1].append(add)
            #si ya es apuntador lo dirige hacia la nueva direccion
            elif(temporal in self.pointer_array[0]):
                index = self.pointer_array[0].index(temporal)
                self.pointer_array[1][index] = add
            self.pointer += 1
            #print(self.pointer_array[0], self.pointer_array[1])
        
        #creacion de la operacion para graficar
        elif(operation == 'GRAPH'):
            index_x = self.funcdir[self.program_name]['var_table'][3][0].index(quad[1])
            index_y = self.funcdir[self.program_name]['var_table'][3][0].index(quad[2])
            list_x = []
            list_y = []
            for i in self.funcdir[self.program_name]['var_table'][3][2][index_x]:
                list_x.append(int(self.find(i)))
            for i in self.funcdir[self.program_name]['var_table'][3][2][index_y]:
                list_y.append(int(self.find(i)))
            
            plt.bar(list_x, list_y)
            plt.title('Graph')
            plt.xlabel('x-axis')
            plt.ylabel('y-axis')
            plt.show()
            self.pointer += 1
        
        elif(operation == 'MEAN'):
            temporal = int(quad[3])
            self.register(temporal)
            index = self.funcdir[self.program_name]['var_table'][3][0].index(quad[1])
            list = []
            for i in self.funcdir[self.program_name]['var_table'][3][2][index]:
                list.append(int(self.find(i)))
            
            average = mean(list)
            self.assign(temporal, average)
            self.pointer += 1
        
        elif(operation == 'MEDIAN'):
            temporal = int(quad[3])
            self.register(temporal)
            index = self.funcdir[self.program_name]['var_table'][3][0].index(quad[1])
            list = []
            for i in self.funcdir[self.program_name]['var_table'][3][2][index]:
                list.append(int(self.find(i)))
            
            average = median(list)
            self.assign(temporal, average)
            self.pointer += 1
        
        elif(operation == 'MODE'):
            temporal = int(quad[3])
            self.register(temporal)
            index = self.funcdir[self.program_name]['var_table'][3][0].index(quad[1])
            list = []
            for i in self.funcdir[self.program_name]['var_table'][3][2][index]:
                list.append(int(self.find(i)))
            
            average = mode(list)
            self.assign(temporal, average)
            self.pointer += 1

            


            




#asigna el valor en una direccion virtual especifica
    def assign(self, virtual_address, value):
        #global int
        if(virtual_address >= 1000 and virtual_address <= 3999):
            index = self.global_mem.int[1].index(virtual_address)
            self.global_mem.int[0][index] = value
        #global float
        elif(virtual_address >= 4000 and virtual_address <= 6999):
            index = self.global_mem.float[1].index(virtual_address)
            self.global_mem.float[0][index] = value
        #global string
        elif(virtual_address >= 7000 and virtual_address <= 9999):
            index = self.global_mem.string[1].index(virtual_address)
            self.global_mem.string[0][index] = value

        #local int
        elif(virtual_address >= 10000 and virtual_address <= 13999):
            index = self.local_mem[-1].int[1].index(virtual_address)
            self.local_mem[-1].int[0][index] = value
        #local float
        elif(virtual_address >= 14000 and virtual_address <= 16999):
            index = self.local_mem[-1].float[1].index(virtual_address)
            self.local_mem[-1].float[0][index] = value
        #local string
        elif(virtual_address >= 17000 and virtual_address <= 19999):
            index = self.local_mem[-1].string[1].index(virtual_address)
            self.local_mem[-1].string[0][index] = value

        #temporal int
        elif(virtual_address >= 20000 and virtual_address <= 23999):
            index = self.temporal_mem[-1].int[1].index(virtual_address)
            self.temporal_mem[-1].int[0][index] = value
        #temporal float
        elif(virtual_address >= 24000 and virtual_address <= 26999):
            index = self.temporal_mem[-1].float[1].index(virtual_address)
            self.temporal_mem[-1].float[0][index] = value
        #temporal string
        elif(virtual_address >= 27000 and virtual_address <= 29999):
            index = self.temporal_mem[-1].string[1].index(virtual_address)
            self.temporal_mem[-1].string[0][index] = value

        #constantes
        elif(virtual_address >= 30000 and virtual_address <= 39999):
            index = self.constant[1].index(virtual_address)
            self.constant[0][index] = value

        
#registra la direccion en la memoria si no esta ya registrado
    def register(self, virtual_address):

        #global int
        if(virtual_address >= 1000 and virtual_address <= 3999):
            #si no lo encuentra que lo registre
            if(virtual_address not in self.global_mem.int[1]):
                self.global_mem.int[1].append(virtual_address)
                self.global_mem.int[0].append(None)
        #global float
        elif(virtual_address >= 4000 and virtual_address <= 6999):
            #si no lo encuentra que lo registre
            if(virtual_address not in self.global_mem.float[1]):
                self.global_mem.float[1].append(virtual_address)
                self.global_mem.float[0].append(None)
        #global string
        elif(virtual_address >= 7000 and virtual_address <= 9999):
            #si no lo encuentra que lo registre
            if(virtual_address not in self.global_mem.string[1]):
                self.global_mem.string[1].append(virtual_address)
                self.global_mem.string[0].append(None)

        #local int
        elif(virtual_address >= 10000 and virtual_address <= 13999):
            #si no lo encuentra que lo registre
            if(virtual_address not in self.local_mem[-1].int[1]):
                self.local_mem[-1].int[1].append(virtual_address)
                self.local_mem[-1].int[0].append(None)
        #local float
        elif(virtual_address >= 14000 and virtual_address <= 16999):
            #si no lo encuentra que lo registre
            if(virtual_address not in self.local_mem[-1].float[1]):
                self.local_mem[-1].float[1].append(virtual_address)
                self.local_mem[-1].float[0].append(None)
        #local string
        elif(virtual_address >= 17000 and virtual_address <= 19999):
            #si no lo encuentra que lo registre
            if(virtual_address not in self.local_mem[-1].string[1]):
                self.local_mem[-1].string[1].append(virtual_address)
                self.local_mem[-1].string[0].append(None)

        #temporal int
        elif(virtual_address >= 20000 and virtual_address <= 23999):
            #si no lo encuentra que lo registre
            if(virtual_address not in self.temporal_mem[-1].int[1]):
                self.temporal_mem[-1].int[1].append(virtual_address)
                self.temporal_mem[-1].int[0].append(None)
        #temporal float
        elif(virtual_address >= 24000 and virtual_address <= 26999):
            #si no lo encuentra que lo registre
            if(virtual_address not in self.temporal_mem[-1].float[1]):
                self.temporal_mem[-1].float[1].append(virtual_address)
                self.temporal_mem[-1].float[0].append(None)
        #temporal string
        elif(virtual_address >= 27000 and virtual_address <= 29999):
            #si no lo encuentra que lo registre
            if(virtual_address not in self.temporal_mem[-1].string[1]):
                self.temporal_mem[-1].string[1].append(virtual_address)
                self.temporal_mem[-1].string[0].append(None)



#regresa el valor desde una direccion
    def find(self, virtual_address):

        #global int
        if(virtual_address >= 1000 and virtual_address <= 3999):
            index = self.global_mem.int[1].index(virtual_address)
            return self.global_mem.int[0][index]
        #global float
        elif(virtual_address >= 4000 and virtual_address <= 6999):
            index = self.global_mem.float[1].index(virtual_address)
            return self.global_mem.float[0][index]
        #global string
        elif(virtual_address >= 7000 and virtual_address <= 9999):
            index = self.global_mem.string[1].index(virtual_address)
            return self.global_mem.string[0][index]
        #local int
        elif(virtual_address >= 10000 and virtual_address <= 13999):
            index = self.local_mem[-1].int[1].index(virtual_address)
            return self.local_mem[-1].int[0][index]
        #local float
        elif(virtual_address >= 14000 and virtual_address <= 16999):
            index = self.local_mem[-1].float[1].index(virtual_address)
            return self.local_mem[-1].float[0][index]
        #local string
        elif(virtual_address >= 17000 and virtual_address <= 19999):
            index = self.local_mem[-1].string[1].index(virtual_address)
            return self.local_mem[-1].string[0][index]
        #temporal int
        elif(virtual_address >= 20000 and virtual_address <= 23999):
            index = self.temporal_mem[-1].int[1].index(virtual_address)
            return self.temporal_mem[-1].int[0][index]
        #temporal float
        elif(virtual_address >= 24000 and virtual_address <= 26999):
            index = self.temporal_mem[-1].float[1].index(virtual_address)
            return self.temporal_mem[-1].float[0][index]
        #temporal string
        elif(virtual_address >= 27000 and virtual_address <= 29999):
            index = self.temporal_mem[-1].string[1].index(virtual_address)
            return self.temporal_mem[-1].string[0][index]
        #constantes
        elif(virtual_address >= 30000 and virtual_address <= 39999):
            index = self.constant[1].index(virtual_address)
            return self.constant[0][index]

#regresa el valor desde una direccion especificamente para parametros, revisando la memoria local y temporal anterior
    def find_parameters(self, virtual_address):

        #global int
        if(virtual_address >= 1000 and virtual_address <= 3999):
            index = self.global_mem.int[1].index(virtual_address)
            return self.global_mem.int[0][index]
        #global float
        elif(virtual_address >= 4000 and virtual_address <= 6999):
            index = self.global_mem.float[1].index(virtual_address)
            return self.global_mem.float[0][index]
        #global string
        elif(virtual_address >= 7000 and virtual_address <= 9999):
            index = self.global_mem.string[1].index(virtual_address)
            return self.global_mem.string[0][index]
        #local int
        elif(virtual_address >= 10000 and virtual_address <= 13999):
            index = self.local_mem[-2].int[1].index(virtual_address)
            return self.local_mem[-2].int[0][index]
        #local float
        elif(virtual_address >= 14000 and virtual_address <= 16999):
            index = self.local_mem[-2].float[1].index(virtual_address)
            return self.local_mem[-2].float[0][index]
        #local string
        elif(virtual_address >= 17000 and virtual_address <= 19999):
            index = self.local_mem[-2].string[1].index(virtual_address)
            return self.local_mem[-2].string[0][index]
        #temporal int
        elif(virtual_address >= 20000 and virtual_address <= 23999):
            index = self.temporal_mem[-2].int[1].index(virtual_address)
            return self.temporal_mem[-2].int[0][index]
        #temporal float
        elif(virtual_address >= 24000 and virtual_address <= 26999):
            index = self.temporal_mem[-2].float[1].index(virtual_address)
            return self.temporal_mem[-2].float[0][index]
        #temporal string
        elif(virtual_address >= 27000 and virtual_address <= 29999):
            index = self.temporal_mem[-2].string[1].index(virtual_address)
            return self.temporal_mem[-2].string[0][index]
        #constantes
        elif(virtual_address >= 30000 and virtual_address <= 39999):
            index = self.constant[1].index(virtual_address)
            return self.constant[0][index]
