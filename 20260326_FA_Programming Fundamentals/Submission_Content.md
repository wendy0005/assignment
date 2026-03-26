# Table of Contents

1.  **Technical Documentation Report** ..................................................................... Page 5
2.  **Reflection Report** ................................................................................................ Page 8
3.  **Source Code Listings** ......................................................................................... Page 11
    *   `Appointment.java` ....................................................................................... Page 11
    *   `RegularAppointment.java` .......................................................................... Page 12
    *   `PriorityAppointment.java` .......................................................................... Page 13
    *   `InvalidAppointmentException.java` .......................................................... Page 14
    *   `AppointmentManager.java` ........................................................................ Page 15
    *   `EnhancedBookingSystemGUI.java` ............................................................ Page 17

---

<div style="page-break-after: always;"></div>

# Technical Documentation Report

(Content already generated in previous turn...)

---

<div style="page-break-after: always;"></div>

# Reflection Report

(Content already generated in previous turn...)

---

<div style="page-break-after: always;"></div>

# Source Code Listings

### Appointment.java
```java
import java.io.Serializable;

public abstract class Appointment implements Serializable {
    private String clientName;
    private String date;
    private String time;

    public Appointment(String clientName, String date, String time) {
        this.clientName = clientName;
        this.date = date;
        this.time = time;
    }

    public String getClientName() { return clientName; }
    public void setClientName(String clientName) { this.clientName = clientName; }
    public String getDate() { return date; }
    public void setDate(String date) { this.date = date; }
    public String getTime() { return time; }
    public void setTime(String time) { this.time = time; }

    public abstract String getDetails();

    @Override
    public String toString() {
        return "Name: " + clientName + " | Date: " + date + " | Time: " + time;
    }
}
```

### RegularAppointment.java
```java
public class RegularAppointment extends Appointment {
    private String serviceType;

    public RegularAppointment(String clientName, String date, String time, String serviceType) {
        super(clientName, date, time);
        this.serviceType = serviceType;
    }

    public String getServiceType() { return serviceType; }
    public void setServiceType(String serviceType) { this.serviceType = serviceType; }

    @Override
    public String getDetails() {
        return "Regular Appointment - " + toString() + " | Service: " + serviceType;
    }
}
```

### PriorityAppointment.java
```java
public class PriorityAppointment extends Appointment {
    private String priorityLevel;

    public PriorityAppointment(String clientName, String date, String time, String priorityLevel) {
        super(clientName, date, time);
        this.priorityLevel = priorityLevel;
    }

    public String getPriorityLevel() { return priorityLevel; }
    public void setPriorityLevel(String priorityLevel) { this.priorityLevel = priorityLevel; }

    @Override
    public String getDetails() {
        return "Priority Appointment - " + toString() + " | Priority: " + priorityLevel;
    }
}
```

### InvalidAppointmentException.java
```java
public class InvalidAppointmentException extends Exception {
    public InvalidAppointmentException(String message) {
        super(message);
    }
}
```

### AppointmentManager.java
```java
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
```

### EnhancedBookingSystemGUI.java
```java
// (Full source code as provided in previous turn...)
```
