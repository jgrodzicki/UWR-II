import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Random;

public class Kid extends JComponent implements Runnable {

    private int x;
    private int y;
    private boolean hasPresent;
    private boolean isSleeping;
    private int movementTime;

    private BufferedImage awake;
    private BufferedImage asleep;
    private BufferedImage withPresent;

    public Kid() {

        hasPresent = false;
        Random r = new Random();
        isSleeping = r.nextBoolean();
        movementTime = r.nextInt(20) + 8;

        int x;
        int y;
        do {
            x = r.nextInt(Data.cols);
            y = r.nextInt(Data.rows);
        } while (!Data.isGoodToSpawn(x, y));

        this.x = x;
        this.y = y;

        Data.in(this.x, this.y);

        setBounds(this.x * Data.SIZE, this.y * Data.SIZE, Data.SIZE, Data.SIZE);

        try {
            awake = ImageIO.read(new File("img/kid_awake.png"));
            asleep = ImageIO.read(new File("img/kid_asleep.png"));
            withPresent = ImageIO.read(new File("img/kid_present.png"));
        } catch (IOException e) {
            System.err.println("Unable to load kid's image: " + e.getMessage());
        }
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);

        if (isSleeping && !hasPresent)
            g.drawImage(asleep, 0, 0, this);
        else if (!hasPresent)
            g.drawImage(awake, 0, 0, this);
        else
            g.drawImage(withPresent, 0, 0, this);
    }

    @Override
    public synchronized void run() {
        while (!hasPresent) {

            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            movementTime--;
            if (movementTime == 0) {
                isSleeping = !isSleeping;
                movementTime = new Random().nextInt(20) + 8;
                this.repaint();
            }

            if (isSleeping) {
                if (Data.ifContactSanta(this.x, this.y)) {
                    hasPresent = true;
                    Data.givePresent();

                    if (Data.ifAllKidsHavePresents())
                        Game.gameWon();


                    this.repaint();
                }
                continue;
            }

            Data.out(this.x, this.y);
            int newX = this.x;
            int newY = this.y;

            switch (Data.whichDirToSanta(this.x, this.y)) {
                case 2:
                    newY--;
                    break;
                case 4:
                    newX--;
                    break;
                case 6:
                    newX++;
                    break;
                case 8:
                    newY++;
                    break;
            }

            if (newX < 0)
                newX = Data.cols-1;
            else if (newX >= Data.cols)
                newX = 0;

            if (newY < 0)
                newY = Data.rows-1;
            else if (newY >= Data.rows)
                newY = 0;

            if (!Data.checkIfOccupied(newX, newY)) {
                this.x = newX;
                this.y = newY;
            }

            Data.in(this.x, this.y);

            if (Data.ifContactSanta(this.x, this.y)) {
                setBounds(this.x * Data.SIZE, this.y * Data.SIZE, Data.SIZE, Data.SIZE);
                this.repaint();
                try {
                    Thread.sleep(200);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                if (Data.ifContactSanta(this.x, this.y))
                    Game.catchSanta();
            }

            setBounds(this.x * Data.SIZE, this.y * Data.SIZE, Data.SIZE, Data.SIZE);
            this.repaint();
        }
    }

    public void stop() {
        hasPresent = true;
    }
}
