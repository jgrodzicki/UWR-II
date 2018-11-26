package Geometria;

public class Trojkat {
    private Punkt a;
    private Punkt b;
    private Punkt c;

    public Trojkat(Punkt a, Punkt b, Punkt c) {
        if (ifOnSameLane(a, b, c)) {
            System.err.println("Błąd - punkty są współliniowe!");
            new Trojkat(new Punkt(0, 0), new Punkt(0, 1), new Punkt(1, 0));
        }
        else {
            this.a = a;
            this.b = b;
            this.c = c;
        }
    }

    private boolean ifOnSameLane(Punkt aP, Punkt bP, Punkt cP) {
        double a = (aP.y - bP.y)/(aP.x - bP.y);
        double b = aP.y - (aP.x * a);

        return cP.y == cP.x*a + b;
    }

    public String toString() {
        return String.format("a: %s\tb: %s\tc: %s", a.toString(), b.toString(), c.toString());
    }

    public Trojkat przesun(Wektor w) {
        return new Trojkat(Punkt.przesun(a, w), Punkt.przesun(b, w), Punkt.przesun(c, w));
    }

    public Trojkat obroc(Punkt p, double kat) {
        return new Trojkat(Punkt.obroc(a, p, kat), Punkt.obroc(b, p, kat), Punkt.obroc(c, p, kat));
    }

    public Trojkat odbij(Prosta p) {
        return new Trojkat(Punkt.odbij(a, p), Punkt.odbij(b, p), Punkt.odbij(c, p));
    }
}
