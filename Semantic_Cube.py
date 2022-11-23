semantic_cube = {}

semantic_cube["int"] = {
    "+" : {"int" : "int", "float" : "float", "string" : "err"},
    "-" : {"int" : "int", "float" : "float", "string" : "err"},
    "*" : {"int" : "int", "float" : "float", "string" : "err"},
    "/" : {"int" : "int", "float" : "float", "string" : "err"},
    "=" : {"int" : "int", "float" : "float", "string" : "err"},
    "==" : {"int" : "int", "float" : "err", "string" : "err"} ,
    "!=" : {"int" : "int", "float" : "int", "string" : "err"} ,
    ">" : {"int" : "int", "float" : "int", "string" : "err"},
    "<" : {"int" : "int", "float" : "int", "string" : "err"},
    ">=" : {"int" : "int", "float" : "int", "string" : "err"},
    "<=" : {"int" : "int", "float" : "int", "string" : "err"},
    "&&" : {"int" : "int", "float" : "int", "string" : "err"},
    "||" : {"int" : "int", "float" : "int", "string" : "err"},
}

semantic_cube["float"] = {
    "+" : {"int" : "float", "float" : "float", "string" : "err"},
    "-" : {"int" : "float", "float" : "float", "string" : "err"},
    "*" : {"int" : "float", "float" : "float", "string" : "err"},
    "/" : {"int" : "float", "float" : "float", "string" : "err"},
    "=" : {"int" : "float", "float" : "float", "string" : "err"},
    "==" : {"int" : "err", "float" : "int", "string" : "err"} ,
    "!=" : {"int" : "int", "float" : "float", "string" : "err"} ,
    ">" : {"int" : "int", "float" : "int", "string" : "err"},
    "<" : {"int" : "int", "float" : "int", "string" : "err"},
    ">=" : {"int" : "int", "float" : "int", "string" : "err"},
    "<=" : {"int" : "int", "float" : "int", "string" : "err"},
    "&&" : {"int" : "int", "float" : "int", "string" : "err"},
    "||" : {"int" : "int", "float" : "int", "string" : "err"},
}

semantic_cube["string"] = {
    "=" :  {"int" : "err", "float" : "err", "string" : "string"} ,
    "==" : {"int" : "err", "float" : "err", "string" : "int"},
    ">" : {"int" : "err", "float" : "err", "string" : "int"},
    "<" : {"int" : "err", "float" : "err", "string" : "int"},
    ">=" : {"int" : "err", "float" : "err", "string" : "int"},
    "<=" : {"int" : "err", "float" : "err", "string" : "int"},
    "&&": {"int" : "int", "float" : "err", "string" : "int"},
    "|" : {"int" : "int", "float" : "err", "string" : "int"},
}