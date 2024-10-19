// Generated by gencpp from file moveit_msgs/GraspPlanningRequest.msg
// DO NOT EDIT!


#ifndef MOVEIT_MSGS_MESSAGE_GRASPPLANNINGREQUEST_H
#define MOVEIT_MSGS_MESSAGE_GRASPPLANNINGREQUEST_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <moveit_msgs/CollisionObject.h>
#include <moveit_msgs/Grasp.h>
#include <moveit_msgs/CollisionObject.h>

namespace moveit_msgs
{
template <class ContainerAllocator>
struct GraspPlanningRequest_
{
  typedef GraspPlanningRequest_<ContainerAllocator> Type;

  GraspPlanningRequest_()
    : group_name()
    , target()
    , support_surfaces()
    , candidate_grasps()
    , movable_obstacles()  {
    }
  GraspPlanningRequest_(const ContainerAllocator& _alloc)
    : group_name(_alloc)
    , target(_alloc)
    , support_surfaces(_alloc)
    , candidate_grasps(_alloc)
    , movable_obstacles(_alloc)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> _group_name_type;
  _group_name_type group_name;

   typedef  ::moveit_msgs::CollisionObject_<ContainerAllocator>  _target_type;
  _target_type target;

   typedef std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> _support_surfaces_type;
  _support_surfaces_type support_surfaces;

   typedef std::vector< ::moveit_msgs::Grasp_<ContainerAllocator> , typename std::allocator_traits<ContainerAllocator>::template rebind_alloc< ::moveit_msgs::Grasp_<ContainerAllocator> >> _candidate_grasps_type;
  _candidate_grasps_type candidate_grasps;

   typedef std::vector< ::moveit_msgs::CollisionObject_<ContainerAllocator> , typename std::allocator_traits<ContainerAllocator>::template rebind_alloc< ::moveit_msgs::CollisionObject_<ContainerAllocator> >> _movable_obstacles_type;
  _movable_obstacles_type movable_obstacles;





  typedef boost::shared_ptr< ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator> const> ConstPtr;

}; // struct GraspPlanningRequest_

typedef ::moveit_msgs::GraspPlanningRequest_<std::allocator<void> > GraspPlanningRequest;

typedef boost::shared_ptr< ::moveit_msgs::GraspPlanningRequest > GraspPlanningRequestPtr;
typedef boost::shared_ptr< ::moveit_msgs::GraspPlanningRequest const> GraspPlanningRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator1> & lhs, const ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator2> & rhs)
{
  return lhs.group_name == rhs.group_name &&
    lhs.target == rhs.target &&
    lhs.support_surfaces == rhs.support_surfaces &&
    lhs.candidate_grasps == rhs.candidate_grasps &&
    lhs.movable_obstacles == rhs.movable_obstacles;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator1> & lhs, const ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace moveit_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "213bcb2a85f6f966990ab629958810a1";
  }

  static const char* value(const ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x213bcb2a85f6f966ULL;
  static const uint64_t static_value2 = 0x990ab629958810a1ULL;
};

template<class ContainerAllocator>
struct DataType< ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "moveit_msgs/GraspPlanningRequest";
  }

  static const char* value(const ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# Requests that grasp planning be performed for the target object\n"
"# returns a list of candidate grasps to be tested and executed\n"
"\n"
"# the planning group used\n"
"string group_name\n"
"\n"
"# the object to be grasped\n"
"CollisionObject target\n"
"\n"
"# the names of the relevant support surfaces (e.g. tables) in the collision map\n"
"# can be left empty if no names are available\n"
"string[] support_surfaces\n"
"\n"
"# an optional list of grasps to be evaluated by the planner\n"
"Grasp[] candidate_grasps\n"
"\n"
"# an optional list of obstacles that we have semantic information about\n"
"# and that can be moved in the course of grasping\n"
"CollisionObject[] movable_obstacles\n"
"\n"
"\n"
"================================================================================\n"
"MSG: moveit_msgs/CollisionObject\n"
"# A header, used for interpreting the poses\n"
"Header header\n"
"\n"
"# The object's pose relative to the header frame.\n"
"# The shapes and subframe poses are defined relative to this pose.\n"
"geometry_msgs/Pose pose\n"
"\n"
"# The id of the object (name used in MoveIt)\n"
"string id\n"
"\n"
"# The object type in a database of known objects\n"
"object_recognition_msgs/ObjectType type\n"
"\n"
"# The collision geometries associated with the object.\n"
"# Their poses are with respect to the object's pose\n"
"\n"
"# Solid geometric primitives\n"
"shape_msgs/SolidPrimitive[] primitives\n"
"geometry_msgs/Pose[] primitive_poses\n"
"\n"
"# Meshes\n"
"shape_msgs/Mesh[] meshes\n"
"geometry_msgs/Pose[] mesh_poses\n"
"\n"
"# Bounding planes (equation is specified, but the plane can be oriented using an additional pose)\n"
"shape_msgs/Plane[] planes\n"
"geometry_msgs/Pose[] plane_poses\n"
"\n"
"# Named subframes on the object. Use these to define points of interest on the object that you want\n"
"# to plan with (e.g. \"tip\", \"spout\", \"handle\"). The id of the object will be prepended to the subframe.\n"
"# If an object with the id \"screwdriver\" and a subframe \"tip\" is in the scene, you can use the frame\n"
"# \"screwdriver/tip\" for planning.\n"
"# The length of the subframe_names and subframe_poses has to be identical.\n"
"string[] subframe_names\n"
"geometry_msgs/Pose[] subframe_poses\n"
"\n"
"# Adds the object to the planning scene. If the object previously existed, it is replaced.\n"
"byte ADD=0\n"
"\n"
"# Removes the object from the environment entirely (everything that matches the specified id)\n"
"byte REMOVE=1\n"
"\n"
"# Append to an object that already exists in the planning scene. If the object does not exist, it is added.\n"
"byte APPEND=2\n"
"\n"
"# If an object already exists in the scene, new poses can be sent (the geometry arrays must be left empty)\n"
"# if solely moving the object is desired\n"
"byte MOVE=3\n"
"\n"
"# Operation to be performed\n"
"byte operation\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/Header\n"
"# Standard metadata for higher-level stamped data types.\n"
"# This is generally used to communicate timestamped data \n"
"# in a particular coordinate frame.\n"
"# \n"
"# sequence ID: consecutively increasing ID \n"
"uint32 seq\n"
"#Two-integer timestamp that is expressed as:\n"
"# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n"
"# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n"
"# time-handling sugar is provided by the client library\n"
"time stamp\n"
"#Frame this data is associated with\n"
"string frame_id\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Pose\n"
"# A representation of pose in free space, composed of position and orientation. \n"
"Point position\n"
"Quaternion orientation\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Point\n"
"# This contains the position of a point in free space\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Quaternion\n"
"# This represents an orientation in free space in quaternion form.\n"
"\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"float64 w\n"
"\n"
"================================================================================\n"
"MSG: object_recognition_msgs/ObjectType\n"
"################################################## OBJECT ID #########################################################\n"
"\n"
"# Contains information about the type of a found object. Those two sets of parameters together uniquely define an\n"
"# object\n"
"\n"
"# The key of the found object: the unique identifier in the given db\n"
"string key\n"
"\n"
"# The db parameters stored as a JSON/compressed YAML string. An object id does not make sense without the corresponding\n"
"# database. E.g., in object_recognition, it can look like: \"{'type':'CouchDB', 'root':'http://localhost'}\"\n"
"# There is no conventional format for those parameters and it's nice to keep that flexibility.\n"
"# The object_recognition_core as a generic DB type that can read those fields\n"
"# Current examples:\n"
"# For CouchDB:\n"
"#   type: 'CouchDB'\n"
"#   root: 'http://localhost:5984'\n"
"#   collection: 'object_recognition'\n"
"# For SQL household database:\n"
"#   type: 'SqlHousehold'\n"
"#   host: 'wgs36'\n"
"#   port: 5432\n"
"#   user: 'willow'\n"
"#   password: 'willow'\n"
"#   name: 'household_objects'\n"
"#   module: 'tabletop'\n"
"string db\n"
"\n"
"================================================================================\n"
"MSG: shape_msgs/SolidPrimitive\n"
"# Define box, sphere, cylinder, cone \n"
"# All shapes are defined to have their bounding boxes centered around 0,0,0.\n"
"\n"
"uint8 BOX=1\n"
"uint8 SPHERE=2\n"
"uint8 CYLINDER=3\n"
"uint8 CONE=4\n"
"\n"
"# The type of the shape\n"
"uint8 type\n"
"\n"
"\n"
"# The dimensions of the shape\n"
"float64[] dimensions\n"
"\n"
"# The meaning of the shape dimensions: each constant defines the index in the 'dimensions' array\n"
"\n"
"# For the BOX type, the X, Y, and Z dimensions are the length of the corresponding\n"
"# sides of the box.\n"
"uint8 BOX_X=0\n"
"uint8 BOX_Y=1\n"
"uint8 BOX_Z=2\n"
"\n"
"\n"
"# For the SPHERE type, only one component is used, and it gives the radius of\n"
"# the sphere.\n"
"uint8 SPHERE_RADIUS=0\n"
"\n"
"\n"
"# For the CYLINDER and CONE types, the center line is oriented along\n"
"# the Z axis.  Therefore the CYLINDER_HEIGHT (CONE_HEIGHT) component\n"
"# of dimensions gives the height of the cylinder (cone).  The\n"
"# CYLINDER_RADIUS (CONE_RADIUS) component of dimensions gives the\n"
"# radius of the base of the cylinder (cone).  Cone and cylinder\n"
"# primitives are defined to be circular. The tip of the cone is\n"
"# pointing up, along +Z axis.\n"
"\n"
"uint8 CYLINDER_HEIGHT=0\n"
"uint8 CYLINDER_RADIUS=1\n"
"\n"
"uint8 CONE_HEIGHT=0\n"
"uint8 CONE_RADIUS=1\n"
"\n"
"================================================================================\n"
"MSG: shape_msgs/Mesh\n"
"# Definition of a mesh\n"
"\n"
"# list of triangles; the index values refer to positions in vertices[]\n"
"MeshTriangle[] triangles\n"
"\n"
"# the actual vertices that make up the mesh\n"
"geometry_msgs/Point[] vertices\n"
"\n"
"================================================================================\n"
"MSG: shape_msgs/MeshTriangle\n"
"# Definition of a triangle's vertices\n"
"uint32[3] vertex_indices\n"
"\n"
"================================================================================\n"
"MSG: shape_msgs/Plane\n"
"# Representation of a plane, using the plane equation ax + by + cz + d = 0\n"
"\n"
"# a := coef[0]\n"
"# b := coef[1]\n"
"# c := coef[2]\n"
"# d := coef[3]\n"
"\n"
"float64[4] coef\n"
"\n"
"================================================================================\n"
"MSG: moveit_msgs/Grasp\n"
"# This message contains a description of a grasp that would be used\n"
"# with a particular end-effector to grasp an object, including how to\n"
"# approach it, grip it, etc.  This message does not contain any\n"
"# information about a \"grasp point\" (a position ON the object).\n"
"# Whatever generates this message should have already combined\n"
"# information about grasp points with information about the geometry\n"
"# of the end-effector to compute the grasp_pose in this message.\n"
"\n"
"# A name for this grasp\n"
"string id\n"
"\n"
"# The internal posture of the hand for the pre-grasp\n"
"# only positions are used\n"
"trajectory_msgs/JointTrajectory pre_grasp_posture\n"
"\n"
"# The internal posture of the hand for the grasp\n"
"# positions and efforts are used\n"
"trajectory_msgs/JointTrajectory grasp_posture\n"
"\n"
"# The position of the end-effector for the grasp.  This is the pose of\n"
"# the \"parent_link\" of the end-effector, not actually the pose of any\n"
"# link *in* the end-effector.  Typically this would be the pose of the\n"
"# most distal wrist link before the hand (end-effector) links began.\n"
"geometry_msgs/PoseStamped grasp_pose\n"
"\n"
"# The estimated probability of success for this grasp, or some other\n"
"# measure of how \"good\" it is.\n"
"float64 grasp_quality\n"
"\n"
"# The approach direction to take before picking an object\n"
"GripperTranslation pre_grasp_approach\n"
"\n"
"# The retreat direction to take after a grasp has been completed (object is attached)\n"
"GripperTranslation post_grasp_retreat\n"
"\n"
"# The retreat motion to perform when releasing the object; this information\n"
"# is not necessary for the grasp itself, but when releasing the object,\n"
"# the information will be necessary. The grasp used to perform a pickup\n"
"# is returned as part of the result, so this information is available for\n"
"# later use.\n"
"GripperTranslation post_place_retreat\n"
"\n"
"# the maximum contact force to use while grasping (<=0 to disable)\n"
"float32 max_contact_force\n"
"\n"
"# an optional list of obstacles that we have semantic information about\n"
"# and that can be touched/pushed/moved in the course of grasping\n"
"string[] allowed_touch_objects\n"
"\n"
"================================================================================\n"
"MSG: trajectory_msgs/JointTrajectory\n"
"Header header\n"
"string[] joint_names\n"
"JointTrajectoryPoint[] points\n"
"\n"
"================================================================================\n"
"MSG: trajectory_msgs/JointTrajectoryPoint\n"
"# Each trajectory point specifies either positions[, velocities[, accelerations]]\n"
"# or positions[, effort] for the trajectory to be executed.\n"
"# All specified values are in the same order as the joint names in JointTrajectory.msg\n"
"\n"
"float64[] positions\n"
"float64[] velocities\n"
"float64[] accelerations\n"
"float64[] effort\n"
"duration time_from_start\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/PoseStamped\n"
"# A Pose with reference coordinate frame and timestamp\n"
"Header header\n"
"Pose pose\n"
"\n"
"================================================================================\n"
"MSG: moveit_msgs/GripperTranslation\n"
"# defines a translation for the gripper, used in pickup or place tasks\n"
"# for example for lifting an object off a table or approaching the table for placing\n"
"\n"
"# the direction of the translation\n"
"geometry_msgs/Vector3Stamped direction\n"
"\n"
"# the desired translation distance\n"
"float32 desired_distance\n"
"\n"
"# the min distance that must be considered feasible before the\n"
"# grasp is even attempted\n"
"float32 min_distance\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Vector3Stamped\n"
"# This represents a Vector3 with reference coordinate frame and timestamp\n"
"Header header\n"
"Vector3 vector\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Vector3\n"
"# This represents a vector in free space. \n"
"# It is only meant to represent a direction. Therefore, it does not\n"
"# make sense to apply a translation to it (e.g., when applying a \n"
"# generic rigid transformation to a Vector3, tf2 will only apply the\n"
"# rotation). If you want your data to be translatable too, use the\n"
"# geometry_msgs/Point message instead.\n"
"\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
;
  }

  static const char* value(const ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.group_name);
      stream.next(m.target);
      stream.next(m.support_surfaces);
      stream.next(m.candidate_grasps);
      stream.next(m.movable_obstacles);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct GraspPlanningRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::moveit_msgs::GraspPlanningRequest_<ContainerAllocator>& v)
  {
    s << indent << "group_name: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>::stream(s, indent + "  ", v.group_name);
    s << indent << "target: ";
    s << std::endl;
    Printer< ::moveit_msgs::CollisionObject_<ContainerAllocator> >::stream(s, indent + "  ", v.target);
    s << indent << "support_surfaces[]" << std::endl;
    for (size_t i = 0; i < v.support_surfaces.size(); ++i)
    {
      s << indent << "  support_surfaces[" << i << "]: ";
      Printer<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>::stream(s, indent + "  ", v.support_surfaces[i]);
    }
    s << indent << "candidate_grasps[]" << std::endl;
    for (size_t i = 0; i < v.candidate_grasps.size(); ++i)
    {
      s << indent << "  candidate_grasps[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::moveit_msgs::Grasp_<ContainerAllocator> >::stream(s, indent + "    ", v.candidate_grasps[i]);
    }
    s << indent << "movable_obstacles[]" << std::endl;
    for (size_t i = 0; i < v.movable_obstacles.size(); ++i)
    {
      s << indent << "  movable_obstacles[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::moveit_msgs::CollisionObject_<ContainerAllocator> >::stream(s, indent + "    ", v.movable_obstacles[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // MOVEIT_MSGS_MESSAGE_GRASPPLANNINGREQUEST_H
