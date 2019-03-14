//
// Created by Jakub Grodzicki on 2019-03-13.
//

#ifndef LISTA_3_TROJKAT_H
#define LISTA_3_TROJKAT_H


#include "punkt.h"

class trojkat {
private:
    punkt a, b, c;

public:
    trojkat(punkt a, punkt b, punkt c);
    trojkat(const trojkat &t);
    void translate(double dx, double dy);
    void rotate(punkt p, double rad);
    double area();
    double per();
    double sign(punkt p1, punkt p2, punkt p3);
    bool is_in(punkt p);
    punkt middle();
    punkt getA();
    punkt getB();
    punkt getC();

    static bool is_separable(trojkat t1, trojkat t2);
    static bool is_containing(trojkat t1, trojkat t2);

    std::string to_string();
};


#endif //LISTA_3_TROJKAT_H
