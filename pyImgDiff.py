#!/usr/bin/env python3
'''
Photos Diff Services



'''
from PIL import Image

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class imgDiff(object):
    def diff(self, img1, img2):
        '''
        # FIXME: need image diff algorithm
        https://www.reddit.com/r/learnpython/comments/1995582/how_to_compare_two_images/
        https://stackoverflow.com/questions/72851122/how-to-compare-how-similar-two-images-are-in-python
        '''
        pass

    def show(self, img1, img2):
        # Load the images
        try: 
            image1 = mpimg.imread(img1)
            image2 = mpimg.imread(img2)
        except Exception as err:
            print("ERROR: Can not load images:", img1, img2)
            return 
        
        # Create a figure and subplots
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        
        # Display the first image
        axes[0].imshow(image1)
        axes[0].set_title('Image 1')
        axes[0].axis('off')  # Hide axes
        
        # Display the second image
        axes[1].imshow(image2)
        axes[1].set_title('Image 2')
        axes[1].axis('off')  # Hide axes
        
        # Adjust layout and show the plot
        plt.tight_layout()
        plt.show()
        return


