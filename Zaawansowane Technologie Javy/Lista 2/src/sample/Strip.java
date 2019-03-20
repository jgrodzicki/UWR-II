package sample;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.*;
import javafx.stage.Stage;
import javafx.util.Pair;

import java.util.Map;
import java.util.Timer;
import java.util.TimerTask;

public class Strip extends Application {
    private Label[][] l = new Label[Data.getRows()][Data.getCols()];
    private Timer timer = new Timer();

    @Override
    public void start(Stage primaryStage) throws Exception {
        primaryStage.setTitle("Strip with numbers");

        setUp(primaryStage);

        TimerTask task = new TimerTask()
        {
            @Override
            public void run()
            {
                Platform.runLater(() -> {
                        repaint();
                    }
                );
            }
        };
        timer.schedule(task,0, 1000/25);


        repaint();

        Data.startThreads();
    }

    private void setUp(Stage primaryStage) {
        for (int i = 0; i < Data.getRows(); i++) {
            for (int j = 0; j < Data.getCols(); j++) {
                l[i][j] = new Label();
                l[i][j].setStyle("-fx-border-color: black; -fx-background-color: white;");
                l[i][j].setAlignment(Pos.CENTER);
                l[i][j].setMinSize(50, 50);
            }
        }

        TilePane tile = new TilePane();
        tile.setStyle("-fx-border-color: black;");
        tile.setPrefColumns(Data.getCols());
        tile.setPrefRows(Data.getRows());

        for (int i = 0; i< Data.getRows(); i++) {
            for(int j = 0; j< Data.getCols(); j++) {
                tile.getChildren().add(l[i][j]);
            }
        }

        VBox root = new VBox();
        root.getChildren().add(tile);
        root.setFillWidth(false);
        primaryStage.setScene(new Scene(root));
        primaryStage.show();
    }

    private void repaint() {
        for (int i = 0; i < Data.getRows(); i++)
            for (int j = 0; j < Data.getCols(); j++)
                l[i][j].setText("");

        for (Map.Entry<Integer, Pair<Integer, Integer>> entry : Data.getPosBeans().entrySet()) {
            int x = entry.getValue().getKey();
            int y = entry.getValue().getValue();
            if (x == -1 && y == -1)
                continue;

            l[x][y].setText(entry.getKey().toString());
        }
    }
}
