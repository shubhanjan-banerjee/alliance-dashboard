User Stories: User Management and Authentication
Epic: User Authentication & Authorization

----------------------------------------------------------------------------------------------------------------------------------------
Story 1.1: Admin Login

As an administrator,

I want to securely log in with a username and password,

So that I can access all data management and reporting features.

Acceptance Criteria:

Given I am on the login page, when I enter valid admin credentials and click "Login", then I am redirected to the admin dashboard.

Given I am on the login page, when I enter invalid credentials, then I see an "Invalid username or password" error message.

The password should be hashed and salted in the database.

----------------------------------------------------------------------------------------------------------------------------------------
Story 1.2: Guest Login

As a guest user,

I want to log in without providing specific credentials (or using a generic guest button),

So that I can view pre-defined dashboards and reports without administrative access.

Acceptance Criteria:

Given I am on the login page, when I click "Login as Guest", then I am redirected to the guest dashboard with read-only access.

Guest users cannot see or access "Data Management" tabs/features.

----------------------------------------------------------------------------------------------------------------------------------------
Story 1.3: User Session Management

As a user,

I want my login session to persist for a reasonable duration and allow logout,

So that I don't have to re-login frequently and can secure my session when done.

Acceptance Criteria:

Given I am logged in, when I navigate between pages, then I remain logged in.

Given I am logged in, when I click the "Logout" button, then my session is terminated, and I am redirected to the login page.

----------------------------------------------------------------------------------------------------------------------------------------
Story 1.4: Admin Password Change (Self-Service)

As an administrator,

I want to be able to change my own password after logging in,

So that I can maintain account security.

Acceptance Criteria:

Given I am logged in as admin, when I navigate to a "Profile" or "Settings" section, then I can see an option to change my password.

When I enter my current password and a new valid password (twice), then my password is updated.

When I enter an incorrect current password, then I receive an error message.

User Stories: Data Ingestion and Management
Epic: Data Lifecycle Management

----------------------------------------------------------------------------------------------------------------------------------------
Story 2.1: Upload Raw Performance Data (Admin)

As an administrator,

I want to upload an Excel file containing raw associate performance data,

So that the system is updated with the latest monthly activity.

Acceptance Criteria:

Given I am logged in as admin and on the "Data Management" tab, when I select an Excel file with the specified "Global Strategic Alliances Partner Performance Dashboard as of May 2025 [Sample data]" sheet, then the data from that sheet is parsed.

When I click "Load Performance Data", then the data is inserted into the performance_data table.

I receive a success or failure message after the upload attempt.

----------------------------------------------------------------------------------------------------------------------------------------
Story 2.2: Upload Global Metrics Data (Admin)

As an administrator,

I want to upload an Excel file containing global metrics data,

So that the dashboard reflects the latest YTD performance.

Acceptance Criteria:

Given I am logged in as admin and on the "Data Management" tab, when I select an Excel file with the specified "Global" sheet, then the data from the relevant rows (e.g., "Metrices YTD", "India", "NA", "GGM") is parsed.

When I click "Load Global Metrics", then the global_metrics table is updated (overwritten).

I receive a success or failure message.

----------------------------------------------------------------------------------------------------------------------------------------
Story 2.3: Upload BU Wise Report Data (Admin)

As an administrator,

I want to upload an Excel file containing Business Unit wise report data,

So that I can track BU-specific targets and achievements.

Acceptance Criteria:

Given I am logged in as admin and on the "Data Management" tab, when I select an Excel file with the specified "BU Wise Report" sheet, then the data is parsed.

When I click "Load BU Metrics", then the bu_metrics table is updated (overwritten).

I receive a success or failure message.

----------------------------------------------------------------------------------------------------------------------------------------
Story 2.4: Upload Alliance Wise Report Data (Admin)

As an administrator,

I want to upload an Excel file containing Alliance Partner wise report data,

So that I can track partner-specific targets and achievements across BUs.

Acceptance Criteria:

Given I am logged in as admin and on the "Data Management" tab, when I select an Excel file with the specified "Alliance Wise Report" sheet, then the data is parsed.

When I click "Load Alliance Metrics", then the alliance_metrics table is updated (overwritten).

I receive a success or failure message.

----------------------------------------------------------------------------------------------------------------------------------------
Story 2.5: Upload Cost Savings Data (Admin)

As an administrator,

I want to upload an Excel file containing cost savings data,

So that I can track financial benefits from alliances.

Acceptance Criteria:

Given I am logged in as admin and on the "Data Management" tab, when I select an Excel file with the specified "Cost Savings" sheet, then the data is parsed.

When I click "Load Cost Savings Data", then the cost_savings table is updated (overwritten).

I receive a success or failure message.

----------------------------------------------------------------------------------------------------------------------------------------
Story 2.6: View Raw Performance Data (Admin)

As an administrator,

I want to view all raw performance data in a sortable and filterable table,

So that I can review and manage individual records.

Acceptance Criteria:

Given I am logged in as admin and on the "Data Management" tab, then I see a table displaying all records from performance_data.

The table columns are sortable (ascending/descending).

I can filter the table by any column value (e.g., Associate Name, Alliance Type).

----------------------------------------------------------------------------------------------------------------------------------------
Story 2.7: Add New Performance Record (Admin)

As an administrator,

I want to manually add a new performance record through a form,

So that I can correct or append individual entries without re-uploading the entire Excel.

Acceptance Criteria:

Given I am logged in as admin and on the "Data Management" tab, when I fill out the "Add New Record" form with valid data and submit, then the record is added to the performance_data table.

I receive a success message, and the table updates to show the new record.

If I submit invalid data (e.g., incorrect date format), I receive an error message.

----------------------------------------------------------------------------------------------------------------------------------------
Story 2.8: Update Performance Record (Admin)

As an administrator,

I want to select an existing performance record and edit its fields,

So that I can correct inaccuracies in the data.

Acceptance Criteria:

Given I am logged in as admin and on the "Data Management" tab, when I select a record ID, then a form pre-populates with that record's data.

When I modify fields and submit the "Update Record" form, then the corresponding record in performance_data is updated.

I receive a success message, and the table updates to reflect the changes.

----------------------------------------------------------------------------------------------------------------------------------------
Story 2.9: Delete Performance Record (Admin)

As an administrator,

I want to select an existing performance record and delete it,

So that I can remove erroneous or outdated entries.

Acceptance Criteria:

Given I am logged in as admin and on the "Data Management" tab, when I select a record ID and click "Delete Record", then the record is removed from performance_data.

I receive a success message, and the table updates to remove the deleted record.

A confirmation dialog should appear before deletion.

----------------------------------------------------------------------------------------------------------------------------------------
Story 2.10: Data Validation on Upload (Admin)

As an administrator,

I want the system to validate the uploaded Excel data,

So that I can prevent incorrect or malformed data from entering the database.

Acceptance Criteria:

Given I upload an Excel file with incorrect date formats in "Completion Date", then the system identifies the errors and provides specific feedback (e.g., "Row X has invalid date format").

Given I upload an Excel file with non-numeric values in expected numeric columns (e.g., "Total" in Global Metrics), then the system identifies these errors.

The system should either reject the entire upload or allow partial upload with clear warnings about skipped/corrected rows.

User Stories: Dashboard and Reporting Features
Epic: Interactive Dashboard & Insights

----------------------------------------------------------------------------------------------------------------------------------------
Story 3.1: View Executive Summary

As an administrator or guest,

I want to see an automatically generated executive summary on the dashboard,

So that I can quickly grasp the key performance highlights.

Acceptance Criteria:

Given I am on the "Dashboard Overview" tab, then I see a "Key Performance Highlights" section.

This section includes: total certifications, overall progress percentage, geographical breakdown (India, NA, GGM percentages), top 3 BUs by goal achievement, BUs below 50% target, and top 3 partner certifications.

All numbers in the summary are dynamically updated based on the latest data.

----------------------------------------------------------------------------------------------------------------------------------------
Story 3.2: View Certifications by Alliance Type Chart

As an administrator or guest,

I want to see a bar chart displaying certifications by Alliance Type,

So that I can understand which partners are contributing most to certifications.

Acceptance Criteria:

Given I am on the "Dashboard Overview" tab, then I see a "Certifications by Alliance Type" bar chart.

The chart accurately reflects the count of certifications for each alliance.

The chart is interactive (e.g., hover to see exact counts).

----------------------------------------------------------------------------------------------------------------------------------------
Story 3.3: View Certifications by Business Unit Chart

As an administrator or guest,

I want to see a bar chart displaying certifications by Business Unit,

So that I can understand performance across different internal teams.

Acceptance Criteria:

Given I am on the "Dashboard Overview" tab, then I see a "Certifications by Business Unit" bar chart.

The chart accurately reflects the count of certifications for each BU.

The chart is interactive.

----------------------------------------------------------------------------------------------------------------------------------------
Story 3.4: View Certifications by Geographical Region Chart

As an administrator or guest,

I want to see a pie/donut chart displaying certifications by Geographical Region,

So that I can understand regional contributions.

Acceptance Criteria:

Given I am on the "Dashboard Overview" tab, then I see a "Certifications by Geographical Region" chart.

The chart shows the proportion of certifications from India, NA, and GGM.

The chart is interactive (e.g., hover to see percentages/counts, drill-down if applicable).

----------------------------------------------------------------------------------------------------------------------------------------
Story 3.5: View Monthly Certification Trend Chart

As an administrator or guest,

I want to see a line chart showing the monthly trend of completed certifications,

So that I can track progress over time.

Acceptance Criteria:

Given I am on the "Dashboard Overview" tab, then I see a "Monthly Certification Completion Trend" line chart.

The X-axis shows months/years, and the Y-axis shows the number of certifications.

The chart is interactive with markers and tooltips.

----------------------------------------------------------------------------------------------------------------------------------------
Story 3.6: View BU Performance vs. Target Chart

As an administrator or guest,

I want to see a grouped bar chart comparing target vs. completed certifications for each Business Unit,

So that I can assess how each BU is performing against its goals.

Acceptance Criteria:

Given I am on the "BU Wise Report" tab, then I see a "Business Unit Performance: Target vs. Completed Certifications" chart.

The chart clearly distinguishes between target and completed values for each BU.

The chart is interactive.

----------------------------------------------------------------------------------------------------------------------------------------
Story 3.7: View BU Goal Achievement Percentage Chart

As an administrator or guest,

I want to see a bar chart displaying the goal achievement percentage for each Business Unit,

So that I can quickly identify high and low performing BUs.

Acceptance Criteria:

Given I am on the "BU Wise Report" tab, then I see a "Business Unit Goal Achievement Percentage" chart.

The chart uses color intensity or distinct colors to highlight percentages.

The chart is interactive.

----------------------------------------------------------------------------------------------------------------------------------------
Story 3.8: View Alliance Partner Performance Chart

As an administrator or guest,

I want to see a bar chart displaying YTD completed certifications for each Alliance Partner,

So that I can see which partners are most active.

Acceptance Criteria:

Given I am on the "Alliance Wise Report" tab, then I see an "Alliance Partner Performance: YTD Completed Certifications" chart.

The chart lists partners and their total completed certifications.

The chart is interactive.

----------------------------------------------------------------------------------------------------------------------------------------
Story 3.9: View Cost Savings Breakdown Chart

As an administrator or guest,

I want to see a stacked bar chart showing cost savings attributed to enablement and certification for each strategic partner,

So that I can understand the financial impact of each alliance.

Acceptance Criteria:

Given I am on the "Cost Savings" tab, then I see a "Cost Savings Breakdown" chart.

The chart clearly shows "Cost-saving thru enablement" and "Cost-saving thru certification" stacked for each partner.

A grand total cost saving is displayed as a metric.

----------------------------------------------------------------------------------------------------------------------------------------
Story 3.10: Interactive Filters (Global)

As an administrator or guest,

I want to filter the dashboard data by Alliance Type, Business Unit, Geo, and Completion Date range,

So that I can analyze specific segments of the data.

Acceptance Criteria:

Given I am on any dashboard tab, when I select values from dropdowns/sliders for Alliance Type, BU, Geo, or a date range, then all relevant charts and summaries on that tab update to reflect the filtered data.

Filters are persistent across tab switches within the same session.

----------------------------------------------------------------------------------------------------------------------------------------
Story 3.11: Year-on-Year Comparison Chart

As an administrator or guest,

I want to see a chart comparing current year's certification performance with previous years' performance for the same period,

So that I can identify long-term trends and growth.

Acceptance Criteria:

Given I am on the "Dashboard Overview" or a dedicated "Historical Trends" section, then I see a multi-line chart showing total certifications (or a selected metric) for the current year and previous years.

The chart allows selection of specific years for comparison.

----------------------------------------------------------------------------------------------------------------------------------------
Story 3.12: Data Tables for Reports

As an administrator or guest,

I want to view the raw data behind the "BU Wise Report", "Alliance Wise Report", and "Cost Savings" sections in a tabular format,

So that I can inspect the exact numbers.

Acceptance Criteria:

Given I am on the "BU Wise Report", "Alliance Wise Report", or "Cost Savings" tab, then I see a data table displaying the corresponding metrics.

The tables are readable and well-formatted.

----------------------------------------------------------------------------------------------------------------------------------------
Story 3.13: Export Dashboard Data (Admin)

As an administrator,

I want to export the displayed data tables (e.g., raw performance, BU metrics, Alliance metrics, Cost Savings) to CSV or Excel,

So that I can perform further offline analysis or share the raw data.

Acceptance Criteria:

Given I am on a tab with a data table, when I click an "Export to CSV/Excel" button, then the current filtered data from that table is downloaded.

----------------------------------------------------------------------------------------------------------------------------------------
Story 3.14: Export Charts as Images (Admin/Guest)

As an administrator or guest,

I want to download individual charts as high-resolution image files (e.g., PNG, SVG),

So that I can easily include them in presentations or reports.

Acceptance Criteria:

Given I am viewing any Plotly chart, then I can see an option to download the chart as an image (this is often built into Plotly).

When I click the download option, the image file is saved.

User Stories: Non-Functional & Technical
Epic: System Foundation & Quality

----------------------------------------------------------------------------------------------------------------------------------------
Story 4.1: Responsive UI

As a user,

I want the application interface to adapt to different screen sizes (desktop, tablet, mobile),

So that I can comfortably view and interact with the dashboard on any device.

Acceptance Criteria:

Given I access the application on a mobile device, then the layout adjusts gracefully, and elements remain usable (e.g., charts resize, forms stack vertically).

No horizontal scrolling is required on standard mobile/tablet orientations.

----------------------------------------------------------------------------------------------------------------------------------------
Story 4.2: Database Connection & Error Handling

As a developer,

I want the application to handle database connection issues gracefully,

So that users receive informative messages instead of crashes.

Acceptance Criteria:

Given the database connection fails, when the application tries to fetch or write data, then a user-friendly error message is displayed (e.g., "Could not connect to database. Please try again later.") instead of a technical traceback.

Relevant errors are logged to the console/log file.

----------------------------------------------------------------------------------------------------------------------------------------
Story 4.3: Data Type Handling

As a developer,

I want the data ingestion process to correctly handle various data types (dates, numbers, strings),

So that data is stored accurately in the database and can be used for calculations.

Acceptance Criteria:

Given an Excel column contains dates in mixed formats, when uploaded, then they are correctly converted to standard date format in the database.

Given an Excel column contains numbers with currency symbols or commas, when uploaded, then they are stored as numeric types in the database.

----------------------------------------------------------------------------------------------------------------------------------------
Story 4.4: Performance Optimization (Initial)

As a user,

I want the dashboards and reports to load quickly,

So that I have a smooth and efficient experience.

Acceptance Criteria:

Given I navigate to any dashboard tab, then all charts and data load within 3-5 seconds (initial target, can be refined).

Data fetching operations are optimized (e.g., using appropriate SQL queries, indexing).

----------------------------------------------------------------------------------------------------------------------------------------
Story 4.5: Code Maintainability

As a developer,

I want the codebase to be well-structured and commented,

So that it is easy to understand, debug, and extend.

Acceptance Criteria:

Code follows Python PEP 8 guidelines.

Functions and complex logic blocks are clearly commented.

Database operations are encapsulated in a separate module.
