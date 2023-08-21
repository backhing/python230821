#function1.py
def setValue(newValue):
    x = newValue
    print("지역변수 x:", x)


result = setValue(5)
print(result)

def swap(x,y):
    return y,x

print(swap(3,4))

