#include <iostream>
#include "punkt.h"
#include "odcinek.h"
#include "trojkat.h"

using namespace std;

int main() {
    punkt p1 = punkt(0.0, 0.0);
    punkt p2 = punkt(1.0, 1.0);
    punkt p3 = punkt(3.0, 3.0);
    punkt p4 = punkt(2.0, 0.0);
    cout << punkt::if_same_point(p1, p2) << endl << endl;


    odcinek o1 = odcinek(p1, p2);
    odcinek o2 = odcinek(p3, p4);
    cout << o1.to_string() << endl;
    cout << o1.middle().to_string() << endl;
    cout << o1.is_on_line_seg(p1) << endl;
    cout << odcinek::is_parallel(o1, o2) << endl;
    cout << odcinek::is_perpendicular(o1, o2) << endl << endl;


    trojkat t1 = trojkat(p1, p2, p4);
    cout << t1.to_string() << endl;
    cout << "Is in? " << t1.is_in(p1) << endl;
    cout << "Pole: " << t1.area() << endl;
    cout << "Middle of triangle: " << t1.middle().to_string() << endl;


    return 0;
}