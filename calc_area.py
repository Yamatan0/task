# Функции 
def calc_circle_area(radius):
    pi = 3.14
    circle_area = pi * (radius**2)
    return circle_area

def calc_triangle_area(a, b, c):
    p = (a + b + c) / 2
    area = p * (p - a) * (p - b) * (p - c)
    if area <= 0:
        return 0
    triangle_area = area ** 0.5
    return  triangle_area

def is_right_triangle(a, b, c):
    sides = [a, b, c]
    gipotenuza=[]
    katets=sides
    
    for i in sides :
        for k in sides:
            for j in sides:
                if i>k>j:
                    gipotenuza.append(i) 
                    katets.remove(i)   
    if sum(katets)**2==sum(gipotenuza):
        triangle='прямоугольный'
    else:
        triangle='не прямоугольный'
    return triangle

# Расчет
print("Введите числовые значения через пробел.")
print("Целую часть отделите точкой.")
input_data = input()
numbers = input_data.strip().split()

sides = []
for num in numbers:
    try:
        sides.append(float(num))
    except ValueError:
        print(f"Значение '{num}' не является числом.")
if len(sides) == 1:
    radius = sides[0]
    if radius <= 0:
        print("Радиус не может быть меньше нуля.")
    area = calc_circle_area(radius)
    print(f"Площадь круга = {area}")
elif len(sides) == 3:
    a, b, c = sides
    if a <= 0 or b <= 0 or c <= 0:
        print("Вы ввели отрицательную длинну стороны")
    if (a + b <= c) or (a + c <= b) or (b + c <= a):
        print("Нельзя постороить треугольник с заданнами сторонами")  
    area = calc_triangle_area(a, b, c)
    print(f"Это {is_right_triangle(a, b, c)} треугольник")
    print(f"Площадь треугольника = {area}") 
else:
    print("Нет функции для данного количества значений")
