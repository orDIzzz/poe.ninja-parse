from poeparser import POEParser

if __name__ == '__main__':
    parser = POEParser()
    print(parser.get_prices(category=['Oils']))
