//
// Created by Jakub Grodzicki on 2019-03-12.
//

#include <iostream>
#include <stdexcept>
#include <cstdlib>
#include <math.h>
#include "odcinek.h"


odcinek::odcinek(punkt start, punkt end) {
    if (punkt::if_same_point(start, end))
        throw std::invalid_argument("nie można utworzyć odcinka o długości 0");
    this->start = start;
    this->end = end;
}

odcinek::odcinek(const odcinek &o) {
    this->start = o.start;
    this->end = o.end;
}

void odcinek::translate(double dx, double dy) {
    this->start.translate(dx, dy);
    this->end.translate(dx, dy);
}

void odcinek::rotate(punkt p, double rad) {
    this->start.rotate(p, rad);
    this->end.rotate(p, rad);
}

double odcinek::length() {
    return sqrt(pow(this->start.getX() - this->end.getX(), 2) + pow(this->start.getY() - this->end.getY(), 2));
}

bool odcinek::is_middle(punkt p) {
    return ((this->start.getX() + this->end.getX())/2 == p.getX() && (this->start.getY() + this->end.getY())/2 == p.getY());
}

bool odcinek::is_on_line_seg(punkt p) {
    if (p.getX() >= this->start.getX() && p.getX() <= this->end.getX() && p.getY() >= this->start.getY() && p.getY() <= this->end.getY()) {
        punkt as = this->start;
        punkt ae = this->end;
        punkt bs = this->start;
        punkt be = p;

        double sin1 = (ae.getY() - as.getY())/this->length();
        double sin2 = (be.getY() - bs.getY())/this->length();

        return sin1 == sin2;
    }

    return false;
}

punkt odcinek::middle() {
    return punkt((this->start.getX() + this->end.getX())/2, (this->start.getY() + this->end.getY())/2);
}

punkt odcinek::getStart() {
    return this->start;
}

punkt odcinek::getEnd() {
    return this->end;
}

bool odcinek::is_parallel(odcinek a, odcinek b) {
    punkt as = a.start;
    punkt ae = a.end;
    punkt bs = b.start;
    punkt be = b.end;

    double sin1 = (ae.getY() - as.getY())/a.length();
    double sin2 = (be.getY() - bs.getY())/a.length();

    return sin1 == sin2;
}

bool odcinek::is_perpendicular(odcinek a, odcinek b) {
    punkt as = a.start;
    punkt ae = a.end;
    punkt bs = b.start;
    punkt be = b.end;

    double sin1 = (ae.getY() - as.getY())/a.length();
    double sin2 = (be.getY() - bs.getY())/a.length();

    return sin1*sin2 == -1;
}

std::string odcinek::to_string() {
    return this->start.to_string() + " <-> " + this->end.to_string();
}