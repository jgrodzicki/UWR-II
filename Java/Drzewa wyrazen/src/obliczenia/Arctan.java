package obliczenia;

public class Arctan extends Wyrazenie {

    Wyrazenie w;

    public Arctan(Wyrazenie w) {
        this.w = w;
    }

    @Override
    public String toString() {
        return String.format("arctan(%s)", w.toString());
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof Arctan && ((Arctan) obj).w.equals(this.w);
    }

    @Override
    public double oblicz() {
        return Math.atan(w.oblicz());
    }
}
