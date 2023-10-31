def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        h_left, h_right = height[left], height[right]
        width = right - left
        current_water = min(h_left, h_right) * width
        max_water = max(max_water, current_water)

        if h_left < h_right:
            left += 1
        else:
            right -= 1

    return max_water


heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
result = max_area(heights)
print(result)  # Output will be 49
