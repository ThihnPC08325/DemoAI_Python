from sympy import symbols, solve

# Vòng lặp
for i in range(10):
    print(f"Số: {i}")

# Điều kiện
age = float(input("Mời bạn nhập tuổi của mình: "))
if age >= 18:
    print("Bạn đã đủ tuổi trưởng thành!")
else:
    print("Bạn chưa đủ tuổi trưởng thành.")


# Yêu cầu người dùng nhập cân nặng và chiều cao
weight = float(input("Nhập cân nặng của bạn (kg): "))
height = float(input("Nhập chiều cao của bạn (m): "))  # VD: 1m75 = 1.75

# Tính BMI
bmi = weight / (height**2)

# Phân loại chỉ số BMI
if bmi < 18.5:
    classification = "Gầy"
elif 18.5 <= bmi < 24.9:
    classification = "Bình thường"
elif 25 <= bmi < 29.9:
    classification = "Thừa cân"
else:
    classification = "Béo phì"

# Hiển thị kết quả
print(f"\nChỉ số BMI của bạn là: {bmi:.2f}")
print(f"Phân loại: {classification}")

# Định nghĩa biến và hệ số
x = symbols("x")  # Biến x
a = float(input("Nhập hệ số a: "))
b = float(input("Nhập hệ số b: "))
c = float(input("Nhập hệ số c: "))
d = float(input("Nhập hệ số d: "))

# Định nghĩa phương trình
equation = a * x**3 + b * x**2 + c * x + d

# Giải phương trình
solutions = solve(equation, x)

# Hiển thị nghiệm
print("\nCác nghiệm của phương trình là:")
for sol in solutions:
    print(f"{sol:.1f}")