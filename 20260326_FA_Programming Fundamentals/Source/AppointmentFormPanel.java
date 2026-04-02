import javax.swing.*;
import java.awt.*;

/**
 * Helper class to encapsulate the Appointment Form UI.
 */
public class AppointmentFormPanel extends JPanel {
    public JTextField nameField, dateField, timeField, extraField;
    public JComboBox<String> typeBox;

    public AppointmentFormPanel() {
        setLayout(new GridLayout(6, 2, 10, 10));
        setBorder(BorderFactory.createEmptyBorder(20, 50, 20, 50));

        add(new JLabel("Client Name:"));
        nameField = new JTextField();
        add(nameField);

        add(new JLabel("Date (DD-MM-YYYY):"));
        dateField = new JTextField();
        add(dateField);

        add(new JLabel("Time (HH:MM):"));
        timeField = new JTextField();
        add(timeField);

        add(new JLabel("Type:"));
        typeBox = new JComboBox<>(new String[]{"Regular", "Priority"});
        add(typeBox);

        add(new JLabel("Service Type / Priority Level:"));
        extraField = new JTextField();
        add(extraField);
    }

    public void clear() {
        nameField.setText("");
        dateField.setText("");
        timeField.setText("");
        extraField.setText("");
    }

    public void setFields(String type, String name, String date, String time, String extra) {
        typeBox.setSelectedItem(type);
        nameField.setText(name);
        dateField.setText(date);
        timeField.setText(time);
        extraField.setText(extra);
    }
}
