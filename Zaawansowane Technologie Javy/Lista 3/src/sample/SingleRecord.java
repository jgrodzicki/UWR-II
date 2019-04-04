package sample;

import javafx.util.StringConverter;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Date;

public class SingleRecord {
    private String name;
    private boolean isCycle;
    private String category;
    private String date;
    private double price;
    private String currency;

    public SingleRecord(String n, String cat, int index, String d, double p, String c) {
        name = n;
        category = cat;
        if (index == 0)
            isCycle = false;
        else
            isCycle = true;
        date = d;
        price = p;
        currency = c;
    }

    public boolean isCycle() {
        return isCycle;
    }

    @Override
    public String toString() {
        return name + "\t" + date + "\t" + price + " " + currency;
    }
}
