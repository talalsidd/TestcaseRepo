import winrm

# Connection details
host = 'qa-w1124h2-3.eng.dtexsystems.com'  # e.g., '192.168.1.100'
username = 'dtexsystems\\talal.siddiqui'  # e.g., 'dtexsystems\\admin'
password = 'Ayeshafatima@2021'

# Create a session
session = winrm.Session(host, auth=(username, password), transport='ntlm')

# Run a command (e.g., get system info)
result = session.run_cmd('systeminfo')

# Print output
print("STDOUT:", result.std_out.decode('utf-8'))
print("STDERR:", result.std_err.decode('utf-8'))
print("Status Code:", result.status_code)