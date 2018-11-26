import java.awt.*;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

public class Main extends Frame {

    Dane dane;
    Labirynt labirynt;

    public Main() {

        super("Lab");
        setSize(625, 655);
        setVisible(true);
        addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                System.exit(0);
            }
        });
        dane = new Dane();
        labirynt = new Labirynt(dane);
        setFocusable(true);
        add(labirynt);
    }

    public static void main(String[] args) {
        new Main();
    }
}
