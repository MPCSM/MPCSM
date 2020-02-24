On the basis of starting rul and wafer, this file executes all decisions of fault and also iterates over all wafer, collecting data of wafer and fault at the same time.
1. Use under Linux system.
2. First, configure the device information we need to connect in the ssh_config file.
3. After configuration, open the makefile file.Go to the directory where the makefile file is located, and execute make net_config for SSH configuration to realize the no-secret login
![ssh](picture/2.png)
4. Then execute make run to start the program. 
![ssh](picture/1.png)