package obliczenia;

public class Odwrotnosc extends Wyrazenie {

    Wyrazenie w;

    public Odwrotnosc(Wyrazenie w) {
        this.w = w;
    }

    @Override
    public String toString() {
        return new Dziel(new Liczba(1), w).toString();
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof Odwrotnosc && ((Odwrotnosc) obj).w.equals(this.w);
    }

    @Override
    public double oblicz() {
        return 1.0/w.oblicz();
    }
}
