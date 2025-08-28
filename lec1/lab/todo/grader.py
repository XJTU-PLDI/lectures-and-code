
# 测试你有没有不小心破坏原本的功能
def test_original_code() -> bool:
    try:
        pass
    except:
        return False
    return True

# 测试你的 "添加 for 语法" 这一任务的完成度
def test_for() -> bool:
    try:
        pass
    except:
        return False
    return True

# 测试你的 "添加内置函数 sin cos tan abs" 这一任务的完成度
def test_builtin_functions() -> bool:
    try:
        pass
    except:
        return False
    return True

def main():
    tests = {
        "测试原功能": test_original_code,
        "测试 for 语法": test_for,
        "测试添加内置函数": test_builtin_functions
    }
    
    score = 0
    max_score = len(tests)
    for name, func in tests.items():
        if func():
            print(f"测试点 {name} 已通过")
            score += 1
        else:
            print(f"测试点 {name} 未通过")

    print(f"你在本次测试中获得了 {score} / {max_score} 分")
    if score == max_score:
        print("恭喜你通过了测试!")
    else:
        print("仍有测试未通过，加油哦")

if __name__ == "__main__":
    main()
