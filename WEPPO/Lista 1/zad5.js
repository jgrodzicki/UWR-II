function fib_rec(n) {
    if (n == 1 || n == 2) {
        return 1;
    }
    return fib_rec(n-1) + fib_rec(n-2);
}

function fib_iter(n) {
    if (n == 1 || n == 2) {
        return 1;
    }
    var last = 1;
    var prev = 0;
    var fib = 0;
    for (var i = 1; i <= n; i++) {
        prev = last;
        last = fib;
        fib = last + prev;
    }
    return fib;
}


console.time('fib_rec_time');
fib_rec(40);
console.timeEnd('fib_rec_time');

console.time('fib_iter_time');
fib_iter(40);
console.timeEnd('fib_iter_time');

