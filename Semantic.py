from Token import *

expression_automata = [
    [0, -1, -1, -1, 0, -1, 1, 10, 3, 2, -1],
    [-2, 0, -2, -2, -2, 1, -2, -2, -2, -2, -2],
    [-3, -3, 5, 4, -3, 2, -3, -3, -3, -3, -3],
    [-4, 0, 5, 4, -4, 3, -4, -4, -4, -4, -4],
    [-5, -5, -5, -5, 4, -5, -5, -5, 2, 2, -5],
    [5, -6, -6, -6, 5, -6, 8, -6, 7, 6, -1],
    [-7, 0, -7, 9, -7, 6, -7, -7, -7, -7, -7],
    [-8, 0, -8, 9, -4, 7, -8, -8, -8, -8, -8],
    [-9, 0, -9, -9, -9, 8, -9, -9, -9, -9, -9],
    [-10, -10, -10, -10, 9, -10, -10, -10, 6, 6, -10],
    [-12, -12, 11, -12, -12, 10, -12, -12, -12, -12, -12],
    [-13, -13, -13, -13, -13, -13, -13, 12, 12, -13, -13],
    [-14, 0, -14, -14, -14, 12, -14, -14, -14, -14, -14]
]

statement_automata = [
    [-1, -1, -1, 5, 8, 1, 0, -1, -1, 0, 0, -1, -1, 12, -1, -1, -1],  # 0
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1],
    [-2, -2, -2, -2, -2, -2, 0, 1, 3, -2, -2, -2, -2, -2, -2, -2, -2],
    [-3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, 3, -3, 4, 4, -3, -3],
    [-4, -4, -4, -4, -4, -4, 0, -4, -4, -4, -4, -4, 4, 6, -4, -4, -4],
    [-5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, 6, -5, -5, -5],  # 5
    [-6, -6, -6, -6, -6, -6, -6, 5, 7, -6, -6, -6, -6, -6, -6, -6, -6],
    [-7, -7, -7, -7, -7, -7, 0, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7],
    [-8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, 9, -8, -8, -8],
    [-9, -9, -9, -9, -9, -9, 0, 8, 10, -9, -9, -9, -9, -9, -9, -9, -9],
    [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, 10, -10, 11, -10, 11, -10],  # 10
    [-11, 10, -11, -11, -11, -11, 0, -11, -11, -11, -11, -11, 11, -11, -11, -11, -11],
    [10, -12, 13, -12, -12, -12, -12, -12, 14, -12, -12, -12, -12, -12, -12, -12, -12],
    [-13, -13, -13, -13, -13, -13, 0, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13],
    [-14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, 14, -14, 15, 4, 11, -14],
    [10, 10, 13, -15, -15, -15, 0, -15, -15, -15, -15, -15, 15, -15, -15, -15, -15]  # 15
]

operation_priority = {'(':1 ,'+': 2, '-': 2, '*': 3, '/': 3}

operation_stack = []
variable_stack = []

defined_var = dict()

def get_value(var):
    try:
        res = int(var)
        return res
    except:
        return defined_var[var][1]


def calculate():
    tmp_operation = operation_stack.pop()
    if tmp_operation == '-':
        first_num = get_value(variable_stack.pop())
        second_num = get_value(variable_stack.pop())
        return [True,second_num - first_num]
    if tmp_operation == '+':
        first_num = get_value(variable_stack.pop())
        second_num = get_value(variable_stack.pop())
        return [True,second_num + first_num]
    if tmp_operation == '*':
        first_num = get_value(variable_stack.pop())
        second_num = get_value(variable_stack.pop())
        return [True,second_num * first_num]
    if tmp_operation == '/':
        first_num = get_value(variable_stack.pop())
        second_num = get_value(variable_stack.pop())
        if first_num == 0:
            return [False,'Division by Zero']
        return [True,second_num / first_num]


def find_end(tokens,start_token,char):
    token_enum = start_token + 0
    if char == ')':
        parentheses_count = 0
        finded = False
        while not finded:
            if tokens[token_enum] == '(':
                parentheses_count += 1
            elif tokens[token_enum] == ')':
                parentheses_count -= 1
            if parentheses_count == 0:
                return token_enum
            token_enum += 1
        return -1
    else:
        if char == '}':
            brace_count = 0
            finded = False
            while not finded:
                if tokens[token_enum] == '{':
                    brace_count += 1
                elif tokens[token_enum] == '}':
                    brace_count -= 1
                if brace_count == 0:
                    return token_enum
                token_enum += 1
            return -1
        elif char == ';':
            finded = False
            while not finded and token_enum<len(tokens):
                if tokens[token_enum] == ';':
                    return token_enum + 1
                token_enum += 1
            return -1


def check_expression(tokens,start=0,end=0):
    current_state = 0
    token_enum = start + 0
    while token_enum < end and current_state >= 0:
        current_state = expression_automata[current_state][token_expression_num(tokens[token_enum].strip())]
        if current_state >= 0 :
            token_enum += 1
    if current_state < 0 :
        return [current_state,False,token_enum]
    return [current_state,True,token_enum]

def sem_check(tokens,start=0,end=0):
    return check_statement(tokens=tokens,start=start,end=end)

def check_statement(tokens,start=0,end=0):
    current_state = 0
    token_enum = start
    token_end = end
    while token_enum < token_end and current_state >= 0:
        tmp_token = tokens[token_enum].strip()
        tmp_state = current_state + 0
        current_state = statement_automata[current_state][token_statement_num(tmp_token)]
        if current_state == 12:
            if tmp_token in defined_var:
                last_variable = tmp_token
            else:
                return [False,token_enum,'Variable is not Defined']
        if current_state == 9:
            if tmp_token not in defined_var:
                defined_var[tmp_token] = ['int',None]
                last_variable = tmp_token
            else:
                return [False,token_enum,'Variable is Defined Before']
        elif current_state == 2 :
            if tmp_token not in defined_var:
                defined_var[tmp_token] = ['char', None]
                last_variable = tmp_token
            else:
                return [False, token_enum, 'Variable is Defined Before']
        elif current_state == 6:
            if tmp_token not in defined_var:
                defined_var[tmp_token] = ['bool', None]
                last_variable = tmp_token
            else:
                return [False, token_enum, 'Variable is Defined Before']
        if current_state == 10 and tmp_token is not '=':
            if len(operation_stack) > 0 and operation_priority[operation_stack[-1]] > operation_priority[tmp_token] and tmp_token is not '(':
                while len(operation_stack) > 0 and operation_priority[operation_stack[-1]] > operation_priority[tmp_token] and tmp_token is not '(':
                    cal_res = calculate()
                    if cal_res[0]:
                        variable_stack.append(cal_res[1])
                    else:
                        return cal_res
            elif len(operation_stack)>0 and tmp_token!='(' and operation_stack[-1]!='(' and operation_priority[operation_stack[-1]] == operation_priority[tmp_token]:
                cal_res = calculate()
                if cal_res[0]:
                    variable_stack.append(cal_res[1])
                else:
                    return cal_res
            operation_stack.append(tmp_token)
        if current_state == 11 :
            if tmp_token == ')':
                while operation_stack[-1] is not '(':
                    cal_res = calculate()
                    if cal_res[0]:
                        variable_stack.append(cal_res[1])
                    else:
                        return cal_res
                operation_stack.pop()
            else:
                variable_stack.append(tmp_token)
        if tmp_state == 11 and current_state == 0:
            while len(operation_stack)> 0:
                cal_res = calculate()
                if cal_res[0]:
                    variable_stack.append(cal_res[1])
                else:
                    return cal_res
            defined_var[last_variable][1] = int(variable_stack.pop())
            print(defined_var[last_variable])
        if current_state == 0 and tmp_token == 'if':
            result = check_if(tokens,start=token_enum+1)
            if result[1]:
                token_enum = result[0] + 1
            else:
                return [result[0], False , result[2]]
        elif current_state == 0 and tmp_token == 'while':
            result = check_while(tokens,start=token_enum+1)
            if result[1]:
                token_enum = result[0] + 1
            else:
                return result
        elif current_state >= 0:
            token_enum += 1
    if current_state != 0:
        return [current_state,False , token_enum]
    return [current_state , True , token_enum]


def check_if(tokens,start):
    token_enum = start + 0
    if tokens[token_enum] == '(':
        start_statement = find_end(tokens, token_enum, char=')')
        result = check_expression(tokens, start=token_enum + 1, end=start_statement)
        if not result[1]:
            return result
        else:
            if tokens[start_statement + 1] == '{':
                end_statement = find_end(tokens, start_statement + 1, char='}')
                statement_bool = check_statement(tokens=tokens, start=start_statement + 2, end=end_statement)
                if not statement_bool[1]:
                    return [statement_bool[0] , False , statement_bool[2]]
            else:
                end_statement = find_end(tokens, start_statement + 1, char=';')
                if end_statement == -1 :
                    return [-1000, False , start_statement+1]
                statement_bool = check_statement(tokens=tokens, start=start_statement + 1, end=end_statement)
                if not statement_bool[1]:
                    return [statement_bool[0] , False , statement_bool[2]]
            if len(tokens) > end_statement+1 and tokens[end_statement+1] == 'else':
                if tokens[end_statement + 2] == '{':
                    end_statement_tmp = find_end(tokens, end_statement + 2, char='}')
                    statement_bool = check_statement(tokens=tokens, start=end_statement + 3, end=end_statement_tmp)
                    if not statement_bool[1]:
                        return [statement_bool[0] , False , statement_bool[2]]
                else:
                    end_statement_tmp = find_end(tokens, end_statement + 2, char=';')
                    if end_statement_tmp == -1:
                        return [start_statement + 1, False, -1000]
                    statement_bool = check_statement(tokens=tokens, start=end_statement + 2, end=end_statement_tmp)
                    if not statement_bool[1]:
                        return [statement_bool[0] , False , statement_bool[2]]
                return [end_statement_tmp , True]
            else:
                return [end_statement , True]
    return -1


def check_while(tokens,start):
    token_enum = start + 0
    if tokens[token_enum] == '(':
        start_statement = find_end(tokens, token_enum, char=')')
        result = check_expression(tokens, start=token_enum + 1, end=start_statement)
        if not result[1]:
            return result
        else:
            if tokens[start_statement+1] == '{':
                end_statement = find_end(tokens, start_statement + 1, char='}')
                result = check_statement(tokens=tokens, start=start_statement + 2, end=end_statement)
                if not result[1]:
                    return [result[0],False , result[2]]
            else:
                end_statement = find_end(tokens, start_statement + 1, char=';')
                if end_statement == -1:
                    return [-1000, False, start+1]
                result = check_statement(tokens=tokens, start=start_statement + 1, end=end_statement)
                if not result[1]:
                    return [result[0], False , result[2]]
            return [end_statement , True]
    return -1