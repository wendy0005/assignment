/*
 * Automated unit tests for Bakery Shop Inventory System (BCL1313 Lab Assessment 2)
 */
#define BAKERY_TEST_BUILD
#include "bakery_inventory.cpp"
#include <cassert>

void assertSortedAscending(const std::vector<Product>& items) {
    for (std::size_t i = 1; i < items.size(); ++i) {
        assert(items[i - 1].price <= items[i].price);
    }
}

int main() {
    // 1. Sample dataset has 10 items
    std::vector<Product> base = createSampleInventory();
    assert(base.size() == 10);

    // 2. Insertion Sort produces ascending price order
    std::vector<Product> ins = base;
    SortMetrics insM = insertionSortByPrice(ins);
    assertSortedAscending(ins);
    assert(ins.front().id == "BK003"); // RM 3.80
    assert(ins.back().id == "BK002");  // RM 25.00
    assert(insM.comparisons > 0);

    // 3. Merge Sort produces identical sorted order as Insertion Sort
    std::vector<Product> mrg = base;
    SortMetrics mrgM = mergeSortByPrice(mrg);
    assertSortedAscending(mrg);
    assert(mrgM.comparisons > 0);
    for (std::size_t i = 0; i < base.size(); ++i) {
        assert(ins[i].id == mrg[i].id);
        assert(ins[i].price == mrg[i].price);
    }

    // 4. Stability check on duplicate prices
    std::vector<Product> dup = {
        {"BK101", "Item A", "Bread", 5.00},
        {"BK102", "Item B", "Cake",  3.00},
        {"BK103", "Item C", "Bread", 5.00}
    };
    std::vector<Product> dupIns = dup;
    std::vector<Product> dupMrg = dup;
    insertionSortByPrice(dupIns);
    mergeSortByPrice(dupMrg);
    assert(dupIns[1].id == "BK101" && dupIns[2].id == "BK103");
    assert(dupMrg[1].id == "BK101" && dupMrg[2].id == "BK103");

    // 5. Linear Search (found, case-insensitive, and not found)
    SearchMetrics l1 = linearSearchById(base, "bk007");
    assert(l1.index == 6 && base[l1.index].name == "Macaron Box (6 pcs)");
    SearchMetrics l2 = linearSearchByName(base, "Garlic Bread");
    assert(l2.index == 2);
    SearchMetrics l3 = linearSearchById(base, "BK999");
    assert(l3.index == -1 && l3.comparisons == 10);

    // 6. Binary Search (min, middle, max, and absent)
    SearchMetrics bMin = binarySearchByPrice(mrg, 3.80);
    assert(bMin.index == 0 && mrg[bMin.index].id == "BK003");
    SearchMetrics bMid = binarySearchByPrice(mrg, 6.50);
    assert(bMid.index != -1 && mrg[bMid.index].id == "BK004");
    SearchMetrics bMax = binarySearchByPrice(mrg, 25.00);
    assert(bMax.index == 9 && mrg[bMax.index].id == "BK002");
    SearchMetrics bMiss = binarySearchByPrice(mrg, 9.90);
    assert(bMiss.index == -1 && bMiss.comparisons <= 4);

    // 7. Empty & single-item edge cases
    std::vector<Product> emptyVec;
    insertionSortByPrice(emptyVec);
    mergeSortByPrice(emptyVec);
    assert(binarySearchByPrice(emptyVec, 5.00).index == -1);
    assert(linearSearchById(emptyVec, "BK001").index == -1);

    std::cout << "ALL 7 TEST SUITES PASSED SUCCESSFULLY.\n";
    return 0;
}
