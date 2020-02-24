EDGES :=wym nano ljr minserver cloud raspberryrul raspberrywafer raspberryfault #Equipment used
se :=raspberryrul raspberrywafer raspberryfault # Three raspberry pies to store the data source
mix :=  raspberryrul raspberrywafer #Except for the fault, the other two raspberry pies
db:=wym #The edge collects the data
db1:=cloud #The cloud collects the data
net_config:	 #SSH security - free login
	@cp ./ssh_config ~/.ssh/config && chmod 600 ~/.ssh/config  
	@-ssh-keygen  
	@for server in $(EDGES) ; do \
		echo "Make password free configuration in $$server";\
		ssh-copy-id $$server; #copy id\
	done
run:
	@for w in `seq 0 68`;do #Traverse the number of decisions on the wafer\
		echo $$w >> date.csv; #Output the current system time to the data.csv file\
		FILE1=divice.sh; 
		#Here is the action to start the fault database
		ssh ${db} bash -c "'cd ~/code/storeResult/wafer$$w-fault; #Connect to wym's computer via SSH, and then go under that directory\
		echo $$FILE1;\
		if [ -f $$FILE1 ]; then #Determines if the file divice.sh under the current directory exists, and if so, launches it\
			echo "in";\
			chmod +x ./$$FILE1;\
			./$$FILE1;\
		fi '"
		ssh ${db1} bash -c "'cd /root/wym/code/storeResult/wafer$$w-fault; #Connect to the cloud and go to the directory\
		echo $$FILE1;\
		if [ -f $$FILE1 ]; then\
			echo "in";\
			chmod +x ./$$FILE1;\
			./$$FILE1;\
		fi '"  
		#Since there are 68 wafer files in the fault, the number of decisions under each wafer file is different, so go into this directory, and then query how many decisions there are, and return
		ssh ${db} bash -c "'cd ~/code/fault/wafer$$w
		m=`ls -l |grep "^d"|wc -l`'"
		for f in `seq 0 $$m`;do    #Traverse each decision under the wafer\
			FILE1=divice.sh;
			#Here's how to start collecting data for the wafer database
			ssh ${db} bash -c "'cd ~/code/storeResult/wafer$$w-fault$$f; #Connect wym via SSH to this directory and launch the.sh file\
			echo $$FILE1;\
			if [ -f $$FILE1 ]; then\
				echo "in";\
				chmod +x ./$$FILE1;\
				./$$FILE1;\
			fi '"
			FILE2=divice.sh;
			ssh ${db1} bash -c "'cd /root/wym/code/storeResult/wafer$$w-fault$$f; #Connect wym via SSH to this directory and launch the.sh file\
			echo $$FILE2;\
			if [ -f $$FILE2 ]; then\
				echo "in";\
				chmod +x ./$$FILE2;\
				./$$FILE2;\
			fi '"
			#Three experiments were started in turn
			# The startup sequence is to start Remaining Useful Life Prediction, then Defect election, and finally Fault Detection 
			for s in $(se);do  \
				if [ $$s = "raspberryrul" ];then #If it's Remaining Useful Life Prediction, start going into the cloud and start all the containers\
					for i in `seq 3 3`;do\
						for server in $(EDGES) ; do\
							if [ $$server = "cloud" ]; then #If the device is a cloud, go to the boot.sh file\
								j=3; #3 represents the cloud, where nano is 0, Laptop computer is 1, and miniserver is 2\
								FILE=device$$i$$j.sh;\
								ssh $$server bash -c  "'cd /root/wym/code/rul/clouddecision$$i;\
								echo $$FILE;\
								if [ -f $$FILE ]; \
								then \
									chmod +x ./$$FILE;\
									./$$FILE;\
								fi '"
							fi
							if [ $$server = "raspberryrul" ];then\
								FILE=sourcecloud60.sh;\
								ssh $$server bash -c  "'cd ~/code/rul/clouddecision$$i; #Start the container on the raspberry pie\
								if [ -f $$FILE ]; \
									then \
									echo "in";\
									chmod +x ./$$FILE;  #Add permissions to the execution of the file\
									./$$FILE;\
								fi '"
							fi 
						done
					done	
				fi
				if [ $$s = "raspberrywafer" ];then #Start the Defect Delection to determine which device each container is on\
					for server in $(EDGES) ; do\
						if [ $$server = "nano" ]; then \
							j=0;\
							FILE=device$$w$$j.sh;\
							ssh $$server bash -c "'cd ~/code/wafer/decision$$w;Enter the nano to determine if the file is available, and if so, execute the.sh file \
							if [ -f $$FILE ]; then\
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi 
						if [ $$server = "cloud" ];then\
							j=3;\
							FILE=device$$w$$j.sh;\
							ssh $$server bash -c "'cd /root/wym/code/wafer/decision$$w; #Enter the cloud to determine if the file is available, and if so, execute the.sh file\
							if [ -f $$FILE ]; \
							then \
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi
						if [ $$server = "minserver" ]; then #Enter the miniserver  to determine if the file is available, and if so, execute the.sh file\
							j=2;\
							FILE=device$$w$$j.sh;\
							ssh $$server bash -c  "'cd ~/wym/code/wafer/decision$$w; \
						
							if [ -f $$FILE ]; then \
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi
						if [ $$server = "ljr" ];then\
							j=1;\
							FILE=device$$w$$j.sh;\
							ssh $$server bash -c "'cd ~/code/wafer/decision$$w;  #Enter the Laptop computer to determine if the file is available, and if so, execute the.sh file\
						
							if [ -f $$FILE ]; then \
							chmod +x ./$$FILE;\
							./$$FILE;\
							fi '"
						fi 
						if [ $$server = "raspberrywafer" ];then\
							FILE=source25.sh;\
							ssh $$server bash -c  "'cd ~/code/wafer/decision$$w; #Enter the raspberry to determine if the file is available, and if so, execute the.sh file\
							echo "wafer";\
							echo $$FILE;\
							if [ -f $$FILE ]; \
								then \
			
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi 
					done	
				fi
				if [ $$s = "raspberryfault" ];then  \
					for server in $(EDGES) ; do\
						if [ $$server = "nano" ]; then \
							j=0;\
							FILE=device$$f$$j.sh;\
							ssh $$server bash -c "'cd ~/code/fault/wafer$$w/decision$$f;\
							echo "fault";\
							echo $$FILE;\
							if [ -f $$FILE ]; then\
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi 
						if [ $$server = "minserver" ]; then\
							j=2;\
							FILE=device$$f$$j.sh;\
							ssh $$server bash -c  "'cd ~/wym/code/fault/wafer$$w/decision$$f;\
							echo "fault";\
							echo $$FILE;\
							if [ -f $$FILE ]; then \
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi
						if [ $$server = "ljr" ];then\
							j=1;\
							FILE=device$$f$$j.sh;\
							ssh $$server bash -c "'cd ~/code/fault/wafer$$w/decision$$f;\
							echo "fault";\
							echo $$FILE;\
							if [ -f $$FILE ]; then \
							chmod +x ./$$FILE;\
							./$$FILE;\
							fi '"
						fi 
						if [ $$server = "cloud" ];then\
							j=3;\
							FILE=device$$f$$j.sh;\
							ssh $$server bash -c "'cd /root/wym/code/fault/wafer$$w/decision$$f;\
							echo "fault";\
							echo $$FILE;\
							if [ -f $$FILE ]; \
							then \
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi
						if [ $$server = "raspberryfault" ];then\
							FILE=source10.sh;\
							ssh $$server bash -c  "'cd ~/code/fault/wafer$$w/decision$$f;\
							echo "fault";\
							echo $$FILE;\
							if [ -f $$FILE ]; \
								then \
								echo "in";\
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi 
						if [ $$server = "raspberryfault" ];then \
							echo $$w >> date.csv; \
							echo $$f >> date.csv;\
							echo "`date`" >> date.csv ; #Write the start time of the program to the date.csv file\
							echo "sleep";\
							sleep 120; #Sleep for 2 minutes \
							echo "`date`";\
							echo "`date`" >> date.csv ; #Write the time after the sleep is complete to the date.csv file\
							FILE=sourcedown10.sh; #Stop the container on the raspberry pie\
							ssh $$server bash -c  "'cd ~/code/fault/wafer$$w/decision$$f;\
							if [ -f $$FILE ]; then \
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi 
					done
					#Stop the container that Fault Detection is in on the other device, go to the device directory, and execute the.sh file
					for server in $(EDGES) ; do\
						if [ $$server = "nano" ]; then \
							j=0;\
							FILE=down$$f$$j.sh;\
							ssh $$server bash -c "'cd ~/code/fault/wafer$$w/decision$$f;\
							echo "fault";\
							echo $$FILE;\
							if [ -f $$FILE ]; then\
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi 
						if [ $$server = "minserver" ]; then\
							j=2;\
							FILE=down$$f$$j.sh;\
							ssh $$server bash -c  "'cd ~/wym/code/fault/wafer$$w/decision$$f;\
							echo "fault";\
							echo $$FILE;\
							if [ -f $$FILE ]; then \
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi
						if [ $$server = "ljr" ];then\
							j=1;\
							FILE=down$$f$$j.sh;\
							ssh $$server bash -c "'cd ~/code/fault/wafer$$w/decision$$f;\
							echo "fault";\
							echo $$FILE;\
							if [ -f $$FILE ]; then \
							chmod +x ./$$FILE;\
							./$$FILE;\
							fi '"
						fi 
						if [ $$server = "cloud" ];then\
							j=3;\
							FILE=down$$f$$j.sh;\
							ssh $$server bash -c "'cd /root/wym/code/fault/wafer$$w/decision$$f;\
							echo "fault";\
							echo $$FILE;\
							if [ -f $$FILE ]; \
							then \
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi
					done	
				fi
			done
			#The following code is the code for down Defect Delection  and  Fault Detection 
			for d in $(mix);do\
				if [ $$d = "raspberryrul" ];then\
					for i in `seq 3 3`;do\
						for server in $(EDGES) ; do\
							if [ $$server = "cloud" ]; then\
								j=3;\
								echo "进入";\
								FILE=down$$i$$j.sh;\
								ssh $$server bash -c  "'cd /root/wym/code/rul/clouddecision$$i;\
								echo "rul";\
								echo $$FILE;\
								if [ -f $$FILE ]; \
								then \
									chmod +x ./$$FILE;\
									./$$FILE;\
								fi '"
							fi
							if [ $$server = "raspberryrul" ];then\
								FILE=sourcedowncloud60.sh;\
								ssh $$server bash -c  "'cd ~/code/rul/clouddecision$$i;\
								echo "rul";\
								echo $$FILE;\
								if [ -f $$FILE ]; \
									then \
									echo "in";\
									chmod +x ./$$FILE;\
									./$$FILE;\
								fi '"
							fi 
						done
					done
				fi	
				#Stop the Defect Delection container on the raspberry pie
				if [ $$d = "raspberrywafer" ];then\
					for server in $(EDGES) ; do\
						if [ $$server = "raspberrywafer" ];then\
							FILE=sourcedown25.sh;\
							ssh $$server bash -c  "'cd ~/code/wafer/decision$$w;\
							echo "wafer";\
							echo $$FILE;\
							if [ -f $$FILE ]; \
								then \
								echo "in";\
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi 
						if [ $$server = "nano" ]; then \
							j=0;\
							FILE=down$$w$$j.sh;\
							ssh $$server bash -c "'cd ~/code/wafer/decision$$w;\
							echo "wafer";\
							echo $$FILE;\
							if [ -f $$FILE ]; then\
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi 
						if [ $$server = "minserver" ]; then\
							j=2;\
							FILE=down$$w$$j.sh;\
							ssh $$server bash -c  "'cd ~/wym/code/wafer/decision$$w;\
							echo "wafer";\
							echo $$FILE;\
							if [ -f $$FILE ]; then \
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi
						if [ $$server = "ljr" ];then\
							j=1;\
							FILE=down$$w$$j.sh;\
							ssh $$server bash -c "'cd ~/code/wafer/decision$$w;\
							echo "wafer";\
							echo $$FILE;\
							if [ -f $$FILE ]; then \
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi 
						if [ $$server = "cloud" ];then\
							j=3;\
							FILE=down$$w$$j.sh;\
							ssh $$server bash -c "'cd /root/wym/code/wafer/decision$$w;\
							echo "wafer";\
							echo $$FILE;\
							if [ -f $$FILE ]; \
							then \
								chmod +x ./$$FILE;\
								./$$FILE;\
							fi '"
						fi
					done		
				fi
			done
			#Stop the Defect Delection collection container
			FILE1=down.sh;
			ssh ${db} bash -c "'cd ~/code/storeResult/wafer$$w-fault$$f;\
			echo "wafer";\
			echo $$FILE1;\
			if [ -f $$FILE1 ]; then\
				echo "in";\
				chmod +x ./$$FILE1;\
				./$$FILE1;\
			fi '"
			FILE2=down.sh;
			ssh ${db1} bash -c "'cd /root/wym/code/storeResult/wafer$$w-fault$$f;\
			echo $$FILE2;\
			if [ -f $$FILE2 ]; then\
				echo "in";\
				chmod +x ./$$FILE2;\
				./$$FILE2;\
			fi '"
		done
		# Stop the  Fault Detection collection container
		FILE2=down.sh;
		ssh ${db1} bash -c "'cd /root/wym/code/storeResult/wafer$$w-fault;\
		echo $$FILE2;\
		if [ -f $$FILE2 ]; then\
			echo "in";\
			chmod +x ./$$FILE2;\
			./$$FILE2;\
		fi '"
		FILE1=down.sh;
		ssh ${db} bash -c "'cd ~/code/storeResult/wafer$$w-fault;\
		echo $$FILE1;\
		if [ -f $$FILE1 ]; then\
			echo "in";\
			chmod +x ./$$FILE1;\
			./$$FILE1;\
		fi '"
	done


	
		
		
		
			
	

