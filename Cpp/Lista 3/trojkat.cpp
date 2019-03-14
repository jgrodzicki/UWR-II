//
// Created by Jakub Grodzicki on 2019-03-13.
//

#include <iostream>
#include <math.h>
#include <stdexcept>
#include <string>
#include "trojkat.h"
#include "odcinek.h"


trojkat::trojkat(punkt a, punkt b, punkt c) {
    this->a = a;
    this->b = b;
    this->c = c;

    if (this->area() == 0)
        throw std::invalid_argument("podane punkty są współliniowe");
}

trojkat::trojkat(const trojkat &t) {
    this->a = t.a;
    this->b = t.b;
    this->c = t.c;
}

void trojkat::translate(double dx, double dy) {
    this->a.translate(dx, dy);
    this->b.translate(dx, dy);
    this->c.translate(dx, dy);
}


void trojkat::rotate(punkt p, double rad) {
    this->a.rotate(p, rad);
    this->b.rotate(p, rad);
    this->c.rotate(p, rad);
}

double trojkat::area() {
    double a = odcinek(this->a, this->b).length();
    double b = odcinek(this->a, this->c).length();
    double c = odcinek(this->b, this->c).length();
    double p = (a+b+c)/2;
    return sqrt(p*(p-a)*(p-b)*(p-c));
}

double trojkat::per() {
    double a = odcinek(this->a, this->b).length();
    double b = odcinek(this->a, this->c).length();
    double c = odcinek(this->b, this->c).length();
    return a+b+c;
}

punkt trojkat::middle() {
    double x = (this->a.getX() + this->b.getX() + this->c.getX())/3;
    double y = (this->a.getY() + this->b.getY() + this->c.getY())/3;
    return punkt(x, y);
}

double trojkat::sign (punkt p1, punkt p2, punkt p3){
    return (p1.getX() - p3.getX()) * (p2.getY() - p3.getY()) - (p2.getX() - p3.getX()) * (p1.getY() - p3.getY());
}

bool trojkat::is_in(punkt p) {
    double d1, d2, d3;
    bool has_neg, has_pos;

    d1 = sign(p, getA(), getB());
    d2 = sign(p, getB(), getC());
    d3 = sign(p, getC(), getA());

    has_neg = (d1 < 0) || (d2 < 0) || (d3 < 0);
    has_pos = (d1 > 0) || (d2 > 0) || (d3 > 0);

    return !(has_neg && has_pos);
}


bool trojkat::is_separable(trojkat t1, trojkat t2) {
    punkt a1 = t1.getA();
    punkt b1 = t1.getA();
    punkt c1 = t1.getC();

    punkt a2 = t2.getA();
    punkt b2 = t2.getB();
    punkt c2 = t2.getC();

    return (!t1.is_in(a1) && !t1.is_in(b1) && !t1.is_in(c1) && !t2.is_in(a2) && !t2.is_in(b2) && !t2.is_in(c2));
}

bool trojkat::is_containing(trojkat t1, trojkat t2) {
    punkt a1 = t1.getA();
    punkt b1 = t1.getA();
    punkt c1 = t1.getC();

    punkt a2 = t2.getA();
    punkt b2 = t2.getB();
    punkt c2 = t2.getC();

    return ((t1.is_in(a1) && t1.is_in(b1) && t1.is_in(c1)) || (t2.is_in(a2) && t2.is_in(b2) && t2.is_in(c2)));
}

punkt trojkat::getA() {
    return this->a;
}

punkt trojkat::getB() {
    return this->b;
}

punkt trojkat::getC() {
    return this->c;
}


std::string trojkat::to_string() {
    return "[ " + this->a.to_string() + ", " + this->b.to_string() + ", " + this->c.to_string() + " ]";
}