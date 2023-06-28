def factorial(n):
    if n == 0 or n == 1:
        return 1 
    else:
        return n * factorial(n - 1)
    
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def calculate_hcf(a, b):
    while b != 0:
        a, b = b, a % b
    return a

print("1 .find factorial , 2.find if the no is prime or not , 3.find hcf of two numbers")
n=int(input("enter desired function number"))
if n==1:
    a=int(input("enter no to find its factorial:"))
    s=factorial(a)
    print(s,"is the factorial of the number")

if n==2:
    a1=int(input("enter number to find whether prime or not"))
    b=is_prime(a1)
    if b==True:
        print("the number is prime")
    else:
        print("the number is not prime")
if n==3:
    c1=int(input("enter first number"))
    c2=int(input("enter second number")) 
    s1=calculate_hcf(c1,c2)
    print(s1,"is the hcf of the given numbers")               


