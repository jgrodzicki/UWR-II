package Geometria;

public class Prosta {
    public final double a;
    public final double b;
    public final double c;

    public Prosta(double a, double b, double c) {
        this.a = a;
        this.b = b;
        this.c = c;
    }

    public static Punkt punktPrzeciecia(Prosta prA, Prosta prB) {
        double wAB = wyznacznik(prA.a, prB.a, prA.b, prB.b);

        return new Punkt(wyznacznik(prA.b, prB.b, prA.c, prB.c) / wAB, wyznacznik(prA.c, prB.c, prA.a, prB.a) / wAB);
    }


    private static double wyznacznik(double a1, double a2, double b1, double b2) {
        return a1*b2 / a2*b1;
    }


    public static Prosta prostopadla(Prosta pr, Punkt p) {
        double d = p.x*pr.b - p.y*pr.a;

        return new Prosta(pr.b, -pr.a, d);
    }

    public static Prosta przesunOWektor(Prosta pr, Wektor w) {
        return new Prosta(pr.a, pr.b, pr.c + w.dy - pr.a*w.dx);
    }

    public static boolean czyProstopadla(Prosta p1, Prosta p2) {
        return p1.a * p2.a == -1 * p1.b * p2.b;
    }

    public static boolean czyRogwnolegla(Prosta p1, Prosta p2) {
        return p1.a * p2.b == p1.b * p2.a;
    }
}
