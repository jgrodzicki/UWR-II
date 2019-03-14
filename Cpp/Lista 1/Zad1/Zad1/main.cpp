//
//  main.cpp
//  Zad1
//
//  Created by Jakub Grodzicki on 26/02/2019.
//  Copyright © 2019 Jakub Grodzicki. All rights reserved.
//

#include <iostream>
#include <math.h>
using namespace std;

int main(int argc, const char * argv[]) {
    float a, b, c;
    clog << "Podaj długości boków trójkąta: ";
    cin >> a;
    cin >> b;
    cin >> c;
    
    if (a < 0 || b < 0 || c < 0 || a >= b + c || b >= a + c || c >= a + b) {
        clog << "Nieprawidłowe długości boków";
        return -1;
    }
    
    float p = (a + b + c)/2;
    cout.precision(2);
    cout << "Pole: " << sqrt(p*(p-a)*(p-b)*(p-c));
    
    return 0;
}
