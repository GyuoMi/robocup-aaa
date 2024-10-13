import numpy as np


def GenerateBasicFormation():

    formation = [
        np.array([-13, 0]),  # Goalkeeper
        np.array([-10, -2]),  # Left Defender
        np.array([-11, 3]),  # Center Back Left
        np.array([-8, 0]),  # Center Back Right
        np.array([-3, 0]),  # Right Defender
        np.array([0, 1]),  # Left Midfielder
        np.array([2, 0]),  # Center Midfielder Left
        np.array([3, 3]),  # Center Midfielder Right
        np.array([8, 0]),  # Right Midfielder
        np.array([9, 1]),  # Forward Left
        np.array([12, 0]),  # Forward Right
    ]

    return formation


def four_four_two():

    # stagger positions by 1 because of algorithm trying to find closest individual stuff
    formation = [
        np.array([-13, 0]),  # Goalkeeper
        #
        np.array([-6, 7]),  # Left Defender
        np.array([-7, -7]),  # Right Defender
        #
        np.array([-9, 3]),  # Center Back Left
        np.array([-10, -3]),  # Center Back Right
        #
        np.array([1, 3]),  # Center Midfielder Left
        np.array([3, -3]),  # Center Midfielder Right
        #
        np.array([6, 7]),  # Left Midfielder
        np.array([8, -7]),  # Right Midfielder
        #
        np.array([9, 4]),  # Forward Left
        np.array([11, -4]),  # Forward Right
    ]

    return formation
