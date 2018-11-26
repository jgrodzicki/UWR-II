package obliczenia;

public class PrzeciwnyZnak extends Wyrazenie {

    Wyrazenie w;

    public PrzeciwnyZnak(Wyrazenie w) {
        this.w = w;
    }

    @Override
    public String toString() {
        return String.format("(- (%s))", w.toString());
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof PrzeciwnyZnak && ((PrzeciwnyZnak) obj).w.equals(this.w);
    }


    @Override
    public double oblicz() {
        return -w.oblicz();
    }
}
