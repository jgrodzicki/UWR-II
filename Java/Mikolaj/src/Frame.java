import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Frame extends JFrame implements ActionListener {
    JButton reset;
    JLabel label;

    public Frame() {
        super("Xmas game");
        setSize(Data.SIZE*Data.cols + 100, Data.SIZE*Data.rows + 20);

        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setVisible(true);

        reset = new JButton("RESET");
        reset.setBounds(Data.SIZE*Data.cols, (Data.SIZE*Data.rows)/2 - 25, 100, 50);
        reset.addActionListener(this);
        this.add(reset);

        label = new JLabel("", SwingConstants.CENTER);
        label.setBounds(Data.SIZE*Data.cols, (Data.SIZE*Data.rows)/4 - 25, 100, 50);
        label.setVisible(false);
        this.add(label);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        Game.stopAll();
        this.dispose();
        Game.newGame();
    }
}
