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
    
