


import ply.yacc as yacc
import ply.lex as lex
import json
from Semantic_Cube import *
from Func_Directory import *
from Quad import *
from Virtual_Memory import *



#DECLARATION OF TOKENS
tokens = [

    #WORDS
    'ID',

    # OPERATORS
    'PLUS' ,        # +
    'MINUS' ,       # -
    'TIMES',     # *
    'DIVIDE',       # /

    #ASSIGNATOR
    'EQUALS',       # =
    'SEMICOLON',    # ;

    #TYPES
    'INT',
    'FLOAT',
    'STRING',

     # COMPARATORS
    'LT',           # <
    'GT',           # >
    'LTE',          # <=
    'GTE',          # >=
    'DOUBLEEQUAL',  # ==
    'NEQUAL',       # !=
    'AND',          # &&
    'OR' ,          # ||


    #BRACKETS
    'LPAREN',       # (
    'RPAREN',       # )
    'LBRACE',       # [
    'RBRACE',       # ]
    'BLOCKSTART',   # {
    'BLOCKEND',     # }
    'COLON',        # :
    'COMMA',        # ,

    'COMMENT',      # %%

]



#RESERVED WORDS
reserved = {
    'if' : 'IF_K',
    'else' : 'ELSE_K',
    'while' : 'WHILE_K',
    'do' : 'DO_K',
    'for' : 'FOR_K',
    'return' : 'RETURN_K',
    'write' : 'WRITE_K',
    'to' : 'TO_K',
    'function' : 'FUNCTION_K',
    'void' : 'VOID_K',
    'vars' : 'VARS_K',
    'program' : 'PROGRAM_K',
    'main' : 'MAIN_K',
    'read' : 'READ_K',
    'int' : 'INT_K',
    'float' : 'FLOAT_K',
    'string' : 'STRING_K',
    'array' : 'ARRAY_K',
    'graph' : 'GRAPH_K',
    'mean'  : 'MEAN_K',
    'median': 'MEDIAN_K',
    'mode'  : 'MODE_K',
}

tokens += list(reserved.values())

#REGULAR EXPRESSIONS
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE = r'\['
t_RBRACE = r'\]'
t_BLOCKSTART = r'\{'
t_BLOCKEND = r'\}'
t_EQUALS = r'\='
t_SEMICOLON = r'\;'
t_GT = r'\>'
t_LT = r'\<'
t_LTE = r'\<\='
t_GTE = r'\>\='
t_DOUBLEEQUAL = r'\=\='
t_NEQUAL = r'\!\='
t_AND = r'\&\&'
t_OR = r'\|\|'
t_COMMENT = r'\%\%.*'
t_ignore  = ' \t'
t_COLON = r'\:'
t_COMMA = R'\,'


def t_FLOAT(t):
    r'(\d*\.\d+)|(\d+\.\d*)'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
     r'"(?:[^"\\]|\\.)*"'
     return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Invalid character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t



lexer = lex.lex()


#data = '''
#4 + 7 * 20
#  + -33 *6
#'''

#lexer.input(data)

#while True:
#    tok = lexer.token()
#    if not tok:
#        break      # No more input
#    print(tok.type, tok.value, tok.lineno, tok.lexpos)




program_name = ""
quads = quad()
funcdir = FuncDirectory()
virtualM = Virtual_Memory()
#[0] es valor, [1] es direccion virtual
constant_table = [[],[]]
last_function = "b"
last_type = "b"
temporal = 1
parameters_counter = 0
last_array = 0



#primer goto para el main
quads.generate_quad('GOTO', '_', '_', '_')
quads.jump_stack.append(quads.counter - 1)

def p_error(p):
    print(">> Syntax error")
    print(">> Unexpected token: ", p)
    exit()


#como comienza el programa
def p_program(p):
    '''PROGRAM : PROGRAM_K ID neural_program_id SEMICOLON VARS MODULES START'''


#guarda el nombre del programa y lo añade al directorio de funciones
def p_neural_program_id(p):
    '''neural_program_id : EMPTY'''

    global last_function
    global program_name

    last_function = p[-1]
    program_name = p[-1]
    funcdir.program_name = p[-1]
    funcdir.decFunction(p[-1], "program", "global")

#bloque de variables
def p_vars(p):
    '''VARS : VARS_K BLOCKSTART VARS_DECL BLOCKEND'''

#variable y le da su declaracion
def p_var(p):
    '''VAR : ID'''
    p[0] = p[1]


#declaracion de variables
def p_vars_decl(p):
    '''VARS_DECL : TYPE VAR neural_var_dec SEMICOLON RVARS_DECL
                | ARRAY_K TYPE VAR neural_array_dec LBRACE CONSTANT neural_constant neural_array_size RBRACE SEMICOLON RVARS_DECL'''

#checa que las variables y sus tipos no han sido declaradas anteriormente en el mismo scope y las almacena en la tabla de variables
def p_neural_var_dec(p):
    '''neural_var_dec : EMPTY'''

    if(p[-1] in funcdir.functions[last_function]['var_table'][0]):
        error_message = "ERROR: Variable '{}' has already been declared".format(p[-1])
        raise Exception(error_message)
    else:
        funcdir.functions[last_function]['var_table'][0].append(p[-1])
        funcdir.functions[last_function]['var_table'][1].append(last_type)
        #funcdir.functions[last_function]['param_order'].append(last_type)

        scope = funcdir.functions[last_function]['scope']
        virtualadd = virtualM.assign(scope, last_type)
        funcdir.functions[last_function]['var_table'][2].append(virtualadd)

#checar si el array ya existe y agregarlo a la tabla de variables
def p_neural_array_dec(p):
    '''neural_array_dec : EMPTY'''
    if(p[-1] in funcdir.functions[last_function]['var_table'][0]):
        error_message = "ERROR: Variable '{}' has already been declared".format(p[-1])
        raise Exception(error_message)
    else:
        funcdir.functions[last_function]['var_table'][0].append(p[-1])
        funcdir.functions[last_function]['var_table'][1].append(last_type)
        #definirlo como array
        
        scope = funcdir.functions[last_function]['scope']
        #la direccion base se asigna en la tabla de variables para mantener indexamiento de variables con direcciones en la tabla de variables
        virtualadd = virtualM.assign(scope, last_type)
        funcdir.functions[last_function]['var_table'][2].append(virtualadd)
        funcdir.functions[last_function]['var_table'][3][0].append(virtualadd)
        #funcdir.functions[last_function]['var_table'][3][2].append(virtualadd)

def p_neural_array_size(p):
    '''neural_array_size : EMPTY'''
    index = constant_table[1].index(quads.op_stack.pop())
    size = constant_table[0][index]
    #asignarle su tamano en el directorio de funciones
    funcdir.functions[last_function]['var_table'][3][1].append(size)
    #asignarle las direcciones virtuales
    scope = funcdir.functions[last_function]['scope']

    array = []
    array.append(funcdir.functions[last_function]['var_table'][3][0][-1])
    #los indexamientos del array se guardan por separado para no mover indexamiento de las demas variables
    for i in range(size-1):
        virtualadd = virtualM.assign(scope, last_type)
        array.append(virtualadd)
    
    funcdir.functions[last_function]['var_table'][3][2].append(array)

def p_rvars_decl(p):
    '''RVARS_DECL : VARS_DECL
                | EMPTY'''




#tipos, y almacena el ultimo tipo en la variable global
def p_type(p):
    '''TYPE : INT_K
            | FLOAT_K
            | STRING_K'''

    global last_type
    last_type = p[1]
    p[0] = p[1]

#constante y le da su valor correspondiente
def p_constant(p):
    '''CONSTANT : INT
                | FLOAT
                | STRING'''
    
    p[0] = p[1]




#modulos
def p_modules(p):
    '''MODULES : MODULES_RETURN
                | MODULES_VOID
                | EMPTY'''
#modulos con return
def p_modules_return(p):
    '''MODULES_RETURN : FUNCTION_K TYPE ID neural_modules LPAREN PARAMETERS RPAREN BLOCKSTART VARS neural_modules_size BODY BLOCKEND neural_endfunc MODULES'''


#modulos con void
def p_modules_void(p):
    '''MODULES_VOID : FUNCTION_K VOID_K ID neural_modules LPAREN PARAMETERS RPAREN BLOCKSTART VARS neural_modules_size BODY BLOCKEND neural_endfunc MODULES'''

#revisa si el nombre de la funcion existe y la mete a la direccion de funciones
def p_neural_modules(p):
    '''neural_modules : EMPTY'''
    
    global last_function
    global last_type
    if(p[-1] in funcdir.functions):
        error_message = "ERROR: Function name: '{}' has already been declared in the scope".format(p[-1])
        raise Exception(error_message)
    else:
        last_function = p[-1]
        last_type = p[-2]
        funcdir.decFunction(last_function, last_type, "local")
        funcdir.functions[funcdir.program_name]['var_table'][0].append(p[-1])
        funcdir.functions[funcdir.program_name]['var_table'][1].append(last_type)
        virtualadd = virtualM.assign('global', last_type)
        funcdir.functions[funcdir.program_name]['var_table'][2].append(virtualadd)

#mete el tamano y la posicion de quad en el funcdir
def p_neural_modules_size(p):
    '''neural_modules_size : EMPTY'''
    local_size = len(funcdir.functions[last_function]['var_table'][0])
    funcdir.functions[last_function]['size'] = local_size
    funcdir.functions[last_function]['start_add'] = quads.counter

#crea el cuadruplo de endfunc y resetea la memoria
def p_neural_endfunc(p):
    '''neural_endfunc : EMPTY'''
    quads.generate_quad('ENDFunc', '_', '_', '_')
    global temporal
    temporal = 1
    virtualM.clear()


def p_parameters(p):
    '''PARAMETERS : TYPE VAR neural_parameters RPARAMETERS
                | EMPTY'''

def p_rparameters(p):
    '''RPARAMETERS : COMMA PARAMETERS
                | EMPTY'''

#checa que no se hayan declarado las variables y las mete a la tabla de variables
def p_neural_parameters(p):
    '''neural_parameters : EMPTY'''
    if(p[-1] in funcdir.functions[last_function]['var_table'][0]):
        error_message = "ERROR: Variable '{}' has already been declared".format(p[-1])
        raise Exception(error_message)
    else:
        funcdir.functions[last_function]['var_table'][0].append(p[-1])
        funcdir.functions[last_function]['var_table'][1].append(last_type)
        funcdir.functions[last_function]['param_order'].append(last_type)

        scope = funcdir.functions[last_function]['scope']
        virtualadd = virtualM.assign(scope, last_type)
        funcdir.functions[last_function]['var_table'][2].append(virtualadd)

#llamada de funciones
def p_function_call(p):
    '''FUNCTION_CALL : ID neural_fc_era LPAREN EXPRESSION_LIST neural_fc_gosub RPAREN'''

#verifica que exista la funcion a llamar y crea el cuadruplo era
def p_neural_fc_era(p):
    '''neural_fc_era : EMPTY'''
    global parameters_counter

    if(p[-1] not in funcdir.functions):
        error_message = "ERROR: Function '{}' does not exist".format(p[-1])
        raise Exception(error_message)
    else:
        size = funcdir.functions[p[-1]]['size']
        quads.generate_quad('ERA', size, '_', p[-1])
        parameters_counter = 1

#verifica que el numero de parametros sea el correcto y crea el cuadruplo gosub
def p_neural_fc_gosub(p):
    '''neural_fc_gosub : EMPTY'''

    global parameters_counter

    if(parameters_counter -1 != len(funcdir.functions[p[-4]]['param_order'])):
        error_message = "ERROR: Invalid amount of parameters, '{}' were given".format(parameters_counter -1)
        raise Exception(error_message)
    
    else:
        start_add = funcdir.functions[p[-4]]['start_add']
        quads.generate_quad('GOSUB', p[-4], '_', start_add)

        #si no es void se le asigna el resultado
        if(funcdir.functions[p[-4]]['type'] != 'void'):
            index = funcdir.functions[program_name]['var_table'][0].index(p[-4])
            type = funcdir.functions[program_name]['var_table'][1][index]
            result = funcdir.functions[program_name]['var_table'][2][index]
            temp = virtualM.assign('temporal', type)
            quads.generate_quad('=', result, '_', temp)
            quads.op_stack.append(temp)
            quads.type_stack.append(type)

#start, esto ya es el programa despues de las funciones y donde esta el main
def p_start(p):
    '''START : MAIN_K neural_main LPAREN RPAREN BLOCKSTART BODY BLOCKEND'''

def p_neural_main(p):
    '''neural_main : EMPTY'''
    main = quads.jump_stack.pop()
    quads.quads[main][3] = quads.counter

def p_body(p):
    '''BODY : STATEMENT RBODY
            | EMPTY'''

def p_rbody(p):
    '''RBODY : BODY'''

def p_statement(p):
    '''STATEMENT : ASSIGN SEMICOLON
                | RETURN
                | READ SEMICOLON
                | WRITE SEMICOLON
                | IFELSE
                | WHILE_STMT
                | DO_WHILE 
                | FUNCTION_CALL SEMICOLON
                | GRAPH SEMICOLON'''

def p_rstatement(p):
    '''RSTATEMENT : STATEMENT RSTATEMENT
                | EMPTY'''

def p_write(p):
    '''WRITE : WRITE_K LPAREN WRITE_LIST RPAREN'''

def p_write_list(p):
    '''WRITE_LIST : R_ASSIGN RWRITE
                    | CONSTANT neural_constant RWRITE'''

def p_rwrite(p):
    '''RWRITE : neural_write COMMA WRITE_LIST
                | neural_write EMPTY'''

def p_graph(p):
    '''GRAPH : GRAPH_K LPAREN VAR neural_check_array COMMA VAR neural_check_array RPAREN neural_graph_quad'''

#revisa si el parametro es una lista y mete su direccion al stack de operandos
def p_neural_check_array(p):
    '''neural_check_array : EMPTY'''
    global program_name
    if(p[-1] in funcdir.functions[last_function]['var_table'][0]):
        index = funcdir.functions[last_function]['var_table'][0].index(p[-1])
        type = funcdir.functions[last_function]['var_table'][1][index]
        virtual_add = funcdir.functions[last_function]['var_table'][2][index]

        quads.op_stack.append(virtual_add)
        quads.type_stack.append(type)
        if(virtual_add not in funcdir.functions[last_function]['var_table'][3][0]):
            error_message = "ERROR: 'List' parameter not an array"
            raise Exception(error_message)
        

    elif(p[-1] in funcdir.functions[program_name]['var_table'][0]):
        index = funcdir.functions[program_name]['var_table'][0].index(p[-1])
        type = funcdir.functions[last_function]['var_table'][1][index]
        virtual_add = funcdir.functions[program_name]['var_table'][2][index]
        quads.op_stack.append(virtual_add)
        quads.type_stack.append(type)
        if(virtual_add not in funcdir.functions[program_name]['var_table'][3][0]):
            error_message = "ERROR: 'List' parameter not an array"
            raise Exception(error_message)
        
    else:
        error_message = "ERROR: Variable '{}' hasn't been declared.".format(p[-1])
        raise Exception(error_message)

def p_neural_graph_quad(p):
    '''neural_graph_quad : EMPTY'''
    y_axis = quads.op_stack.pop()
    x_axis = quads.op_stack.pop()
    quads.type_stack.pop()
    quads.type_stack.pop()

    
    index = funcdir.functions[program_name]['var_table'][3][0].index(y_axis)
    size = funcdir.functions[program_name]['var_table'][3][1][index]
    index = funcdir.functions[last_function]['var_table'][3][0].index(y_axis)
    size = funcdir.functions[last_function]['var_table'][3][1][index]

    quads.generate_quad('GRAPH', x_axis, y_axis, size)

def p_mean(p):
    '''MEAN : MEAN_K LPAREN VAR neural_check_array RPAREN neural_mean_quad'''

def p_neural_mean_quad(p):
    '''neural_mean_quad : EMPTY'''
    list = quads.op_stack.pop()
    type = quads.type_stack.pop()
    temp = virtualM.assign('temporal', type)

    quads.generate_quad('MEAN', list, '_', temp)
    quads.op_stack.append(temp)
    quads.type_stack.append(type)

def p_median(p):
    '''MEDIAN : MEDIAN_K LPAREN VAR neural_check_array RPAREN neural_median_quad'''

def p_neural_median_quad(p):
    '''neural_median_quad : EMPTY'''
    list = quads.op_stack.pop()
    type = quads.type_stack.pop()
    temp = virtualM.assign('temporal', type)

    quads.generate_quad('MEDIAN', list, '_', temp)
    quads.op_stack.append(temp)
    quads.type_stack.append(type)

def p_mode(p):
    '''MODE : MODE_K LPAREN VAR neural_check_array RPAREN neural_mode_quad'''

def p_neural_mode_quad(p):
    '''neural_mode_quad : EMPTY'''
    list = quads.op_stack.pop()
    type = quads.type_stack.pop()
    temp = virtualM.assign('temporal', type)

    quads.generate_quad('MODE', list, '_', temp)
    quads.op_stack.append(temp)
    quads.type_stack.append(type)


#creacion del cuadruplo de write
def p_neural_write(p):
    '''neural_write : EMPTY'''
    result = quads.op_stack.pop()
    quads.type_stack.pop()
    quads.generate_quad('WRITE', '_', '_', result)



def p_read(p):
    '''READ : READ_K LPAREN ID_LIST RPAREN'''

def p_id_list(p):
    '''ID_LIST : ID neural_read RID_LIST'''

#genera el cuadruplo
def p_neural_read(p):
    '''neural_read : EMPTY'''
    quads.generate_quad('READ', '_', '_', p[-1])

def p_rid_list(p):
    '''RID_LIST : COMMA ID_LIST
                | EMPTY'''


def p_assign(p):
    '''ASSIGN : ARRAY EQUALS neural_equals R_ASSIGN neural_assign_quad
                | VAR neural_assign EQUALS neural_equals R_ASSIGN neural_assign_quad'''
    
def p_r_assign(p):
    '''R_ASSIGN : EXPRESSION
                | FUNCTION_CALL
                | ARRAY
                | MEAN
                | MEDIAN
                | MODE'''

def p_array(p):
    '''ARRAY : VAR neural_assign LBRACE neural_array_pop EXPRESSION neural_array_ver RBRACE'''

def p_neural_array_pop(p):
    '''neural_array_pop : EMPTY'''
    global last_array

    quads.type_stack.pop()
    last_array = quads.op_stack.pop()

#crea el apuntador para navegar a la casilla deseada, con el cuadruplo GET
def p_neural_array_ver(p):
    '''neural_array_ver : EMPTY'''
    global last_array
    quads.type_stack.pop()
    exp = quads.op_stack.pop()

    if(last_array in funcdir.functions[last_function]['var_table'][3][0]):
        index = funcdir.functions[last_function]['var_table'][3][0].index(last_array)
        size = funcdir.functions[last_function]['var_table'][3][1][index]
    elif(last_array in funcdir.functions[program_name]['var_table'][3][0]):
        index = funcdir.functions[program_name]['var_table'][3][0].index(last_array)
        size = funcdir.functions[program_name]['var_table'][3][1][index]
    else:
        error_message = "ERROR: Array '{}' hasn't been declared.".format(p[-1])
        raise Exception(error_message)

    result = virtualM.assign('temporal', 'int')
    size = funcdir.functions
    quads.generate_quad('GET', exp, last_array, result)
    quads.op_stack.append(result)
    quads.type_stack.append('int')

#busca que la variable exista y mete su tipo y operando a sus stacks
def p_neural_assign(p):
    '''neural_assign : EMPTY'''
    if(p[-1] in funcdir.functions[last_function]['var_table'][0]):
        i = funcdir.functions[last_function]['var_table'][0].index(p[-1])
        type = funcdir.functions[last_function]['var_table'][1][i]
        operand = funcdir.functions[last_function]['var_table'][2][i]
        quads.type_stack.append(type)
        quads.op_stack.append(operand)
    elif(p[-1] in funcdir.functions[program_name]['var_table'][0]):
        i = funcdir.functions[program_name]['var_table'][0].index(p[-1])
        type = funcdir.functions[program_name]['var_table'][1][i]
        operand = funcdir.functions[program_name]['var_table'][2][i]
        quads.type_stack.append(type)
        quads.op_stack.append(operand)
    else:
        error_message = "ERROR: Variable '{}' hasn't been declared.".format(p[-1])
        raise Exception(error_message)

#mete el operador al stack popers
def p_neural_equals(p):
    '''neural_equals : EMPTY'''
    quads.poper.append(p[-1])

#revisa el cubo semantico y genera el cuadruplo
def p_neural_assign_quad(p):
    '''neural_assign_quad : EMPTY'''
    
    right_op = quads.op_stack.pop()
    right_type = quads.type_stack.pop()
    left_op = quads.op_stack.pop()
    left_type = quads.type_stack.pop()
    operator = quads.poper.pop()
    result_type = semantic_cube[left_type][operator][right_type]
    
    if(result_type != 'err'):
        quads.generate_quad(operator, right_op, '_', left_op)
    else:
        error_message = "ERROR: Type missmatch '{}' '{}' '{}' " .format(left_type, operator, right_type)
        raise Exception(error_message)

def p_return(p):
    '''RETURN : RETURN_K LPAREN EXPRESSION RPAREN SEMICOLON'''
    quads.generate_quad('RETURN', '_', '_', quads.op_stack.pop())
#_____________________________________________________________________________________________________________________________________________


def p_ifelse(p):
    '''IFELSE : IF_K LPAREN H_EXPRESSION RPAREN neural_ifelse BLOCKSTART RSTATEMENT BLOCKEND NELSE neural_ifelse_end'''

#revisa el tipo de la condicion del if, genera el quad y mete el quadcounter a la jumpstack
def p_neural_ifelse(p):
    '''neural_ifelse : EMPTY'''
    exp_type = quads.type_stack.pop()
    if(exp_type != 'int'):
        error_message = "ERROR: Type missmatch '{}' is not valid for an if-statement".format(exp_type)
        raise Exception(error_message)
    else:
        result = quads.op_stack.pop()
        quads.generate_quad('GOTOF', result, '_', '_')
        quads.jump_stack.append(quads.counter - 1)

#mete el quadcounter al ultimo brinco
def p_neural_ifelse_end(p):
    '''neural_ifelse_end : EMPTY'''
    end = quads.jump_stack.pop()
    quads.quads[end][3] = quads.counter

def p_nelse(p):
    '''NELSE : ELSE
            | EMPTY'''

def p_else(p):
    '''ELSE : neural_else ELSE_K BLOCKSTART RSTATEMENT BLOCKEND'''

#genera un quad, mete el quadcounter al ultimo brinco
def p_neural_else(p):
    '''neural_else : EMPTY'''
    quads.generate_quad('GOTO', '_', '_', '_')
    false = quads.jump_stack.pop()
    quads.jump_stack.append(quads.counter - 1)
    quads.quads[false][3] = quads.counter




def p_while_stmt(p):
    '''WHILE_STMT : WHILE_K neural_while_push LPAREN H_EXPRESSION RPAREN neural_while BLOCKSTART RSTATEMENT BLOCKEND neural_while_end'''

#push el counter a la jumpstack
def p_neural_while_push(p):
    '''neural_while_push : EMPTY'''
    quads.jump_stack.append(quads.counter)

#revisa el tipo de la condicion, genera el quad y mete el quadcounter a la jumpstack
def p_neural_while(p):
    '''neural_while : EMPTY'''
    exp_type = quads.type_stack.pop()
    if(exp_type != 'int'):
        error_message = "ERROR: Type missmatch '{}' is not valid for a while-statement".format(exp_type)
        raise Exception(error_message)
    else:
        result = quads.op_stack.pop()
        quads.generate_quad('GOTOF', result, '_', '_')
        quads.jump_stack.append(quads.counter - 1)

#genera el quad y mete el counter al ultimo brinco        
def p_neural_while_end(p):
    '''neural_while_end : EMPTY'''
    end = quads.jump_stack.pop()
    returnn = quads.jump_stack.pop()
    quads.generate_quad('GOTO', '_', '_', returnn)
    quads.quads[end][3] = quads.counter




def p_do_while(p):
    '''DO_WHILE : DO_K neural_do_while BLOCKSTART RSTATEMENT BLOCKEND WHILE_K LPAREN H_EXPRESSION RPAREN neural_do_while_end SEMICOLON'''

#push al jumpstack
def p_neural_do_while(p):
    '''neural_do_while : EMPTY'''
    quads.jump_stack.append(quads.counter)

#revisa el tipo de la condicion, genera el quad
def p_neural_do_while_end(p):
    '''neural_do_while_end : EMPTY'''
    exp_type = quads.type_stack.pop()
    if(exp_type != 'int'):
        error_message = "ERROR: Type missmatch '{}' is not valid for a do_while-statement".format(exp_type)
        raise Exception(error_message)
    else:
        returnn = quads.jump_stack.pop()
        result = quads.op_stack.pop()
        quads.generate_quad('GOTOT', result, '_', returnn)


#_____________________________________________________________________________________________________________________________________________

def p_expression_list(p):
    '''EXPRESSION_LIST : H_EXPRESSION neural_param_exp REXPRESSION_LIST'''

def p_rexpression_list(p):
    '''REXPRESSION_LIST : COMMA EXPRESSION_LIST
                        | EMPTY'''


#creacion del cuadruplo parameter, para poder verificar los parametros en la maquina virtual, despues de validar su tipo y su orden
def p_neural_param_exp(p):
    '''neural_param_exp : EMPTY'''
    
    global parameters_counter
    global last_function

    argument = quads.op_stack.pop()
    argument_type = quads.type_stack.pop()

    if(argument_type == funcdir.functions[last_function]['param_order'][parameters_counter - 1]):
        quads.generate_quad('PARAMETER', argument, '_', parameters_counter-1)
        parameters_counter += 1
    
    else:
        error_message = "ERROR: Argument type '{}' does not match current function".format(argument_type)
        raise Exception(error_message)

#hiper expresion (||, &&)
def p_h_expression(p):
    '''H_EXPRESSION : S_EXPRESSION H_REXPRESSION'''

def p_h_rexpression(p):
    '''H_REXPRESSION : OR neural_op H_EXPRESSION neural_hexpression
                    | AND neural_op H_EXPRESSION
                    | EMPTY'''

def p_neural_hexpression(p):
    '''neural_hexpression : EMPTY'''
    global temporal
    
    if quads.poper:
        if (quads.poper[-1] in ['&&', '||']):
            right_op = quads.op_stack.pop()
            right_type = quads.type_stack.pop()
            left_op = quads.op_stack.pop()
            left_type = quads.type_stack.pop()
            operator = quads.poper.pop()
            result_type = semantic_cube[left_type][operator][right_type]
            if(result_type != 'err'):
                #result = 't' + str(temporal)
                result = virtualM.assign('temporal', result_type)
                temporal += 1
                quads.generate_quad(operator, left_op, right_op, result)
                quads.op_stack.append(result)
                quads.type_stack.append(result_type)
            
            else:
                error_message = "ERROR: Type missmatch '{}' '{}' '{}' " .format(left_type, operator, right_type)
                raise Exception(error_message)

#super expresion (>, >=, <, <=, ==)
def p_s_expression(p):
    '''S_EXPRESSION : EXPRESSION S_REXPRESSION'''

def p_s_rexpression(p):
    '''S_REXPRESSION : GT neural_op S_EXPRESSION neural_sexpression
                    | GTE neural_op S_EXPRESSION neural_sexpression
                    | LT neural_op S_EXPRESSION neural_sexpression
                    | LTE neural_op S_EXPRESSION neural_sexpression
                    | DOUBLEEQUAL neural_op S_EXPRESSION neural_sexpression
                    | NEQUAL neural_op S_EXPRESSION neural_sexpression
                    | EMPTY'''

def p_neural_sexpression(p):
    '''neural_sexpression : EMPTY'''

    global temporal
    
    if quads.poper:
        if (quads.poper[-1] in ['>', '>=', '<', '<=', '==', '!=']):
            right_op = quads.op_stack.pop()
            right_type = quads.type_stack.pop()
            left_op = quads.op_stack.pop()
            left_type = quads.type_stack.pop()
            operator = quads.poper.pop()
            result_type = semantic_cube[left_type][operator][right_type]
            if(result_type != 'err'):
                #result = 't' + str(temporal)
                result = virtualM.assign('temporal', result_type)
                temporal += 1
                quads.generate_quad(operator, left_op, right_op, result)
                quads.op_stack.append(result)
                quads.type_stack.append(result_type)
            
            else:
                error_message = "ERROR: Type missmatch '{}' '{}' '{}' " .format(left_type, operator, right_type)
                raise Exception(error_message)

#expresion (+, -)
def p_expression(p):
    '''EXPRESSION : TERM neural_expression REXPRESSION'''

#checa si el ultimo en el poper es + - y en caso de que si, revisa el cubo semantico y genera el cuadruplo
def p_neural_expression(p):
    '''neural_expression : EMPTY'''
    global temporal
    #para que no marque error si esta vacia la lista
    if quads.poper:
        if(quads.poper[-1] in ['+', '-']):
            right_op = quads.op_stack.pop()
            right_type = quads.type_stack.pop()
            left_op = quads.op_stack.pop()
            left_type = quads.type_stack.pop()
            operator = quads.poper.pop()
            result_type = semantic_cube[left_type][operator][right_type]

            if(result_type != 'err'):
                #result = 't' + str(temporal)
                result = virtualM.assign('temporal', result_type)
                temporal += 1
                quads.generate_quad(operator, left_op, right_op, result)
                quads.op_stack.append(result)
                quads.type_stack.append(result_type)

            else:
                error_message = "ERROR: Type missmatch '{}' '{}' '{}' " .format(left_type, operator, right_type)
                raise Exception(error_message)


def p_rexpression(p):
    '''REXPRESSION : PLUS neural_op EXPRESSION
                    | MINUS neural_op EXPRESSION
                    | EMPTY'''

#agregar operadores al poper
def p_neural_op(p):
    '''neural_op : EMPTY'''
    quads.poper.append(p[-1])

#termino (*, /)
def p_term(p):
    '''TERM : FACTOR neural_term RTERM'''

#checa si el ultimo en el poper es * / y en caso de que si, revisa el cubo semantico y genera el cuadruplo
def p_neural_term(p):
    '''neural_term : EMPTY'''
    global temporal
    #para que no marque error si esta vacia la lista
    if quads.poper:
        if(quads.poper[-1] in ['*', '/']):
            right_op = quads.op_stack.pop()
            right_type = quads.type_stack.pop()
            left_op = quads.op_stack.pop()
            left_type = quads.type_stack.pop()
            operator = quads.poper.pop()
            result_type = semantic_cube[left_type][operator][right_type]

            if(result_type != 'err'):
                #result = 't' + str(temporal)
                result = virtualM.assign('temporal', result_type)
                temporal += 1
                quads.generate_quad(operator, left_op, right_op, result)
                quads.op_stack.append(result)
                quads.type_stack.append(result_type)

            else:
                error_message = "ERROR: Type missmatch '{}' '{}' '{}' " .format(left_type, operator, right_type)
                raise Exception(error_message)
            

def p_rterm(p):
    '''RTERM : TIMES neural_op TERM
            | DIVIDE neural_op TERM
            | EMPTY'''



def p_factor(p):
    '''FACTOR : ID neural_factor_id
                | CONSTANT neural_constant
                | LPAREN H_EXPRESSION RPAREN'''

#revisa que tipo es la constante, lo mete al stack de tipos y mete el operando al stack de operandos y a si no esta, en la tabla de constantes
def p_neural_constant(p):
    '''neural_constant : EMPTY'''

    if (isinstance(p[-1], int)):
        quads.type_stack.append('int')
        type = 'int'
    elif (isinstance(p[-1], float)):
        quads.type_stack.append('float')
        type = 'float'
    elif (isinstance(p[-1], str)):
        quads.type_stack.append('string')
        type = 'string'
    else:
        raise Exception("AAAAAA")
    
    if(p[-1] not in constant_table[0]):
        constant_table[0].append(p[-1])
        virtualadd = virtualM.assign('constant', type)
        constant_table[1].append(virtualadd)

    index = constant_table[0].index(p[-1])
    operand = constant_table[1][index]
    quads.op_stack.append(operand)

#revisa si la variable existe y si si agrega a la pila su tipo y operando
def p_neural_factor_id(p):
    '''neural_factor_id : EMPTY'''
    #checar si existe local
    if(p[-1] in funcdir.functions[last_function]['var_table'][0]):
        i = funcdir.functions[last_function]['var_table'][0].index(p[-1])
        type = funcdir.functions[last_function]['var_table'][1][i]
        operand = funcdir.functions[last_function]['var_table'][2][i]
        quads.type_stack.append(type)
        quads.op_stack.append(operand)
    #checar si existe global
    elif(p[-1] in funcdir.functions[program_name]['var_table'][0]):
        i = funcdir.functions[program_name]['var_table'][0].index(p[-1])
        type = funcdir.functions[program_name]['var_table'][1][i]
        operand = funcdir.functions[program_name]['var_table'][2][i]
        quads.type_stack.append(type)
        quads.op_stack.append(operand)
    
    else:
        error_message = "ERROR: Variable '{}' hasn't been declared.".format(p[-1])
        raise Exception(error_message)
    


def p_empty(p):
    '''EMPTY : '''


















parser = yacc.yacc()

input_file = "stat.txt"

s = ""
with open(input_file) as f:
    lines = f.readlines()
    for l in lines:
        s += l[:-1]
    print(">> Parsing " + input_file + "...")

lexer.input(s)
parser.parse(s)
j = 0
for i in quads.quads:
    
    print(j,i)
    j += 1

print(funcdir.functions)


with open('funcdir.txt', 'w') as file:
    file.write(json.dumps(funcdir.functions))

dictation = {"dictation" : constant_table}
with open('constants.txt', 'w') as file:
    file.write(json.dumps(dictation))

dictation = {"dictation" : quads.quads}
with open('quads.txt', 'w') as file:
    file.write(json.dumps(dictation))