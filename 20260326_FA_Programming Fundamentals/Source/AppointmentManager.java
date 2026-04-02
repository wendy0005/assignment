import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class AppointmentManager {
    private List<Appointment> appointments;
    private final String FILE_NAME = "appointments_data.txt";

    public AppointmentManager() { this.appointments = new ArrayList<>(); }
    public void addAppointment(Appointment a) { appointments.add(a); }
    public List<Appointment> getAppointments() { return new ArrayList<>(appointments); }
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
            if (a.getClientName().equalsIgnoreCase(name)) results.add(a);
        }
        return results;
    }
    public void saveToFile() throws IOException {
        try (PrintWriter writer = new PrintWriter(new FileWriter(FILE_NAME))) {
            for (Appointment a : appointments) {
                String type = (a instanceof RegularAppointment) ? "Regular" : "Priority";
                String extra = (a instanceof RegularAppointment) ? ((RegularAppointment) a).getServiceType() : ((PriorityAppointment) a).getPriorityLevel();
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
                String[] parts = scanner.nextLine().split("\\|");
                if (parts.length == 5) {
                    if (parts[0].equals("Regular")) appointments.add(new RegularAppointment(parts[1], parts[2], parts[3], parts[4]));
                    else appointments.add(new PriorityAppointment(parts[1], parts[2], parts[3], parts[4]));
                }
            }
        }
    }
    public void validateAppointmentData(String name, String date, String time, String extra) throws InvalidAppointmentException {
        if (name == null || name.trim().isEmpty()) throw new InvalidAppointmentException("Client name cannot be empty.");
        if (!date.matches("\\d{2}-\\d{2}-\\d{4}")) throw new InvalidAppointmentException("Invalid date format. Use DD-MM-YYYY.");
        if (!time.matches("\\d{2}:\\d{2}")) throw new InvalidAppointmentException("Invalid time format. Use HH:MM.");
        if (extra == null || extra.trim().isEmpty()) throw new InvalidAppointmentException("Service/Priority cannot be empty.");
    }
}
