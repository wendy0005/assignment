import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.*;
import java.io.IOException;
import java.util.List;

public class EnhancedBookingSystemGUI extends JFrame implements ActionListener {
    private AppointmentManager manager = new AppointmentManager();
    private AppointmentFormPanel formPanel = new AppointmentFormPanel();
    private DefaultTableModel tableModel = new DefaultTableModel(new String[]{"Type", "Client Name", "Date", "Time", "Details"}, 0);
    private JTable appointmentTable = new JTable(tableModel);
    private JTextField searchField = new JTextField(20);

    public EnhancedBookingSystemGUI() {
        setTitle("Appointment Booking System V2.1");
        setSize(800, 600);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        JTabbedPane tabs = new JTabbedPane();
        tabs.addTab("Manage", createManageTab());
        tabs.addTab("View", createViewTab());
        add(tabs);

        try { manager.loadFromFile(); refreshTable(); } catch (IOException e) {}
        setVisible(true);
    }

    private JPanel createManageTab() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.add(formPanel, BorderLayout.CENTER);

        JPanel buttons = new JPanel();
        String[] labels = {"Add", "Update", "Delete", "Clear", "Save", "Load"};
        for (String label : labels) {
            JButton btn = new JButton(label);
            btn.addActionListener(this);
            buttons.add(btn);
        }
        panel.add(buttons, BorderLayout.SOUTH);
        return panel;
    }

    private JPanel createViewTab() {
        JPanel panel = new JPanel(new BorderLayout());
        JPanel header = new JPanel();
        header.add(new JLabel("Search:"));
        header.add(searchField);
        JButton searchBtn = new JButton("Search");
        searchBtn.addActionListener(this);
        header.add(searchBtn);
        panel.add(header, BorderLayout.NORTH);
        panel.add(new JScrollPane(appointmentTable), BorderLayout.CENTER);
        return panel;
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        String cmd = e.getActionCommand();
        try {
            if (cmd.equals("Add")) handleAdd();
            else if (cmd.equals("Update")) handleUpdate();
            else if (cmd.equals("Delete")) handleDelete();
            else if (cmd.equals("Clear")) formPanel.clear();
            else if (cmd.equals("Save")) { manager.saveToFile(); msg("Saved!"); }
            else if (cmd.equals("Load")) { manager.loadFromFile(); refreshTable(); msg("Loaded!"); }
            else if (cmd.equals("Search")) populateTable(manager.searchByClientName(searchField.getText()));
        } catch (Exception ex) { msg("Error: " + ex.getMessage()); }
    }

    private void handleAdd() throws InvalidAppointmentException {
        Appointment a = getFromForm();
        manager.addAppointment(a);
        refreshTable();
        formPanel.clear();
    }

    private void handleUpdate() throws InvalidAppointmentException {
        int row = appointmentTable.getSelectedRow();
        if (row != -1) {
            manager.updateAppointment(row, getFromForm());
            refreshTable();
        } else msg("Select a row first!");
    }

    private void handleDelete() {
        int row = appointmentTable.getSelectedRow();
        if (row != -1) {
            manager.deleteAppointment(row);
            refreshTable();
        } else msg("Select a row first!");
    }

    private Appointment getFromForm() throws InvalidAppointmentException {
        String name = formPanel.nameField.getText();
        String date = formPanel.dateField.getText();
        String time = formPanel.timeField.getText();
        String extra = formPanel.extraField.getText();
        String type = (String) formPanel.typeBox.getSelectedItem();

        manager.validateAppointmentData(name, date, time, extra);
        return type.equals("Regular") ? new RegularAppointment(name, date, time, extra) : new PriorityAppointment(name, date, time, extra);
    }

    private void refreshTable() { populateTable(manager.getAppointments()); }

    private void populateTable(List<Appointment> list) {
        tableModel.setRowCount(0);
        for (Appointment a : list) {
            String type = (a instanceof RegularAppointment) ? "Regular" : "Priority";
            String extra = (a instanceof RegularAppointment) ? ((RegularAppointment) a).getServiceType() : ((PriorityAppointment) a).getPriorityLevel();
            tableModel.addRow(new Object[]{type, a.getClientName(), a.getDate(), a.getTime(), extra});
        }
    }

    private void msg(String s) { JOptionPane.showMessageDialog(this, s); }

    public static void main(String[] args) { SwingUtilities.invokeLater(EnhancedBookingSystemGUI::new); }
}
