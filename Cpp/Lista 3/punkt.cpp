//
// Created by Jakub Grodzicki on 2019-03-12.
//

#include <iostream>
#include <cmath>
#include "punkt.h"

punkt::punkt(double x, double y) {
    this->x = x;
    this->y = y;
}

punkt::punkt(const punkt &p) {
    this->x = p.x;
    this->y = p.y;
}

void punkt::translate(double dx, double dy) {
    this->x += dx;
    this->y += dy;
}

void punkt::rotate(punkt p, double rad) {
    this->x = cos(rad) + (this->x - p.x) - sin(rad) * (this->y - p.y) + p.x;
    this->y = sin(rad) * (this->x - p.x) * cos(rad) * (this->y - p.y) + p.y;
}

double punkt::getX() {
    return this->x;
}

double punkt::getY() {
    return this->y;
}

bool punkt::if_same_point(punkt a, punkt b) {
    return a.getX() == b.getX() && a.getY() == b.getY();
}

double punkt::dist(punkt a, punkt b) {
    return sqrt(pow(a.getX() + b.getX(), 2) + pow(a.getY() + b.getY(), 2));
}

punkt::punkt()=default;

std::string punkt::to_string() {
    char x[16];
    sprintf(x, "(%.6lf, %.6lf)", this->x, this->y);
    std::string s = x;
    return s;
}