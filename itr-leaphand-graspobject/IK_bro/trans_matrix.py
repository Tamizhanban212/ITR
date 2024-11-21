import numpy as np

class TransMatrix:
    @staticmethod
    def compute_obj_pos(object_pose_cam, palm_wrt_cam):
        """
        Computes the position of the object with respect to the palm.

        Parameters:
        - object_pose_cam: numpy array, the 4x4 transformation matrix of the object's pose in the camera frame.
        - palm_wrt_cam: numpy array, the 4x4 transformation matrix of the palm's pose in the camera frame.

        Returns:
        - numpy array: The position (x, y, z) of the object with respect to the palm frame.
        """
        # Compute the transformation matrix of the object with respect to the palm
        obj_wrt_palm = np.linalg.inv(palm_wrt_cam) @ object_pose_cam
        
        # Extract the (x, y, z) position from the last column of the transformation matrix
        x, y, z = obj_wrt_palm[0, 3], obj_wrt_palm[1, 3], obj_wrt_palm[2, 3]
        
        return np.array([x, y, z])

    @staticmethod
    def compute_contact_points(object_pose_cam, palm_wrt_cam, offsets):
        """
        Computes the contact points of the palm with the object.

        Parameters:
        - object_pose_cam: numpy array, the 4x4 transformation matrix of the object's pose in the camera frame.
        - palm_wrt_cam: numpy array, the 4x4 transformation matrix of the palm's pose in the camera frame.
        - offsets: list of numpy arrays, offsets [b1, b2] to compute the contact points.

        Returns:
        - list of numpy arrays: The contact points of the palm with the object.
        """
        # Compute the transformation matrix of the object with respect to the palm
        obj_wrt_palm = np.linalg.inv(palm_wrt_cam) @ object_pose_cam

        # Extract the object's position and orientation with respect to the palm
        obj_position = obj_wrt_palm[:3, 3]  # Position (x, y, z)
        obj_orientation = obj_wrt_palm[:3, :3]  # Orientation matrix (3x3)

        # Compute contact points by applying offsets to the object's position
        contact_points = []
        for offset in offsets:
            # Transform the offset into the palm frame
            contact_point = obj_position + obj_orientation @ offset.flatten()
            contact_points.append(contact_point)

        return contact_points
