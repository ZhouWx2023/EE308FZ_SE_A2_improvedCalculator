# -*- coding: utf-8 -*-
import re, time, math

def math_sign(sign, par_ans):
    if sign == 'cos':
        par_ans = str(math.cos(math.radians(float(par_ans))))
    elif sign == 'sin':
        par_ans = str(math.sin(math.radians(float(par_ans))))
    elif sign == 'tan':
        par_ans = str(math.tan(math.radians(float(par_ans))))
    elif sign == 'log':
        par_ans = str(math.log(float(par_ans)) / math.log(10))
    elif sign == 'ln':
        par_ans = str(math.log(float(par_ans)))
    elif sign == 'abs':
        par_ans = str(abs(float(par_ans)))
    return par_ans


def clean(string):
    '''Judge if the data is illegal or not'''
    b = 0
    for i in string:  # Judge 
        if b < 0: break
        if i == "(":
            b += 1
        elif i == ")":
            b -= 1
    #    character = re.search("[a-zA-Z\=]", string)  # No letter is empty
    kh = len(re.findall("\d+\.?\d*[\(]", string))  # judge if the bracket with data
    kh1 = len(re.findall("[()]", string))  # judge if there is bracket
    #    dian = re.search("(\d+\.\.\d+)", string)  # judge if the point is repeated ..
    if kh1 % 2 == b == kh:
        return string.replace(" ", "")  # remove the space in the string
    return 0


def sign_replace(string):
    '''replace the sign'''
    string = str(string)
    string = string.replace("++", "+")
    string = string.replace("+-", "-")
    string = string.replace("-+", "-")
    string = string.replace("--", "+")
    string = string.replace("*+", "*")
    string = string.replace("/+", "/")
    return string


def ccf(xx):
    '''Product and division'''
    if re.search("\(", xx): xx = xx[1:-1]  # remove the bracket
    while re.search("[\*\/\%]", xx):
        times = re.search("\d+\.?\d*[\*\/\%]{1}\-?\d+\.?\d*", xx)
        if times:
            times = times.group()
            if times.count("*") == 1:  # product operation
                a, b = times.split("*")
                xx = xx.replace(times, str(float(a) * float(b)))
            elif times.count("/") == 1:
                a, b = times.split("/") # division operation
                xx = xx.replace(times, str(float(a) / float(b)))
            elif times.count('%') == 1:
                a, b = times.split("%") # mod operation
                xx = xx.replace(times, str(int(a) % int(b)))
        else:
            return xx
    return xx


def jjf(xx):
    '''addition and substraction'''
    if "(" in xx: xx = xx[1:-1]  # remove bracket
    while re.search("\d+\.?\d*[\+\-]\d+\.?\d*", xx):
        findret = re.search("[\-]?\d+\.?\d*[\+\-]\d+\.?\d*", xx)
        if findret:
            findret = findret.group()
            if re.search("\d+\.?\d*\+\d+\.?\d*", findret):  # addition
                a, b = findret.split("+")
                xx = xx.replace(findret, str(float(a) + float(b)))
            elif re.search("\d+\.?\d*\-\d+\.?\d*", findret):  # substraction
                a, b = findret.split("-")
                xx = xx.replace(findret, str(float(a) - float(b)))
        else:
            return xx
    return xx


def parre(string):
    '''searching for the bracket'''
    string = re.search("[a-z]*(\([^()]+\))", string)
    if string: return string.group()  # when bracket is found return the result
    return 0  # if it is not found return zero


def expo(string):
    string = re.search("[a-z0-9\.]*(\{[^{}]+\})", string)
    if string: return string.group()  # when exponent number is find return the result
    return 0  # if it is not found return zero


def iter(string):
    string = re.search("[0-9]*!", string)
    if string: return string.group()  # when the iteration sign is found return the result
    return 0  # if it is not found return zero


def count(sample):
    sample = clean(sample)  # judge if the formula is illegal or not
    sample = sample.replace('mod', '%')
    sample = sample.replace('e', str(math.e))
    sample = sample.replace('pi', str(math.pi))
    if sample:  # if it is legal then do the special extended function 
        while sample.count('!') > 0:
            iters = iter(sample)
            num = iters[:-1]
            num = int(num)
            temp = 1
            for i in range(1, num + 1):
                temp *= i
            sample = sample.replace(iters, str(temp))
        while sample.count('{') > 0:  # dealing with the exponential number
            exp = expo(sample)
            exp_place = exp.find('{')
            x = exp[0:exp_place]
            exp_part = exp[exp_place:]
            exp_ans = float(x) ** float(exp_part[1:-1])
            sample = sample.replace(exp, str(exp_ans))
        while sample.count("(") > 0:  # if the bracket is kept on
            par = parre(sample)  # searching the bracket
            if par[0] == '(':
                sample = sample.replace(par, str(count(sign_replace(par[1:-1]))))  # replace the bracket
            else:
                par_place = par.find('(')
                sign = par[0:par_place]
                par_part = par[par_place:]
                par_ans = count(sign_replace(par_part[1:-1]))
                ans = math_sign(sign, par_ans)
                sample = sample.replace(par, ans)
        else:  # without bracket
            ret = jjf(ccf(sign_replace(sample)))
            if "+" in ret: ret = ret[1:]  # get the sign before the positive number
            while len(re.findall("\d+\.?\d*[\+\-\*\/\%]+\d+\.?\d*", ret)) > 0:
                ret = jjf(ccf(sign_replace(ret)))
    else:
        print("The program is illegal, cannot be calculated")
    return ret



