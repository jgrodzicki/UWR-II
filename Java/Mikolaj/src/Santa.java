import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Random;

public class Santa extends JComponent implements Runnable, KeyListener {

    private int x;
    private int y;
    private int dir[] = {0, 0};
    private boolean isSantaUncaught;

    private BufferedImage img;

    public Santa() {
        Random r = new Random();
        this.x = r.nextInt(Data.cols);
        this.y = r.nextInt(Data.rows);

        this.isSantaUncaught = true;

        Data.santaIn(this.x, this.y);
        setBounds(this.x * Data.SIZE, this.y * Data.SIZE, Data.SIZE, Data.SIZE);

        try {
            img = ImageIO.read(new File("img/santa.png"));
        } catch (IOException e) {
            System.err.println("Unable to load santa's image: " + e.getMessage());
        }

        addKeyListener(this);
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);

        g.drawImage(img, 0, 0, this);
    }

    @Override
    public synchronized void run() {
        while (this.isSantaUncaught) {
            this.requestFocus();
            try {
                Thread.sleep(250);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            Data.santaOut(this.x, this.y);

            int newX = this.x;
            int newY = this.y;

            newX += dir[0];
            newY += dir[1];

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

            Data.santaIn(this.x, this.y);

            setBounds(this.x * Data.SIZE, this.y * Data.SIZE, Data.SIZE, Data.SIZE);
            this.repaint();
        }
    }

    public void setSantaUncaught() {
        this.isSantaUncaught = true;
    }

    @Override
    public void keyTyped(KeyEvent e) {

    }

    @Override
    public void keyPressed(KeyEvent e) {

        switch (e.getKeyCode()) {
            case KeyEvent.VK_LEFT:
                dir[0] = -1;
                dir[1] = 0;
                break;
            case KeyEvent.VK_UP:
                dir[0] = 0;
                dir[1] = -1;
                break;
            case KeyEvent.VK_RIGHT:
                dir[0] = 1;
                dir[1] = 0;
                break;
            case KeyEvent.VK_DOWN:
                dir[0] = 0;
                dir[1] = 1;
                break;
        }
    }

    @Override
    public void keyReleased(KeyEvent e) {
        dir[0] = 0;
        dir[1] = 0;
    }

    public void stop() {
        isSantaUncaught = false;
    }
}
