public class Game {
    private static Thread santaThread;
    private static Santa santa;

    private static Thread kidThread[] = new Thread[12];
    private static Kid[] kid = new Kid[12];

    private static Frame frame;

    private static Board board;


    public static void catchSanta() {
        frame.label.setVisible(true);
        frame.label.setText("GAME LOST");
        santa.setSantaUncaught();
        santa.setVisible(false);
        for (Kid k : kid)
            k.setVisible(false);
        stopAll();
    }

    public static void gameWon() {
        frame.label.setVisible(true);
        frame.label.setText("GAME WON");
        santa.setVisible(false);
        for (Kid k : kid)
            k.setVisible(false);
        stopAll();
    }

    public static void newGame() {
        Data.empty(30, 20);
        frame = new Frame();
        board = new Board();
        santa = new Santa();

        for (int i = 0; i < 12; i++) {
            kid[i] = new Kid();
            frame.add(kid[i]);
            kidThread[i] = new Thread(kid[i]);
        }
        santaThread = new Thread(santa);

        frame.add(santa);
        frame.add(board);

        frame.repaint();
        initThreads();
    }

    public static void stopAll() {
        santa.stop();
        for (Kid k : kid)
            k.stop();
    }

    private static synchronized void initThreads() {
        santaThread.start();
        for (int i = 0; i < 12; i++)
            kidThread[i].start();
    }
}
