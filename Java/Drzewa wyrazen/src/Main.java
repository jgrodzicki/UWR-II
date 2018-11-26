import obliczenia.*;

public class Main {

    public static void main(String[] args) {

        //3+5
        Wyrazenie w1 = new Dodaj(new Liczba(3), new Liczba(5));
        System.out.println(w1.toString());
        System.out.println(w1.oblicz());
        System.out.println();

        //2+x*7
        Zmienna.dodajZmienna("x", 5.5);
        Wyrazenie w2 = new Dodaj(new Liczba(2), new Mnoz(new Zmienna("x"), new Liczba(7)));
        System.out.println(w2.toString());
        System.out.println(w2.oblicz());
        System.out.println();

        //(3*11-1)/(7+5)
        Wyrazenie w3 = new Dziel(new Odejmij(new Mnoz(new Liczba(3), new Liczba(11)), new Liczba(1)), new Dodaj(new Liczba(7), new Liczba(5)));
        System.out.println(w3.toString());
        System.out.println(w3.oblicz());
        System.out.println();

        //arctan(((x+13) * x) / 2)
        Wyrazenie w4 = new Arctan(new Dziel(new Mnoz(new Dodaj(new Zmienna("x"), new Liczba(13)), new Zmienna("x")), new Liczba(2)));
        System.out.println(w4.toString());
        System.out.println(w4.oblicz());
        System.out.println();

        //pow(2, 5)+x*log(2, y)
        Zmienna.dodajZmienna("y", 4.0);
        Wyrazenie w5 = new Dodaj(
                new Potega(
                        new Liczba(2),
                        new Liczba(5)),
                new Mnoz(
                        new Zmienna("x"),
                        new Logarytm(
                                new Liczba(2),
                                new Zmienna("y"))));
        System.out.println(w5.toString());
        System.out.println(w5.oblicz());

        //suma 3 wyrazen
        System.out.printf("\nSuma wyrażen: %s, %s, %s = %f\n\n", w1.toString(), w2.toString(), w3.toString(), Wyrazenie.suma(w1, w2, w3));

        //iloczyn 3 wyrazen
        System.out.printf("Iloczyn wyrażen: %s, %s, %s = %f", w1.toString(), w2.toString(), w3.toString(), Wyrazenie.iloczyn(w1, w2, w3));
    }
}
