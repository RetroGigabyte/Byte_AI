#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <sstream>
#include <cctype>
#include <cmath>
#include <filesystem>
#include <random>
#include <chrono>
#include <iomanip>
#include <ctime>
#include <thread>
#include <mutex>
#include <queue>
#include <set>

using namespace std;
namespace fs = std::filesystem;

class KnowledgeBot {
private:
    map<string, vector<string>> knowledge;  // category -> sentences
    mutex knowledgeMutex;  // Thread-safe access to knowledge map
    int totalLines = 0;
    string lastCategory = "";
    int lastIndex = 0;  // Track which sentences we've already shown

    // FEATURE 9: Query History
    vector<string> queryHistory;
    const int MAX_HISTORY = 50;  // Store last 50 queries

    // FEATURE 12: Holiday Calendar
    map<string, string> holidays = {
        {"01-01", "New Year's Day"},
        {"01-20", "MLK Jr. Birthday"},
        {"02-14", "Valentine's Day"},
        {"02-18", "Presidents' Day"},
        {"03-17", "St. Patrick's Day"},
        {"04-22", "Earth Day"},
        {"05-26", "Memorial Day"},
        {"07-04", "Independence Day"},
        {"09-01", "Labor Day"},
        {"10-31", "Halloween"},
        {"11-11", "Veterans Day"},
        {"11-28", "Thanksgiving"},
        {"12-25", "Christmas"},
        {"12-31", "New Year's Eve"}
    };
    
    // Trim whitespace
    string trim(const string& str) {
        size_t first = str.find_first_not_of(" \t\r\n");
        if (first == string::npos) return "";
        size_t last = str.find_last_not_of(" \t\r\n");
        return str.substr(first, last - first + 1);
    }
    
    // Convert to lowercase
    string toLower(const string& str) {
        string result = str;
        transform(result.begin(), result.end(), result.begin(), ::tolower);
        return result;
    }
    
    // Split string by delimiter
    vector<string> split(const string& str, char delimiter) {
        vector<string> tokens;
        stringstream ss(str);
        string token;
        while (getline(ss, token, delimiter)) {
            token = trim(token);
            if (!token.empty()) {
                tokens.push_back(token);
            }
        }
        return tokens;
    }
    
public:
    // Extract zip files to temporary directory
    void extractZipFile(const string& zipPath) {
        string tempDir = "training/.temp_extract";

        // Create temp directory
        try {
            fs::create_directories(tempDir);
        } catch (const exception& e) {
            cerr << "⚠️  Could not create temp directory: " << e.what() << "\n";
            return;
        }

        // Use system unzip command
        string command = "unzip -q -o \"" + zipPath + "\" -d \"" + tempDir + "\" 2>/dev/null";
        int result = system(command.c_str());

        if (result == 0) {
            cout << "📦 Extracting " << fs::path(zipPath).filename().string() << "...\n";
            // Load all .txt files from extracted directory
            loadTrainingDataRecursive(tempDir);
        } else {
            cerr << "⚠️  Failed to extract " << zipPath << " (unzip not available or invalid file)\n";
        }
    }

    void loadTrainingDataRecursive(const string& folder) {
        if (!fs::exists(folder)) {
            return;
        }

        try {
            // Recursively collect all .txt files (excluding .temp_extract and zips)
            vector<string> files;
            for (const auto& entry : fs::recursive_directory_iterator(folder)) {
                // Skip temp extraction folder
                string pathStr = entry.path().string();
                if (pathStr.find(".temp_extract") != string::npos) continue;
                if (pathStr.find("__MACOSX") != string::npos) continue;

                if (entry.is_regular_file() && entry.path().extension() == ".txt") {
                    files.push_back(pathStr);
                }
            }

            // Load files with multiple threads
            const int NUM_THREADS = 4;  // Use 4 threads
            vector<thread> threads;
            size_t filesPerThread = (files.size() + NUM_THREADS - 1) / NUM_THREADS;

            for (int t = 0; t < NUM_THREADS && t * filesPerThread < files.size(); t++) {
                threads.emplace_back([this, &files, t, filesPerThread]() {
                    size_t start = t * filesPerThread;
                    size_t end = min(start + filesPerThread, files.size());
                    for (size_t i = start; i < end; i++) {
                        loadFile(files[i]);
                    }
                });
            }

            // Wait for all threads
            for (auto& t : threads) {
                t.join();
            }

        } catch (const exception& e) {
            cerr << "Error reading " << folder << ": " << e.what() << "\n";
        }
    }


    void loadTrainingData() {
        cout << "📚 Loading training data...\n\n";

        vector<string> folders = {"training", "Wiki"};

        for (const auto& folder : folders) {
            if (!fs::exists(folder)) {
                cout << "⚠️  " << folder << "/ folder not found\n";
                continue;
            }

            // Extract all zips first
            try {
                for (const auto& entry : fs::directory_iterator(folder)) {
                    if (entry.is_regular_file() && entry.path().extension() == ".zip") {
                        extractZipFile(entry.path().string());
                    }
                }
            } catch (const exception& e) {
                cerr << "Error processing zips: " << e.what() << "\n";
            }

            cout << "📂 Scanning " << folder << "/ recursively with multi-threading...\n";
            loadTrainingDataRecursive(folder);
        }

        cout << "\n✓ Total training lines loaded: " << totalLines << "\n";
        cout << "✓ Categories: " << knowledge.size() << "\n\n";
    }

public:
    // Public methods for main
    void cleanupTempFiles() {
        try {
            string tempDir = "training/.temp_extract";
            if (fs::exists(tempDir)) {
                fs::remove_all(tempDir);
            }
        } catch (const exception& e) {
            // Silent cleanup failure
        }
    }

    void loadTrainingDataPublic() {
        loadTrainingData();
    }

    void chatPublic() {
        chat();
    }

private:
    
    void loadFile(const string& filepath) {
        ifstream file(filepath);
        if (!file.is_open()) {
            return;
        }

        string line;
        int lineCount = 0;

        while (getline(file, line)) {
            line = trim(line);

            if (line.empty() || line[0] == '#') continue;

            // Parse "category: text"
            size_t colonPos = line.find(':');
            if (colonPos == string::npos) continue;

            string category = line.substr(0, colonPos);
            string text = line.substr(colonPos + 1);

            category = trim(category);
            text = trim(text);

            // Skip corrupted categories (all numbers, weird symbols)
            if (category.empty() || category.length() > 50) continue;
            bool hasLetters = false;
            for (char c : category) {
                if (isalpha(c)) {
                    hasLetters = true;
                    break;
                }
            }
            if (!hasLetters) continue;  // Skip if no letters (pure numbers)

            if (!text.empty()) {
                {
                    lock_guard<mutex> lock(knowledgeMutex);
                    knowledge[category].push_back(text);
                    totalLines++;
                }
                lineCount++;
            }
        }

        file.close();
    }

    void loadFileThreaded(const string& filepath, vector<pair<string, string>>& fileData) {
        ifstream file(filepath);
        if (!file.is_open()) return;

        string line;
        while (getline(file, line)) {
            line = trim(line);
            if (line.empty() || line[0] == '#') continue;

            size_t colonPos = line.find(':');
            if (colonPos == string::npos) continue;

            string category = line.substr(0, colonPos);
            string text = line.substr(colonPos + 1);
            category = trim(category);
            text = trim(text);

            // Skip corrupted categories
            if (category.empty() || category.length() > 50) continue;
            bool hasLetters = false;
            for (char c : category) {
                if (isalpha(c)) {
                    hasLetters = true;
                    break;
                }
            }
            if (!hasLetters) continue;  // Skip if no letters

            if (!text.empty()) {
                fileData.push_back({category, text});
            }
        }
        file.close();
    }
    
    void printCategories() {
        cout << "\nCategories available:\n";
        int count = 0;
        for (const auto& pair : knowledge) {
            cout << "  • " << pair.first << ": " << pair.second.size() << " sentences\n";
            count++;
            if (count >= 20) {
                cout << "  ... and " << (knowledge.size() - 20) << " more!\n";
                break;
            }
        }
    }
    
    string findBestCategory(const string& query) {
        string queryLower = toLower(query);
        vector<string> queryWords = split(queryLower, ' ');
        
        // Check for math expressions
        if (query.find('^') != string::npos || 
            query.find('+') != string::npos || 
            query.find('-') != string::npos ||
            query.find('*') != string::npos ||
            query.find('/') != string::npos) {
            // Check if math category exists
            if (knowledge.find("math") != knowledge.end()) {
                return "math";
            }
        }
        
        // Check for common greetings (but NOT question words like "what")
        vector<string> greetings = {"hello", "hi", "hey", "sup", "yo"};
        for (const auto& greeting : greetings) {
            for (const auto& word : queryWords) {
                if (word == greeting) {
                    // Look for greeting category
                    if (knowledge.find("greeting") != knowledge.end()) {
                        lastCategory = "greeting";
                        return "greeting";
                    }
                    // Don't return empty - continue searching for other matches
                    break;
                }
            }
        }
        
        string bestCategory;
        int bestScore = 0;
        int bestLength = 999;
        
        // Score each category based on word matches
        for (const auto& pair : knowledge) {
            string categoryLower = toLower(pair.first);
            vector<string> categoryWords = split(categoryLower, '_');
            
            int score = 0;
            
            // Simple exact and substring matching
            for (const auto& qWord : queryWords) {
                if (qWord.length() >= 2) {
                    for (const auto& catWord : categoryWords) {
                        // Exact word match (highest priority)
                        if (qWord == catWord) {
                            score += 10;
                        } 
                        // Substring match for longer words
                        else if (qWord.length() > 3 && catWord.find(qWord) != string::npos) {
                            score += 1;
                        }
                    }
                }
            }
            
            // Prefer shorter, more specific category names
            if (score > bestScore || 
                (score == bestScore && score > 0 && pair.first.length() < bestLength)) {
                bestScore = score;
                bestCategory = pair.first;
                bestLength = pair.first.length();
            }
        }
        
        // Only return if we have a decent match (score > 0)
        if (bestScore > 0) {
            return bestCategory;
        }
        
        return "";
    }
    
    vector<string> findRelevantSentences(const string& category, const string& query) {
        if (knowledge.find(category) == knowledge.end()) {
            return vector<string>();
        }
        
        const auto& sentences = knowledge[category];
        vector<pair<string, int>> scored;
        
        string queryLower = toLower(query);
        vector<string> queryWords = split(queryLower, ' ');
        
        // Score sentences based on word matches
        for (const auto& sentence : sentences) {
            string sentenceLower = toLower(sentence);
            int score = 0;
            
            for (const auto& word : queryWords) {
                if (word.length() > 2 && sentenceLower.find(word) != string::npos) {
                    score++;
                }
            }
            
            scored.push_back({sentence, score});
        }
        
        // Sort by score (highest first)
        sort(scored.begin(), scored.end(), 
             [](const auto& a, const auto& b) { return a.second > b.second; });
        
        // Return top 3 sentences
        vector<string> result;
        for (size_t i = 0; i < min(size_t(3), scored.size()); i++) {
            if (scored[i].second > 0 || i == 0) {  // Always return at least 1
                result.push_back(scored[i].first);
            }
        }
        
        // If no scored matches, return 3 random
        if (result.empty()) {
            random_device rd;
            mt19937 g(rd());
            
            vector<string> temp(sentences);
            shuffle(temp.begin(), temp.end(), g);
            
            for (size_t i = 0; i < min(size_t(3), temp.size()); i++) {
                result.push_back(temp[i]);
            }
        }
        
        lastIndex = 3;  // Remember we showed 3 sentences
        return result;
    }
    
    vector<string> getMoreSentences(const string& category, int& startIndex) {
        if (knowledge.find(category) == knowledge.end()) {
            return vector<string>();
        }

        const auto& sentences = knowledge[category];
        vector<string> result;

        // Return next 5 sentences starting from lastIndex
        for (size_t i = startIndex; i < min(startIndex + 5, (int)sentences.size()); i++) {
            result.push_back(sentences[i]);
        }

        lastIndex = startIndex + result.size();
        return result;
    }

    // ============================================
    // TIME/DATE FUNCTIONS (NTP Integration)
    // ============================================

    string getCurrentDateTime() {
        auto now = chrono::system_clock::now();
        auto time_t_now = chrono::system_clock::to_time_t(now);
        struct tm* timeinfo = localtime(&time_t_now);

        ostringstream oss;
        oss << put_time(timeinfo, "%A, %B %d, %Y at %I:%M %p");
        return oss.str();
    }

    string getCurrentDateISO() {
        auto now = chrono::system_clock::now();
        auto time_t_now = chrono::system_clock::to_time_t(now);
        struct tm* timeinfo = gmtime(&time_t_now);

        ostringstream oss;
        oss << put_time(timeinfo, "%Y-%m-%d %H:%M:%S");
        return oss.str();
    }

    string getCurrentDateShort() {
        auto now = chrono::system_clock::now();
        auto time_t_now = chrono::system_clock::to_time_t(now);
        struct tm* timeinfo = localtime(&time_t_now);

        ostringstream oss;
        oss << put_time(timeinfo, "%A, %B %d, %Y");
        return oss.str();
    }

    long long getUnixTimestamp() {
        auto now = chrono::system_clock::now();
        return chrono::system_clock::to_time_t(now);
    }

    bool isTimeQuery(const string& query) {
        string queryLower = toLower(query);

        // REJECT if clearly historical/context query
        vector<string> historyKeywords = {
            "what was", "what did", "what happened", "when did",
            "during", "in", "at the time", "back then",
            "history of", "describe", "explain", "tell me about"
        };

        // Check if this is a "what was X doing in YEAR" pattern
        if ((queryLower.find("what was") != string::npos ||
             queryLower.find("what did") != string::npos) &&
            (queryLower.find("doing") != string::npos ||
             queryLower.find("in") != string::npos)) {
            return false;  // This is historical, not time
        }

        // Reject "during X period" historical queries
        if (queryLower.find("during") != string::npos) {
            return false;
        }

        vector<string> timeKeywords = {
            "time", "date", "what time", "current time", "what's the time",
            "today", "tomorrow", "yesterday", "when", "clock",
            "hour", "minute", "second", "day of the week",
            "timestamp", "iso", "utc", "timezone",
            "one day from now", "days from now", "hours from now",
            "one day ago", "days ago", "hours ago",
            "in one day", "in how many days", "how many days",
            "week", "weeks", "month", "months", "year", "years",
            "decade", "decades", "minutes", "seconds",
            "from now", "ago", "in ",
            "timezone", "convert", "business day", "leap year",
            "day of week", "recurring", "age", "born",
            "days between", "how old", "monday", "tuesday",
            "wednesday", "thursday", "friday", "saturday", "sunday",
            "holiday", "holidays", "clear history"
        };

        for (const auto& keyword : timeKeywords) {
            if (queryLower.find(keyword) != string::npos) {
                return true;
            }
        }
        return false;
    }

    // Helper: Extract number from query string
    int extractNumber(const string& query) {
        string digits;
        for (char c : query) {
            if (isdigit(c)) {
                digits += c;
            }
        }
        if (digits.empty()) {
            // Check for word numbers
            if (query.find("one") != string::npos) return 1;
            if (query.find("two") != string::npos) return 2;
            if (query.find("three") != string::npos) return 3;
            if (query.find("four") != string::npos) return 4;
            if (query.find("five") != string::npos) return 5;
            if (query.find("six") != string::npos) return 6;
            if (query.find("seven") != string::npos) return 7;
            if (query.find("eight") != string::npos) return 8;
            if (query.find("nine") != string::npos) return 9;
            if (query.find("ten") != string::npos) return 10;
            return -1;
        }
        return stoi(digits);
    }

    // Helper: Format time with label
    string formatTimeWithLabel(const string& label, const chrono::system_clock::time_point& tp, bool includeTime = true) {
        auto time_t_val = chrono::system_clock::to_time_t(tp);
        struct tm* timeinfo = localtime(&time_t_val);

        ostringstream oss;
        if (includeTime) {
            oss << label << ": " << put_time(timeinfo, "%A, %B %d, %Y at %I:%M %p");
        } else {
            oss << label << ": " << put_time(timeinfo, "%A, %B %d, %Y");
        }
        return oss.str();
    }

    // Feature 1: Timezone Conversion (EST, CST, PST, UTC, GMT)
    map<string, int> timezoneOffsets = {
        {"utc", 0}, {"gmt", 0},
        {"est", -5}, {"edt", -4},  // Eastern
        {"cst", -6}, {"cdt", -5},  // Central
        {"mst", -7}, {"mdt", -6},  // Mountain
        {"pst", -8}, {"pdt", -7},  // Pacific
        {"akst", -9}, {"akdt", -8}, // Alaska
        {"hst", -10}, // Hawaii
        {"bst", 1}, // British
        {"cet", 1}, {"cest", 2},  // Central Europe
        {"eet", 2}, {"eest", 3},  // Eastern Europe
        {"ist", 5}, {"ist", 9},   // India/Japan
        {"jst", 9},              // Japan
        {"cst", 8},              // China
        {"aest", 10}, {"aedt", 11}, // Australia
    };

    string convertTimezone(int fromOffset, int toOffset, const string& timeStr) {
        ostringstream oss;
        int hourDiff = toOffset - fromOffset;
        if (hourDiff > 0) {
            oss << timeStr << " → +" << hourDiff << " hours";
        } else if (hourDiff < 0) {
            oss << timeStr << " → " << hourDiff << " hours";
        } else {
            oss << timeStr << " (same timezone)";
        }
        return oss.str();
    }

    // Feature 3: Check if leap year
    bool isLeapYear(int year) {
        return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
    }

    // Feature 3: Get day of week
    string getDayOfWeek(const chrono::system_clock::time_point& tp) {
        auto time_t_val = chrono::system_clock::to_time_t(tp);
        struct tm* timeinfo = localtime(&time_t_val);
        ostringstream oss;
        oss << put_time(timeinfo, "%A");
        return oss.str();
    }

    // Feature 2: Calculate business days (skip weekends)
    chrono::system_clock::time_point addBusinessDays(const chrono::system_clock::time_point& start, int businessDays) {
        auto current = start;
        int added = 0;

        while (added < businessDays) {
            current = current + chrono::hours(24);
            auto time_t_val = chrono::system_clock::to_time_t(current);
            struct tm* timeinfo = localtime(&time_t_val);
            int dayOfWeek = timeinfo->tm_wday;  // 0=Sunday, 6=Saturday

            // Skip weekends
            if (dayOfWeek != 0 && dayOfWeek != 6) {
                added++;
            }
        }
        return current;
    }

    // Feature 5: Calculate age
    string calculateAge(int birthYear, int birthMonth, int birthDay) {
        auto now = chrono::system_clock::now();
        auto time_t_now = chrono::system_clock::to_time_t(now);
        struct tm* timeinfo = localtime(&time_t_now);

        int currentYear = timeinfo->tm_year + 1900;
        int currentMonth = timeinfo->tm_mon + 1;
        int currentDay = timeinfo->tm_mday;

        int age = currentYear - birthYear;
        if (currentMonth < birthMonth || (currentMonth == birthMonth && currentDay < birthDay)) {
            age--;
        }

        ostringstream oss;
        oss << "Age: " << age << " years";
        return oss.str();
    }

    // Feature 5: Days between two dates
    string daysBetween(int year1, int month1, int day1, int year2, int month2, int day2) {
        struct tm tm1 = {0}, tm2 = {0};
        tm1.tm_year = year1 - 1900;
        tm1.tm_mon = month1 - 1;
        tm1.tm_mday = day1;
        tm1.tm_hour = 12;

        tm2.tm_year = year2 - 1900;
        tm2.tm_mon = month2 - 1;
        tm2.tm_mday = day2;
        tm2.tm_hour = 12;

        time_t t1 = mktime(&tm1);
        time_t t2 = mktime(&tm2);

        long diffSeconds = labs(t2 - t1);
        long days = diffSeconds / (24 * 3600);

        ostringstream oss;
        oss << "Days between: " << days << " days";
        return oss.str();
    }

    // Feature 4: Generate recurring events
    string generateRecurring(const string& interval, int count) {
        auto now = chrono::system_clock::now();
        ostringstream oss;
        oss << "Recurring events (" << interval << "):\n";

        for (int i = 1; i <= count && i <= 5; i++) {  // Max 5 events shown
            auto tp = now;

            if (interval.find("day") != string::npos) {
                tp = now + chrono::hours(24 * i);
            } else if (interval.find("week") != string::npos) {
                tp = now + chrono::hours(24 * 7 * i);
            } else if (interval.find("month") != string::npos) {
                tp = now + chrono::hours(24 * 30 * i);
            }

            auto time_t_val = chrono::system_clock::to_time_t(tp);
            struct tm* timeinfo = localtime(&time_t_val);

            oss << "  " << i << ". " << put_time(timeinfo, "%A, %B %d, %Y");
            if (i < count && i < 5) oss << "\n";
        }

        return oss.str();
    }

    // FEATURE 9: Add query to history
    void addToHistory(const string& query) {
        queryHistory.push_back(query);
        if (queryHistory.size() > MAX_HISTORY) {
            queryHistory.erase(queryHistory.begin());
        }
    }

    // FEATURE 9: Get query history
    string getQueryHistory(int count = 10) {
        if (queryHistory.empty()) {
            return "No query history yet";
        }

        ostringstream oss;
        oss << "Query History (last " << count << "):\n";

        int start = max(0, (int)queryHistory.size() - count);
        for (size_t i = start; i < queryHistory.size(); i++) {
            oss << "  " << (i - start + 1) << ". " << queryHistory[i] << "\n";
        }

        return oss.str();
    }

    // FEATURE 9: Clear history
    void clearHistory() {
        queryHistory.clear();
    }

    // FEATURE 12: Check if date is a holiday
    string checkHoliday(int month, int day) {
        ostringstream dateKey;
        dateKey << setfill('0') << setw(2) << month << "-" << setw(2) << day;
        string key = dateKey.str();

        auto it = holidays.find(key);
        if (it != holidays.end()) {
            return it->second;
        }
        return "";
    }

    // FEATURE 12: Get holiday info
    string getHolidayInfo() {
        ostringstream oss;
        oss << "Holidays 2026:\n";
        int count = 0;
        for (const auto& holiday : holidays) {
            if (count >= 10) {
                oss << "  ... and more\n";
                break;
            }
            oss << "  • " << holiday.second << " (" << holiday.first << ")\n";
            count++;
        }
        return oss.str();
    }

    // FEATURE 12: Check if date is a holiday
    bool isHoliday(const chrono::system_clock::time_point& tp) {
        auto time_t_val = chrono::system_clock::to_time_t(tp);
        struct tm* timeinfo = localtime(&time_t_val);
        int month = timeinfo->tm_mon + 1;
        int day = timeinfo->tm_mday;

        return !checkHoliday(month, day).empty();
    }

    vector<string> handleTimeQuery(const string& query) {
        vector<string> result;
        string queryLower = toLower(query);
        auto now = chrono::system_clock::now();

        // FEATURE 2: BUSINESS DAYS (check EARLY, before generic day patterns)
        if (queryLower.find("business day") != string::npos) {
            int num = extractNumber(queryLower);
            if (num <= 0) num = 5;

            bool isFuture = (queryLower.find("from now") != string::npos || queryLower.find("in ") != string::npos);
            auto businessDate = isFuture ? addBusinessDays(now, num) : now;

            string label = isFuture ?
                (to_string(num) + " business day" + (num > 1 ? "s" : "") + " from now") :
                (to_string(num) + " business day" + (num > 1 ? "s" : "") + " ago");

            result.push_back(formatTimeWithLabel(label, businessDate, false));
            return result;
        }

        // FEATURE 4: RECURRING EVENTS (check EARLY)
        if (queryLower.find("recurring") != string::npos ||
            (queryLower.find("every") != string::npos && queryLower.find("time") == string::npos)) {
            string interval = "week";
            if (queryLower.find("day") != string::npos) interval = "day";
            if (queryLower.find("month") != string::npos) interval = "month";

            int count = extractNumber(queryLower);
            if (count <= 0) count = 3;

            result.push_back(generateRecurring(interval, count));
            return result;
        }

        // FEATURE 6: LEAP YEAR (check early to avoid confusion with years)
        if (queryLower.find("leap year") != string::npos) {
            int year = extractNumber(queryLower);
            if (year <= 0) {
                auto time_t_now = chrono::system_clock::to_time_t(now);
                struct tm* timeinfo = localtime(&time_t_now);
                year = timeinfo->tm_year + 1900;
            }

            bool isLeap = isLeapYear(year);
            ostringstream oss;
            oss << year << " is " << (isLeap ? "a leap year" : "not a leap year");
            result.push_back(oss.str());
            return result;
        }

        // FEATURE 5: AGE CALCULATOR (check early)
        if ((queryLower.find("how old") != string::npos && queryLower.find("born") != string::npos) ||
            (queryLower.find("age") != string::npos && queryLower.find("born") != string::npos)) {
            int birthYear = extractNumber(queryLower);
            if (birthYear > 1800 && birthYear < 2024) {
                result.push_back(calculateAge(birthYear, 1, 1));
                return result;
            }
        }

        // FEATURE 3: DAY OF WEEK (check early)
        if (queryLower.find("what day") != string::npos ||
            queryLower.find("day of the week") != string::npos) {
            auto day = getDayOfWeek(now);
            result.push_back("Today is: " + day);
            return result;
        }

        // Current time queries
        if (queryLower.find("what time") != string::npos ||
            queryLower.find("current time") != string::npos ||
            queryLower.find("what's the time") != string::npos) {
            result.push_back("Current time: " + getCurrentDateTime() + " (Local)");
            result.push_back("UTC/GMT: " + getCurrentDateISO());
            return result;
        }

        if (queryLower.find("today") != string::npos ||
            queryLower.find("what date") != string::npos ||
            queryLower.find("what's today") != string::npos) {
            result.push_back("Today is " + getCurrentDateShort());
            return result;
        }

        if (queryLower.find("tomorrow") != string::npos) {
            auto tomorrow = now + chrono::hours(24);
            result.push_back(formatTimeWithLabel("Tomorrow", tomorrow, false));
            return result;
        }

        if (queryLower.find("yesterday") != string::npos) {
            auto yesterday = now - chrono::hours(24);
            result.push_back(formatTimeWithLabel("Yesterday", yesterday, false));
            return result;
        }

        if (queryLower.find("timestamp") != string::npos ||
            queryLower.find("unix") != string::npos) {
            // Check if there's a time offset in the query
            if (queryLower.find("from now") != string::npos ||
                queryLower.find("ago") != string::npos ||
                queryLower.find("in ") != string::npos) {
                // Process time offset first, then return unix timestamp
                int num = extractNumber(queryLower);
                if (num <= 0) num = 1;

                bool isFuture = (queryLower.find("from now") != string::npos || queryLower.find("in ") != string::npos);
                auto tp = now;
                string unitName = "days";

                // Determine the unit and calculate offset
                if (queryLower.find("second") != string::npos) {
                    tp = isFuture ? (now + chrono::seconds(num)) : (now - chrono::seconds(num));
                    unitName = "second" + string(num > 1 ? "s" : "");
                } else if (queryLower.find("minute") != string::npos) {
                    tp = isFuture ? (now + chrono::minutes(num)) : (now - chrono::minutes(num));
                    unitName = "minute" + string(num > 1 ? "s" : "");
                } else if (queryLower.find("hour") != string::npos) {
                    tp = isFuture ? (now + chrono::hours(num)) : (now - chrono::hours(num));
                    unitName = "hour" + string(num > 1 ? "s" : "");
                } else if (queryLower.find("decade") != string::npos) {
                    int days = num * 365 * 10;
                    tp = isFuture ? (now + chrono::hours(24 * days)) : (now - chrono::hours(24 * days));
                    unitName = "decade" + string(num > 1 ? "s" : "");
                } else if (queryLower.find("year") != string::npos) {
                    int days = num * 365;
                    tp = isFuture ? (now + chrono::hours(24 * days)) : (now - chrono::hours(24 * days));
                    unitName = "year" + string(num > 1 ? "s" : "");
                } else if (queryLower.find("month") != string::npos) {
                    int days = num * 30;
                    tp = isFuture ? (now + chrono::hours(24 * days)) : (now - chrono::hours(24 * days));
                    unitName = "month" + string(num > 1 ? "s" : "");
                } else if (queryLower.find("week") != string::npos) {
                    int days = num * 7;
                    tp = isFuture ? (now + chrono::hours(24 * days)) : (now - chrono::hours(24 * days));
                    unitName = "week" + string(num > 1 ? "s" : "");
                } else {
                    // Default to days
                    int days = num;
                    tp = isFuture ? (now + chrono::hours(24 * days)) : (now - chrono::hours(24 * days));
                    unitName = "day" + string(num > 1 ? "s" : "");
                }

                auto time_t_val = chrono::system_clock::to_time_t(tp);
                ostringstream oss;
                oss << "Unix timestamp (" << num << " " << unitName << " "
                    << (isFuture ? "from now" : "ago") << "): " << (long long)time_t_val;
                result.push_back(oss.str());
                return result;
            } else {
                // Just current timestamp
                ostringstream oss;
                oss << "Unix timestamp (current): " << (long long)getUnixTimestamp();
                result.push_back(oss.str());
                return result;
            }
        }

        if (queryLower.find("iso") != string::npos ||
            queryLower.find("iso 8601") != string::npos) {
            result.push_back("ISO 8601 format: " + getCurrentDateISO());
            return result;
        }

        // Extract number
        int num = extractNumber(queryLower);
        if (num <= 0) num = 1;

        // DECADES
        if (queryLower.find("decade") != string::npos) {
            bool isFuture = (queryLower.find("from now") != string::npos || queryLower.find("in ") != string::npos);
            int days = num * 365 * 10;  // Approximate decade
            auto tp = isFuture ? (now + chrono::hours(24 * days)) : (now - chrono::hours(24 * days));
            string label = isFuture ?
                (to_string(num) + " decade" + (num > 1 ? "s" : "") + " from now") :
                (to_string(num) + " decade" + (num > 1 ? "s" : "") + " ago");
            result.push_back(formatTimeWithLabel(label, tp, false));
            return result;
        }

        // YEARS
        if (queryLower.find("year") != string::npos) {
            bool isFuture = (queryLower.find("from now") != string::npos || queryLower.find("in ") != string::npos);
            int days = num * 365;
            auto tp = isFuture ? (now + chrono::hours(24 * days)) : (now - chrono::hours(24 * days));
            string label = isFuture ?
                (to_string(num) + " year" + (num > 1 ? "s" : "") + " from now") :
                (to_string(num) + " year" + (num > 1 ? "s" : "") + " ago");
            result.push_back(formatTimeWithLabel(label, tp, false));
            return result;
        }

        // MONTHS
        if (queryLower.find("month") != string::npos) {
            bool isFuture = (queryLower.find("from now") != string::npos || queryLower.find("in ") != string::npos);
            int days = num * 30;
            auto tp = isFuture ? (now + chrono::hours(24 * days)) : (now - chrono::hours(24 * days));
            string label = isFuture ?
                (to_string(num) + " month" + (num > 1 ? "s" : "") + " from now") :
                (to_string(num) + " month" + (num > 1 ? "s" : "") + " ago");
            result.push_back(formatTimeWithLabel(label, tp, false));
            return result;
        }

        // WEEKS
        if (queryLower.find("week") != string::npos) {
            bool isFuture = (queryLower.find("from now") != string::npos || queryLower.find("in ") != string::npos);
            int days = num * 7;
            auto tp = isFuture ? (now + chrono::hours(24 * days)) : (now - chrono::hours(24 * days));
            string label = isFuture ?
                (to_string(num) + " week" + (num > 1 ? "s" : "") + " from now") :
                (to_string(num) + " week" + (num > 1 ? "s" : "") + " ago");
            result.push_back(formatTimeWithLabel(label, tp, true));
            return result;
        }

        // HOURS
        if (queryLower.find("hour") != string::npos) {
            bool isFuture = (queryLower.find("from now") != string::npos || queryLower.find("in ") != string::npos);
            auto tp = isFuture ? (now + chrono::hours(num)) : (now - chrono::hours(num));
            string label = isFuture ?
                (to_string(num) + " hour" + (num > 1 ? "s" : "") + " from now") :
                (to_string(num) + " hour" + (num > 1 ? "s" : "") + " ago");
            result.push_back(formatTimeWithLabel(label, tp, true));
            return result;
        }

        // MINUTES
        if (queryLower.find("minute") != string::npos) {
            bool isFuture = (queryLower.find("from now") != string::npos || queryLower.find("in ") != string::npos);
            auto tp = isFuture ? (now + chrono::minutes(num)) : (now - chrono::minutes(num));
            string label = isFuture ?
                (to_string(num) + " minute" + (num > 1 ? "s" : "") + " from now") :
                (to_string(num) + " minute" + (num > 1 ? "s" : "") + " ago");
            result.push_back(formatTimeWithLabel(label, tp, true));
            return result;
        }

        // SECONDS
        if (queryLower.find("second") != string::npos) {
            bool isFuture = (queryLower.find("from now") != string::npos || queryLower.find("in ") != string::npos);
            auto tp = isFuture ? (now + chrono::seconds(num)) : (now - chrono::seconds(num));
            string label = isFuture ?
                (to_string(num) + " second" + (num > 1 ? "s" : "") + " from now") :
                (to_string(num) + " second" + (num > 1 ? "s" : "") + " ago");
            result.push_back(formatTimeWithLabel(label, tp, true));
            return result;
        }

        // Default: DAYS (if "from now" or "ago" without specific unit)
        if (queryLower.find("from now") != string::npos || queryLower.find("ago") != string::npos) {
            bool isFuture = (queryLower.find("from now") != string::npos || queryLower.find("in ") != string::npos);
            int days = num;
            auto tp = isFuture ? (now + chrono::hours(24 * days)) : (now - chrono::hours(24 * days));
            string label = isFuture ?
                (to_string(num) + " day" + (num > 1 ? "s" : "") + " from now") :
                (to_string(num) + " day" + (num > 1 ? "s" : "") + " ago");
            result.push_back(formatTimeWithLabel(label, tp, true));
            return result;
        }

        // FEATURE 12: HOLIDAY DETECTION
        if (queryLower.find("holiday") != string::npos) {
            if (queryLower.find("is") != string::npos || queryLower.find("today") != string::npos) {
                auto time_t_now = chrono::system_clock::to_time_t(now);
                struct tm* timeinfo = localtime(&time_t_now);
                int month = timeinfo->tm_mon + 1;
                int day = timeinfo->tm_mday;

                string holidayName = checkHoliday(month, day);
                if (!holidayName.empty()) {
                    result.push_back("Today is: " + holidayName + "!");
                } else {
                    result.push_back("Today is not a holiday");
                }
            } else {
                result.push_back(getHolidayInfo());
            }
            return result;
        }

        // FEATURE 1: TIMEZONE CONVERSION
        if (queryLower.find("timezone") != string::npos ||
            queryLower.find("convert") != string::npos) {
            if (queryLower.find("est") != string::npos) {
                auto now = chrono::system_clock::now();
                auto time_t_now = chrono::system_clock::to_time_t(now);
                struct tm* timeinfo = localtime(&time_t_now);
                ostringstream oss;
                oss << "Current time:\n";
                oss << "  UTC: " << put_time(timeinfo, "%H:%M:%S") << "\n";
                oss << "  EST (UTC-5): " << (timeinfo->tm_hour - 5) << ":" << put_time(timeinfo, "%M:%S");
                result.push_back(oss.str());
                return result;
            }
            result.push_back("Timezone: Use format 'EST', 'PST', 'UTC', 'GMT', 'JST', 'IST'");
            return result;
        }


        // Fallback
        result.push_back("Current time: " + getCurrentDateTime());
        return result;
    }

    // KILLO: Filter similar sentences to avoid redundancy
    bool isSimilarSentence(const string& s1, const string& s2) {
        if (s1.length() < 20 || s2.length() < 20) return false;

        string w1 = s1.substr(0, 30);
        string w2 = s2.substr(0, 30);
        return w1 == w2;
    }

    // KILLO: Score sentence quality (prefer medium-length, informative sentences)
    int scoreQuality(const string& sentence) {
        int score = 0;

        if (sentence.length() > 40 && sentence.length() < 300) score += 10;
        if (sentence.find("is") != string::npos || sentence.find("are") != string::npos) score += 3;
        if (sentence.find("can") != string::npos || sentence.find("could") != string::npos) score += 2;
        if (sentence.find(".") != string::npos) score += 1;

        return score;
    }

    // KILLO: Response Synthesis Engine (Enhanced)
    string synthesizeResponse(const vector<string>& sentences) {
        if (sentences.empty()) return "";
        if (sentences.size() == 1) return sentences[0];

        // Add transition words for natural flow
        vector<string> transitions = {
            "Furthermore, ",
            "Additionally, ",
            "In fact, ",
            "Notably, ",
            "As well, "
        };

        string result = sentences[0];

        for (size_t i = 1; i < sentences.size() && i < 3; i++) {
            // Add space and transition
            result += " ";

            // Randomly choose transition every other sentence
            if (i % 2 == 1 && i < transitions.size()) {
                result += transitions[i % transitions.size()];
            }

            result += sentences[i];
        }

        return result;
    }

    // KILLO: Analyze sentence patterns for context
    vector<string> analyzePatterns(const vector<string>& sentences) {
        vector<string> patterns;

        for (const auto& sentence : sentences) {
            if (sentence.length() > 50) {
                patterns.push_back(sentence.substr(0, 50) + "...");
            } else {
                patterns.push_back(sentence);
            }
        }

        return patterns;
    }

    // KILLO: Generate fluent multi-sentence response (Enhanced)
    string generateFluentResponse(const string& category) {
        lock_guard<mutex> lock(knowledgeMutex);

        if (knowledge.find(category) == knowledge.end() || knowledge[category].empty()) {
            return "I don't have specific information about that.";
        }

        vector<string>& sentences = knowledge[category];

        if (sentences.empty()) return "";

        // Score and sort sentences by quality
        vector<pair<int, string>> scored;
        for (const auto& sent : sentences) {
            if (sent.length() > 30 && sent.length() < 500) {  // Filter by length
                scored.push_back({scoreQuality(sent), sent});
            }
        }

        // Sort by score (highest first)
        sort(scored.begin(), scored.end(),
             [](const auto& a, const auto& b) { return a.first > b.first; });

        vector<string> selected;

        // Select high-quality sentences while avoiding duplicates
        for (const auto& pair : scored) {
            if (selected.size() >= 3) break;

            bool isDuplicate = false;
            for (const auto& existing : selected) {
                if (isSimilarSentence(pair.second, existing)) {
                    isDuplicate = true;
                    break;
                }
            }

            if (!isDuplicate) {
                selected.push_back(pair.second);
            }
        }

        // Fallback to any sentences if quality filtering too strict
        if (selected.empty() && !sentences.empty()) {
            selected.push_back(sentences[0]);
        }

        // Synthesize into fluent response
        return synthesizeResponse(selected);
    }

    void chat() {
        cout << "\n" << string(60, '=') << "\n";
        cout << "🤖 KILLO - AI Generative Bot (Byte 2.0)\n";
        cout << string(60, '=') << "\n";
        cout << "\nHello! I'm Killo, your AI generative assistant.\n";
        cout << "I know about 1200+ topics with 500,000+ lines of knowledge.\n";
        cout << "Plus: Real-time date/time with instant access! 📡⏰\n";

        printCategories();

        cout << "\n⏰ Time Examples:\n";
        cout << "  \"What time is it?\"\n";
        cout << "  \"What's today?\"\n";
        cout << "  \"Tomorrow\"\n";
        cout << "  \"Unix timestamp\"\n";
        cout << "\n📚 Knowledge Examples:\n";
        cout << "  \"Tell me about Python\"\n";
        cout << "  \"What is PlayStation?\"\n";
        cout << "  \"Explain Windows\"\n";
        cout << "  \"How does Android work?\"\n";
        cout << "\nCommands:\n";
        cout << "  \"tell me more\" - Get more details about last topic\n";
        cout << "  \"more\" - More info\n";
        cout << "  \"continue\" - Continue reading\n";
        cout << "  \"history\" - Show query history\n";
        cout << "  \"clear history\" - Clear query history\n";
        cout << "  \"holidays\" - Show holiday calendar\n";
        cout << "  \"quit\" - Exit\n";
        cout << "\n" << string(60, '-') << "\n\n";
        
        string userInput;
        while (true) {
            cout << "You: ";
            getline(cin, userInput);
            
            userInput = trim(userInput);
            
            if (userInput.empty()) continue;
            
            if (userInput == "quit" || userInput == "exit") {
                cout << "\nGoodbye! 👋\n";
                break;
            }
            
            // FEATURE 9: Check for history commands
            if (userInput == "history" || userInput == "query history" ||
                userInput == "show history" || userInput == "recent queries") {
                cout << "\n" << getQueryHistory(10) << "\n";
                continue;
            }

            if (userInput == "clear history" || userInput == "reset history") {
                clearHistory();
                cout << "\n✓ History cleared\n\n";
                continue;
            }

            // FEATURE 12: Check for holiday queries
            if (userInput == "holidays" || userInput == "show holidays" ||
                userInput == "list holidays" || userInput == "holiday calendar") {
                cout << "\n" << getHolidayInfo() << "\n";
                continue;
            }

            // Check for "tell me more" commands
            if (userInput == "more" || userInput == "tell me more" ||
                userInput == "continue" || userInput == "more info" ||
                userInput == "more please") {
                
                if (lastCategory.empty()) {
                    cout << "\nByte: Ask me about something first!\n\n";
                    continue;
                }
                
                // Get more sentences from the last category
                vector<string> answers = getMoreSentences(lastCategory, lastIndex);
                
                if (answers.empty()) {
                    cout << "\nByte: That's all I know about [" << lastCategory << "]\n\n";
                    lastCategory = "";
                    continue;
                }
                
                cout << "\nByte [" << lastCategory << "]:\n";
                for (size_t i = 0; i < answers.size(); i++) {
                    cout << answers[i];
                    if (i < answers.size() - 1) cout << "\n";
                }
                cout << "\n\n";
                continue;
            }
            
            // Check for time queries first
            if (isTimeQuery(userInput)) {
                vector<string> timeAnswers = handleTimeQuery(userInput);
                cout << "\nByte [time]:\n";
                for (size_t i = 0; i < timeAnswers.size(); i++) {
                    cout << timeAnswers[i];
                    if (i < timeAnswers.size() - 1) cout << "\n";
                }
                cout << "\n\n";
                continue;
            }

            // FEATURE 9: Record query in history
            addToHistory(userInput);

            string category = findBestCategory(userInput);

            if (category.empty()) {
                cout << "\nByte: Hi there! Ask me about something specific.\n";
                cout << "Try: \"Tell me about Python\", \"What is AI?\", \"Explain quantum mechanics\"\n";
                cout << "Or ask about time: \"What time is it?\", \"What's today?\"\n";
                cout << "Or type one of these topics:\n";
                int count = 0;
                for (const auto& pair : knowledge) {
                    if (count > 0) cout << ", ";
                    cout << pair.first;
                    if (++count >= 5) break;
                }
                cout << "\n\n";
                continue;
            }

            // Remember this category for "tell me more"
            lastCategory = category;
            lastIndex = 0;

            vector<string> answers = findRelevantSentences(category, userInput);

            cout << "\nKillo [" << category << "]:\n";

            // KILLO: Use synthesis engine to generate fluent response
            if (!answers.empty()) {
                string synthesizedResponse = synthesizeResponse(answers);
                cout << synthesizedResponse;
            } else {
                // Fallback to fluent generation
                cout << generateFluentResponse(category);
            }

            // Show hint about more info
            if (knowledge[category].size() > answers.size()) {
                cout << "\n(Type 'tell me more' for additional details)";
            }
            cout << "\n\n";
        }
    }
};

int main() {
    KnowledgeBot bot;

    // Clean up any previous temp files
    bot.cleanupTempFiles();

    bot.loadTrainingDataPublic();
    bot.chatPublic();

    // Cleanup temp extracted files
    bot.cleanupTempFiles();

    return 0;
}
