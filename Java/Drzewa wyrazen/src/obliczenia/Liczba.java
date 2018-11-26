package obliczenia;

public class Liczba extends Wyrazenie {

    double liczba;

    public Liczba(double liczba) {
        this.liczba = liczba;
    }

    @Override
    public String toString() {
        return Double.toString(liczba);
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof Liczba && ((Liczba) obj).liczba == this.liczba;
    }

    @Override
    public double oblicz() {
        return liczba;
    }
}
