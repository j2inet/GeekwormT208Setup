#General Update
sudo apt-get update
sudo apt-get upgrade


#Ensure Python is present
sudo apt-get install python-pip

#Install GPIO
sudo pip install Jetson.GPIO

#Install I2C dev library
sudo apt-get install libi2c-dev i2c-tools
pip install smbus

#detect i2c devices
#T208 should be at address 0x36
sudo i2cdetect -y -r 1


#Install management scripts
wget https://wiki.geekworm.com/images/c/c2/Bat.py --no-check-certificate
wget https://wiki.geekworm.com/images/8/8d/Pld.py --no-check-certificate