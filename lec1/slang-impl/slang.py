import sys
from tokenizer import tokenize
from parser import parse
from interpreter import interpret

def main():
    if len(sys.argv) < 2:
        print("使用方法: python slang.py <源文件>")
        return

    filename = sys.argv[1]
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()

    tokens = tokenize(source)
    module = parse(tokens)
    return_value = interpret(module)
    print(f"主函数的返回值是: {return_value}")

if __name__ == '__main__':
    main()
