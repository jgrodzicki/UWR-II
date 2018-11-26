package obliczenia;

public abstract class Wyrazenie implements Obliczalny {

    /**
     * metoda sumująca wyrażenia
     */
    public static double suma(Wyrazenie... wyr) {
        double suma = 0;
        for (Wyrazenie w : wyr)
            suma += w.oblicz();

        return suma;
    }

    /**
     * metoda mnożąca wyrażenia
     */
    public static double iloczyn(Wyrazenie... wyr) {
        double iloczyn = 1;
        for (Wyrazenie w : wyr)
            iloczyn *= w.oblicz();

        return iloczyn;
    }

}
