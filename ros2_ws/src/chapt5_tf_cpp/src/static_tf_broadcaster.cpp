#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2_ros/static_transform_broadcaster.h"

class StaticTFBroadcaster : public rclcpp::Node
{
    public:
        StaticTFBroadcaster() : Node("static_tf_broadcaster")
        {
            tf_broadcaster_ = std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);
            geometry_msgs::msg::TransformStamped t;
            t.header.stamp = this->get_clock()->now();
            t.header.frame_id = "base_link";
            t.child_frame_id = "laser_link";
            t.transform.translation.x = 0.0 ;
            t.transform.translation.y = 0.0 ;
            t.transform.translation.z = 0.1 ;

            tf2::Quaternion q;
            q. setRPY ( 0.0 , 0.0 , 0.0 );
            t.transform.rotation.x = q. x ();
            t.transform.rotation.y = q. y ();
            t.transform.rotation.z = q. z ();
            t.transform.rotation.w = q. w ();

            tf_broadcaster_->sendTransform(t);
            RCLCPP_INFO ( this -> get_logger (), "静态TF已发布：base_link -> laser_link" );
        }

    private:
        std::shared_ptr<tf2_ros::StaticTransformBroadcaster> tf_broadcaster_;
};
int main(int argc, char *argv[])
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<StaticTFBroadcaster>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
