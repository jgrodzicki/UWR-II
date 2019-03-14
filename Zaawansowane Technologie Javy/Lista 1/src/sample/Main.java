package sample;

import javafx.application.Application;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

import java.math.BigInteger;

public class Main extends Application {
    final int WIDTH = 300;
    final int HEIGHT = 300;

    BigInteger number = BigInteger.valueOf(0);
    BigInteger prev_number = BigInteger.valueOf(0);

    char oper = ' ';

    TextField numb;

    @Override
    public void start(Stage primaryStage) throws Exception{
        primaryStage.setTitle("Kalkulator binarny");

        GridPane pane = new GridPane();
        pane.setAlignment(Pos.CENTER);
        pane.setHgap(10);
        pane.setVgap(10);
        Scene scene = new Scene(pane, WIDTH, HEIGHT);

        numb = new TextField();
        numb.setEditable(false);
        setLabel();

        Button b0 = new Button("0");
        Button b1 = new Button("1");


        Button bPlus = new Button("+");
        Button bMinus = new Button("-");
        Button bMult = new Button("*");
        Button bDiv = new Button("/");
        Button bMod = new Button("mod");

        Button bCl = new Button("C");
        Button bEq = new Button("=");


        b0.setOnAction((event -> {
            number = number.multiply(BigInteger.valueOf(2));
            setLabel();
        }));

        b1.setOnAction((event -> {
            number = number.multiply(BigInteger.valueOf(2));
            number = number.add(BigInteger.valueOf(1));
            setLabel();
        }));

        bPlus.setOnAction((event -> {
            prev_number = number;
            number = BigInteger.valueOf(0);
            oper = '+';
            setLabel();
        }));

        bMinus.setOnAction((event -> {
            prev_number = number;
            number = BigInteger.valueOf(0);
            oper = '-';
            setLabel();
        }));

        bMult.setOnAction((event -> {
            prev_number = number;
            number = BigInteger.valueOf(0);
            oper = '*';
            setLabel();
        }));

        bDiv.setOnAction((event -> {
            prev_number = number;
            number = BigInteger.valueOf(0);
            oper = '/';
            setLabel();
        }));

        bMod.setOnAction((event -> {
            prev_number = number;
            number = BigInteger.valueOf(0);
            oper = 'm';
            setLabel();
        }));

        bCl.setOnAction((event -> {
            if (number.equals(BigInteger.valueOf(0))) {
                prev_number = BigInteger.valueOf(0);
                oper = ' ';
            }
            number = BigInteger.valueOf(0);
            setLabel();
        }));

        bEq.setOnAction((event -> {
            switch (oper) {
                case '+':
                    number = prev_number.add(number);
                    break;
                case '-':
                    number = prev_number.subtract(number);
                    break;
                case '*':
                    number = prev_number.multiply(number);
                    break;
                case '/':
                    number = prev_number.divide(number);
                    break;
                case 'm':
                    number = prev_number.mod(number);
            }
            prev_number = BigInteger.valueOf(0);
            setLabel();
        }));


        pane.add(b0, 2, 8);
        pane.add(b1, 2, 9);

        pane.add(bPlus, 3, 7);
        pane.add(bMinus, 3, 8);
        pane.add(bMult, 3, 9);
        pane.add(bDiv, 3, 10);
        pane.add(bMod, 3, 11);
        pane.add(bCl, 5, 7);
        pane.add(bEq, 5, 8);

        pane.add(numb, 0, 0, 6, 1);

        primaryStage.setScene(scene);
        primaryStage.show();
    }

    private void setLabel() {
        numb.setText(number.toString(2));
    }


    public static void main(String[] args) {
        launch(args);
    }
}