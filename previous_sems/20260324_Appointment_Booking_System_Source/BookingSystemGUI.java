import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;

/**
 * Main GUI class for the Appointment Booking System.
 * Demonstrates GUI components and File Handling with Try-Catch.
 */
public class BookingSystemGUI extends JFrame implements ActionListener {
    private JTextField nameField, dateField, timeField, extraField;
    private JComboBox<String> typeBox;
    private JTextArea displayArea;
    private JButton addButton, viewButton, searchButton, saveButton, loadButton;
    private ArrayList<Appointment> appointments;
    private final String FILE_NAME = "appointments.txt";

    public BookingSystemGUI() {
        appointments = new ArrayList<>();
        setTitle("Appointment Booking System");
        setSize(500, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // Input Panel
        JPanel inputPanel = new JPanel(new GridLayout(6, 2, 5, 5));
        inputPanel.add(new JLabel(" Client Name:"));
        nameField = new JTextField();
        inputPanel.add(nameField);

        inputPanel.add(new JLabel(" Date (DD-MM-YYYY):"));
        dateField = new JTextField();
        inputPanel.add(dateField);

        inputPanel.add(new JLabel(" Time (HH:MM):"));
        timeField = new JTextField();
        inputPanel.add(timeField);

        inputPanel.add(new JLabel(" Appointment Type:"));
        typeBox = new JComboBox<>(new String[]{"Regular", "Priority"});
        inputPanel.add(typeBox);

        inputPanel.add(new JLabel(" Service/Priority Level:"));
        extraField = new JTextField();
        inputPanel.add(extraField);

        addButton = new JButton("Add Appointment");
        addButton.addActionListener(this);
        inputPanel.add(addButton);

        add(inputPanel, BorderLayout.NORTH);

        // Display Area
        displayArea = new JTextArea();
        displayArea.setEditable(false);
        add(new JScrollPane(displayArea), BorderLayout.CENTER);

        // Button Panel
        JPanel buttonPanel = new JPanel(new FlowLayout());
        viewButton = new JButton("View All");
        searchButton = new JButton("Search Name");
        saveButton = new JButton("Save to File");
        loadButton = new JButton("Load from File");

        viewButton.addActionListener(this);
        searchButton.addActionListener(this);
        saveButton.addActionListener(this);
        loadButton.addActionListener(this);

        buttonPanel.add(viewButton);
        buttonPanel.add(searchButton);
        buttonPanel.add(saveButton);
        buttonPanel.add(loadButton);
        add(buttonPanel, BorderLayout.SOUTH);

        setVisible(true);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == addButton) {
            addAppointment();
        } else if (e.getSource() == viewButton) {
            viewAppointments();
        } else if (e.getSource() == searchButton) {
            searchAppointment();
        } else if (e.getSource() == saveButton) {
            saveToFile();
        } else if (e.getSource() == loadButton) {
            loadFromFile();
        }
    }

    private void addAppointment() {
        String name = nameField.getText();
        String date = dateField.getText();
        String time = timeField.getText();
        String type = (String) typeBox.getSelectedItem();
        String extra = extraField.getText();

        if (name.isEmpty() || date.isEmpty() || time.isEmpty() || extra.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Please fill all fields.");
            return;
        }

        if (type.equals("Regular")) {
            appointments.add(new RegularAppointment(name, date, time, extra));
        } else {
            appointments.add(new PriorityAppointment(name, date, time, extra));
        }

        displayArea.setText("Appointment added successfully for " + name);
        clearFields();
    }

    private void viewAppointments() {
        if (appointments.isEmpty()) {
            displayArea.setText("No appointments found.");
            return;
        }
        StringBuilder sb = new StringBuilder("--- All Appointments ---\n");
        for (Appointment a : appointments) {
            sb.append(a.getDetails()).append("\n");
        }
        displayArea.setText(sb.toString());
    }

    private void searchAppointment() {
        String searchName = JOptionPane.showInputDialog(this, "Enter Client Name to search:");
        if (searchName == null || searchName.isEmpty()) return;

        boolean found = false;
        StringBuilder sb = new StringBuilder("--- Search Results for '" + searchName + "' ---\n");
        for (Appointment a : appointments) {
            if (a.getClientName().equalsIgnoreCase(searchName)) {
                sb.append(a.getDetails()).append("\n");
                found = true;
            }
        }
        if (!found) {
            displayArea.setText("No appointment found for " + searchName);
        } else {
            displayArea.setText(sb.toString());
        }
    }

    private void saveToFile() {
        // File Handling with Try-Catch
        try (PrintWriter writer = new PrintWriter(new FileWriter(FILE_NAME))) {
            for (Appointment a : appointments) {
                String type = (a instanceof RegularAppointment) ? "Regular" : "Priority";
                String extra = (a instanceof RegularAppointment) ? ((RegularAppointment) a).getServiceType() : ((PriorityAppointment) a).getPriorityLevel();
                writer.println(type + "," + a.getClientName() + "," + a.getDate() + "," + a.getTime() + "," + extra);
            }
            displayArea.setText("Data saved to " + FILE_NAME);
        } catch (IOException ex) {
            displayArea.setText("Error saving to file: " + ex.getMessage());
        }
    }

    private void loadFromFile() {
        // File Handling with Try-Catch
        try (Scanner scanner = new Scanner(new File(FILE_NAME))) {
            appointments.clear();
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                String[] parts = line.split(",");
                if (parts.length == 5) {
                    String type = parts[0];
                    String name = parts[1];
                    String date = parts[2];
                    String time = parts[3];
                    String extra = parts[4];

                    if (type.equals("Regular")) {
                        appointments.add(new RegularAppointment(name, date, time, extra));
                    } else {
                        appointments.add(new PriorityAppointment(name, date, time, extra));
                    }
                }
            }
            displayArea.setText("Data loaded from " + FILE_NAME);
            viewAppointments();
        } catch (FileNotFoundException ex) {
            displayArea.setText("No saved file found.");
        } catch (Exception ex) {
            displayArea.setText("Error loading file: " + ex.getMessage());
        }
    }

    private void clearFields() {
        nameField.setText("");
        dateField.setText("");
        timeField.setText("");
        extraField.setText("");
    }

    public static void main(String[] args) {
        new BookingSystemGUI();
    }
}
