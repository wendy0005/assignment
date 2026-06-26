import java.io.Serializable;

/**
 * Abstract class Appointment demonstrating Abstraction and Encapsulation.
 * This class serves as the base for different types of appointments.
 */
public abstract class Appointment implements Serializable {
    private String clientName;
    private String date;
    private String time;

    public Appointment(String clientName, String date, String time) {
        this.clientName = clientName;
        this.date = date;
        this.time = time;
    }

    // Encapsulation: Getters and Setters
    public String getClientName() {
        return clientName;
    }

    public void setClientName(String clientName) {
        this.clientName = clientName;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

    // Abstraction: Abstract method to be implemented by subclasses
    public abstract String getDetails();

    // Polymorphism: Overriding toString()
    @Override
    public String toString() {
        return "Name: " + clientName + " | Date: " + date + " | Time: " + time;
    }
}
