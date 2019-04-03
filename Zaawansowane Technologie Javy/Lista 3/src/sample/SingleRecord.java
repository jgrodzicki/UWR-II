package sample;

import javafx.util.StringConverter;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Date;

public class SingleRecord {
    private String name;
    private String category;
    private String date;
    private double price;
    private String currency;

    public SingleRecord(String n, String cat, String d, double p, String c) {
        name = n;
        category = cat;
        date = d;
        price = p;
        currency = c;
    }

    @Override
    public String toString() {
        return name + "\t" + category + "\t" + date + "\t" + price + " " + currency;
    }
}
