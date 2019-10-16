outerloop:
for (var i = 2; i < 100; i++) {
    if (i % 2 == 0) {
        continue;
    }
    for (var j = 3; j <= i/2; j+=2) {
        if (i % j == 0) {
            continue outerloop;
        }
    }
    console.log(i);

}