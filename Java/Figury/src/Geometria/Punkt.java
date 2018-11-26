package Geometria;

import static java.lang.Math.*;

public class Punkt {

    double x;
    double y;

    public Punkt(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public String toString() {
        return String.format("x = %f\ty = %f", x, y);
    }

    public static Punkt przesun(Punkt p, Wektor w) {
        return new Punkt(p.x + w.dx, p.y + w.dy);
    }

    public static Punkt obroc(Punkt p1, Punkt p2, double kat) {

        double newX = (p1.x - p2.x) * cos(kat) - (p1.y - p2.y) * sin(kat) + p2.x;
        double newY = (p1.x - p2.x) * sin(kat) - (p1.y - p2.y) * cos(kat) + p2.y;

        return new Punkt(newX, newY);

    }

    public static Punkt odbij(Punkt p, Prosta pr) {

        Prosta prost = Prosta.prostopadla(pr, p);

        Punkt przec = Prosta.punktPrzeciecia(pr, prost);

        return new Punkt((przec.x - p.x) * 2 + p.x, (przec.y - p.y) * 2 + p.y);
    }
}
