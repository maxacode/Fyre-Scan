import os 


def check_user_id():
    script_directory = os.path.dirname(os.path.abspath(__file__))  # Get the directory path of the current script
    file_path = os.path.join(script_directory, 'user.ide')  # Create the file path for the user ID file
    
    if os.path.exists(file_path):  # Check if the user ID file already exists
        if os.path.getsize(file_path) == 0:  # Check if the file is empty
            user_id = input("Enter your user ID: ")  # Prompt the user to enter their user ID
            with open(file_path, 'a') as file:  # Open the file in append mode
                file.write(user_id + '\n')  # Write the encrypted user ID to the file
                print("User ID added successfully.")  # Print a success message
        else:
            print("User ID file already exists.")  # Print a message indicating the file already exists and is not empty
    else:
        user_id = input("Enter your user ID: ")  # Prompt the user to enter their user ID
        with open(file_path, 'w') as file:  # Open the file in write mode (creates a new file if it doesn't exist)
            file.write(user_id + '\n')  # Write the encrypted user ID to the file
            print("User ID file created and user ID added successfully.")  # Print a success message

check_user_id()  # Call the function to check user ID
