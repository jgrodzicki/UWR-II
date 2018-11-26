package obliczenia;

public class Logarytm extends Wyrazenie {

    Wyrazenie w1;
    Wyrazenie w2;

    public Logarytm(Wyrazenie w1, Wyrazenie w2) {
        this.w1 = w1;
        this.w2 = w2;
    }

    @Override
    public String toString() {
        return String.format("log%s (%s)", w1, w2);
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof Logarytm && ((Logarytm) obj).w1.equals(this.w1) && ((Logarytm) obj).w2.equals(this.w2);
    }

    @Override
    public double oblicz() {
        return Math.log(w1.oblicz())/Math.log(w2.oblicz());
    }
}
