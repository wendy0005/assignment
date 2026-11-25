// Regression tests for state preservation, ordering and boundary cases.
#define RESTAURANT_TEST
#include "restaurant_orders.cpp"
#include <cassert>

Order numbered(int number) {
    return {"T" + std::to_string(number), "Test", "Rice", 1};
}

int main() {
    Order removed;
    OrderQueue queue;
    assert(queue.empty() && queue.front() == nullptr);
    assert(!queue.dequeue(removed));
    queue.enqueue(numbered(1));
    queue.enqueue(numbered(2));
    assert(queue.front()->id == "T1" && queue.size() == 2);
    assert(queue.dequeue(removed) && removed.id == "T1");
    assert(queue.dequeue(removed) && removed.id == "T2");
    assert(queue.empty());
    std::cout << "PASS 1: Queue FIFO, nonmutating Peek, empty Dequeue.\n";

    // Repeat more than one full cycle to catch circular indexing mistakes.
    for (int round = 0; round < 3; ++round) {
        for (int i = 0; i < static_cast<int>(CAPACITY); ++i)
            assert(queue.enqueue(numbered(i)));
        assert(queue.full() && !queue.enqueue(numbered(99)));
        assert(queue.size() == CAPACITY);
        for (int i = 0; i < static_cast<int>(CAPACITY); ++i) {
            assert(queue.dequeue(removed));
            assert(removed.id == "T" + std::to_string(i));
        }
    }
    // Partial drain then refill ensures wraparound preserves live items.
    for (int i = 0; i < 10; ++i) assert(queue.enqueue(numbered(i)));
    for (int i = 0; i < 4; ++i) assert(queue.dequeue(removed));
    for (int i = 10; i < 14; ++i) assert(queue.enqueue(numbered(i)));
    for (int i = 4; i < 14; ++i) {
        assert(queue.dequeue(removed));
        assert(removed.id == "T" + std::to_string(i));
    }
    std::cout << "PASS 2: Queue capacity, repeated reuse and partial wraparound.\n";

    OrderStack stack;
    assert(stack.peek() == nullptr && !stack.pop(removed));
    for (int i = 0; i < 10; ++i) assert(stack.push(numbered(i)));
    assert(stack.full() && !stack.push(numbered(99)));
    assert(stack.peek()->id == "T9" && stack.size() == 10);
    for (int i = 9; i >= 0; --i) {
        assert(stack.pop(removed));
        assert(removed.id == "T" + std::to_string(i));
    }
    assert(stack.empty() && stack.push(numbered(20)));
    std::cout << "PASS 3: Stack LIFO, Peek, overflow, underflow and reuse.\n";

    std::ostringstream log;
    RestaurantSystem system;
    assert(!system.processOrder(log) && !system.popCompleted(log));
    system.peekIncoming(log); system.peekCompleted(log);
    for (int i = 0; i < 5; ++i) assert(system.addOrder(SAMPLE_ORDERS[i], log));
    for (int i = 0; i < 3; ++i) {
        assert(system.processOrder(log));
        assert(system.latestOrder()->id == SAMPLE_ORDERS[i].id);
        assert(system.latestOrder()->customer == SAMPLE_ORDERS[i].customer);
        assert(system.latestOrder()->food == SAMPLE_ORDERS[i].food);
        assert(system.latestOrder()->quantity == SAMPLE_ORDERS[i].quantity);
    }
    assert(system.addOrder(SAMPLE_ORDERS[5], log));
    assert(system.pendingCount() == 3 && system.completedCount() == 3);
    assert(system.nextOrder()->id == "ORD004");
    assert(system.popCompleted(log));
    assert(system.latestOrder()->id == "ORD002");
    assert(system.pendingCount() == 3 && system.completedCount() == 2);
    std::cout << "PASS 4: Automatic transfer preserves every field; Pop leaves queue unchanged.\n";

    RestaurantSystem blocked;
    for (int i = 0; i < 10; ++i) {
        assert(blocked.addOrder(numbered(i), log));
        assert(blocked.processOrder(log));
    }
    assert(blocked.addOrder(numbered(10), log));
    assert(!blocked.processOrder(log));
    assert(blocked.pendingCount() == 1 && blocked.nextOrder()->id == "T10");
    assert(blocked.completedCount() == 10);
    assert(blocked.popCompleted(log) && blocked.processOrder(log));
    assert(blocked.pendingCount() == 0 && blocked.latestOrder()->id == "T10");
    std::cout << "PASS 5: Full completed stack retains pending order; retry succeeds after Pop.\n";

    assert(!blocked.addOrder({"T11", "Test", "Rice", 0}, log));
    assert(!blocked.addOrder({"T11", "", "Rice", 1}, log));
    int value = 0;
    assert(!parseInteger("2abc", value) && !parseInteger("1.5", value));
    assert(!parseInteger("999999999999999999999", value));
    assert(!parseInteger("", value) && parseInteger(" 2 ", value) && value == 2);
    std::cout << "PASS 6: Invalid fields and malformed integers rejected.\n";

    std::ostringstream actual;
    runDemo(actual);
    const auto text = actual.str();
    assert(text.find("Final counts: pending = 3, completed = 2, popped = 1") != std::string::npos);
    assert(text.find("Popped ORD003") != std::string::npos);
    std::cout << "PASS 7: Assessment demonstration reaches expected final state.\n";
    std::cout << "All seven C++ test groups passed.\n";
}
