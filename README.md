# Programming the microcontroller

These instructions apply to the Linux OS. Using windows is probably possible but untested. The package **dfu-util** should be installed. When connected to the USB cable the microcontroller is seen as a USB CDC device so it is mapped to a **/dev/tty** device, let's say **/dev/ttyACM0**.

To upload the file **test.bin**
  * Enter programming mode either by pressing twice within half a
    second the reset button, or by setting the line speed to 1200 baud with
	
	**stty 1200 -F /dev/ttyACM0**

	In programming mode the yellow led is pulsing.
	
  * upload the file *test.bin* with 
  
    **dfu-util -D test.bin -a0 -R**

# Sending commands to the microcontroller

Once programmed, the microcontroller remains a USB CDC device so any program that can open a tty device and send and receive characters can be used to send commands. Examples are **cutecom**, the serial package in Python or just plain C. Warning: to not open the device at 1200 baud, or you will trigger the update mode. 

All commands are two letters ascii characters, case insensitive, followed by parameters when required. Spaces are ignored. The device will respond with **OK** or **?** for a valid or invalid command, respectively. See the documentation of each program for a complete list.

As an alternative, a GUI based on PyQt is contained in the **python** directory. Run, i.e., *dds.py* with

**python dds.py**
  

