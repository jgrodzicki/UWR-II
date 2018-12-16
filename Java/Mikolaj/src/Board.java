import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Random;

public class Board extends JPanel {

    private int board[][];

    private BufferedImage background[] = new BufferedImage[4];

    public Board() {

        board = new int[Data.cols][Data.rows];
        generateBoard();

        setBounds(0, 0, Data.SIZE*Data.cols, Data.SIZE*Data.rows);

        try {
            String path = "img/background";
            for (int i = 0; i < background.length; i++) {
                background[i] = ImageIO.read(new File(path + Integer.toString(i) + ".jpeg"));
            }
        } catch (IOException e) {
            System.err.println("Unable to load background board images: " + e.getMessage());
            System.exit(1);
        }
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);

        for (int i = 0; i < Data.cols; i++)
            for (int j = 0; j < Data.rows; j++)
                g.drawImage(background[board[i][j]], i * Data.SIZE, j * Data.SIZE, this);
    }

    private void generateBoard() {
        for (int i = 0; i < Data.cols; i++)
            for (int j = 0; j < Data.rows; j++)
                board[i][j] = new Random().nextInt(background.length);
    }
}
