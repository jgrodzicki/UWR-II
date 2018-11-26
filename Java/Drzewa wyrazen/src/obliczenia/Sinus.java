package obliczenia;

public class Sinus extends Wyrazenie {

    Wyrazenie w;

    public Sinus(Wyrazenie w) {
        this.w = w;
    }

    @Override
    public String toString() {
        return String.format("sin(%s)", w.toString());
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof Sinus && ((Sinus) obj).w.equals(this.w);
    }


    @Override
    public double oblicz() {
        return Math.sin(w.oblicz());
    }
}
