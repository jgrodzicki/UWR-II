import java.util.Random;

public class Data {
    static final int SIZE = 25;
    static int cols;
    static int rows;
    private static boolean[][] posOccupied;
    private static int[] santaPos = new int[2];
    private static int kidsWithPresents = 0;


    private final static int VISIBLE_RANGE = 5;

    public static void empty(int c, int r) {
        cols = c;
        rows = r;

        posOccupied = new boolean[cols][rows];

        for (int i = 0; i < cols; i++)
            for (int j = 0; j < rows; j++)
                posOccupied[i][j] = false;
    }

    public static void santaIn(int x, int y) {
        santaPos[0] = x;
        santaPos[1] = y;
        in(x, y);
    }

    public static void santaOut(int x, int y) {
        out(x, y);
    }

    public static void in(int x, int y) {
        posOccupied[x][y] = true;
    }

    public static void out(int x, int y) {
        posOccupied[x][y] = false;
    }

    public static boolean checkIfOccupied(int x, int y) {
        return posOccupied[x][y];
    }

    public static boolean isGoodToSpawn(int x, int y) {
        int[][] fieldsToCheck = new int[9][2];
        fieldsToCheck[0][0] = x;
        fieldsToCheck[0][1] = y;
        int index = 1;
        if (x > 0) {
            fieldsToCheck[index][0] = x-1;
            fieldsToCheck[index][1] = y;
            index++;

            if (y > 0) {
                fieldsToCheck[index][0] = x-1;
                fieldsToCheck[index][1] = y-1;
                index++;
            }
            else if (y < Data.rows-1) {
                fieldsToCheck[index][0] = x-1;
                fieldsToCheck[index][1] = y+1;
                index++;
            }
        }
        if (y > 0) {
            fieldsToCheck[index][0] = x;
            fieldsToCheck[index][1] = y-1;
            index++;
        }
        else if (y < Data.rows-1) {
            fieldsToCheck[index][0] = x;
            fieldsToCheck[index][1] = y+1;
            index++;
        }
        if (x < Data.cols-1) {
            fieldsToCheck[index][0] = x+1;
            fieldsToCheck[index][1] = y;
            index++;

            if (y > 0) {
                fieldsToCheck[index][0] = x+1;
                fieldsToCheck[index][1] = y-1;
                index++;
            }
            else if (y < Data.rows-1) {
                fieldsToCheck[index][0] = x+1;
                fieldsToCheck[index][1] = y+1;
                index++;
            }
        }

        return Data.checkIfFieldsInArrayAreGoodToSpawn(fieldsToCheck, index);
    }

    public static int whichDirToSanta(int x, int y) {
        int xDist = xDistToSanta(x);
        int yDist = yDistToSanta(y);

        if (xDist > VISIBLE_RANGE || yDist > VISIBLE_RANGE)
            return new Random().nextInt(2) * 2 + new Random().nextInt(4) * 2;



        int xDir = dirToSanta(x, santaPos[0], cols);
        int yDir = dirToSanta(y, santaPos[1], rows);

//        System.out.println(xDist + "\t" + yDist + "\t" + xDir + "\t" + yDir);

        if (xDist < yDist) {
            if (yDir == -1)
                return 2;
            else
                return 8;
        }
        else {
            if (xDir == -1)
                return 4;
            else
                return 6;
        }
    }

    public static boolean ifContactSanta(int x, int y) {
        int xDiff = Math.abs(x-santaPos[0]);
        int yDiff = Math.abs(y-santaPos[1]);
        return xDiff*yDiff == 0 && xDiff+yDiff==1;
    }

    public static void givePresent() {
        kidsWithPresents++;
    }

    public static boolean ifAllKidsHavePresents() {
        return kidsWithPresents == 12;
    }

    private static int xDistToSanta(int x) {
        int dist1 = Math.abs(x - santaPos[0]);
        int dist2 = cols - santaPos[0] + x;
        int dist3 = cols - x + santaPos[0];

        if (dist1 <= dist2 && dist1 <= dist3)
            return dist1;
        if (dist2 <= dist1 && dist2 <= dist3)
            return dist2;
        return dist3;
    }

    private static int yDistToSanta(int y) {
        int dist1 = Math.abs(y - santaPos[1]);
        int dist2 = rows - santaPos[1] + y;
        int dist3 = rows - y + santaPos[1];

        if (dist1 <= dist2 && dist1 <= dist3)
            return dist1;
        if (dist2 <= dist1 && dist2 <= dist3)
            return dist2;
        return dist3;
    }

    private static boolean checkIfFieldsInArrayAreGoodToSpawn(int[][] arr, int length) {
        for (int i = 0; i < length; i++)
            if (posOccupied[arr[i][0]][arr[i][1]])
                return false;

        return true;
    }

    private static int dirToSanta(int co, int santaCo, int size) {
        int dist[] = {co - santaCo, santaCo - co, size - santaCo + co, size - co + santaCo};

        int minIndex = -1;
        int min = size;
        for (int i = 0; i < dist.length; i++)
            if (dist[i] > 0 && dist[i] < min) {
                min = dist[i];
                minIndex = i;
            }

        if (minIndex == 0 || minIndex == 2)
            return -1;
        return 1;
    }
}
