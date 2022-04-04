# Park_SLAM
An implementation of multiple SLAM algorithms for parking testing.

## Algorithms:
Supports:
 - `gmapping`
 - `hdl_graph_slam`
 - `slam_toolbox`
 - `RTAB-MAP`

 ## Data:
 
 Supports ROS bag data with PointCloud messages, or live Hesai LiDAR data.

 PointCloud messages are expected on any of the following topics:
 - `/kitti/velo/pointcloud`
 - `/hesai/pandar`
 - `/cloud`

 ## Installation:
 A full ROS Noetic Desktop installation is expected, with the following packages:

- `ros-noetic-gmapping`
- `ros-noetic-hector-trajectory-server`
- `ros-noetic-map-server` 
- `ros-noetic-laser-scan-matcher`
- `ros-noetic-slam-toolbox`
- `ros-noetic-pcl-ros` 
- `ros-noetic-pointcloud-to-laserscan`



`hdl_graph_slam` should be installed from source using the following instructions: https://github.com/koide3/hdl_graph_slam#requirements


`rtab-map` and `rtabmap_ros` should be built from source with support for `libpointmatcher` using the following instructions: https://github.com/introlab/rtabmap_ros#build-from-source (The standard ROS versions can be used, but have much poorer performance with LiDAR sensors)

## Docker
Alternatively, the included Dockerfile can be used to automatically set up the required environment by running `"docker build -t park-slam ."` in the source folder.

 This is fully compatible with WSL to allow the program to be ran on Windows.

After this, the environment can be opened using:

`"docker run -a stdin -a stdout -i -t -e DISPLAY=host.docker.internal:0.0 -v "C:\:/data"park-slam /bin/bash"`

(note that C:\\ can be replaced by any drive/directory you want to share with the container)

Graphical workarounds for the container may vary by platform and version (i.e. WSL)

## Running
After the environment has been correctly set up, copy the source folder to your home directory (`~/`), change your current directory to the `park_slam` folder, and run `python3 ./src/main.py` to start the application. 

The application assumes an instance of `roscore` is already running.




