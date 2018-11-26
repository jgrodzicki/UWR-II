import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class Labirynt extends Canvas implements KeyListener {

    static final int ROZMIAR_POLA = 25;

    private Dane dane;

    private Image kV;
    private Image kH;
    private Image kL;
    private Image kR;
    private Image kT;
    private Image kB;
    private Image kTR;
    private Image kTL;
    private Image kBL;
    private Image kBR;
    private Image kNR;
    private Image kNL;
    private Image kNT;
    private Image kNB;
    private Image kA;
    private Image kN;

    private Image ziomek;

    private int ziomekX;
    private int ziomekY;

    private boolean ifFinished;

    public Labirynt(Dane d) {
        super();
        this.dane = d;
        setSize(Dane.SIZE * ROZMIAR_POLA, Dane.SIZE * ROZMIAR_POLA);
        setVisible(true);

        addKeyListener(this);

        try {
            kV = ImageIO.read(new File("img/vertical.gif"));
            kH = ImageIO.read(new File("img/horizontal.gif"));
            kL = ImageIO.read(new File("img/left.gif"));
            kR = ImageIO.read(new File("img/right.gif"));
            kT = ImageIO.read(new File("img/top.gif"));
            kB = ImageIO.read(new File("img/bottom.gif"));
            kTR = ImageIO.read(new File("img/top-right.gif"));
            kTL = ImageIO.read(new File("img/top-left.gif"));
            kBL = ImageIO.read(new File("img/bottom-left.gif"));
            kBR = ImageIO.read(new File("img/bottom-right.gif"));
            kNR = ImageIO.read(new File("img/no-right.gif"));
            kNL = ImageIO.read(new File("img/no-left.gif"));
            kNT = ImageIO.read(new File("img/no-top.gif"));
            kNB = ImageIO.read(new File("img/no-bottom.gif"));
            kA = ImageIO.read(new File("img/all.gif"));
            kN = ImageIO.read(new File("img/nothing.gif"));

            ziomek = ImageIO.read(new File("img/ziomek.gif"));
        } catch (IOException e) {
            System.err.print("Nie można wczytać grafik");
            System.exit(1);
        }
        ziomekX = 0;
        ziomekY = 0;

        ifFinished = false;
    }


    @Override
    public void paint(Graphics g) {

        narysujLabirynt(g);
        g.drawImage(ziomek, ziomekX, ziomekY, this);
    }


    private void narysujLabirynt(Graphics g) {
        for (int i = 0; i < Dane.SIZE; i++) {
            for (int j = 0; j < Dane.SIZE; j++) {
                Image image = null;

                boolean sciany[] = dane.sciany[i][j];

                if (sciany[0] && !sciany[1] && !sciany[2] && !sciany[3])
                    image = kT;
                else if (sciany[1] && !sciany[0] && !sciany[2] && !sciany[3])
                    image = kR;
                else if (sciany[2] && !sciany[0] && !sciany[1] && !sciany[3])
                    image = kB;
                else if (sciany[3] && !sciany[0] && !sciany[1] && !sciany[2])
                    image = kL;

                else if (sciany[0] && sciany[1] && !sciany[2] && !sciany[3])
                    image = kTR;
                else if (sciany[1] && sciany[2] && !sciany[3] && !sciany[0])
                    image = kBR;
                else if (sciany[2] && sciany[3] && !sciany[0] && !sciany[1])
                    image = kBL;
                else if (sciany[3] && sciany[0] && !sciany[1] && !sciany[2])
                    image = kTL;

                else if (sciany[0] && sciany[2] && !sciany[1] && !sciany[3])
                    image = kH;
                else if (sciany[1] && sciany[3] && !sciany[0] && !sciany[2])
                    image = kV;

                else if (sciany[0] && sciany[1] && sciany[2] && !sciany[3])
                    image = kNL;
                else if (sciany[1] && sciany[2] && sciany[3] && !sciany[0])
                    image = kNT;
                else if (sciany[2] && sciany[3] && sciany[0] && !sciany[1])
                    image = kNR;
                else if (sciany[3] && sciany[0] && sciany[1] && !sciany[2])
                    image = kNB;

                else if (sciany[0] && sciany[1] && sciany[2] && sciany[3])
                    image = kA;
                else if (!sciany[0] && !sciany[1] && !sciany[2] && !sciany[3])
                    image = kN;

                else {
                    System.err.println(sciany[0] + "\t" + sciany[1] + "\t" + sciany[2] + "\t" + sciany[3]);
                    System.exit(1);
                }

                g.drawImage(image, ROZMIAR_POLA * i, ROZMIAR_POLA * j, this);
            }
        }
    }

    @Override
    public void keyTyped(KeyEvent e) {

    }

    @Override
    public void keyPressed(KeyEvent e) {
        if (ifFinished)
            return;

        switch (e.getKeyCode()) {
            case KeyEvent.VK_DOWN:
                if (!dane.sciany[ziomekX/ROZMIAR_POLA][ziomekY/ROZMIAR_POLA][2])
                    ziomekY += ROZMIAR_POLA;
                break;
            case KeyEvent.VK_UP:
                if (!dane.sciany[ziomekX/ROZMIAR_POLA][ziomekY/ROZMIAR_POLA][0])
                    ziomekY -= ROZMIAR_POLA;
                break;
            case KeyEvent.VK_RIGHT:
                if (!dane.sciany[ziomekX/ROZMIAR_POLA][ziomekY/ROZMIAR_POLA][1])
                    ziomekX += ROZMIAR_POLA;
                break;
            case KeyEvent.VK_LEFT:
                if (!dane.sciany[ziomekX/ROZMIAR_POLA][ziomekY/ROZMIAR_POLA][3])
                    ziomekX -= ROZMIAR_POLA;
                break;

            case KeyEvent.VK_A:
                ziomekX = (Dane.SIZE-1) * ROZMIAR_POLA;
                ziomekY = ziomekX;
                break;
        }

        repaint();

        if (ziomekX/ROZMIAR_POLA == Dane.SIZE && ziomekY/ROZMIAR_POLA == Dane.SIZE-1) {
            ifFinished = true;
            System.out.print("WYGRANANANA");
        }
    }

    @Override
    public void keyReleased(KeyEvent e) {

    }
}
