import sys
import re


def parse_equation(equation):
    lefthand, righthand = equation.split('=')
    
    def parse_terms(side):
        terms = re.findall(r'([+-]?\d*\.?\d*)\s*\*\s*X\^(\d+)', side)
        parsed_dict = {}
        for coef, exp in terms:
            coef = coef.replace(' ', '')
            if coef in (' ', ''):
                coef = 1
            elif coef == '-':
                coef = -1
            else:
                coef = float(coef)
            exp = int(exp) if exp else 0
            parsed_dict[exp] = parsed_dict.get(exp, 0) + coef
        return parsed_dict
    
    left_terms = parse_terms(lefthand)
    right_terms = parse_terms(righthand)
    
    for exp, coef in right_terms.items():
        left_terms[exp] = left_terms.get(exp, 0) - coef
    
    return left_terms


def reduce_equation(terms):
    reduced = ' + '.join(f'{coef} * X^{exp}' for exp, coef in sorted(terms.items(), reverse=False) if coef != 0)
    reduced = reduced.replace('+ -', '- ')
    return reduced + ' = 0'


def computerv1(terms):
    degree = max(terms.keys())
    
    if degree > 2:
        return "The polynomial degree is strictly greater than 2, I can't solve."
    
    if degree == 0:
        if terms[0] == 0:
            return "All real numbers are solutions."
        else:
            return "No solution."
    
    if degree == 1:
        a, b = terms.get(1, 0), terms.get(0, 0)
        solution = -b / a
        return f"The solution is: {solution}"
    
    if degree == 2:
        a, b, c = terms.get(2, 0), terms.get(1, 0), terms.get(0, 0)
        discriminant = b**2 - 4*a*c
        
        if discriminant > 0:
            x1 = (-b + (discriminant)**0.5) / (2*a)
            x2 = (-b - (discriminant)**0.5) / (2*a)
            return f"Discriminant is strictly positive, the two solutions are:\n{x1}\n{x2}"
        elif discriminant == 0:
            x = -b / (2*a)
            return f"Discriminant is zero, the solution is:\n{x}"
        else:
            return "Discriminant is strictly negative, there are no real solutions." 


def main():
    if len(sys.argv) != 2:
        print("Usage: python computerv1.py \"equation\"")
        return
    
    equation = sys.argv[1]
    terms = parse_equation(equation)
    reduced_form = reduce_equation(terms)
    degree = max(terms.keys())
    
    print(f"Reduced form: {reduced_form}")
    print(f"Polynomial degree: {degree}")
    print(computerv1(terms))


if __name__ == '__main__':
    main()