# 
# 
# input s='abcabcabb'
# output 3


# s ='bbbbb'
# output='1'

#  input s=pwwkew
# output 3
s="abcabcabb"
 
def longest_substring_without_repeating_chars(s):
    # Initialize variables for the sliding window
    start = 0  # Start of the current substring
    max_length = 0  # Length of the longest substring
    char_index_map = {}  # Dictionary to store the index of each character

    for end in range(len(s)):
        # If the character is in the map and its index is greater than or equal to the start of the current substring
        if s[end] in char_index_map and char_index_map[s[end]] >= start:
            # Move the start of the current substring just after the last occurrence of the character
            start = char_index_map[s[end]] + 1

        # Update the index of the character in the map
        char_index_map[s[end]] = end

        # Update the maximum length if a longer substring is found
        max_length = max(max_length, end - start + 1)
        print(char_index_map)
    return max_length

# Example usage:
input_str = "abcabcbb"
result = longest_substring_without_repeating_chars(s)
print("The length of the longest substring without repeating characters is:", result)
