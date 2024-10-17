def setup():
    size(400, 400)
    global img
    img = loadImage("pol.png")
    # img.resize(200, 200)  
    img.loadPixels()
    image(img, 0, 0)  
    convert_image_to_array()

def convert_image_to_array():
    global img_array
    img_array = []  # Initialize a 2D list to store pixel values
    for y in range(img.height):
        row = []  # Initialize a list for each row of pixels
        for x in range(img.width):
            loc = x + y * img.width
            pixel_value = brightness(img.pixels[loc])  # brightness of the pixel
            row.append(pixel_value)
        img_array.append(row)  # Append the row to the 2D list   
        # println(img_array) 
    process_array()

def process_array():
    threshold = 30  
    diff_results = []

    # horizontal differences
    for col_index in range(img.width - 1):
        for row_index in range(img.height):
            difference = abs(img_array[row_index][col_index + 1] - img_array[row_index][col_index])
            if difference <= threshold:
                start_index = row_index * img.width + col_index
                end_index = row_index * img.width + col_index + 1
                diff_results.append((start_index, end_index, difference))

    # vertical differences
    for col_index in range(img.width):
        for row_index in range(img.height - 1):
            difference = abs(img_array[row_index + 1][col_index] - img_array[row_index][col_index])
            if difference <= threshold:
                start_index = row_index * img.width + col_index
                end_index = (row_index + 1) * img.width + col_index
                diff_results.append((start_index, end_index, difference))

    # diagonal differences (top-left to bottom-right)
    for row_index in range(img.height - 1):
        for col_index in range(img.width - 1):
            difference = abs(img_array[row_index + 1][col_index + 1] - img_array[row_index][col_index])
            if difference <= threshold:
                start_index = row_index * img.width + col_index
                end_index = (row_index + 1) * img.width + col_index + 1
                diff_results.append((start_index, end_index, difference))

    # Sort the difference results based on the third element (difference) of each tuple
    diff_results_sorted = sorted(diff_results, key=lambda x: x[2])
    # print(diff_results_sorted)
    

    # Segment initialization
    seg = [i for i in range(img.width * img.height)]

    # Union-Find Helper Functions
    def find(x):
        if seg[x] != x:
            seg[x] = find(seg[x])
        return seg[x]

    def union(x, y):
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            seg[rootY] = rootX

    # Apply Union-Find based on the difference results
    for result in diff_results_sorted:
        union(result[0], result[1])

    # Flatten the segments
    for i in range(len(seg)):
        seg[i] = find(i)

    # Create a new image to display the segmented image
    segmented_img = createImage(img.width, img.height, RGB)

   # Assign a unique color to each segment
    segment_colors = {}
    unique_segments = set(seg)
    for segment_index in unique_segments:
        segment_colors[segment_index] = color(random(255), random(255), random(255))

    # Update pixels in the segmented image with segment colors
    segmented_img.loadPixels()
    for y in range(img.height):
        for x in range(img.width):
            loc = x + y * img.width
            segment_index = seg[loc]
            segmented_img.pixels[loc] = segment_colors[segment_index]
    segmented_img.updatePixels()

    # Display the segmented image
    image(segmented_img, img.width, 0)

    # Print the original seg array and total number of segments
    total_segments = len(unique_segments)
    # println(unique_segments)
    print("Total number of segments in the final array:", total_segments)
