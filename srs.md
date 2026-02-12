# Software Requirements Specification (SRS)
## Project: Yad2 Scraper
**Version:** 1.0 (As-Built)
**Date:** 2024-02-12

---

## 1. Introduction

### 1.1 Purpose
The purpose of this document is to specify the software requirements for the **Yad2 Scraper** project. This tool is designed to automate the process of searching for new rental listings on the Yad2 website and notifying the user immediately via Telegram.

### 1.2 Scope
The Yad2 Scraper is a Python-based application that:
- Periodically queries the Yad2 Real Estate API for rental listings.
- Identifies new listings by comparing current results against a historical record.
- Sends real-time notifications to a specified Telegram chat.
- Persists data to a JSON file and commits changes back to the repository using GitHub Actions.

## 2. Overall Description

### 2.1 Product Perspective
The software operates as a scheduled task within a **GitHub Actions** workflow. It is designed to run automatically at defined intervals (e.g., every 10 minutes) without manual intervention, leveraging the GitHub infrastructure for execution and state storage.

### 2.2 Product Functions
The major functions of the system are:
1.  **Data Retrieval**: Fetching rental listing data from the Yad2 API.
2.  **Data Parsing**: Extracting relevant details (price, location, rooms, URL) from the raw API response.
3.  **Change Detection**: Checking new listings against a persistent history of seen listing IDs.
4.  **Notification**: Sending formatted alerts for new listings to a Telegram user or group.
5.  **State Persistence**: Saving the IDs of seen listings to a JSON file (`data/rentals.json`) to prevent duplicate notifications.
6.  **Self-Update**: Committing and pushing the updated state file back to the repository (handled by CI/CD).

### 2.3 User Characteristics
The intended users are individuals looking for rental properties who want immediate alerts. The user is expected to have basic technical knowledge to set up GitHub Secrets (Telegram API Token, Chat ID) and modify the search parameters in the code if necessary.

## 3. Specific Requirements

### 3.1 Functional Requirements

#### 3.1.1 Scraping Module
*   **REQ-1**: The system shall initiate an HTTP GET request to the Yad2 API endpoint.
*   **REQ-2**: The system shall use hardcoded search parameters (City, Area, Rooms, etc.) defined in the `API_URL` constant.
*   **REQ-3**: The system shall handle HTTP errors and JSON decoding errors gracefully, logging failures to the console.

#### 3.1.2 Data Processing
*   **REQ-4**: The system shall parse the JSON response to extract a list of property markers.
*   **REQ-5**: For each marker, the system shall extract:
    *   Unique Token (ID)
    *   Street and City Name
    *   Price
    *   Number of Rooms
    *   Item URL
*   **REQ-6**: The system shall filter out invalid markers (missing tokens).

#### 3.1.3 State Management
*   **REQ-7**: The system shall load previously seen listing IDs from `data/rentals.json`.
*   **REQ-8**: The system shall compare current listing IDs against the loaded history.
*   **REQ-9**: The system shall identify any ID not present in the history as a "new item".
*   **REQ-10**: The system shall append new IDs to the history file and save it to `data/rentals.json`.
*   **REQ-11**: The system shall create a trigger file (`push_me`) if new items were found, signaling the workflow to commit changes.

#### 3.1.4 Notification System
*   **REQ-12**: The system shall read Telegram credentials (`API_TOKEN`, `CHAT_ID`) from environment variables.
*   **REQ-13**: If new items are found, the system shall construct a message containing the count of new items and details for each (Address, Rooms, Price, URL).
*   **REQ-14**: The system shall send the message to the Telegram Bot API via HTTP POST.

### 3.2 External Interface Requirements

#### 3.2.1 APIs
*   **Yad2 API**: The system interacts with `https://gw.yad2.co.il` to retrieve real estate data.
    *   Protocol: HTTPS
    *   Format: JSON
 *   **Telegram Bot API**: The system interacts with `https://api.telegram.org` to send messages.
    *   Protocol: HTTPS
    *   Method: `sendMessage`

### 3.3 Non-Functional Requirements

#### 3.3.1 Security
*   **SEC-1**: Sensitive credentials (Telegram Bot Token, Chat ID) shall not be hardcoded in the source code. They must be supplied via environment variables or GitHub Secrets.

#### 3.3.2 Reliability
*   **REL-1**: The scraper is scheduled to run every 10 minutes via GitHub Actions cron syntax `*/10 * * * *`.
*   **REL-2**: The system relies on GitHub Actions availability; execution is not guaranteed (best-effort by GitHub).

#### 3.3.3 Performance
*   **PERF-1**: The script is lightweight and stateless (except for the JSON file), designed to run quickly within the limits of GitHub Actions runners.

## 4. Current Limitations & Future Work
*   **Hardcoded Query**: The search parameters (City, Area, Rooms) are currently hardcoded in the `scraper.py` file. Future versions may implement a configuration file (e.g., `config.json`) to allow easier modification of search criteria without code changes, as mentioned in the project README.
*   **Single Search**: The system currently supports a single search URL. Multi-query support is planned but not yet implemented in the core logic.
