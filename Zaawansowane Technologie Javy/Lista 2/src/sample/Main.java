package sample;

import javafx.application.Application;

public class Main  {

    public static void main(String[] args) {
        Data.init(150, 15, 15);

        Application.launch(Strip.class, args);
    }
}
