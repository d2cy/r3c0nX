# r3c0nX - Recon and Enumeration Automation Tool
### Description

r3c0nX is a Python-based tool designed to automate basic reconnaissance and enumeration tasks for use in penetration testing, capture the flag (CTF) challenges, or similar scenarios. It streamlines the initial information-gathering phase by automating common tasks, allowing you to focus on more critical aspects of your assessment.
### Prerequisites

Before using r3c0nX, ensure that you have the following prerequisites installed on your system:
-   xterm
-   nmap
-   hydra
-   enum4linux
-   seclists
-   ffuf

## Installation

To install r3c0nX, follow these steps:

1. Clone this repository to your local machine.

    ```bash
    git clone https://github.com/d2cy/r3c0nX.git
    ```

2. Navigate to the project directory.
    ```bash
    cd r3c0nX
    ```
3. Install the tool using pip3.
    ```bash
    pip3 install .
    ```

#### **Note:**

> Edit Config Files in config folder to add Custom Tools/Wordlists before installing the tool.

> Default Config Files are provided for reference.

> Detailed instructions for creating custom config files are provided at the end of this document.




## Usage

Once r3c0nX is installed, you can use it as follows:
```bash
r3c0nX -m [MACHINE_NAME] -i [IP] -p [PATH]
```
- `-p` or `--path`: Path to create folders for organizing results.
- `-m` or `--machine`: Machine name or IP address.
- `-i` or `--ip`: Machine IP address.

**Path can be either absolute or relative.** 

Example:

```bash
r3c0nX -m TargetMachine -i 192.168.1.100 -p /path/to/folder
```
The tool will create a directory structure as follows:
```
Machine Name Folder (e.g., TargetMachine)
|
|____Enumeration
|
|____Exploits
|
|____Notes
|
|____Screenshots
|
|_____Others

```


## **About the Project**

r3c0nX is designed to simplify the initial phase of a penetration test or CTF challenge. Here's an overview of its functionality:

**Folder Structure:** The tool automatically creates a directory structure based on the machine name provided, organizing your files neatly.

**Port Scanning:** It scans for open ports on the target using nmap.

**NSE Scripting:** It runs nmap with NSE scripts based on the open ports and services detected, gathering additional information.

**Service-Specific Tools:** r3c0nX identifies services and runs relevant enumeration tools simultaneously using multithreading. For example, it uses ffuf for HTTP and hydra for FTP.

By automating these tasks and leveraging multithreading, r3c0nX helps you gather essential information efficiently, saving time and effort during your assessments.

## **Configuration Files**

r3c0nX provides a flexible way for users to customize and extend the tool's functionality by using configuration files. These configuration files are located in the config folder and are organized based on specific services or protocols. You can easily add your own tools and commands to tailor the reconnaissance and enumeration process to your requirements.

### **Creating Service-Specific Configuration Files**

**To add tools specific to a particular service or protocol, follow these steps:**

1. Navigate to the config folder in the r3c0nX directory.
2. Create a new configuration file with a .ini extension for the service you want to customize. 
    - For example, if you want to add tools for enumerating MySQL, create a mysql.ini file.

### **Defining Tools and Commands**

Inside the service-specific configuration file (e.g., mysql.ini), you can define the tools and commands you want to run under the [Tools] section. Here's an example of how to structure the configuration:

```ini
[General]
ip = **[BLANK]**
path = **[BLANK]**
machine = **[BLANK]**
port = **[BLANK]**

[Wordlist]
1 = Path Of Wordlist
2 = Path of Wordlist

[Tools]
1 = command1
2 = command2

```
#### Format of Command :

hydra -C `${Wordlist:1}` -o `${General:path}`/`${General:machine}`/enumeration/ftp_hydra.ftp -u `${General:ip}` ftp

## To-Do List
1.  **Expand Toolset**:
   
2. **Enhance Customization**:
   - Develop a user-friendly configuration system to allow easy customization of tools, their parameters, and order of execution.
   - Implement a modular approach for adding and configuring new tools.

3. **Report Generation Function**:
   - Create a function to generate comprehensive reports using the outputs of all tools used during reconnaissance and enumeration.
   - Provide options to export reports in various formats (e.g., HTML, PDF, plaintext).

4. **Modularize Code**:
   - Refactor the codebase into modular components, making it more organized, maintainable, and extensible.

5. **Optimize Multithreading**:

6. **Interactive Mode**:
   - Implement an interactive mode that allows users to choose which tools to run and configure them interactively.
   - Provide real-time feedback during the reconnaissance process.


