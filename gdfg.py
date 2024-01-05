def calculate_xp_for_next_level(current_level):
    xp_needed = 0
    for level in range(current_level + 1):
        xp_needed += 100 * (level + 1)  # Adjust the XP amount based on the user's level
    return xp_needed

current_level = 25
xp_needed_for_next_level = calculate_xp_for_next_level(current_level)
print(f"XP needed to reach level {current_level + 1}: {xp_needed_for_next_level}")
