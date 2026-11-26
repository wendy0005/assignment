/*
 * BCL1313 Algorithms & Complexity - Lab Assessment 2
 * Sorting and Searching in Inventory Management (Bakery Shop Inventory System)
 * Student: Chan Jing Yi (SUOL2500321)
 * Language: C++17
 */

#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <string>
#include <vector>

struct Product {
    std::string id;
    std::string name;
    std::string category;
    double price;
};

struct SortMetrics {
    long long comparisons = 0;
    long long movements = 0;
};

struct SearchMetrics {
    int index = -1;
    long long comparisons = 0;
};

// Returns the 10 sample bakery records from Task 1.
std::vector<Product> createSampleInventory() {
    return {
        {"BK001", "Butter Croissant",    "Pastry",  4.50},
        {"BK002", "Chocolate Cake",      "Cake",    25.00},
        {"BK003", "Garlic Bread",        "Bread",   3.80},
        {"BK004", "Red Velvet Cupcake",  "Cake",    6.50},
        {"BK005", "Cheese Tart",         "Pastry",  5.20},
        {"BK006", "Whole Wheat Loaf",    "Bread",   6.00},
        {"BK007", "Macaron Box (6 pcs)", "Cookies", 12.00},
        {"BK008", "Blueberry Muffin",    "Cake",    4.80},
        {"BK009", "Banana Bread",        "Bread",   7.50},
        {"BK010", "Oatmeal Cookies",     "Cookies", 8.00}
    };
}

// Helper to convert string to lowercase for case-insensitive search.
std::string toLowerCase(std::string text) {
    for (char& ch : text) {
        if (ch >= 'A' && ch <= 'Z') {
            ch = static_cast<char>(ch - 'A' + 'a');
        }
    }
    return text;
}

// Prints a formatted table of bakery products.
void displayInventory(const std::vector<Product>& items, const std::string& title) {
    std::cout << title << "\n";
    std::cout << std::string(64, '-') << "\n";
    std::cout << std::left
              << std::setw(10) << "Prod ID"
              << std::setw(24) << "Product Name"
              << std::setw(14) << "Category"
              << std::right << std::setw(12) << "Price (RM)" << "\n";
    std::cout << std::string(64, '-') << "\n";
    for (const auto& item : items) {
        std::cout << std::left
                  << std::setw(10) << item.id
                  << std::setw(24) << item.name
                  << std::setw(14) << item.category
                  << std::right << std::setw(12) << std::fixed << std::setprecision(2)
                  << item.price << "\n";
    }
    std::cout << std::string(64, '-') << "\n";
}

// Prints a single product's details.
void displayProductDetails(const Product& item) {
    std::cout << "  Product ID   : " << item.id << "\n"
              << "  Product Name : " << item.name << "\n"
              << "  Category     : " << item.category << "\n"
              << "  Price (RM)   : " << std::fixed << std::setprecision(2)
              << item.price << "\n";
}

/*
 * Task 2A: Insertion Sort (Ascending by Price)
 * Time Complexity: Best O(n), Average O(n^2), Worst O(n^2)
 * Space Complexity: O(1) in-place, Stable
 */
SortMetrics insertionSortByPrice(std::vector<Product>& items) {
    SortMetrics metrics;
    const std::size_t n = items.size();

    for (std::size_t i = 1; i < n; ++i) {
        Product key = items[i];
        ++metrics.movements;
        std::size_t j = i;

        while (j > 0) {
            ++metrics.comparisons;
            if (items[j - 1].price > key.price) {
                items[j] = items[j - 1];
                ++metrics.movements;
                --j;
            } else {
                break;
            }
        }
        items[j] = key;
        ++metrics.movements;
    }
    return metrics;
}

/*
 * Task 2B: Merge Sort (Ascending by Price)
 * Time Complexity: Best/Average/Worst O(n log n)
 * Space Complexity: O(n) auxiliary buffer, Stable
 */
void mergeRanges(std::vector<Product>& items, std::size_t left,
                 std::size_t mid, std::size_t right,
                 std::vector<Product>& buffer, SortMetrics& metrics) {
    std::size_t i = left;
    std::size_t j = mid + 1;
    std::size_t k = left;

    while (i <= mid && j <= right) {
        ++metrics.comparisons;
        if (items[i].price <= items[j].price) {
            buffer[k++] = items[i++];
        } else {
            buffer[k++] = items[j++];
        }
        ++metrics.movements;
    }

    while (i <= mid) {
        buffer[k++] = items[i++];
        ++metrics.movements;
    }
    while (j <= right) {
        buffer[k++] = items[j++];
        ++metrics.movements;
    }

    for (std::size_t idx = left; idx <= right; ++idx) {
        items[idx] = buffer[idx];
        ++metrics.movements;
    }
}

void mergeSortRecursive(std::vector<Product>& items, std::size_t left,
                        std::size_t right, std::vector<Product>& buffer,
                        SortMetrics& metrics) {
    if (left >= right) {
        return;
    }
    std::size_t mid = left + (right - left) / 2;
    mergeSortRecursive(items, left, mid, buffer, metrics);
    mergeSortRecursive(items, mid + 1, right, buffer, metrics);
    mergeRanges(items, left, mid, right, buffer, metrics);
}

SortMetrics mergeSortByPrice(std::vector<Product>& items) {
    SortMetrics metrics;
    if (items.size() <= 1) {
        return metrics;
    }
    std::vector<Product> buffer(items.size());
    mergeSortRecursive(items, 0, items.size() - 1, buffer, metrics);
    return metrics;
}

/*
 * Task 3A: Linear Search (by Product ID or Product Name, works on unsorted data)
 * Time Complexity: Best O(1), Average/Worst O(n)
 * Space Complexity: O(1)
 */
SearchMetrics linearSearchById(const std::vector<Product>& items,
                               const std::string& targetId) {
    SearchMetrics metrics;
    const std::string needle = toLowerCase(targetId);

    for (std::size_t i = 0; i < items.size(); ++i) {
        ++metrics.comparisons;
        if (toLowerCase(items[i].id) == needle) {
            metrics.index = static_cast<int>(i);
            return metrics;
        }
    }
    return metrics;
}

SearchMetrics linearSearchByName(const std::vector<Product>& items,
                                 const std::string& targetName) {
    SearchMetrics metrics;
    const std::string needle = toLowerCase(targetName);

    for (std::size_t i = 0; i < items.size(); ++i) {
        ++metrics.comparisons;
        if (toLowerCase(items[i].name) == needle) {
            metrics.index = static_cast<int>(i);
            return metrics;
        }
    }
    return metrics;
}

/*
 * Task 3B: Binary Search (by Price on price-sorted dataset)
 * Time Complexity: Best O(1), Average/Worst O(log n)
 * Space Complexity: O(1) iterative
 */
SearchMetrics binarySearchByPrice(const std::vector<Product>& sortedItems,
                                  double targetPrice) {
    SearchMetrics metrics;
    if (sortedItems.empty()) {
        return metrics;
    }

    const double eps = 1e-6;
    int low = 0;
    int high = static_cast<int>(sortedItems.size()) - 1;

    while (low <= high) {
        int mid = low + (high - low) / 2;
        ++metrics.comparisons;
        double diff = sortedItems[mid].price - targetPrice;

        if (std::fabs(diff) < eps) {
            metrics.index = mid;
            return metrics;
        }
        if (sortedItems[mid].price < targetPrice) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return metrics;
}

// Generates a deterministic synthetic dataset of size n for scalability analysis.
std::vector<Product> generateSyntheticInventory(std::size_t count) {
    std::vector<Product> items;
    items.reserve(count);
    const std::vector<std::string> categories = {"Bread", "Pastry", "Cake", "Cookies"};
    unsigned int seed = 20261129u;

    for (std::size_t i = 0; i < count; ++i) {
        seed = seed * 1664525u + 1013904223u;
        double price = 2.00 + static_cast<double>((seed >> 12) % 4800) / 100.0;
        std::ostringstream idStream;
        idStream << "BK" << std::setw(4) << std::setfill('0') << (i + 1);
        items.push_back({
            idStream.str(),
            "Bakery Item " + std::to_string(i + 1),
            categories[i % categories.size()],
            price
        });
    }
    return items;
}

// Runs all required demonstration tasks with clean sectioned output.
void runDemo() {
    const std::vector<Product> original = createSampleInventory();

    std::cout << "=== TASK 1: INITIAL BAKERY INVENTORY DATASET (10 ITEMS) ===\n";
    displayInventory(original, "Original Unsorted Bakery Inventory:");

    std::cout << "\n=== TASK 2A: INSERTION SORT (PRICE ASCENDING) ===\n";
    std::vector<Product> insertionSorted = original;
    SortMetrics insMetrics = insertionSortByPrice(insertionSorted);
    displayInventory(insertionSorted, "Sorted by Price (Insertion Sort):");
    std::cout << "Metrics (n = " << insertionSorted.size() << "): "
              << insMetrics.comparisons << " comparisons, "
              << insMetrics.movements << " element movements\n";

    std::cout << "\n=== TASK 2B: MERGE SORT (PRICE ASCENDING) ===\n";
    std::vector<Product> mergeSorted = original;
    SortMetrics mrgMetrics = mergeSortByPrice(mergeSorted);
    displayInventory(mergeSorted, "Sorted by Price (Merge Sort):");
    std::cout << "Metrics (n = " << mergeSorted.size() << "): "
              << mrgMetrics.comparisons << " comparisons, "
              << mrgMetrics.movements << " element movements\n";

    std::cout << "\n=== TASK 3: SEARCHING ALGORITHMS (LINEAR & BINARY SEARCH) ===\n";
    // Linear Search: Found by ID
    SearchMetrics linIdFound = linearSearchById(original, "BK007");
    std::cout << "[Linear Search by Product ID] Query: \"BK007\"\n";
    if (linIdFound.index != -1) {
        std::cout << "Status: FOUND at unsorted index " << linIdFound.index
                  << " (" << linIdFound.comparisons << " comparisons)\n";
        displayProductDetails(original[linIdFound.index]);
    } else {
        std::cout << "Status: NOT FOUND (" << linIdFound.comparisons << " comparisons)\n";
    }

    // Linear Search: Not Found by Name
    SearchMetrics linNameMiss = linearSearchByName(original, "Matcha Brownie");
    std::cout << "\n[Linear Search by Product Name] Query: \"Matcha Brownie\"\n";
    if (linNameMiss.index != -1) {
        std::cout << "Status: FOUND at unsorted index " << linNameMiss.index
                  << " (" << linNameMiss.comparisons << " comparisons)\n";
        displayProductDetails(original[linNameMiss.index]);
    } else {
        std::cout << "Status: Product \"Matcha Brownie\" not found in inventory ("
                  << linNameMiss.comparisons << " comparisons)\n";
    }

    // Binary Search: Found by Price (on Merge-Sorted inventory)
    SearchMetrics binFound = binarySearchByPrice(mergeSorted, 6.50);
    std::cout << "\n[Binary Search by Price on Sorted Inventory] Query: RM 6.50\n";
    if (binFound.index != -1) {
        std::cout << "Status: FOUND at sorted index " << binFound.index
                  << " (" << binFound.comparisons << " comparisons)\n";
        displayProductDetails(mergeSorted[binFound.index]);
    } else {
        std::cout << "Status: NOT FOUND (" << binFound.comparisons << " comparisons)\n";
    }

    // Binary Search: Not Found by Price
    SearchMetrics binMiss = binarySearchByPrice(mergeSorted, 9.90);
    std::cout << "\n[Binary Search by Price on Sorted Inventory] Query: RM 9.90\n";
    if (binMiss.index != -1) {
        std::cout << "Status: FOUND at sorted index " << binMiss.index
                  << " (" << binMiss.comparisons << " comparisons)\n";
        displayProductDetails(mergeSorted[binMiss.index]);
    } else {
        std::cout << "Status: No product priced at RM 9.90 found in inventory ("
                  << binMiss.comparisons << " comparisons)\n";
    }

    std::cout << "\n=== TASK 4: SCALABILITY BENCHMARK (n = 10 vs n = 1,000) ===\n";
    std::vector<Product> largeA = generateSyntheticInventory(1000);
    std::vector<Product> largeB = largeA;
    SortMetrics largeIns = insertionSortByPrice(largeA);
    SortMetrics largeMrg = mergeSortByPrice(largeB);

    // Search for an absent price/ID in 1,000 items (worst-case search comparison)
    SearchMetrics largeLinWorst = linearSearchById(largeB, "BK9999");
    SearchMetrics largeBinWorst = binarySearchByPrice(largeB, 999.99);

    std::cout << "Sorting Comparison (Price Ascending):\n"
              << "  n =    10 | Insertion Sort: " << std::setw(8) << insMetrics.comparisons
              << " comparisons | Merge Sort: " << std::setw(6) << mrgMetrics.comparisons << " comparisons\n"
              << "  n = 1,000 | Insertion Sort: " << std::setw(8) << largeIns.comparisons
              << " comparisons | Merge Sort: " << std::setw(6) << largeMrg.comparisons << " comparisons\n\n"
              << "Worst-Case Search Comparison (Absent Target):\n"
              << "  n =    10 | Linear Search:  " << std::setw(8) << linNameMiss.comparisons
              << " comparisons | Binary Search: " << std::setw(3) << binMiss.comparisons << " comparisons\n"
              << "  n = 1,000 | Linear Search:  " << std::setw(8) << largeLinWorst.comparisons
              << " comparisons | Binary Search: " << std::setw(3) << largeBinWorst.comparisons << " comparisons\n";
}

// Interactive console menu for manual testing.
void runInteractive() {
    std::vector<Product> inventory = createSampleInventory();
    bool sortedByPrice = false;
    int choice = -1;

    while (choice != 0) {
        std::cout << "\n--- Bakery Shop Inventory System ---\n"
                  << "1. Display Current Inventory\n"
                  << "2. Sort by Price (Insertion Sort)\n"
                  << "3. Sort by Price (Merge Sort)\n"
                  << "4. Linear Search by Product ID\n"
                  << "5. Binary Search by Price (RM)\n"
                  << "0. Exit\n"
                  << "Select option: ";

        if (!(std::cin >> choice)) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "Invalid input. Please enter a number.\n";
            continue;
        }
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        if (choice == 1) {
            displayInventory(inventory, "Current Bakery Inventory:");
        } else if (choice == 2) {
            SortMetrics m = insertionSortByPrice(inventory);
            sortedByPrice = true;
            displayInventory(inventory, "Sorted by Price (Insertion Sort):");
            std::cout << "Comparisons: " << m.comparisons << ", Movements: " << m.movements << "\n";
        } else if (choice == 3) {
            SortMetrics m = mergeSortByPrice(inventory);
            sortedByPrice = true;
            displayInventory(inventory, "Sorted by Price (Merge Sort):");
            std::cout << "Comparisons: " << m.comparisons << ", Movements: " << m.movements << "\n";
        } else if (choice == 4) {
            std::string target;
            std::cout << "Enter Product ID (e.g., BK007): ";
            std::getline(std::cin, target);
            SearchMetrics m = linearSearchById(inventory, target);
            if (m.index != -1) {
                std::cout << "Found (" << m.comparisons << " comparisons):\n";
                displayProductDetails(inventory[m.index]);
            } else {
                std::cout << "Product \"" << target << "\" not found (" << m.comparisons << " comparisons).\n";
            }
        } else if (choice == 5) {
            if (!sortedByPrice) {
                std::cout << "Inventory is not yet sorted by price; running Merge Sort first...\n";
                mergeSortByPrice(inventory);
                sortedByPrice = true;
            }
            double price = 0.0;
            std::cout << "Enter exact price in RM (e.g., 6.50): ";
            if (std::cin >> price) {
                SearchMetrics m = binarySearchByPrice(inventory, price);
                if (m.index != -1) {
                    std::cout << "Found (" << m.comparisons << " comparisons):\n";
                    displayProductDetails(inventory[m.index]);
                } else {
                    std::cout << "No product found at RM " << std::fixed << std::setprecision(2)
                              << price << " (" << m.comparisons << " comparisons).\n";
                }
            }
        } else if (choice != 0) {
            std::cout << "Unknown option.\n";
        }
    }
}

#ifndef BAKERY_TEST_BUILD
int main(int argc, char* argv[]) {
    if (argc > 1 && std::string(argv[1]) == "--interactive") {
        runInteractive();
    } else {
        runDemo();
    }
    return 0;
}
#endif
