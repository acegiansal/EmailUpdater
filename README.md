# Google Tools Email Updater
Giancarlo Salvador

## Description

This program will look through a google sheet using the google API and will email a user based on the results found. The parsing of the google sheet is scheduled and will happen once a day, depending on the time that the user inputs in the *userconfig.json* file. One run of the script can handle multiple notifiers, as long as the userconfig.json file is properly set up.

**ONLY THE ASSIGNMENT TYPE SHEET IS IMPLEMENTED**

## Requirements

- A gmail account (with access to google sheets)
- An app password for the previously mentioned gmail account ([How to get one](https://support.google.com/accounts/answer/185833?hl=en))
- Google api setup properly (Follow the [Setup environment instructions](https://developers.google.com/sheets/api/quickstart/python#set_up_your_environment))
- The google sheet(s) must be shared to the "sender" email

## Setup
1. Get the URL info of the google sheet. It is the long string between after /spreadsheets
2. Edit the userconfig.json file with the proper information (Multiple can be made by adding more objects with the same fields to the list)
   1. The range should not contain the header of the table
3. Start the schedule_tasks.py main
4. Input the app password when prompted

## Supported Sheet Types
Each type of sheet has a specific implementation, thus must follow a set of rules.

### Assignment Type Sheet
The attributes (columns) of the sheet must follow this order:

`['class_code', 'assignment', 'status', 'weight', 'time', 'start_date', 'due_date']`

The date must be in the following format: 'Wed, Jan 25, 2023'

It will notify the user these days before the due date: `[5, 3, 1]`
