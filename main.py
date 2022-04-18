from __future__ import print_function
import pickle
import os.path
import io
from re import X
import shutil
import requests
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
  
class DriveAPI:
    global SCOPES
      
    # Define the scopes
    SCOPES = ['https://www.googleapis.com/auth/drive']
  
    def __init__(self):       
        self.creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
  
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('./credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
  
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
        self.service = build('drive', 'v3', credentials=self.creds)
  
        results = self.service.files().list(
            pageSize=100, fields="files(id, name)").execute()
        items = results.get('files', [])
        print("Here's a list of files: \n")
        print(*items, sep="\n", end="\n\n")
  
    def FileDownload(self, file_id, file_name):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
          
        # Initialise a downloader object to download the file
        downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
        done = False
  
        try:
            # Download the data in chunks
            while not done:
                done = downloader.next_chunk()
  
            fh.seek(0)
              
            # Write the received data to the file
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(fh, f)
  
            print("File Downloaded")
            # Return True if file Downloaded successfully
            return True
        except:
            
            # Return False if something went wrong
            print("Something went wrong.")
            return False
  
    def FileUpload(self, filepath):
        
        # Extract the file name out of the file path
        name = filepath.split('/')[-1]
          
        # Find the MimeType of the file
        mimetype = MimeTypes().guess_type(name)[0]
          
        # create file metadata
        file_metadata = {'name': name}
  
        try:
            media = MediaFileUpload(filepath, mimetype=mimetype)
              
            # Create a new file in the Drive storage
            file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            
            print("File Uploaded.")
          
        except:
              
            # Raise UploadError if file is not uploaded.
            print("Can't Upload File.")
  
if __name__ == "__main__":
    obj = DriveAPI()
    x = int(input("Enter your choice: 1 - Download file, 2- Upload File, 3- Exit.\n"))
      
    if x == 1:
        f_id = input("Enter file id: ")
        f_name = input("Enter file name: ")
        obj.FileDownload(f_id, f_name)
          
    elif x == 2:
        f_path = input("Enter full file path: ")
        obj.FileUpload(f_path)
      
    else:
        exit()