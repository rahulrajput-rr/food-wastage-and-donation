import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

admin_credentials = {
    'Admin': 'admin',
}

donor_info = {}

recipient_credentials = {}
recipient_credentials['a'] = {'id': 'a', 'password': 'a'}

donors = []
recipients = []

donated_items = {}

purchased_items = {}


def load_data(file_path):
    data = pd.read_csv(file_path)
    return data


def get_y_axis_options(data):
    return data.columns[2:]

# Function to analyze data and create graphs


def analyze_data(data, graph_type, y_axis_column=None, countries_filter=None):
    if countries_filter:
        data = data[data['Country'].isin(countries_filter)]

    if graph_type == "pie":
        data_grouped = data.groupby(
            'Country')['Household estimate (kg/capita/year)'].sum()
        plt.figure(figsize=(10, 10))
        plt.pie(data_grouped, labels=data_grouped.index, autopct='%1.1f%%')
        plt.title('Food Waste by Country (Household estimate)')
        plt.show()
    elif graph_type == "bar":
        if y_axis_column:
            data_grouped = data.groupby('Country')[y_axis_column].sum()
        else:
            data_grouped = data.groupby(
                'Country')['Retail estimate (tonnes/year)'].sum()
        plt.figure(figsize=(10, 6))
        data_grouped.plot(kind='bar')
        plt.xlabel('Countries')
        plt.ylabel(
            y_axis_column if y_axis_column else 'Retail estimate (tonnes/year)')
        plt.title('Retail Food Waste by Country')
        plt.show()
    elif graph_type == "line":
        if y_axis_column:
            data_grouped = data.groupby('Country')[y_axis_column].sum()
        else:
            data_grouped = data.groupby(
                'Country')['Food service estimate (tonnes/year)'].sum()
        plt.figure(figsize=(12, 6))
        data_grouped.plot(kind='line')
        plt.xlabel('Countries')
        plt.ylabel(
            y_axis_column if y_axis_column else 'Food service estimate (tonnes/year)')
        plt.title('Food Service Food Waste by Country')
        plt.show()
    else:
        print("Invalid graph type. Please choose from 'pie', 'bar', or 'line'.")


def data_analysis():
    file_path = input("Enter the CSV file path: ")
    data = load_data(file_path)
    y_axis_options = get_y_axis_options(data)

    while True:
        graph_type = input(
            "Choose a graph type (pie, bar, line, or 'exit' to quit): ")
        if graph_type == 'exit':
            break

        print("Available Y-axis column options:")
        for idx, option in enumerate(y_axis_options):
            print(f"{idx + 1}. {option}")

        y_axis_choice = input(
            "Enter the number of the Y-axis column you want to use (or press Enter to use default): ")
        if y_axis_choice:
            y_axis_column = y_axis_options[int(y_axis_choice) - 1]
        else:
            y_axis_column = None

        countries_filter = input(
            "Enter countries to filter (comma-separated, or press Enter for no filter): ")
        countries_filter1 = countries_filter.split(
            ',') if countries_filter else None
        countries_filter = [word.capitalize() for word in countries_filter1]

        analyze_data(data, graph_type, y_axis_column, countries_filter)


def login():
    print("Welcome to the Administrator Login Page")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in admin_credentials and admin_credentials[username] == password:
        print("Login successful. Welcome, {}!".format(username))
        admin_panel(username)
    else:
        print("Login failed. Please check your username and password.")


def admin_panel(username):
    while True:
        print("\nAdministrator Panel")
        print("1. Add Donor")
        print("2. Add Recipient")
        print("3. Remove Donor")
        print("4. Remove Recipient")
        print("5. View Donors")
        print("6. View Recipients and Their Purchases")
        print("7. Data Analysis")
        print("8. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_donor()
        elif choice == '2':
            add_recipient()
        elif choice == '3':
            remove_donor()
        elif choice == '4':
            remove_recipient()
        elif choice == '5':
            view_donors()
        elif choice == '6':
            view_recipients_info()
        elif choice == '7':
            data_analysis()
        elif choice == '8':
            print("Logging out. Goodbye, {}!".format(username))
            break
        else:
            print("Invalid choice. Please try again.")


def add_donor():
    name = input("Enter donor's name: ")
    username = input("Enter donor's username: ")
    password = input("Enter donor's password: ")
    contact_number = input("Enter donor's contact number: ")

    donors.append(name)
    donor_info[username] = {
        'name': name, 'password': password, 'contact_number': contact_number}

    print("{} has been added as a donor with username '{}', password '{}', and contact number '{}'.".format(
        name, username, password, contact_number))


def add_recipient():
    name = input("Enter recipient's name: ")
    recipient_id = input("Enter recipient's ID: ")
    recipient_password = input("Enter recipient's password: ")

    recipients.append(name)
    recipient_credentials[name] = {
        'id': recipient_id, 'password': recipient_password}

    print("{} has been added as a recipient with ID '{}' and password '{}'.".format(
        name, recipient_id, recipient_password))


def remove_donor():
    name = input("Enter the name of the donor to remove: ")
    if name in donors:
        donors.remove(name)
        username = None

        for donor_username, donor_data in donor_info.items():
            if donor_data['name'] == name:
                username = donor_username
                break

        if username:
            del donor_info[username]

        print("{} has been removed as a donor.".format(name))
    else:
        print("{} is not in the list of donors.".format(name))


def remove_recipient():
    name = input("Enter the name of the recipient to remove: ")
    if name in recipients:
        recipients.remove(name)
        print("{} has been removed as a recipient.".format(name))
    else:
        print("{} is not in the list of recipients.".format(name))


def view_donors():
    print("\nDonors:")
    for donor in donors:
        print(donor)


def show_admin_dashboard():
    print("Welcome to the Administrative Dashboard!")


def view_recipients_info():
    print("\nRecipients and Their Purchases:")
    print("{:<15} {:<15} {:<30} {:<30} {:<20}".format("Recipient Name",
          "Recipient ID", "Purchased Items", "Donor's Name", "Donor's Contact Number"))
    print("=" * 100)

    recipient_names = []
    recipient_ids = []
    donor_names = []
    donor_contact_numbers = []
    purchased_percentages = []

    for recipient, info in recipient_credentials.items():
        recipient_name = recipient
        recipient_id = info['id']
        purchases = purchased_items.get(recipient_name, [])
        purchases_list = ", ".join(purchases)

        donor_name = None
        donor_contact_number = ""

        for username, donor_data in donor_info.items():
            if donor_data['name'] == recipient_name:
                donor_name = donor_data['name']
                donor_contact_number = donor_data['contact_number']
                break

        recipient_names.append(recipient_name)
        recipient_ids.append(recipient_id)
        donor_names.append(donor_name)
        donor_contact_numbers.append(donor_contact_number)

        total_items = len(donated_items.get(recipient_name, []))

        if total_items > 0:
            purchased_percentage = len(purchases) / total_items * 100
        else:
            purchased_percentage = 0  # Set to 0 if no total_items to avoid division by zero

        purchased_percentages.append(purchased_percentage)

        if donor_name is None:
            donor_name = "N/A"
        if donor_contact_number == "":
            donor_contact_number = "N/A"

        print("{:<15} {:<15} {:<30} {:<30} {:<20}".format(recipient_name,
              recipient_id, purchases_list, donor_name, donor_contact_number))


def show_donor_dashboard(username):
    print("Welcome to the Donor Dashboard, {}!".format(username))

    password = input("Enter your donor password: ")
    if username in donor_info and donor_info[username]['password'] == password:
        print("Authentication successful.")
        donate_food(username)
    else:
        print("Authentication failed. Please check your username and password.")


def donate_food(username):
    while True:
        food_item = input(
            "Enter the food item you want to donate (or 'done' to finish): ")

        if food_item.lower() == 'done':
            break

        if username not in donated_items:
            donated_items[username] = []

        donated_items[username].append(food_item)

        print("Thank you for donating {}. Your donation has been recorded.".format(
            food_item))


def show_existing_recipient_dashboard(recipient_name):
    print("Welcome to the Recipient Dashboard, {}!".format(recipient_name))

    while True:
        print("\nRecipient Menu:")
        print("1. View Donated Items")
        print("2. Choose Items to Buy")
        print("3. View Purchased Items")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            view_donated_items(recipient_name)
        elif choice == '2':
            choose_items_to_buy(recipient_name)
        elif choice == '3':
            view_purchased_items(recipient_name)
        elif choice == '4':
            print("Returning to the Main Menu.")
            break
        else:
            print("Invalid choice. Please try again.")


def view_donated_items(recipient_name):
    print("\nView Donated Items by Donor:")

    selected_donor = input(
        "Enter the name of the donor whose donated items you want to view: ")

    if selected_donor in donor_info:
        donated_items_list = donated_items.get(selected_donor, [])

        if not donated_items_list:
            print(f"No donated items available from {selected_donor}.")
        else:
            for i, item in enumerate(donated_items_list, 1):
                print("{}. {}".format(i, item))
    else:
        print(f"{selected_donor} is not a valid donor.")


def view_purchased_items(recipient_name):
    print("\nYour Purchased Items:")
    if recipient_name in purchased_items:
        purchases_list = ", ".join(purchased_items[recipient_name])
        print(purchases_list)
    else:
        print("No purchased items yet.")


def choose_items_to_buy(recipient_name):
    print("\nSelect the donated food items you want to buy (or 'cancel' to cancel):")
    selected_donor = input(
        "Enter the name of the donor whose donated items you want to choose from: ")

    if selected_donor in donated_items:
        donated_items_list = donated_items.get(selected_donor, [])

        if not donated_items_list:
            print(f"No donated items available from {selected_donor}.")
        else:
            while True:
                for i, item in enumerate(donated_items_list, 1):
                    print("{}. {}".format(i, item))

                choice = input(
                    "Enter the number of the item you want to buy (or 'cancel' to cancel): ")

                if choice.lower() == 'cancel':
                    print("Cancelled. No items purchased.")
                    break

                try:
                    choice = int(choice)

                    if choice < 1 or choice > len(donated_items_list):
                        print("Invalid choice. Please enter a valid number.")
                    else:
                        selected_item = donated_items_list.pop(choice - 1)
                        print("You purchased: {}".format(selected_item))

                        if recipient_name not in purchased_items:
                            purchased_items[recipient_name] = []

                        purchased_items[recipient_name].append(selected_item)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")


while True:
    print("Please select an option:")
    print("1. Administrative Dashboard")
    print("2. Donor Dashboard")
    print("3. Recipient Dashboard")
    print("4. Exit")

    choice = input("Enter the number of your choice: ")

    if choice == '1':
        show_admin_dashboard()
        login()
    elif choice == '2':
        username = input("Enter your donor username: ")
        show_donor_dashboard(username)
    elif choice == '3':
        recipient_name = input("Enter your recipient name: ")
        recipient_password = input("Enter your recipient password: ")

        for name, credentials in recipient_credentials.items():
            if name == recipient_name and credentials['password'] == recipient_password:
                print("Authentication successful.")
                show_existing_recipient_dashboard(recipient_name)
                break
        else:
            print("Authentication failed. Please check your name and password.")
    elif choice == '4':
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please select a valid option (1, 2, 3, or 4).")
