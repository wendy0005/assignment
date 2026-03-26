import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/**
 * Manager class to handle business logic for appointments.
 * Demonstrates Separation of Concerns, File Handling, and CRUD operations.
 */
public class AppointmentManager {
    private List<Appointment> appointments;
    private final String FILE_NAME = "appointments_data.txt";

    public AppointmentManager() {
        this.appointments = new ArrayList<>();
    }

    public void addAppointment(Appointment a) {
        appointments.add(a);
    }

    public List<Appointment> getAppointments() {
        return new ArrayList<>(appointments); // Return copy to preserve encapsulation
    }

    public boolean updateAppointment(int index, Appointment a) {
        if (index >= 0 && index < appointments.size()) {
            appointments.set(index, a);
            return true;
        }
        return false;
    }

    public boolean deleteAppointment(int index) {
        if (index >= 0 && index < appointments.size()) {
            appointments.remove(index);
            return true;
        }
        return false;
    }

    public List<Appointment> searchByClientName(String name) {
        List<Appointment> results = new ArrayList<>();
        for (Appointment a : appointments) {
            if (a.getClientName().equalsIgnoreCase(name)) {
                results.add(a);
            }
        }
        return results;
    }

    public void saveToFile() throws IOException {
        try (PrintWriter writer = new PrintWriter(new FileWriter(FILE_NAME))) {
            for (Appointment a : appointments) {
                String type = (a instanceof RegularAppointment) ? "Regular" : "Priority";
                String extra = (a instanceof RegularAppointment) ? 
                                ((RegularAppointment) a).getServiceType() : 
                                ((PriorityAppointment) a).getPriorityLevel();
                writer.println(type + "|" + a.getClientName() + "|" + a.getDate() + "|" + a.getTime() + "|" + extra);
            }
        }
    }

    public void loadFromFile() throws IOException {
        File file = new File(FILE_NAME);
        if (!file.exists()) return;

        appointments.clear();
        try (Scanner scanner = new Scanner(file)) {
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                String[] parts = line.split("\\|");
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
        }
    }

    // Validation Methods
    public void validateAppointmentData(String name, String date, String time, String extra) throws InvalidAppointmentException {
        if (name == null || name.trim().isEmpty()) {
            throw new InvalidAppointmentException("Client name cannot be empty.");
        }
        if (!isValidDate(date)) {
            throw new InvalidAppointmentException("Invalid date format. Use DD-MM-YYYY.");
        }
        if (!isValidTime(time)) {
            throw new InvalidAppointmentException("Invalid time format. Use HH:MM.");
        }
        if (extra == null || extra.trim().isEmpty()) {
            throw new InvalidAppointmentException("Additional info (Service/Priority) cannot be empty.");
        }
    }

    private boolean isValidDate(String date) {
        // Simple regex for DD-MM-YYYY
        return date.matches("\\d{2}-\\d{2}-\\d{4}");
    }

    private boolean isValidTime(String time) {
        // Simple regex for HH:MM
        return time.matches("\\d{2}:\\d{2}");
    }
}
