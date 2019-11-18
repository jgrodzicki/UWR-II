process.stdin.once('data', (name) => {
    process.stdout.write('Witaj ' + name)
    process.exit();
});