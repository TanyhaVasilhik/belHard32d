test = input("Введите текст")
dict = {symbol:test.count(symbol) for symbol in test}

print(dict)