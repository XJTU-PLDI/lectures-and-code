function main() {
    accumulator = 42;
    accumulator = sin(accumulator);
    accumulator = accumulator + cos(accumulator) - tan(accumulator);
    return abs(accumulator);
}
