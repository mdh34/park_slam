FROM osrf/ros:noetic-desktop-full
run apt update
RUN apt install -y build-essential software-properties-common git python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool ros-noetic-gmapping ros-noetic-hector-trajectory-server ros-noetic-map-server ros-noetic-laser-scan-matcher ros-noetic-slam-toolbox ros-noetic-pcl-ros ros-noetic-geodesy ros-noetic-nmea-msgs ros-noetic-libg2o ros-noetic-pointcloud-to-laserscan ros-noetic-rtabmap ros-noetic-rtabmap-ros ros-noetic-libnabo
RUN apt remove -y ros-noetic-rtabmap ros-noetic-rtabmap-ros

RUN mkdir -p /root/catkin_ws/src
WORKDIR /root/catkin_ws/src
RUN /bin/bash -c '. /opt/ros/noetic/setup.bash; catkin_init_workspace'
RUN git clone https://github.com/koide3/ndt_omp.git
RUN git clone https://github.com/SMRT-AIST/fast_gicp.git --recursive
RUN git clone https://github.com/koide3/hdl_graph_slam
WORKDIR /root/catkin_ws
RUN /bin/bash -c '. /opt/ros/noetic/setup.bash; catkin_make -DCMAKE_BUILD_TYPE=Release -j2'

RUN mkdir /root/src
WORKDIR /root/src
RUN git clone https://github.com/ethz-asl/libpointmatcher.git
RUN mkdir /root/src/libpointmatcher/build
WORKDIR /root/src/libpointmatcher/build
RUN /bin/bash -c '. /opt/ros/noetic/setup.bash; cmake .. && make && make install'

RUN add-apt-repository ppa:borglab/gtsam-release-4.0 
RUN apt update && apt install -y libgtsam-dev libgtsam-unstable-dev 
WORKDIR /root/src
RUN git clone https://github.com/introlab/rtabmap.git rtabmap
WORKDIR /root/src/rtabmap/build 
RUN /bin/bash -c '. /opt/ros/noetic/setup.bash; cmake .. && make -j2 && make install'

WORKDIR /root/catkin_ws
RUN git clone https://github.com/introlab/rtabmap_ros.git src/rtabmap_ros
RUN /bin/bash -c '. /opt/ros/noetic/setup.bash; catkin_make -DCMAKE_BUILD_TYPE=Release -j2'
RUN sed -i "6i source \"/root/catkin_ws/devel/setup.bash\"" /ros_entrypoint.sh

COPY . /root/park_slam/
WORKDIR /

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
