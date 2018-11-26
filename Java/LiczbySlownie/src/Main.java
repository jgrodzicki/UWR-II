import java.text.DecimalFormat;
import java.util.Arrays;

public class Main {

    private static final String[] jednosci = {"", "jeden ", "dwa ", "trzy ", "cztery ", "pięć ", "sześć ", "siedem ", "osiem ", "dziewięć"};

    private static final String[] dziesiatki = {"", "dwadzieścia ", "trzydzieści ", "czterdzieści ", "pięćdziesiąt ", "sześćdziesiąt ", "siedemdziesiąt ", "osiemdziesiąt ", "dziewięćdziesiąt "};

    private static final String[] nastki = {
            "dziesięć ", "jedenaście ", "dwanaście ", "trzynaście ", "czternaście ", "piętnaście ", "szestnaście ", "siedemnaście ", "osiemnaście ", "dziewiętnaście "};

    private static final String[] setki = {"", "sto ", "dwieście ", "trzysta ", "czterysta ", "pięćset ", "sześćset ", "siedemset ", "osiemset ", "dziewięćset "};


    private static String convert(long n) {

        if (n == 0)
            return "zero";

        String res = "";

        String fromLong = new DecimalFormat("0000000000").format(n);

        if (fromLong.charAt(0) == '-') {
            res = "minus ";
            fromLong = fromLong.substring(1);
        }

        switch (fromLong.charAt(0)) {
            case '1':
                res += "miliard ";
                break;

            case '2':
                res += "dwa miliardy ";
                break;
        }

        String miliony = fromLong.substring(1, 4);
        String convertedMil = convert3(miliony);
        if (!convertedMil.isEmpty()) {

            switch (convertedMil) {
                case "jeden ":
                    res += "milion ";
                    break;

                case "dwa ":
                case "trzy ":
                case "cztery ":
                    res += convertedMil + "miliony ";
                    break;

                default:
                    res += convertedMil + "milionów ";
                    break;
            }
        }


        String tysiace = fromLong.substring(4, 7);
        String convertedK = convert3(tysiace);
        if (!convertedK.isEmpty()) {

            switch (convertedK) {
                case "jeden ":
                    res += "tysiąc ";
                    break;

                case "dwa ":
                case "trzy ":
                case "cztery ":
                    res += convertedK + "tysiące ";
                    break;

                default:
                    res += convertedK + "tysięcy ";
                    break;
             }
        }

        res += convert3(fromLong.substring(7));

        return res;
    }

    private static String convert3(String number) {

        String res = "";

        if (number.charAt(0) != '0')
            res = setki[number.charAt(0) - '0'];

        if (number.charAt(1) == '1')
            res += nastki[number.charAt(2) - '0'];
        else
            res += dziesiatki[number.charAt(1) - '0'];

        res += jednosci[number.charAt(2) - '0'];

        return res;
    }

    public static void main(String[] args) {

        for (String a : args) {
            apply(new Integer(a));
        }
//
//        apply(0);
//        apply(10);
//        apply(-2147483648);
//        apply(2147483647);
//        apply(1001002003);
    }

    private static void apply(int n) {



        try {
            String output = convert(n);

            System.out.format("******************\nKonwertowana liczba: %d\nWynik konwersji: %s\n", n, convert(n));
        } catch (NumberFormatException e) {
            System.err.println("Exception: " + e.getMessage());
        }
    }
}
