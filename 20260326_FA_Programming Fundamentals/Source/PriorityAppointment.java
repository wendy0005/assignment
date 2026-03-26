/**
 * PriorityAppointment class demonstrating Inheritance.
 * Extends Appointment to add specific priority level.
 */
public class PriorityAppointment extends Appointment {
    private String priorityLevel;

    public PriorityAppointment(String clientName, String date, String time, String priorityLevel) {
        super(clientName, date, time);
        this.priorityLevel = priorityLevel;
    }

    public String getPriorityLevel() {
        return priorityLevel;
    }

    public void setPriorityLevel(String priorityLevel) {
        this.priorityLevel = priorityLevel;
    }

    @Override
    public String getDetails() {
        return "Priority Appointment - " + toString();
    }

    @Override
    public String toString() {
        return super.toString() + " | Priority: " + priorityLevel;
    }
}
