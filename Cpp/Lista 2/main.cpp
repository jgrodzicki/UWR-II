#include <iostream>
#include <string>
#include <vector>

using namespace std;

vector<pair<int, string>> m = {{1000, "M"}, {900, "CM"}, {500, "D"}, {400, "CD"}, {100, "C"}, {90, "XC"}, {50, "L"}, {40, "XL"},
                      {10, "X"}, {9, "IX"}, {5, "V"}, {4, "IV"}, {1, "I"}};
//int tab[] = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 5, 4, 1};

string bin2rzym(int x) {
    string res = "";

    for (auto a: m) {
        while (x >= a.first) {
            x -= a.first;
            res += a.second;
        }
    }

    return res + "\n";
}


int main(int argc, char* argv[]) {
    for (int i = 1; i < argc; i++) {

        bool if_good = true;

        for (int j = 0; j < strlen(argv[i]); j++) {
            if (argv[i][j]-'0' < 0 || argv[i][j]-'0' > 9) {
                cerr << argv[i] << " nie jest prawidłowym argumentem!\n";
                if_good = false;
                break;
            }
        }
        if (!if_good)
            continue;

        if (argv[i][0] == '0') {
            cerr << argv[i] << " nie jest prawidłowym argumentem!\n";
            continue;
        }

        try {
            int liczba = stoi(argv[i]);
            if (liczba <= 0 || liczba >= 4000) {
                cerr << argv[i] << " nie jest prawidłową liczbą!\n";
                continue;
            }
            cout << liczba << " -- " << bin2rzym(liczba);

        } catch (...) {
            cerr << argv[i] << " nie jest prawidłowym argumentem! hvyfvyvy\n";
        }


    }


    return 0;
}