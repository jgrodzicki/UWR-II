package sample;

import javafx.util.Pair;

import java.util.Random;

public class NumberZeroBean extends NumberBean implements Runnable {

    @Override
    public void run() {
        while(true) {
            move();
            try {
                Thread.sleep(new Random().nextInt(10)*10 + 300);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    private void move() {
        Random r = new Random();
        Pair<Integer, Integer> pos = Data.getPos(0);
        Pair<Integer, Integer> newPos;

        do {
            int dir = r.nextInt(2)*2-1;
            if (r.nextBoolean()) //po ox
                newPos = new Pair<>(pos.getKey() + dir, pos.getValue());
            else //po oy
                newPos = new Pair<>(pos.getKey(), pos.getValue() + dir);

        } while (!Data.isInBounds(newPos));

        if (Data.isPosOccupied(newPos)) {
            int no = Data.getNoOfInPos(newPos);

            if (Data.getIfPrime(no))
                Data.swapPosZeroWith(no);

            else {
                Data.getLiczbaBy(no).endTread();
                Data.delete(no);
                Data.moveToPos(0, newPos);
            }
        }
        else
            Data.moveToPos(0, newPos);
    }

}
