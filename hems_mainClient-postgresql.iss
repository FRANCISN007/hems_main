; Script for Hotel and Event Management System Installer
#define MyAppName "Hotel and Event Management Sys"
#define MyAppVersion "1.5"
#define MyAppPublisher "School of Accounting Package"
#define MyAppURL "https://www.example.com/"
#define MyAppExeName "start.py"
#define PostgreSQLInstaller "postgresql-15.11-1-windows-x64.exe"   ; Adjust this to match the correct version
#define PostgreSQLDataDir "{commonappdata}\PostgreSQL\data"
#define PostgreSQLPort "5432"
#define PostgreSQLPassword "REPOMAN"  ; Change this to a secure password

[Setup]
PrivilegesRequired=admin
AppId={{7C26CBC0-0FD9-4943-9A21-2204ED49422F}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=C:\Users\KLOUNGE\Documents\HEMS-main\license.txt
OutputDir=C:\Users\KLOUNGE\Desktop
OutputBaseFilename=hems-postg
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\KLOUNGE\Documents\HEMS-main\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\KLOUNGE\Downloads\{#PostgreSQLInstaller}"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\env\Scripts\python.exe"; Parameters: """{app}\start.py"""
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\env\Scripts\python.exe"; Parameters: """{app}\start.py"""; Tasks: desktopicon

[Run]
; Install PostgreSQL silently
Filename: "{tmp}\{#PostgreSQLInstaller}"; Parameters: "--mode unattended --unattendedmodeui minimal --superpassword {#PostgreSQLPassword} --serverport {#PostgreSQLPort} --datadir {#PostgreSQLDataDir}"; Flags: waituntilterminated runhidden

; Open firewall for PostgreSQL
Filename: "netsh"; Parameters: "advfirewall firewall add rule name=""PostgreSQL"" dir=in action=allow protocol=TCP localport={#PostgreSQLPort}"; Flags: runhidden

; Open firewall for the hotel application
Filename: "netsh"; Parameters: "advfirewall firewall add rule name=""HEMS"" dir=in action=allow protocol=TCP localport=8000"; Flags: runhidden

; Run the application
Filename: "{app}\env\Scripts\python.exe"; Parameters: """{app}\start.py"""; WorkingDir: "{app}"; Flags: nowait runminimized
