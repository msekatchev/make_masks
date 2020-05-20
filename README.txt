 
Current workflow to make masks:
    1. Run slice_no_repeats.py to cut up large images with random crops 
    2. Run make_NN_dataset.py to randomly select some of those images and sort them into directories for NN input
    3. Run draw_mask.py (annotate_dir() to do a dataset directory) to make labels for images and save them in correct folders with correct names
    4. (train neural net)
    5. Run find_centroids.py to get PMT and bolt locations
    

