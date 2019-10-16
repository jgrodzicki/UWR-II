S = new Set();
for (var i = 1; i <= 1000000; i++) {
    sum = 0;
    number = i;
    var flag = true;
    while (number) {
        var d = number % 10;
        if (number % d) {
            flag = false;
            break;
        }
        sum += d;
        number = Math.floor(number / 10);
    }

    if (flag && !(number % sum)) {
        S.add(i);
    }
}
console.log(S.size)