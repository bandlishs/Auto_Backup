def create_zip(path, file_name):
    # use shutil to create a zip file
    try:
        shutil.make_archive(f"archive/{file_name}", 'zip', path)
        return True
    except FileNotFoundError as e:
        return False
        
        
def google_auth():
    gauth = GoogleAuth() 
    # use local default browser for authentication
    gauth.LocalWebserverAuth()        
    drive = GoogleDrive(gauth) 
    return gauth, drive
    
    
def upload_backup(drive, path, file_name):
    # create a google drive file instance with title metadata
    f = drive.CreateFile({'title': file_name}) 
    # set the path to zip file
    f.SetContentFile(os.path.join(path, file_name)) 
    # start upload
    f.Upload() 
    # set f to none because of a vulnerability found in PyDrive
    f = None
    
    
def controller():
    # folder path to backup
    path = r"/home/user/Desktop/gdrive-file-backup/backup_me"
    # get machine date and time
    now = datetime.now()
    # new backup name
    file_name = "backup " + now.strftime(r"%d/%m/%Y %H:%M:%S").replace('/', '-')
    # if zip creation fails then abort execution
    if  not create_zip(path, file_name):
        sys.exit(0)
    # start API authentication
    auth, drive = google_auth()
    # start file upload
    upload_backup(drive, r"/home/user/Desktop/gdrive-file-backup/archive", file_name+'.zip')
    
    
    if __name__=="__main__":
    # set 12:00 am as time to trigger controller()
    schedule.every().day.at("00:00").do(controller)
    # check for pending tasks and execute if any
    while True:
        schedule.run_pending()
