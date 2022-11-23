import ast
import json
from Virtual_Machine import *

#extraer el directorio de funciones
file = open("funcdir.txt", "r")
filecontent = file.read()
funcdir = ast.literal_eval(filecontent)
file.close()

#extraer la tabla de constantes
file = open("constants.txt", "r")
filecontent = file.read()
constant_table_dir = ast.literal_eval(filecontent)
file.close()
constant_table = constant_table_dir['dictation']

#extraer los cuadruplos
file = open("quads.txt", "r")
filecontent = file.read()
quads_dir = ast.literal_eval(filecontent)
file.close()
quads = quads_dir['dictation']

#sacar el nombre del programa para extraer sus variables
program = next(iter(funcdir))


#creacion y asignacion de datos a la memoria
virtual_machine = Virtual_Machine()
virtual_machine.program_name = program
virtual_machine.funcdir = funcdir
virtual_machine.quads = quads
virtual_machine.constant = constant_table
variables = funcdir[program]['var_table'][2]

#meter las variables globales a la memoria global
for i in variables:
    if(i >= 1000 and i <= 3999):
        virtual_machine.global_mem.int[0].append(None)
        virtual_machine.global_mem.int[1].append(i)
    if(i >= 4000 and i <= 6999):
        virtual_machine.global_mem.float[0].append(None)
        virtual_machine.global_mem.float[1].append(i)
    if(i >= 7000 and i <= 9999):
        virtual_machine.global_mem.string[0].append(None)
        virtual_machine.global_mem.string[1].append(i)


virtual_machine.start()

