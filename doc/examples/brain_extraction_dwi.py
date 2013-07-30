"""
=================================================
Brain segmentation with dipy.segment.mask.
=================================================

We show how to extract brain information and mask from a b0 image using dipy's
segment.mask module.

First import the necessary modules:
"""

import os.path
import numpy as np
import nibabel as nib

"""
Download and read the data for this tutorial.
The scil_b0 dataset contains different data from different companies and models.
For this example, the data comes from a 3 tesla GE MRI.
"""

from dipy.data import fetch_scil_b0, read_scil_b0
fetch_scil_b0()
img = read_scil_b0()
data = np.squeeze(img.get_data())

"""
img contains a nibabel Nifti1Image object. Data is the actual brain data as a
numpy ndarray.

Segment the brain using dipy's mask module.
`medostu` returns the segmented brain data an a binary mask of the brain.
It is possible to fine tune the `medotsu`'s parameters (median_radius and
num_pass) if extraction yields incorrect results but the default parameters work
well on most volumes. For this example, default parameters (4, 4) will be used.
"""

from dipy.segment.mask import medotsu
b0_mask, mask = medotsu(data.copy(), 4, 4)

"""
Saving the segmentation results is very easy using nibabel. We need the b0_mask,
and the binary mask volumes. The affine matrix which transform the image's
coordinates to the world coordinates is also needed. Here, we choose to save
both images in float32.
"""

mask_img = nib.Nifti1Image(mask.astype(np.float32), img.get_affine())
b0_img = nib.Nifti1Image(b0_mask.astype(np.float32), img.get_affine())

fname = './ge_3t'
nib.save(mask_img, fname+'_binary_mask.nii.gz')
nib.save(b0_img, fname+'_mask.nii.gz')

"""

Quick view of the results middle slice using matplotlib.
"""

import matplotlib.pyplot as plt

slice = data.shape[2]/2
plt.figure('Brain segmentation')
plt.subplot(1,2,1)
plt.imshow(data[:,:,slice])
plt.subplot(1,2,2)
plt.imshow(b0_mask[:,:,slice])
plt.show()

"""
`medostu` can also automaticaly crop the outputs to remove the largest possible
number of backgroud voxels. This makes outputted data significantly smaller.
`medostu`'s auto cropping is activated by setting the autocrop parameter to True.
"""

b0_mask_crop, mask_crop = medotsu(data.copy(), 4, 4, autocrop=True)

"""
Saving cropped data using nibabel as demonstrated previously.
"""

mask_img_crop = nib.Nifti1Image(mask_crop.astype(np.float32), img.get_affine())
b0_img_crop = nib.Nifti1Image(b0_mask_crop.astype(np.float32), img.get_affine())
nib.save(mask_img_crop, fname+'_binary_mask_crop.nii.gz')
nib.save(b0_img_crop, fname+'_mask_crop.nii.gz')
