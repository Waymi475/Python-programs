while True:
    try:
        a = float(input("Введите первое число: "))
        op = input("Введите операцию (+, -, *, /): ")
        b = float(input("Введите второе число: "))

        if op == "+":
            print("Результат:", a + b)

        elif op == "-":
            print("Результат:", a - b)

        elif op == "*":
            print("Результат:", a * b)

        elif op == "/":
            if b == 0:
                while True:
                    print("я умею делить на ноль")
            else:
                print("Результат:", a / b)

        else:
            print("я не понял ваши буквы")

    except ValueError:
        print("Ошибка стоп 0000")