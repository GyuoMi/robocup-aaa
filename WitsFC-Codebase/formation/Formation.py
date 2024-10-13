import numpy as np

# TODO: BIG we need to rearrange the positions to correlate to the player closest to said position


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


# counter attack
def four_four_two():

    formation = [
        np.array([-13, 0]),  # Goalkeeper
        #
        np.array([-7, 7]),  # Left Defender
        np.array([-7, -7]),  # Right Defender
        #
        np.array([-10, 3]),  # Center Back Left
        np.array([-10, -3]),  # Center Back Right
        #
        np.array([3, 3]),  # Center Midfielder Left
        np.array([3, -3]),  # Center Midfielder Right
        #
        np.array([8, 7]),  # Left Midfielder
        np.array([8, -7]),  # Right Midfielder
        #
        np.array([11, 4]),  # Forward Left
        np.array([11, -4]),  # Forward Right
    ]

    return formation


# attack
def three_four_three():

    formation = [
        np.array([-13, 0]),  # Goalkeeper
        #
        np.array([-7, 7]),  # Left Defender
        np.array([-9, 0]),  # Center Back Left
        np.array([-7, -7]),  # Right Defender
        #
        #
        np.array([1, 3]),  # Center Midfielder Left
        np.array([1, -3]),  # Center Midfielder Right
        #
        np.array([0, 5]),  # Left Midfielder
        np.array([0, -5]),  # Right Midfielder
        #
        np.array([9, 4]),  # Forward Left
        np.array([9, -4]),  # Forward Right
        np.array([12, 0]),  # Center Back Right
    ]

    return formation


# defend
def five_four_one():
    formation = [
        np.array([-13, 0]),  # Goalkeeper
        #
        np.array([-8, 6]),  # Left Defender
        np.array([-10, 0]),  # Center Back Left
        np.array([-8, -6]),  # Right Defender
        #
        #
        np.array([-9, 4]),  # Center Midfielder Left
        np.array([-9, -4]),  # Center Midfielder Right
        #
        np.array([-4, 7]),  # Left Midfielder
        np.array([-4, -7]),  # Right Midfielder
        #
        np.array([-3, 2]),  # Forward Left
        np.array([-3, -2]),  # Forward Right
        np.array([0, 0]),  # Center Back Right
    ]

    return formation
