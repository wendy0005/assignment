/**
 * RegularAppointment class demonstrating Inheritance.
 * Extends Appointment to add specific service type.
 */
public class RegularAppointment extends Appointment {
    private String serviceType;

    public RegularAppointment(String clientName, String date, String time, String serviceType) {
        super(clientName, date, time);
        this.serviceType = serviceType;
    }

    public String getServiceType() {
        return serviceType;
    }

    public void setServiceType(String serviceType) {
        this.serviceType = serviceType;
    }

    @Override
    public String getDetails() {
        return "Regular Appointment - " + toString();
    }

    @Override
    public String toString() {
        return super.toString() + " | Service: " + serviceType;
    }
}
