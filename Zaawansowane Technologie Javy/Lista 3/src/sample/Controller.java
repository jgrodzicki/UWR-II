package sample;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;

import java.net.URL;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.ResourceBundle;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.*;
import javafx.scene.text.Text;
import javafx.util.StringConverter;

public class Controller implements Initializable {

    private static List<SingleRecord> records = new ArrayList<>();
    private static double sumConst = 0.0;
    private static double sumCycle = 0.0;

    private String nameText;
    private String categoryText;
    private String dateText;
    private String priceText;
    private String currencyText;

    private SimpleDateFormat dateFormat;

    private ResourceBundle bundle;
    @FXML private Button submitBtn;
    @FXML private TextField nameTF;
    @FXML private ComboBox categoryCB;
    @FXML private DatePicker dateDP;
    @FXML private TextField priceTF;
    @FXML private Text errorText;
    @FXML private Text currency;
    @FXML private TextArea historyConstantTA;
    @FXML private TextArea historyCycleTA;

    private String category[] = new String[2];

    private boolean isValid(String name, int index, String price) {
        if (name.isEmpty() || index == -1)
            return false;

        try {
            Double.parseDouble(price);
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
            Date date = java.sql.Date.valueOf(dateDP.getValue());
            errorText.setVisible(false);
            setTexts();
            SingleRecord added = new SingleRecord(name, category[index], index, dateFormat.format(date), Double.parseDouble(price), currencyText);
            records.add(added);
            if (index == 0)
                sumConst += Double.parseDouble(price);
            else
                sumCycle += Double.parseDouble(price);

            sethistoryConstantTA();
            setHistoryCycleTA();
        }
        else
            errorText.setVisible(true);
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        bundle = resources;
        category[0] = resources.getString("cat_constant");
        category[1] = resources.getString("cat_cycle");

        ObservableList<String> list = FXCollections.observableArrayList();
        list.addAll(category[0], category[1]);
        categoryCB.setItems(list);

        sethistoryConstantTA();
        setHistoryCycleTA();

        String pattern = resources.getString("dateFormat");
        dateFormat = new SimpleDateFormat(pattern);

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

    private void sethistoryConstantTA() {
        String res = "";
        for (SingleRecord rec : records) {
            if (!rec.isCycle())
                res += rec.toString() + "\n";
        }
        String sum = bundle.getString("sumConstant");
        res += "\n\n" + sum + ": " + sumConst;
        historyConstantTA.setText(res);
    }

    private void setHistoryCycleTA() {
        String res = "";
        for (SingleRecord rec : records) {
            if (rec.isCycle())
                res += rec.toString() + "\n";
        }
        String sum = bundle.getString("sumCycle");
        res += "\n\n" + sum + ": " + sumCycle;
        historyCycleTA.setText(res);
    }

    private void setTexts() {
        nameText = bundle.getString("name");
        categoryText = bundle.getString("category");
        dateText = bundle.getString("date");
        priceText = bundle.getString("price");
        currencyText = bundle.getString("currency");
    }
}