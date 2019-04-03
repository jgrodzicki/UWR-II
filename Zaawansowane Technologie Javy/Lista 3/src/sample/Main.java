package sample;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.*;
import javafx.stage.Stage;

import java.io.IOException;
import java.util.Locale;
import java.util.ResourceBundle;

public class Main extends Application {

    private Stage stage;

    @Override
    public void start(Stage primaryStage) {
        stage = primaryStage;
        Button btnEN = new Button();
        btnEN.setText("English");
        btnEN.setOnAction((event) -> {
                loadView(new Locale("eng", "ENG"));
        });

        Button btnPL = new Button();
        btnPL.setText("Polski");
        btnPL.setOnAction((event) -> {
                loadView(new Locale("pl", "PL"));
        });

        Button btnNG = new Button();
        btnNG.setText("Nigerian");
        btnNG.setOnAction((event) -> {
                loadView(new Locale("igbo", "IGBO"));
        });

        VBox root = new VBox(20);
        root.getChildren().add(HBoxBuilder.create().spacing(10).style("-fx-background-color: gray").padding(new Insets(5)).children(btnEN, btnPL, btnNG).build());
        root.getChildren().add(new StackPane());
        primaryStage.setScene(new Scene(root, 600, 300));
        primaryStage.show();
    }

    private void loadView(Locale locale) {
        try {
            FXMLLoader fxmlLoader = new FXMLLoader();
            fxmlLoader.setResources(ResourceBundle.getBundle("MyBundle", locale));
            Pane pane = (GridPane) fxmlLoader.load(this.getClass().getResource("sample.fxml").openStream());

            stage.setTitle(fxmlLoader.getResources().getString("programName"));
            // replace the content
            StackPane content = (StackPane) ((VBox) stage.getScene().getRoot()).getChildren().get(1);
            content.getChildren().clear();
            content.getChildren().add(pane);
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}