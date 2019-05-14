# ROS Package for communicating with Clearpath's Jackal robotic ground vehicle  
```
his package currently has node for providing tranform between odometry and base_link of jackal robot. 

Here, Jackal has ROS MASTER running and Desktop machine act as slave.
Laser Scan from Jackal is published over topic /scan and then used it over gmapping stack on desktop machine to produce a map of an environment.

```