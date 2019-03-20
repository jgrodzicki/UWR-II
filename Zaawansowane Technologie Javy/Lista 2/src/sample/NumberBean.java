package sample;

import javafx.util.Pair;

import java.io.Serializable;
import java.util.Random;

public class NumberBean implements Serializable, Runnable {
    private boolean isPrime;
    private boolean isAlive = true;
    private int no;

    public NumberBean() {}

    public void setNo(int no) {
        this.no = no;
        this.isPrime = ifPrime();
    }

    public void startThread() {
        new Thread(this).start();
    }

    public void endTread() {
        isAlive = false;
    }

    public boolean getIsPrime() {
        return isPrime;
    }

    @Override
    public void run() {
        while(isAlive) {
            move();
            try {
                Thread.sleep(new Random().nextInt(10)*10 + 300);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    private void move() {
        Pair<Integer, Integer> pos = Data.getPos(no);
        Pair<Integer, Integer> pos0 = Data.getPos(0);

        Pair<Integer, Integer> newPos = direction(pos, pos0);
        Data.moveToPos(this.no, newPos);
    }

    private Pair<Integer, Integer> direction(Pair<Integer, Integer> pos, Pair<Integer, Integer> pos0) {
        int deltaX = pos.getKey() - pos0.getKey();
        int deltaY = pos.getValue() - pos0.getValue();

        Random r = new Random();
        int prob = deltaX+deltaY;
        Pair<Integer, Integer> newPos;

        for (int i = 0; i < 2; i++) {
            if (r.nextInt(10) >= prob) { //dzida do 0
                if (r.nextBoolean()) { //po ox
                    int dir = deltaX > 0 ? -1 : 1;
                    newPos = (new Pair<>(pos.getKey() + dir, pos.getValue()));
                }
                else { //po oy
                    int dir = deltaY > 0 ? -1 : 1;
                    newPos = (new Pair<>(pos.getKey(), pos.getValue() + dir));
                }
            }
            else { // losowo
                int dir = r.nextInt(2)*2-1;

                if (r.nextBoolean()) //po ox
                    newPos = (new Pair<>(pos.getKey() + dir, pos.getValue()));
                else //po oy
                    newPos = (new Pair<>(pos.getKey(), pos.getValue() + dir));
            }

            if (Data.isPosGood(newPos))
                return newPos;
        }
        return pos;
    }

    private boolean ifPrime() {
        for (int i = 2; i <= no/2; i++) {
            if (no%i == 0)
                return false;
        }
        return true;
    }
}
