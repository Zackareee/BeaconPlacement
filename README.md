# BeaconPlacement
Generate Minecraft beacon circles accurately. 
Places points on integer coordinates in an equal distribution around an origin.

In response to the [Youtube video](https://youtu.be/VcsEm7FnheU?si=LSM72IzqdgnMjRc_) where beacons are shown to be best placed in a non-circular pattern, I have put together a python module to do exactly that in a variable fashion. 

Here we can see a placement of 96 points around the origin with a minimum radius of 16 and a maximum radius of 20. 

<img width="500" alt="Screenshot 2024-08-08 at 6 32 50 pm" src="https://github.com/user-attachments/assets/4de789e5-1811-4345-b6d1-2782eceb6e7e">

The red lines here simply show the equal distribution of points around the origin. 
This graph can be viewed [here](https://www.desmos.com/calculator/j6ghmovccm).

The same set of coordinates can be generated using a count of 96, and the appropriate minimum and maximum values.
```
import coordinate_placement from beacon_placer
coordinates = coordinate_placement(count=96, minimum=30, maximum=45)
print(coordinates) # (31, 2), (38, 5), (30, 6), (41, 11), (41, 14), (41, 17), (30, 15), ...]
```

In the case you have a desired centerpoint, say (500,500) the origin can be changed with the offset keyword.
```
coordinaes = coordinate_placement(count=96, offset=[500,500], minimum=30, maximum=45)
```
A more legible example can be seen here of 12 points between a radius of 10 and 12 from 0,0. Note the points are as at the closest integer coordinate to the line without sacrificing accuracy. 

<img width="500" alt="Screenshot 2024-08-08 at 3 49 31 pm" src="https://github.com/user-attachments/assets/c8956ec9-3df0-4fe6-bb09-a4fbd795c016">
