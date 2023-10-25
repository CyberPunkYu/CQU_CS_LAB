
#function :f(x)=x**2+y***2
def get_gradient(x, y):
    return 2*x, 2*y


def gradient_descent():
    x, y = 1,3  
    alpha = 0.1
    epsilon = 0.03
    
    while  x ** 2 + y ** 2> epsilon ** 2:
        grad = get_gradient(x, y)
        x -= alpha * grad[0]  
        y -= alpha * grad[1]
        print("（{},{})".format(x, y))
        
       
    print("the final({},{})value is{}".format(x, y, x ** 2 + y ** 2))


gradient_descent()