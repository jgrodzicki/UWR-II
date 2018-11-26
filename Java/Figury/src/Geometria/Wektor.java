package Geometria;

public class Wektor {

    public final double dx;
    public final double dy;

    public Wektor(double dx, double dy) {
        this.dx = dx;
        this.dy = dy;
    }

    public static Wektor zloz(Wektor w1, Wektor w2) {
        return new Wektor(w1.dx + w2.dx, w1.dy + w2.dy);
    }
}
