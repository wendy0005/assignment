// BCL1313 Lab Assessment 1: Stack and Queue Implementation
// Chan Jing Yi | SUOL2500321
// C++17. Custom bounded structures; no std::queue or std::stack.
#include <array>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

constexpr std::size_t CAPACITY = 10;

struct Order {
    std::string id;
    std::string customer;
    std::string food;
    int quantity = 0;
};

void printOrder(const Order& order, std::ostream& out) {
    out << std::left << std::setw(10) << order.id
        << std::setw(18) << order.customer
        << std::setw(22) << order.food << order.quantity << '\n';
}

void printHeader(std::ostream& out) {
    out << std::left << std::setw(10) << "Order ID"
        << std::setw(18) << "Customer" << std::setw(22) << "Food item"
        << "Quantity\n";
}

class OrderQueue {
    std::array<Order, CAPACITY> items{};
    std::size_t frontIndex = 0;
    std::size_t count = 0;

public:
    bool empty() const { return count == 0; }
    bool full() const { return count == CAPACITY; }
    std::size_t size() const { return count; }

    bool enqueue(const Order& order) {
        if (full()) return false;
        // Modulo reuses slots freed by previous dequeues.
        items[(frontIndex + count) % CAPACITY] = order;
        ++count;
        return true;
    }

    bool dequeue(Order& removed) {
        if (empty()) return false;
        removed = items[frontIndex];
        items[frontIndex] = Order{};
        frontIndex = (frontIndex + 1) % CAPACITY;
        --count;
        return true;
    }

    const Order* front() const {
        return empty() ? nullptr : &items[frontIndex];
    }

    void display(std::ostream& out) const {
        out << "Incoming queue (front to rear), count = " << count << '\n';
        if (empty()) { out << "Queue is empty.\n"; return; }
        printHeader(out);
        for (std::size_t i = 0; i < count; ++i)
            printOrder(items[(frontIndex + i) % CAPACITY], out);
    }
};

class OrderStack {
    std::array<Order, CAPACITY> items{};
    std::size_t count = 0;

public:
    bool empty() const { return count == 0; }
    bool full() const { return count == CAPACITY; }
    std::size_t size() const { return count; }

    bool push(const Order& order) {
        if (full()) return false;
        items[count] = order;
        ++count;
        return true;
    }

    bool pop(Order& removed) {
        if (empty()) return false;
        removed = items[count - 1];
        items[count - 1] = Order{};
        --count;
        return true;
    }

    const Order* peek() const {
        return empty() ? nullptr : &items[count - 1];
    }

    void display(std::ostream& out) const {
        out << "Completed stack (top to bottom), count = " << count << '\n';
        if (empty()) { out << "Stack is empty.\n"; return; }
        printHeader(out);
        for (std::size_t i = count; i > 0; --i)
            printOrder(items[i - 1], out);
    }
};

class RestaurantSystem {
    OrderQueue incoming;
    OrderStack completed;

public:
    bool addOrder(const Order& order, std::ostream& out) {
        if (order.id.empty() || order.customer.empty() || order.food.empty()
            || order.quantity <= 0) {
            out << "Rejected: order fields must be nonempty and quantity positive.\n";
            return false;
        }
        if (!incoming.enqueue(order)) {
            out << "Queue is full. Order was not added.\n";
            return false;
        }
        out << "Enqueued " << order.id << '\n';
        return true;
    }

    bool processOrder(std::ostream& out) {
        if (incoming.empty()) {
            out << "Queue is empty. No order processed.\n";
            return false;
        }
        // Check destination capacity BEFORE changing either structure.
        if (completed.full()) {
            out << "Completed stack is full. Incoming order retained.\n";
            return false;
        }
        Order order;
        incoming.dequeue(order);
        completed.push(order);  // Guaranteed space in this single threaded program.
        out << "Processed " << order.id << " -> automatically pushed "
            << order.id << " to completed stack.\n";
        return true;
    }

    bool popCompleted(std::ostream& out) {
        Order removed;
        if (!completed.pop(removed)) {
            out << "Stack is empty. No order popped.\n";
            return false;
        }
        out << "Popped " << removed.id << " from completed stack.\n";
        return true;
    }

    void peekIncoming(std::ostream& out) const {
        if (const Order* order = incoming.front()) {
            out << "Front/Peek (queue unchanged):\n";
            printHeader(out); printOrder(*order, out);
        } else out << "Queue is empty. No front order.\n";
    }

    void peekCompleted(std::ostream& out) const {
        if (const Order* order = completed.peek()) {
            out << "Peek (stack unchanged):\n";
            printHeader(out); printOrder(*order, out);
        } else out << "Stack is empty. No top order.\n";
    }

    void showQueue(std::ostream& out) const { incoming.display(out); }
    void showStack(std::ostream& out) const { completed.display(out); }
    std::size_t pendingCount() const { return incoming.size(); }
    std::size_t completedCount() const { return completed.size(); }
    const Order* nextOrder() const { return incoming.front(); }
    const Order* latestOrder() const { return completed.peek(); }
};

const std::array<Order, 6> SAMPLE_ORDERS{{
    {"ORD001", "Aiman", "Chicken Rice", 2},
    {"ORD002", "Bella", "Fried Rice", 1},
    {"ORD003", "Chen", "Burger", 2},
    {"ORD004", "Devi", "Nasi Lemak", 1},
    {"ORD005", "Ethan", "Spaghetti", 2},
    {"ORD006", "Farah", "Mee Goreng", 1}
}};

void runDemo(std::ostream& out) {
    RestaurantSystem system;
    out << "=== TASK 2A: FIVE INCOMING ORDERS AND FRONT/PEEK ===\n";
    for (std::size_t i = 0; i < 5; ++i) system.addOrder(SAMPLE_ORDERS[i], out);
    system.showQueue(out);
    system.peekIncoming(out);
    out << "After Peek: pending count = " << system.pendingCount() << "\n\n";

    out << "=== TASK 2B: DEQUEUE, AUTOMATIC PUSH AND NEW ENQUEUE ===\n";
    system.processOrder(out);
    system.showQueue(out);
    system.showStack(out);
    system.addOrder(SAMPLE_ORDERS[5], out);
    system.showQueue(out);
    out << '\n';

    out << "=== TASK 3A: THREE ORDERS PROCESSED IN TOTAL ===\n";
    system.processOrder(out);
    system.processOrder(out);
    system.showQueue(out);
    system.showStack(out);
    system.peekCompleted(out);
    out << "After Peek: completed count = " << system.completedCount() << "\n\n";

    out << "=== TASK 3B: POP MOST RECENTLY COMPLETED ORDER ===\n";
    system.popCompleted(out);
    system.showStack(out);
    system.showQueue(out);
    out << "Final counts: pending = " << system.pendingCount()
        << ", completed = " << system.completedCount() << ", popped = 1\n";
}

// Full line parsing rejects inputs such as 2abc and 1.5.
bool parseInteger(const std::string& text, int& value) {
    std::istringstream input(text);
    char trailing;
    return (input >> value) && !(input >> trailing);
}

bool readText(const std::string& prompt, std::string& value, std::size_t limit) {
    while (true) {
        std::cout << prompt;
        if (!std::getline(std::cin, value)) return false;
        const auto first = value.find_first_not_of(" \t\r");
        if (first != std::string::npos) {
            const auto last = value.find_last_not_of(" \t\r");
            value = value.substr(first, last - first + 1);
            if (value.size() <= limit) return true;
        }
        std::cout << "Enter 1 to " << limit << " characters.\n";
    }
}

void runInteractive() {
    RestaurantSystem system;
    int nextId = 1;
    while (true) {
        std::cout << "\nRESTAURANT ORDER MANAGEMENT\n"
                  << "1. Enqueue new order\n2. Process next order (Dequeue + Push)\n"
                  << "3. Front/Peek incoming\n4. Display incoming\n"
                  << "5. Peek completed\n6. Pop completed\n7. Display completed\n"
                  << "0. Exit\nChoice: ";
        std::string line;
        if (!std::getline(std::cin, line)) break;
        int choice;
        if (!parseInteger(line, choice) || choice < 0 || choice > 7) {
            std::cout << "Invalid choice. Enter an integer from 0 to 7.\n";
            continue;
        }
        if (choice == 0) break;
        if (choice == 1) {
            Order order;
            if (!readText("Customer (maximum 16 characters): ", order.customer, 16)
                || !readText("Food item (maximum 20 characters): ", order.food, 20)) break;
            while (true) {
                std::cout << "Quantity (1 to 999): ";
                if (!std::getline(std::cin, line)) return;
                if (parseInteger(line, order.quantity)
                    && order.quantity >= 1 && order.quantity <= 999) break;
                std::cout << "Invalid quantity. Enter an integer from 1 to 999.\n";
            }
            std::ostringstream id;
            id << "ORD" << std::setfill('0') << std::setw(3) << nextId;
            order.id = id.str();
            if (system.addOrder(order, std::cout)) ++nextId;
        } else if (choice == 2) system.processOrder(std::cout);
        else if (choice == 3) system.peekIncoming(std::cout);
        else if (choice == 4) system.showQueue(std::cout);
        else if (choice == 5) system.peekCompleted(std::cout);
        else if (choice == 6) system.popCompleted(std::cout);
        else if (choice == 7) system.showStack(std::cout);
    }
    std::cout << "Session ended.\n";
}

#ifndef RESTAURANT_TEST
int main(int argc, char* argv[]) {
    if (argc == 1) { runInteractive(); return 0; }
    if (argc == 2 && std::string(argv[1]) == "--demo") {
        runDemo(std::cout); return 0;
    }
    std::cerr << "Usage: restaurant_orders [--demo]\n";
    return 1;
}
#endif
