import os
import numpy as np
import cv2
import argparse
#import matplotlib.pyplot as plt
from PIL import Image



parser = argparse.ArgumentParser('create image pairs')
parser.add_argument('--fold_A', dest='fold_A', help='input directory for image A', type=str, default=r"data\\photosketch_Data_subset\\image")
parser.add_argument('--fold_B', dest='fold_B', help='input directory for image B', type=str, default=r"data\\photosketch_Data_subset\\sketch")
parser.add_argument('--fold_AB', dest='fold_AB', help='output directory', type=str, default=r"data\\photosketch_Data_subset\\combined")
parser.add_argument('--num_imgs', dest='num_imgs', help='number of images', type=int, default=300)
parser.add_argument('--use_AB', dest='use_AB', help='if true: (0001_A, 0001_B) to (0001_AB)', action='store_true')
args = parser.parse_args()

for arg in vars(args):
    print('[%s] = ' % arg, getattr(args, arg))

splits_A = os.listdir(args.fold_A)
splits_B = os.listdir(args.fold_B)

img_list_A=[]
img_list_B=[]
for sp in splits_A:
    img_fold_A = os.path.join(args.fold_A, sp)
    img_list_A.extend(os.listdir(img_fold_A))
for sp in splits_B:
    img_fold_B = os.path.join(args.fold_B, sp)
    img_list_B.extend(os.listdir(img_fold_B))
    #img_fold_B = os.path.join(args.fold_B, sp)


    if args.use_AB:
        img_list_B = [img_path for img_path in img_list if '_B.' in img_path]
        img_list_A= [img_path for img_path in img_list if '_A.' in img_path]

    #num_imgs = min(args.num_imgs, len(img_list_A))
    #print('split = %s, use %d/%d images' % (sp, num_imgs, len(img_list_B)))
    img_fold_AB = os.path.join(args.fold_AB, sp)
    if not os.path.isdir(img_fold_AB):
        os.makedirs(img_fold_AB)
    #print('split = %s, number of images = %d' % (sp, num_imgs))
print(splits_B)
for i in splits_B:
    for a in range(len(img_list_A)):
        for b in range(len(img_list_B)):

            name_A = img_list_A[a]
            #print(name_A)
            name_B= img_list_B[b]
            img_fold_A = os.path.join(args.fold_A, i)
            img_fold_B = os.path.join(args.fold_B, i)
            img_fold_AB = os.path.join(args.fold_AB, i)

            path_A = os.path.join(img_fold_A, name_A)
            path_B= os.path.join(img_fold_B, name_B)
        #print(path_A)
        # if args.use_AB:
        #     name_B = name_A.replace('_A.', '_B.')
        # else:
        #     name_B = name_A
        # path_B = os.path.join(img_fold_B, name_B)
        #print(path_B)
        #print(os.path.isfile(path_B))
            if os.path.isfile(path_A) and os.path.isfile(path_B):

                if img_list_A[a].rsplit('.',1)[0] in img_list_B[b]:
                    name_AB = name_B
                    if args.use_AB:
                        name_AB = name_AB.replace('_A.', '.')  # remove _A
                    path_AB = os.path.join(img_fold_AB, name_AB)
                    im_A = cv2.imread(path_A, 1) # python2: cv2.CV_LOAD_IMAGE_COLOR; python3: cv2.IMREAD_COLOR
            #print(im_A)
                    im_B = cv2.imread(path_B, 1) # python2: cv2.CV_LOAD_IMAGE_COLOR; python3: cv2.IMREAD_COLOR
                    im_AB = np.concatenate([im_A, im_B], 1)
                    cv2.imwrite(path_AB, im_AB)