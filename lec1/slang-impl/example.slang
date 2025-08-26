# 全局赋值
g1 = 42; # 这是一个整数
g2 = 3.14; # 这是一个浮点数

# 函数定义，参数测试
function foo(x, y) {
    # 块语句
    {
        z = x + y; # 求和
        print(z);
    }
    # if-else 测试
    if (x > y) print(x);
    else {
        print(y);
    }
    # while 测试
    while (z > 0) {
        z = z - 1;
        if (z == 2) {
            continue; # 跳过2
        }
        if (z < 1) {
            break; # 跳出循环
        }
        print(z);
    }
    # return 测试
    return z;
}

# 单参数函数
function bar(a) {
    b = -a * 2 + 5 / 2 - (a + 1);
    print(b);
    return b != 0;
}

# 无参数函数
function noArg() {
    print(123);
    return;
}

# 嵌套调用
function main() {
    res = foo(10, 20);
    flag = bar(res);
    if (!flag) noArg();
    # 复杂表达式
    v = (g1 + g2) * (res - 1) / 2;
    print(v);
    return 1;
}

