#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "tf2_ros/buffer.h"
#include "tf2_ros/transform_listener.h"

class TFListener : public rclcpp::Node
{
public:
  TFListener() : Node("tf_listener")
  {
    tf_buffer_ = std::make_shared<tf2_ros::Buffer>(this->get_clock());
    tf_listener_ = std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);
    timer_ = this->create_wall_timer(
      std::chrono::seconds(1),
      std::bind(&TFListener::timer_callback, this));
  }

private:
  void timer_callback()
  {
    try {
      auto trans = tf_buffer_->lookupTransform(
        "base_link", "laser_link", tf2::TimePointZero);
      auto translation = trans.transform.translation;
      auto rotation = trans.transform.rotation;
      RCLCPP_INFO(this->get_logger(),
        "laser_link相对base_link: 平移 x=%.3f, y=%.3f, z=%.3f, 旋转(四元数) z=%.3f, w=%.3f",
        translation.x, translation.y, translation.z, rotation.z, rotation.w);
    } catch (tf2::TransformException & ex) {
      RCLCPP_WARN(this->get_logger(), "暂时查不到TF，请确认广播者已启动: %s", ex.what());
    }
  }

  std::shared_ptr<tf2_ros::Buffer> tf_buffer_;
  std::shared_ptr<tf2_ros::TransformListener> tf_listener_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char *argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<TFListener>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
