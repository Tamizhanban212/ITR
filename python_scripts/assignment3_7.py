import numpy as np

def dh_transform(a, alpha, d, theta):
    """Computes the transformation matrix using DH parameters."""
    return np.array([
        [np.cos(theta), -np.sin(theta)*np.cos(alpha),  np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
        [np.sin(theta),  np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
        [0,              np.sin(alpha),               np.cos(alpha),              d],
        [0,              0,                           0,                          1]
    ])

def compute_jacobian(dh_params, joint_types=None):
    """
    Computes the manipulator Jacobian, end-effector position, and end-effector velocity.
    
    :param dh_params: DH parameters in the form of an (N, 4) matrix where N is the number of links.
                      Each row should be [a, alpha, d, theta].
    :param joint_types: Optional list of 'R' (Revolute) or 'P' (Prismatic) indicating joint types. 
                        Defaults to all 'R' if not provided.
    :return: A tuple (Jacobian matrix, end-effector position, end-effector velocity).
    """
    num_links = dh_params.shape[0]
    joint_types = joint_types if joint_types else ['R'] * num_links
    
    T = np.eye(4)
    z = np.array([0, 0, 1])
    o = np.array([0, 0, 0])
    
    Jv = []
    Jw = []
    
    transformations = []
    
    # Compute the transformation matrices and store intermediate steps
    for i in range(num_links):
        a, alpha, d, theta = dh_params[i]
        T_i = dh_transform(a, alpha, d, theta)
        T = T @ T_i
        transformations.append(T)

    end_effector_pos = T[:3, 3]
    
    # Compute the Jacobian
    for i in range(num_links):
        T_prev = np.eye(4) if i == 0 else transformations[i-1]
        o_prev = T_prev[:3, 3]
        z_prev = T_prev[:3, 2]
        
        if joint_types[i] == 'R':
            Jv_i = np.cross(z_prev, (end_effector_pos - o_prev))
            Jw_i = z_prev
        elif joint_types[i] == 'P':
            Jv_i = z_prev
            Jw_i = np.array([0, 0, 0])
        
        Jv.append(Jv_i)
        Jw.append(Jw_i)
    
    Jv = np.array(Jv).T
    Jw = np.array(Jw).T
    Jacobian = np.vstack((Jv, Jw))
    
    # End-effector velocity assuming joint velocities are unity
    joint_velocities = np.ones(num_links)
    end_effector_velocity = Jacobian @ joint_velocities
    
    return Jacobian, end_effector_pos, end_effector_velocity

# Example usage:
dh_params = np.array([
    [0, -np.pi/2, 1, 0],
    [0, -np.pi/2, 1, -np.pi/2],
    [0, 0, 1, 0]
])
jacobian, end_effector_pos, end_effector_velocity = compute_jacobian(dh_params, ['P', 'P', 'P'])
print("Jacobian:\n", jacobian)
print("End-Effector Position:\n", end_effector_pos)
print("End-Effector Velocity:\n", end_effector_velocity)
