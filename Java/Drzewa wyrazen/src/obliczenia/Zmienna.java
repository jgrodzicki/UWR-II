package obliczenia;

import java.util.HashMap;

public class Zmienna extends Wyrazenie {

    private static HashMap<String, Double> zmienne = new HashMap<>();
    private String zmienna;

    public Zmienna(String zmienna) {
        this.zmienna = zmienna;
    }

    public static void dodajZmienna(String zmienna, Double wartosc) {
        zmienne.put(zmienna, wartosc);
    }

    @Override
    public String toString() {
        return zmienna;
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof Zmienna && ((Zmienna) obj).zmienna.equals(zmienna);
    }

    @Override
    public double oblicz() {
        return zmienne.get(zmienna);
    }
}
