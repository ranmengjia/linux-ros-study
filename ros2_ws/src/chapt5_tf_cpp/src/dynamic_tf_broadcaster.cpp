#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2_ros/transform_broadcaster.h"

class DynamicTFBroadcaster : public rclcpp::Node
{
public:
  DynamicTFBroadcaster() : Node("dynamic_tf_broadcaster")
  {
    tf_broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);
    timer_ = this->create_wall_timer(
      std::chrono::milliseconds(10),
      std::bind(&DynamicTFBroadcaster::timer_callback, this));
  }

private:
  void timer_callback()
  {
    geometry_msgs::msg::TransformStamped t;
    t.header.stamp = this->get_clock()->now();
    t.header.frame_id = "base_link";
    t.child_frame_id = "laser_link";

    t.transform.translation.x = 0.0;
    t.transform.translation.y = 0.0;
    t.transform.translation.z = 0.1;

    double now = this->get_clock()->now().nanoseconds() * 1e-9;
    double angle = std::fmod(now, 2 * M_PI);
    tf2::Quaternion q;
    q.setRPY(0.0, 0.0, angle);
    t.transform.rotation.x = q.x();
    t.transform.rotation.y = q.y();
    t.transform.rotation.z = q.z();
    t.transform.rotation.w = q.w();

    tf_broadcaster_->sendTransform(t);
  }

  std::shared_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char *argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<DynamicTFBroadcaster>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
