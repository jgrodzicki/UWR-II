package obliczenia;

public class Cosinus extends Wyrazenie {

    Wyrazenie w;

    public Cosinus(Wyrazenie w) {
        this.w = w;
    }

    @Override
    public String toString() {
        return String.format("cos(%s)", w.toString());
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof Cosinus && ((Cosinus) obj).w.equals(this.w);
    }

    @Override
    public double oblicz() {
        return Math.cos(w.oblicz());
    }
}
