from psutil import TimeoutExpired
from hdl_graph_slam.srv import DumpGraph
from hdl_graph_slam.srv import SaveMap as hdl_SaveMap
from hector_nav_msgs.srv import GetRobotTrajectory
from tf.transformations import euler_from_quaternion
import roslaunch
import rospy
import csv
import glob
import subprocess
import shutil
import os


class RosInterface():
    def __init__(self):
        rospy.init_node('parkslam_gui', anonymous=True)

    def launch(self, algo_name, bag_path, input_method, lidar_ext):
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)

        file_str = "src/launch/" + algo_name + ".launch"
        bag_str = "bag_path:=" + bag_path
        input_str = "input_method:=" + input_method
        lidar_x_str = 'lidar_x_ext:=' + str(lidar_ext[0])
        lidar_y_str = 'lidar_y_ext:=' + str(lidar_ext[1])
        lidar_z_str = 'lidar_z_ext:=' + str(lidar_ext[2])

        cli_args = [file_str, bag_str, input_str, lidar_x_str,
                    lidar_y_str, lidar_z_str]
        roslaunch_args = cli_args[1:]
        roslaunch_ref = [
            (roslaunch.rlutil.resolve_launch_arguments(cli_args)[0], roslaunch_args)]

        self.launch_proc = roslaunch.parent.ROSLaunchParent(
            uuid, roslaunch_ref)
        self.launch_proc.start()
        rospy.loginfo("ParkSLAM: Started ROS Nodes")

    def stop(self):
        self.launch_proc.shutdown()

    def hector_traj_to_csv(self, out_path):
        try:
            traj_service = rospy.ServiceProxy(
                '/trajectory', GetRobotTrajectory)
            traj = traj_service()
            with open(out_path + "/poses.csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(("ts", "x", "y", "z", "roll", "pitch", "yaw"))
                for pose in traj.trajectory.poses:
                    # convert quaternion to roll pitch yaw
                    quaternion = (
                        pose.pose.orientation.x,
                        pose.pose.orientation.y,
                        pose.pose.orientation.z,
                        pose.pose.orientation.w)

                    euler = euler_from_quaternion(quaternion)
                    # normalise timestamp format
                    ts_temp = "{:d}{:09d}".format(
                        pose.header.stamp.secs, pose.header.stamp.nsecs)
                    writer.writerow((ts_temp, pose.pose.position.x,
                                    pose.pose.position.y, pose.pose.position.z, euler[0], euler[1], euler[2]))
                return True
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
            return False

    def hdl_graph_save(self, out_path):
        try:
            map_service = rospy.ServiceProxy(
                '/hdl_graph_slam/save_map', hdl_SaveMap)
            save_state = map_service(
                False, 0.05, out_path+"/map.pcd")
            return save_state
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
            return False

    def map_saver(self, out_path):
        fname = out_path + '/map'
        proc = subprocess.Popen(
            ['rosrun', 'map_server', 'map_saver', '-f', fname])
        try:
            return_code = proc.wait(timeout=30)
            return (return_code == 0)
        except subprocess.TimeoutExpired as e:
            print("Map saving timed out")
            proc.kill()
            return False

    def save_latest_pcd(self, out_path):
        # launch file saves all map files to /tmp, only move latest updated one
        map_files = list(glob.glob("/tmp/parkslam_rtab_*"))
        map_files.sort(key=lambda x: os.path.getmtime(x))
        shutil.copy2(map_files[0], out_path)
        return True
