function main() {
    sum = 0
    product = 1
    for (i = 1; i <= 10; i = i + 1) {
        sum = sum + i
        product = product * i
    }
    return sum + product;
}
