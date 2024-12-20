



import math

def derivative(expr, x):
    
    
    h = 0.0001
    return (eval(expr.replace('x', str(x + h))) - eval(expr.replace('x', str(x)))) / h

def integral(expr, a, b):
    
    
    n = 1000  
    total = 0
    dx = (b - a) / n
    
    for i in range(n):
        x = a + i * dx
        total += eval(expr.replace('x', str(x))) * dx
        
    return total

def main():
    while True:
        print("\nCalc Calculator")
        print("1. Find derivative")
        print("2. Find integral")
        print("3. Exit")
        
        choice = input("Pick what to do (1-3): ")
        
        if choice == '1':
            expr = input("Enter function (use x as variable, like x**2): ")
            x = float(input("Find derivative at x = "))
            try:
                result = derivative(expr, x)
                print(f"Derivative at x = {x} is approximately {result:.4f}")
            except:
                print("Oops something went wrong! Check your function")
                
        elif choice == '2':
            expr = input("Enter function to integrate: ")
            a = float(input("Lower bound: "))
            b = float(input("Upper bound: "))
            try:
                result = integral(expr, a, b)
                print(f"Integral from {a} to {b} is approximately {result:.4f}")
            except:
                print("Oops something went wrong! Check your function")
                
        elif choice == '3':
            break
            
        else:
            print("Pick 1, 2 or 3!")

if __name__ == "__main__":
    main()
