# Read data from CSV file
import os
import csv
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.folder import Folder

# Credentials for source SharePoint site
source_username = input("Enter source SharePoint username: ")
source_password = input("Enter source SharePoint password: ")

# Credentials for destination SharePoint site
destination_username = input("Enter destination SharePoint username: ")
destination_password = input("Enter destination SharePoint password: ")

# Get CSV file path from user input
csv_file_path = input("Enter path to the CSV file: ")

# Read data from CSV file
print("\nProcessing CSV file...")
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)  # Read header row
    source_site_column = header.index("Source Site")  # Index of the column containing source site URLs in the CSV
    destination_site_column = header.index("Destination Site")  # Index of the column containing destination site URLs in the CSV
    
    for row in csv_reader:
        source_site_name = row[source_site_column].strip()  # Assuming this is the site name like '3070CONTRACT'
        destination_site_name = row[destination_site_column].strip()

        # Source and destination folder paths
        source_folder_path = f"/sites/{source_site_name}/Shared Documents/"
        destination_folder_path = f"/sites/{destination_site_name}/Shared Documents/"

        print(f"\nProcessing link pair:")
        print(f"Source Site: {source_url + source_folder_path}")
        print(f"Destination Site: {destination_url + destination_folder_path}")

        # Download entire folder from source site
        source_ctx_auth = AuthenticationContext(source_url)
        source_ctx_auth.acquire_token_for_user(source_username, source_password)
        source_ctx = ClientContext(source_url, source_ctx_auth)
        source_folder = source_ctx.web.get_folder_by_server_relative_url(source_folder_path)
        source_ctx.load(source_folder)
        source_ctx.execute_query()

        # Upload folder to destination site
        destination_ctx_auth = AuthenticationContext(destination_url)
        destination_ctx_auth.acquire_token_for_user(destination_username, destination_password)
        destination_ctx = ClientContext(destination_url, destination_ctx_auth)
        destination_folder = destination_ctx.web.get_folder_by_server_relative_url(destination_folder_path)

        # Create destination folder if it doesn't exist
        if not destination_folder.exists:
            destination_folder = Folder.create_folder(destination_ctx, destination_folder_path)
            destination_ctx.execute_query()

     # Copy files from source to destination folder
        for file in source_folder.files:
            file_path = os.path.join(source_folder_path, file.properties["Name"])
            response = File.open_binary(source_ctx, file_path)
            target_file_path = os.path.join(destination_folder_path, file.properties["Name"])
            File.save_binary(destination_ctx, target_file_path, response.content)


            # Compare file versions and upload only if newer version exists in the source site
            if target_file.exists and target_file.time_last_modified < source_ctx.web.get_file_by_server_relative_path(target_file_path).time_last_modified:
                with open(temp_file_path, 'rb') as content_file:
                    file_content = content_file.read()

             # Upload file to destination site
                File.save_binary(destination_ctx, target_file_path, file_content)  # upload the file

        # Clean up temporary file
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

print("\nProcessing completed.")
