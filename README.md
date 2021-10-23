# Simulating CANBUS bits using UNIX tools

### modprobe the kernel to allow virtual `can`
```
sudo modprobe vcan
```

### create virtual `can` with:

```
sudo ip link add name vcan0 type vcan
sudo ip link set vcan0 mtu 72         # For CAN-FD
sudo ip link set dev vcan0 up
```


### limit datarate to <= 1 Mbit/s
```
sudo tc qdisc add dev vcan0 root tbf rate 300kbit latency 100ms burst 1000
```


### install candump and cangen
#### https://github.com/linux-can/can-utils
```
sudo apt install can-utils
```


### install a SocketCAN over Ethernet tunnel
#### https://github.com/mguentner/cannelloni
```
sudo apt install cannelloni
```
