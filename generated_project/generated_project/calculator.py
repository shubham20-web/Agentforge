class Calculator:
  def __init__(self):
    pass
  def add(self, num1, num2):
    return num1 + num2
  def subtract(self, num1, num2):
    return num1 - num2
  def multiply(self, num1, num2):
    return num1 * num2
  def divide(self, num1, num2):
    if num2 == 0:
      raise ZeroDivisionError('Cannot divide by zero')
    return num1 / num2

def main():
  calculator = Calculator()
  print(calculator.add(5, 3))
  print(calculator.subtract(10, 4))
  print(calculator.multiply(7, 2))
  print(calculator.divide(9, 3))
  try:
    print(calculator.divide(9, 0))
  except ZeroDivisionError as e:
    print(e)

if __name__ == "__main__":
  main()