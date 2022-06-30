import h5py
import nibabel as nib
import numpy as np
import os

def nifty2h5(eig_nifty, d_nifty, directory,fname):

    vol_name = eig_nifty.split('/')[-1].split('_max_eig.nii.gz')[0]
    print(vol_name)

    vol_nii_1 = nib.load(eig_nifty)
    vol_1 = vol_nii_1.get_fdata()  # (180,220,120,3) WHD C

    vol_trans_1 = vol_1.transpose(3, 2, 1, 0)  # (3, 120, 220, 180)
    # print(vol_trans_1.shape)
    #    label = (label > 0).astype(np.uint8)
    #    w, h, d = label.shape

    vol_nii_2 = nib.load(d_nifty)
    vol_2 = vol_nii_2.get_fdata()  # (180,220,120,3) WHD C
    vol_trans_2 = vol_2.transpose(3, 2, 1, 0)  # (3, 120, 220, 180)


    vol_trans = np.concatenate((vol_trans_1, vol_trans_2), axis=0)
    """
    gt_nii = nib.load(e_nifty)
    gt = gt_nii.get_fdata()
    # print(gt.shape)
    gt_trans = gt.transpose(3, 2, 1, 0)
    # print(gt_trans.shape)
    """
    f = h5py.File(directory+fname + '.h5', 'w')
    f.create_dataset('raw', data=vol_trans, compression="gzip")
    # f.create_dataset('label', data=gt_trans, compression="gzip")
    f.close()
    """
    gt = nib.load(vol_fn.replace('Ds','normE'))
    print(gt.shape)
    gt = nib.load(vol_fn.replace('Ds','normE_whole')) 
    print(gt.shape)
    """
    # gt_name=gt.split('/')[-1].split('.jpg')[0]
    # need to be (C DHW)
    return vol_trans

def h52nifty(h5,nii_save_path):
    h5f = h5py.File(h5, 'r')
    pre = h5f['predictions'][:]  # [3,120,220,180]
    pre_trans = pre.transpose(3, 2, 1, 0)
    nib.save(nib.Nifti1Image(pre_trans[:].astype(np.float32), np.eye(4)), nii_save_path + '.nii.gz')
