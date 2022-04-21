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
        # File token.pickle lưu trữ các mã truy cập và làm mới của token, và
        # được tạo tự động khi cấp quyền hoàn tất trong lần đầu tiên

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
        print("Files có trong drive: \n")
        print(*items, sep="\n", end="\n\n")
  
    def FileDownload(self, file_id, file_name):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
          
        # Khởi tạo đối tượng tải xuống để tải tệp xuống
        downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
        done = False
  
        try:
            # Tải xuống dữ liệu theo từng phần
            while not done:
                done = downloader.next_chunk()
  
            fh.seek(0)
              
            # Ghi dữ liệu đã nhận vào tệp
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(fh, f)
  
            print("File tai ve thanh cong")
            # Nếu file tải về thành công in như trên
            return True
        except:  
            print("Không tải được file.")
            # Nếu file tải về thành công in như trên
            return False
  
    def FileUpload(self, filepath):
        
        # Giải nén tên tệp ra khỏi đường dẫn tệp
        name = filepath.split('/')[-1]
          
        # Tìm MimeType của file
        mimetype = MimeTypes().guess_type(name)[0]
          
        # Tạo file metadata
        file_metadata = {'name': name}
  
        try:
            media = MediaFileUpload(filepath, mimetype=mimetype)
              
            # Tạo file mới trong drive
            file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            
            print("File da tai len.")
          
        except:
              
            print("Khong tai duoc file len.")
            # Nếu file không tải lên được
if __name__ == "__main__":
    obj = DriveAPI()
    x = int(input("Enter your choice: 1 - Tải file về máy, 2- Tải file lên drive, 3- Thoát.\n"))
      
    if x == 1:
        f_id = input("Nhap file id: ")
        f_name = input("Nhap tên file: ")
        obj.FileDownload(f_id, f_name)
          
    elif x == 2:
        f_path = input("Nhập địa chỉ đầy đủ của file: ")
        obj.FileUpload(f_path)
      
    else:
        exit()