package sample;

import javafx.util.Pair;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public class Data {
    private static int rows;
    private static int cols;

    private static HashMap<Integer, Pair<Integer, Integer>> posBeans = new HashMap<>();
    private static HashMap<Integer, NumberBean> numbers = new HashMap<>();

    private static Random r;

    public static Pair<Integer, Integer> getPos(int no) {
        return posBeans.get(no);
    }

    public static void init(int nb, int rows, int cols) {
        posBeans = new HashMap<>();
        numbers = new HashMap<>();


        r = new Random();
        Data.rows = rows;
        Data.cols = cols;

        numbers.put(0, new NumberZeroBean());
        posBeans.put(0, randomPair());

        for (int i = 0; i < nb; i++) {
            Random r = new Random();
            int x;
            do {
                x = r.nextInt(5 * nb) + 10;
            } while (posBeans.containsKey(x));

            posBeans.put(x, randomPair());

            numbers.put(x, new NumberBean());
            numbers.get(x).setNo(x);
        }


    }

    public static void startThreads() {
        for (Map.Entry<Integer, NumberBean> entry : numbers.entrySet())
            numbers.get(entry.getKey()).startThread();
    }

    public static synchronized boolean isPosGood(Pair<Integer, Integer> p) {
        return !isPosOccupied(p) && isInBounds(p);
    }

    public static synchronized boolean isPosOccupied(Pair<Integer, Integer> p) {
        return posBeans.containsValue(p);
    }

    public static boolean isInBounds(Pair<Integer, Integer> p) {
        return p.getKey() >= 0 && p.getKey() < cols && p.getValue() >= 0 && p.getValue() < rows;
    }

    public static synchronized int getNoOfInPos(Pair<Integer, Integer> p) {
        for (Map.Entry<Integer, Pair<Integer, Integer>> entry : posBeans.entrySet()) {
            if (p.equals(entry.getValue()))
                return entry.getKey();
        }
        return -1;
    }

    public static synchronized void moveToPos(int i, Pair<Integer, Integer> pos) {
        posBeans.replace(i, pos);
    }

    public static synchronized void swapPosZeroWith(int a) {
        System.out.println("Swap: 0 with " + a);
        Pair<Integer, Integer> p0 = posBeans.get(0);
        posBeans.replace(0, posBeans.get(a));
        posBeans.replace(a, p0);
    }

    public static boolean getIfPrime(int no) {
        return numbers.get(no).getIsPrime();
    }

    public static NumberBean getLiczbaBy(int no) {
        return numbers.get(no);
    }

    public static void delete(int no) {
        System.out.println("Delete:\t" + no);
        posBeans.replace(no, new Pair<>(-1, -1));
        numbers.get(no).endTread();
    }

    private static Pair<Integer, Integer> randomPair() {
        Pair<Integer, Integer> p;
        do {
            p = new Pair<>(r.nextInt(rows), r.nextInt(cols));
        } while (posBeans.containsValue(p));

        return p;
    }

    public static int getRows() {
        return rows;
    }

    public static int getCols() {
        return cols;
    }

    public static HashMap<Integer, Pair<Integer, Integer>> getPosBeans() {
        return posBeans;
    }
}
