import 'package:flutter/foundation.dart';

class CampusSession extends ChangeNotifier {
  CampusSession(this.email);

  final String email;
  bool reminders = true;
  bool libraryUnread = true;
  int _nextBooking = 2841;
  int _nextTicket = 2916;
  final Map<String, String> _reservations = {};
  final Map<String, String> _tickets = {};
  final Set<String> _pendingPayments = {};

  String get firstName {
    final name = email.split('@').first.split(RegExp(r'[._-]')).first;
    return name[0].toUpperCase() + name.substring(1);
  }

  String get fullName =>
      email == 'aina@university.edu' ? 'Aina Rahman' : firstName;

  void setReminders(bool enabled) {
    reminders = enabled;
    notifyListeners();
  }

  void readLibraryNotice() {
    libraryUnread = false;
    notifyListeners();
  }

  bool reserved(String date, String time) =>
      _reservations.containsKey('$date/$time');

  String? reserve(String date, String time) {
    if (date.startsWith('Wednesday') && time == '2:00 PM' ||
        reserved(date, time)) {
      return null;
    }
    final reference = 'LIB-${_nextBooking++}';
    _reservations['$date/$time'] = reference;
    return reference;
  }

  bool isPending(String event) => _pendingPayments.contains(event);

  void setPending(String event, bool pending) {
    if (pending) {
      _pendingPayments.add(event);
    } else {
      _pendingPayments.remove(event);
    }
  }

  String? ticketFor(String event) => _tickets[event];

  String issueTicket(String event) {
    final reference = _tickets.putIfAbsent(event, () => 'EVT-${_nextTicket++}');
    notifyListeners();
    return reference;
  }
}
