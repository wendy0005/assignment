import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.util.List;

/**
 * Enhanced GUI for the Appointment Booking System.
 * Demonstrates JTabbedPane, JTable, and interaction with AppointmentManager.
 */
public class EnhancedBookingSystemGUI extends JFrame implements ActionListener {
    private AppointmentManager manager;
    private JTabbedPane tabbedPane;

    // Input Fields
    private JTextField nameField, dateField, timeField, extraField;
    private JComboBox<String> typeBox;
    private JButton addButton, updateButton, deleteButton, saveButton, loadButton, clearButton;

    // View Components
    private JTable appointmentTable;
    private DefaultTableModel tableModel;
    private JTextField searchField;
    private JButton searchButton, refreshButton;

    public EnhancedBookingSystemGUI() {
        manager = new AppointmentManager();
        setTitle("Integrated Appointment System - V2.0");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        tabbedPane = new JTabbedPane();

        // 1. Manage Tab
        tabbedPane.addTab("Manage Appointments", createManagePanel());

        // 2. View Tab
        tabbedPane.addTab("View & Search", createViewPanel());

        add(tabbedPane);

        // Initial Load Attempt
        try {
            manager.loadFromFile();
            refreshTableData();
        } catch (IOException e) {
            // Silently ignore if file doesn't exist yet
        }

        setVisible(true);
    }

    private JPanel createManagePanel() {
        JPanel panel = new JPanel(new BorderLayout());

        // Input Form
        JPanel formPanel = new JPanel(new GridLayout(6, 2, 10, 10));
        formPanel.setBorder(BorderFactory.createEmptyBorder(20, 50, 20, 50));

        formPanel.add(new JLabel("Client Name:"));
        nameField = new JTextField();
        formPanel.add(nameField);

        formPanel.add(new JLabel("Date (DD-MM-YYYY):"));
        dateField = new JTextField();
        formPanel.add(dateField);

        formPanel.add(new JLabel("Time (HH:MM):"));
        timeField = new JTextField();
        formPanel.add(timeField);

        formPanel.add(new JLabel("Type:"));
        typeBox = new JComboBox<>(new String[]{"Regular", "Priority"});
        formPanel.add(typeBox);

        formPanel.add(new JLabel("Service Type / Priority Level:"));
        extraField = new JTextField();
        formPanel.add(extraField);

        panel.add(formPanel, BorderLayout.CENTER);

        // Button Controls
        JPanel controlPanel = new JPanel(new FlowLayout());
        addButton = new JButton("Add New");
        updateButton = new JButton("Update Selected");
        deleteButton = new JButton("Delete Selected");
        clearButton = new JButton("Clear Form");
        saveButton = new JButton("Save Data");
        loadButton = new JButton("Load Data");

        addButton.addActionListener(this);
        updateButton.addActionListener(this);
        deleteButton.addActionListener(this);
        clearButton.addActionListener(this);
        saveButton.addActionListener(this);
        loadButton.addActionListener(this);

        controlPanel.add(addButton);
        controlPanel.add(updateButton);
        controlPanel.add(deleteButton);
        controlPanel.add(clearButton);
        controlPanel.add(new JSeparator(SwingConstants.VERTICAL));
        controlPanel.add(saveButton);
        controlPanel.add(loadButton);

        panel.add(controlPanel, BorderLayout.SOUTH);

        return panel;
    }

    private JPanel createViewPanel() {
        JPanel panel = new JPanel(new BorderLayout());

        // Search Header
        JPanel searchHeader = new JPanel(new FlowLayout(FlowLayout.LEFT));
        searchField = new JTextField(20);
        searchButton = new JButton("Search Name");
        refreshButton = new JButton("Refresh All");

        searchButton.addActionListener(this);
        refreshButton.addActionListener(this);

        searchHeader.add(new JLabel("Search Client:"));
        searchHeader.add(searchField);
        searchHeader.add(searchButton);
        searchHeader.add(refreshButton);
        panel.add(searchHeader, BorderLayout.NORTH);

        // Data Table
        String[] columns = {"Type", "Client Name", "Date", "Time", "Details"};
        tableModel = new DefaultTableModel(columns, 0);
        appointmentTable = new JTable(tableModel);
        panel.add(new JScrollPane(appointmentTable), BorderLayout.CENTER);

        return panel;
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        Object source = e.getSource();

        if (source == addButton) {
            handleCreate();
        } else if (source == updateButton) {
            handleUpdate();
        } else if (source == deleteButton) {
            handleDelete();
        } else if (source == clearButton) {
            clearForm();
        } else if (source == saveButton) {
            handleSave();
        } else if (source == loadButton) {
            handleLoad();
        } else if (source == searchButton) {
            handleSearch();
        } else if (source == refreshButton) {
            refreshTableData();
        }
    }

    private void handleCreate() {
        try {
            String name = nameField.getText();
            String date = dateField.getText();
            String time = timeField.getText();
            String extra = extraField.getText();
            String type = (String) typeBox.getSelectedItem();

            manager.validateAppointmentData(name, date, time, extra);

            Appointment a;
            if ("Regular".equals(type)) {
                a = new RegularAppointment(name, date, time, extra);
            } else {
                a = new PriorityAppointment(name, date, time, extra);
            }

            manager.addAppointment(a);
            JOptionPane.showMessageDialog(this, "Appointment added successfully.");
            refreshTableData();
            clearForm();
        } catch (InvalidAppointmentException ex) {
            JOptionPane.showMessageDialog(this, "Validation Error: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void handleUpdate() {
        int selectedRow = appointmentTable.getSelectedRow();
        if (selectedRow == -1) {
            JOptionPane.showMessageDialog(this, "Please select an appointment from the table in 'View' tab to update.");
            return;
        }

        try {
            String name = nameField.getText();
            String date = dateField.getText();
            String time = timeField.getText();
            String extra = extraField.getText();
            String type = (String) typeBox.getSelectedItem();

            manager.validateAppointmentData(name, date, time, extra);

            Appointment a;
            if ("Regular".equals(type)) {
                a = new RegularAppointment(name, date, time, extra);
            } else {
                a = new PriorityAppointment(name, date, time, extra);
            }

            manager.updateAppointment(selectedRow, a);
            JOptionPane.showMessageDialog(this, "Appointment updated successfully.");
            refreshTableData();
        } catch (InvalidAppointmentException ex) {
            JOptionPane.showMessageDialog(this, "Validation Error: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void handleDelete() {
        int selectedRow = appointmentTable.getSelectedRow();
        if (selectedRow == -1) {
            JOptionPane.showMessageDialog(this, "Please select an appointment from the table to delete.");
            return;
        }

        int confirm = JOptionPane.showConfirmDialog(this, "Are you sure you want to delete this appointment?", "Confirm Delete", JOptionPane.YES_NO_OPTION);
        if (confirm == JOptionPane.YES_OPTION) {
            manager.deleteAppointment(selectedRow);
            refreshTableData();
            JOptionPane.showMessageDialog(this, "Appointment deleted.");
        }
    }

    private void handleSave() {
        try {
            manager.saveToFile();
            JOptionPane.showMessageDialog(this, "Data saved successfully.");
        } catch (IOException ex) {
            JOptionPane.showMessageDialog(this, "Error saving: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void handleLoad() {
        try {
            manager.loadFromFile();
            refreshTableData();
            JOptionPane.showMessageDialog(this, "Data loaded successfully.");
        } catch (IOException ex) {
            JOptionPane.showMessageDialog(this, "Error loading: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void handleSearch() {
        String query = searchField.getText();
        if (query.isEmpty()) {
            refreshTableData();
            return;
        }

        List<Appointment> results = manager.searchByClientName(query);
        populateTable(results);
    }

    private void refreshTableData() {
        populateTable(manager.getAppointments());
    }

    private void populateTable(List<Appointment> data) {
        tableModel.setRowCount(0);
        for (Appointment a : data) {
            String type = (a instanceof RegularAppointment) ? "Regular" : "Priority";
            String extra = (a instanceof RegularAppointment) ? ((RegularAppointment) a).getServiceType() : ((PriorityAppointment) a).getPriorityLevel();
            tableModel.addRow(new Object[]{type, a.getClientName(), a.getDate(), a.getTime(), extra});
        }
    }

    private void clearForm() {
        nameField.setText("");
        dateField.setText("");
        timeField.setText("");
        extraField.setText("");
    }

    public static void main(String[] args) {
        // Run on Event Dispatch Thread
        SwingUtilities.invokeLater(() -> new EnhancedBookingSystemGUI());
    }
}
