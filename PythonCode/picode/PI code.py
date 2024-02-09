import os 

def encode(text, shift):
    encrypted_text = ""  # Initialize an empty string to store the encrypted text
    for char in text:  # Iterate through each character in the input text
        if char.isalpha():  # Check if the character is an alphabet
            shifted = ord(char) + shift  # Calculate the shifted value of the character
            if char.islower():  # Check if the character is lowercase
                if shifted > ord('z'):  # Check if the shifted value exceeds 'z'
                    shifted -= 26  # Wrap around the alphabet if it exceeds 'z'
                encrypted_text += chr(shifted)  # Append the encrypted character to the result
            elif char.isupper():  # Check if the character is uppercase
                if shifted > ord('Z'):  # Check if the shifted value exceeds 'Z'
                    shifted -= 26  # Wrap around the alphabet if it exceeds 'Z'
                encrypted_text += chr(shifted)  # Append the encrypted character to the result
        else:
            encrypted_text += char  # If the character is not an alphabet, append it as it is
    return encrypted_text  # Return the encrypted text

def decode(text, shift):# might end up moving this to the cloud-end 
    decrypted_text = ""  # Initialize an empty string to store the decrypted text
    for char in text:  # Iterate through each character in the input text
        if char.isalpha():  # Check if the character is an alphabet
            shifted = ord(char) - shift  # Calculate the shifted value of the character
            if char.islower():  # Check if the character is lowercase
                if shifted < ord('a'):  # Check if the shifted value is below 'a'
                    shifted += 26  # Wrap around the alphabet if it's below 'a'
                decrypted_text += chr(shifted)  # Append the decrypted character to the result
            elif char.isupper():  # Check if the character is uppercase
                if shifted < ord('A'):  # Check if the shifted value is below 'A'
                    shifted += 26  # Wrap around the alphabet if it's below 'A'
                decrypted_text += chr(shifted)  # Append the decrypted character to the result
        else:
            decrypted_text += char  # If the character is not an alphabet, append it as it is
    return decrypted_text  # Return the decrypted text

def check_user_id():
    script_directory = os.path.dirname(os.path.abspath(__file__))  # Get the directory path of the current script
    file_path = os.path.join(script_directory, 'user.ide')  # Create the file path for the user ID file
    
    if os.path.exists(file_path):  # Check if the user ID file already exists
        if os.path.getsize(file_path) == 0:  # Check if the file is empty
            user_id = input("Enter your user ID: ")  # Prompt the user to enter their user ID
            encrypted_user_id = encode(user_id, 7)  # Encrypt the user ID using Caesar cipher with shift 1
            with open(file_path, 'a') as file:  # Open the file in append mode
                file.write(encrypted_user_id + '\n')  # Write the encrypted user ID to the file
                print("User ID added successfully.")  # Print a success message
        else:
            print("User ID file already exists.")  # Print a message indicating the file already exists and is not empty
    else:
        user_id = input("Enter your user ID: ")  # Prompt the user to enter their user ID
        encrypted_user_id = encode(user_id, 7)  # Encrypt the user ID using Caesar cipher with shift 1
        with open(file_path, 'w') as file:  # Open the file in write mode (creates a new file if it doesn't exist)
            file.write(encrypted_user_id + '\n')  # Write the encrypted user ID to the file
            print("User ID file created and user ID added successfully.")  # Print a success message

# Example usage
check_user_id()  # Call the function to check user ID
