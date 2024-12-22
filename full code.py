import pytesseract
from PIL import Image
import os
import re

# Set up the path for Tesseract (adjust the path according to your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # For Windows
# For macOS or Linux, you typically don't need to set this line if tesseract is in your PATH

def read_business_card(image_path):
    """
    Function to extract text from a business card image using Tesseract OCR.
    """
    try:
        # Open the image file using Pillow
        img = Image.open(image_path)

        # Use pytesseract to perform OCR on the image
        text = pytesseract.image_to_string(img)

        return text
    except Exception as e:
        print(f"Error processing image: {e}")
        return ""

def extract_contact_info(text):
    """
    Function to extract contact information (name, phone, email) from the OCR result.
    """
    contact_info = {
        'Name': '',
        'Job Title': '',
        'Company': '',
        'Phone': '',
        'Email': ''
    }

    # Define regex patterns for phone numbers and emails
    phone_pattern = re.compile(r'\+?(\d[\d\-\(\) ]{7,}\d)')
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    # Find phone and email matches in the OCR text
    phone_match = phone_pattern.findall(text)
    email_match = email_pattern.findall(text)

    # Extracting phone number and email
    if phone_match:
        contact_info['Phone'] = phone_match[0]
    if email_match:
        contact_info['Email'] = email_match[0]

    # Split the extracted text into lines and try to get Name, Job Title, and Company
    lines = text.split('\n')
    contact_info['Name'] = lines[0].strip() if len(lines) > 0 else 'Not Found'
    contact_info['Job Title'] = lines[1].strip() if len(lines) > 1 else 'Not Found'
    contact_info['Company'] = lines[2].strip() if len(lines) > 2 else 'Not Found'

    return contact_info

def process_images_in_folder(folder_path):
    """
    Process all images in the provided folder, extracting text and contact info.
    """
    # Get a list of all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    # Prepare a file to save the results
    output_file_path = os.path.join(folder_path, 'extracted_contacts.txt')

    with open(output_file_path, 'w') as output_file:
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            
            # Read text from the image
            extracted_text = read_business_card(image_path)
            if not extracted_text:
                continue

            # Extract contact information
            contact_info = extract_contact_info(extracted_text)

            # Write the extracted information to the output file
            output_file.write(f"--- Contact from {image_file} ---\n")
            for key, value in contact_info.items():
                output_file.write(f"{key}: {value}\n")
            output_file.write("\n")

    print(f"Extraction complete. Results saved to: {output_file_path}")

def main():
    # Folder containing the business card images
    folder_path = r'C:\Users\Siri Teja\Downloads\Test'  # Update with the correct folder path

    # Process all images in the folder
    process_images_in_folder(folder_path)

if __name__ == "__main__":
    main()
