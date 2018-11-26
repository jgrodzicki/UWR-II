package obliczenia;

public class WartoscBezwzgledna extends Wyrazenie {

    Wyrazenie w;

    public WartoscBezwzgledna(Wyrazenie w) {
        this.w = w;
    }

    @Override
    public String toString() {
        return String.format("|%s|", w.toString());
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof WartoscBezwzgledna && ((WartoscBezwzgledna) obj).w.equals(this.w);
    }


    @Override
    public double oblicz() {
        return Math.abs(w.oblicz());
    }
}
