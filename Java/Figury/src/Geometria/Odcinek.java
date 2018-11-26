package Geometria;

public class Odcinek {

    Punkt s;
    Punkt e;

    public Odcinek(Punkt s, Punkt e) {
        if (ifSamePoints(s, e)) {
            System.err.println("Błąd - Odcinek zaczyna i kończy się w tym samym miejscu!");
            new Odcinek(new Punkt(0, 0), new Punkt(1, 1));
        }
        else {
            this.s = s;
            this.e = e;
        }
    }

    private boolean ifSamePoints(Punkt a, Punkt b) {
        return a.x == b.x && a.y == b.y;
    }

    public String toString() {
        return String.format("start: %s\tend: %s", s.toString(), e.toString());
    }

    public Odcinek przesun(Wektor w) {
        return new Odcinek(new Punkt(s.x + w.dx, s.y + w.dy), new Punkt(e.x + w.dx, e.y + w.dy));
    }

    public Odcinek obroc(Punkt p, double kat) {
        return new Odcinek(Punkt.obroc(s, p, kat), Punkt.obroc(e, p, kat));
    }

    public Odcinek odbij(Prosta p) {
        return new Odcinek(Punkt.odbij(s, p), Punkt.odbij(e, p));
    }
}
