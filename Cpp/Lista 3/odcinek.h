//
// Created by Jakub Grodzicki on 2019-03-12.
//

#ifndef LISTA_3_ODCINEK_H
#define LISTA_3_ODCINEK_H

#include "punkt.h"

class odcinek {
private:
    punkt start, end;

public:
    odcinek(punkt start, punkt end);
    odcinek(const odcinek &o);
    odcinek operator=(const odcinek &o) const {return odcinek(o);};
    void translate(double dx, double dy);
    void rotate(punkt p, double rad);
    double length();
    bool is_middle(punkt p);
    bool is_on_line_seg(punkt p);
    punkt middle();
    punkt getStart();
    punkt getEnd();

    static bool is_parallel(odcinek a, odcinek b);
    static bool is_perpendicular(odcinek a, odcinek b);
    static punkt cross(odcinek a, odcinek b);

    std::string to_string();
};


#endif //LISTA_3_ODCINEK_H
