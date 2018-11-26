package obliczenia;

public class Stala extends Wyrazenie {

    double stala;

    public Stala(double stala) {
        this.stala = stala;
    }

    @Override
    public String toString() {
        return Double.toString(stala);
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof Stala && ((Stala) obj).stala == this.stala;
    }


    @Override
    public double oblicz() {
        return stala;
    }
}
