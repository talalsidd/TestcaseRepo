# --- 1. Credentials & Configuration ---
$Username = "YourUsername"
$Password = "YourPassword"
$ExePath  = "C:\Program Files\Windows Event Reporting"

# --- 2. Execute Configuration Commands ---
if (Test-Path $ExePath) {
    Set-Location -Path $ExePath
    Write-Host "Configuring Windows Event Reporting..." -ForegroundColor Cyan
    
    # Execute commands using the call operator (&)
    & .\ConfigurationCmd.exe -a $Username -p $Password -set fileHashingType 2
    & .\ConfigurationCmd.exe -a $Username -p $Password -set fileHashingScopeFlags 15
} else {
    Write-Warning "Directory not found: $ExePath"
}

# --- 3. Desktop Operations ---
$DesktopPath = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop")
$FolderName  = "TempAutomationFolder"
$FullFolderPath = Join-Path -Path $DesktopPath -ChildPath $FolderName

$FileName    = "DataFile.txt"
$NewFileName = "RenamedDataFile.txt"

# Create the folder
Write-Host "Creating folder: $FolderName" -ForegroundColor Yellow
New-Item -Path $FullFolderPath -ItemType Directory -Force

# Create a file and add content
$FilePath = Join-Path -Path $FullFolderPath -ChildPath $FileName
Set-Content -Path $FilePath -Value "This is the initial content of the file."
Write-Host "File created with content."

# Rename the file
#$NewFilePath = Join-Path -Path $FullFolderPath -ChildPath $NewFileName
Rename-Item -Path $FilePath -NewName $NewFileName
Write-Host "File renamed to: $NewFileName"

# Wait a moment so you can see it (Optional)
Start-Sleep -Seconds 2

# Delete the folder and everything inside it
Remove-Item -Path $FullFolderPath -Recurse -Force
Write-Host "Folder deleted successfully." -ForegroundColor Green