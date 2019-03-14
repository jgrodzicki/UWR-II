//
// Created by Jakub Grodzicki on 2019-03-12.
//

#ifndef LISTA_3_PUNKT_H
#define LISTA_3_PUNKT_H


class punkt {
private:
    double x, y;

public:
    punkt(double x, double y);
    punkt(const punkt &p);
    punkt();

    void translate(double dx, double dy);
    void rotate(punkt p, double rad);
    double getX();
    double getY();

    static bool if_same_point(punkt a, punkt b);
    static double dist(punkt a, punkt b);

    std::string to_string();
};


#endif //LISTA_3_PUNKT_H
