package obliczenia;

public class Potega extends Wyrazenie {

    Wyrazenie w1;
    Wyrazenie w2;

    public Potega(Wyrazenie w1, Wyrazenie w2) {
        this.w1 = w1;
        this.w2 = w2;
    }

    @Override
    public String toString() {
        return String.format("%s^%s", w1.toString(), w2.toString());
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof Potega && ((Potega) obj).w1.equals(this.w1) && ((Potega) obj).w2.equals(this.w2);
    }

    @Override
    public double oblicz() {
        return Math.pow(w1.oblicz(), w2.oblicz());
    }
}
