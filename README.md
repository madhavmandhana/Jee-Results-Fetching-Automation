# Jee-Results-Fetching-Automation

This code automates the retrieval of exam results from a website by simulating user interactions using Selenium WebDriver. The code is designed to handle the extraction of specific details from a CSV file containing application details, such as application numbers and dates of birth, and fetch the corresponding exam results from the website. Below is an overview of the system's functionalities and components:

## Functionality
The system offers the following main functionalities:

Data Retrieval: Retrieves exam results from a designated website by inputting application details such as application numbers and dates of birth.
Error Handling: Implements mechanisms to handle errors gracefully, such as unexpected alerts or failures during the data retrieval process.
Parallel Processing: Utilizes multiprocessing to enhance performance by processing multiple requests simultaneously.
Screenshot Capture: Captures screenshots of the result page for verification purposes and saves them locally.
Profile Picture Retrieval: Downloads profile pictures associated with the exam results, if available, and saves them locally.

## Components
The system consists of the following key components:

Selenium WebDriver Module: Utilizes the Selenium WebDriver library to automate web browser interactions, enabling the system to input application details, submit forms, and retrieve result data.
ChromeOptions Configuration: Configures the ChromeOptions to customize the browser behavior, including headless mode, printing preferences, and other settings.
Data Processing Functions: Includes functions to process input data from a CSV file, extract application details, and pass them to the Selenium WebDriver for result retrieval.
Result Retrieval Function: Implements a function to interact with the website, input application details, and extract result data. This function also handles errors and captures screenshots as needed.
Result Data Extraction: Extracts specific details such as roll numbers, candidate names, subject-wise scores, and All India Rank (AIR) from the result page using Selenium WebDriver's find_element methods.
Profile Picture Retrieval: Downloads profile pictures associated with the exam results, if available, and saves them locally for further processing.

## Usage
To use the system, follow these steps:

Prepare Input Data: Create a CSV file containing application details such as application numbers and dates of birth.
Configure WebDriver: Ensure that the appropriate WebDriver executable (e.g., chromedriver) is available and configured correctly in the system path.
Execute the Script: Run the main function, which initiates the data retrieval process and handles error conditions automatically.
Review Output: Check the generated CSV files for successful and failed result data, as well as any captured screenshots and downloaded profile pictures.
