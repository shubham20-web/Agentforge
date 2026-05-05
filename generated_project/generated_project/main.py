import pandas as pd
import matplotlib.pyplot as plt

class Calculator:
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

def load_csv(file_path):
  try:
    data = pd.read_csv(file_path)
    return data
  except Exception as e:
    print(f'Error loading CSV: {e}')

def display_statistics(data):
  print('Data Statistics:')
  print(data.describe())

def plot_graph(data, column):
  try:
    plt.figure(figsize=(10,6))
    plt.plot(data[column])
    plt.title(f'{column} Graph')
    plt.xlabel('Index')
    plt.ylabel(column)
    plt.show()
  except Exception as e:
    print(f'Error plotting graph: {e}')

def main():
  calculator = Calculator()
  while True:
    print('1. Addition')
    print('2. Subtraction')
    print('3. Multiplication')
    print('4. Division')
    print('5. Quit')
    print('6. Load CSV')
    choice = input('Choose an operation (1/2/3/4/5/6): ')
    if choice in ('1', '2', '3', '4'):
      try:
        num1 = float(input('Enter first number: '))
        num2 = float(input('Enter second number: '))
        if choice == '1':
          print(f'{num1} + {num2} = {calculator.add(num1, num2)}')
        elif choice == '2':
          print(f'{num1} - {num2} = {calculator.subtract(num1, num2)}')
        elif choice == '3':
          print(f'{num1} * {num2} = {calculator.multiply(num1, num2)}')
        elif choice == '4':
          try:
            print(f'{num1} / {num2} = {calculator.divide(num1, num2)}')
          except ZeroDivisionError as e:
            print(str(e))
      except ValueError:
        print('Invalid input. Please enter a number.')
    elif choice == '5':
      break
    elif choice == '6':
      file_path = input('Enter CSV file path: ')
      data = load_csv(file_path)
      if data is not None:
        display_statistics(data)
        column = input('Enter column name to plot: ')
        plot_graph(data, column)
    else:
      print('Invalid choice. Please choose a valid operation.')

if __name__ == '__main__':
  main()