package Geometria;

public class Main {

    public static void main(String[] args) {
        Punkt a = new Punkt(1.0, 1.0);
        Punkt b = new Punkt(2.0, 2.0);
        Punkt c = new Punkt(3.0, 3.1);

        Odcinek o = new Odcinek(a, b);

        Trojkat t = new Trojkat(a, b, c);

        System.out.println("o\t" + o.toString());

        System.out.println("t\t" + t.toString());

        Wektor w = new Wektor(1, 2);
        System.out.printf("\nOdcinek o przesunięty o wektor [1, 2]: %s", o.przesun(w).toString());
        System.out.printf("\nTrójkąt t przesunięty o wektor [1, 2]: %s\n", t.przesun(w).toString());


        Punkt p = new Punkt(0, 0);
        double kat = Math.PI;

        System.out.printf("\nOdcinek o obrócony ([10, 10], 1.2): %s", o.obroc(p, kat).toString());
        System.out.printf("\nTrójkąt t obrócony ([10, 10], 1.2): %s\n", t.obroc(p, kat).toString());

        Prosta pr = new Prosta(1, 2, 3);
        System.out.printf("\nOdcinek o odbity (1x + 2y + 3) %s", o.odbij(pr).toString());
        System.out.printf("\nTrójkąt t odbity (1x + 2y + 3): %s\n", t.odbij(pr).toString());


        Prosta pr1 = new Prosta(1, 1, 1);
        Prosta pr2 = new Prosta(1, 1, 1);
        Prosta pr3 = new Prosta(-1, 1, 1);

        System.out.printf("\nCzy (x + y + 1) i (x + y + 1) prostopadłe?\t%b", Prosta.czyProstopadla(pr1, pr2));
        System.out.printf("\nCzy (x + y + 1) i (x + y + 1) równoległe?\t%b", Prosta.czyRogwnolegla(pr1, pr2));

        System.out.printf("\nCzy (x + y + 1) i (-x + y + 1) prostopadłe?\t%b", Prosta.czyProstopadla(pr1, pr3));
        System.out.printf("\nCzy (x + y + 1) i (-x + y + 1) równoległe?\t%b", Prosta.czyRogwnolegla(pr1, pr3));

    }
}
