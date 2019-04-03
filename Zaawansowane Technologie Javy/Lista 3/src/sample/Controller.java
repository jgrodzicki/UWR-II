package sample;

import javafx.event.ActionEvent;

import java.net.URL;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ResourceBundle;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.DatePicker;
import javafx.scene.control.TextField;
import javafx.scene.text.Text;
import javafx.util.StringConverter;

public class Controller implements Initializable {

    private ResourceBundle bundle;
    @FXML private Button submitBtn;
    @FXML private TextField nameTF;
    @FXML private ComboBox categoryCB;
    @FXML private DatePicker dateDP;
    @FXML private TextField priceTF;
    @FXML private Text errorText;
    @FXML private Text currency;

    private String category[] = new String[2];

    private boolean isValid(String name, int index, String price) {
        if (name.isEmpty() || index == -1)
            return false;

        try {
            Integer.parseInt(price);
            java.sql.Date.valueOf(dateDP.getValue());
        } catch (NumberFormatException | NullPointerException e) {
            return false;
        }
        return true;
    }

    @FXML public void handleAction(ActionEvent e) {
        String name = nameTF.getText();

        int index = categoryCB.getSelectionModel().getSelectedIndex();
        String price = priceTF.getText();

        if (isValid(name, index, price)) {
            errorText.setVisible(false);
            System.out.println(name + "\t" + category[index] + "\t" + java.sql.Date.valueOf(dateDP.getValue()) + "\t" + price);
        }
        else
            errorText.setVisible(true);
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        bundle = resources;
        category[0] = resources.getString("cat_constant");
        category[1] = resources.getString("cat_cycle");

        dateDP.setConverter(new StringConverter<LocalDate>() {
            String pattern = resources.getString("dateFormat");
            DateTimeFormatter dateFormatter = DateTimeFormatter.ofPattern(pattern);

            @Override
            public String toString(LocalDate date) {
                if (date != null) {
                    return dateFormatter.format(date);
                } else {
                    return "";
                }
            }

            @Override
            public LocalDate fromString(String string) {
                if (string != null && !string.isEmpty()) {
                    return LocalDate.parse(string, dateFormatter);
                } else {
                    return null;
                }
            }
        });
    }
}