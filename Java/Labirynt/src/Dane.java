import javafx.util.Pair;

import java.util.Random;
import java.util.Stack;

public class Dane {

    static final int SIZE = 25;
    boolean odwiedzone[][] = new boolean[SIZE][SIZE];
    boolean sciany[][][] = new boolean[SIZE][SIZE][4];
    private Random r;
    private int liczbaPol;
    private Stack<Pair<Integer, Integer>> stack;

    public Dane() {
        r = new Random();
        liczbaPol = 0;
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                odwiedzone[i][j] = false;
                for (int k = 0; k < 4; k++)
                    sciany[i][j][k] = true;
            }
        }

        stack = new Stack<>();

        generuj(SIZE-1, SIZE-1);
        sciany[SIZE-1][SIZE-1][1] = false;
    }

    private void generuj(int x, int y) {
        liczbaPol++;
        stack.push(new Pair<>(x, y));
        odwiedzone[x][y] = true;

        int nextX = x;
        int nextY = y;
        boolean ifChecked[] = {false, false, false, false};

        outerloop:
        while (!(ifChecked[0] && ifChecked[1] && ifChecked[2] && ifChecked[3])) {
            switch (r.nextInt(4)) {
                case 0:
                    if (czyDobre(x-1, y)) {
                        nextX = x-1;
                        break outerloop;
                    }
                    ifChecked[0] = true;
                    break;
                case 1:
                    if (czyDobre(x+1, y)) {
                        nextX = x+1;
                        break outerloop;
                    }
                    ifChecked[1] = true;
                    break;
                case 2:
                    if (czyDobre(x, y-1)) {
                        nextY = y-1;
                        break outerloop;
                    }
                    ifChecked[2] = true;
                    break;
                case 3:
                    if (czyDobre(x, y+1)) {
                        nextY = y+1;
                        break outerloop;
                    }
                    ifChecked[3] = true;
                    break;
            }
        }

        if (nextX == x && nextY == y) {
            if (liczbaPol < SIZE*SIZE) {
                stack.pop();
                Pair last = stack.pop();
                liczbaPol--;
                generuj((int)last.getKey(), (int)last.getValue());
                return;
            }
            else {
                return;
            }
        }

        if (nextX > x) {
            sciany[x][y][1] = false;
            sciany[nextX][y][3] = false;
        }
        else if (nextX < x) {
            sciany[x][y][3] = false;
            sciany[nextX][y][1] = false;
        }
        else if (nextY > y) {
            sciany[x][y][2] = false;
            sciany[x][nextY][0] = false;
        }
        else {
            sciany[x][y][0] = false;
            sciany[x][nextY][2] = false;
        }
        generuj(nextX, nextY);

    }

    private boolean czyDobre(int nextX, int nextY) {
        if (nextX >= SIZE-1 && nextY >= SIZE-1)
            return false;
        if (nextX < 0 || nextX > SIZE-1 || nextY < 0 || nextY > SIZE-1)
            return false;
        return !odwiedzone[nextX][nextY];
    }
}