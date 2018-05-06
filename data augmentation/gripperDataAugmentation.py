# pip install scikit-image, numpy, matplotlib
import skimage
from skimage import data, io, transform
import numpy as np
import random
from PIL import Image, ImageDraw
import os
from matplotlib import colors as mcolors


# import matplotlib for displaying images
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
# matplotlib inline

# camera=data.camera()
# io.imshow(camera)
# img = Image.fromarray(camera)
# img.save('my.png')
# img.show()
import random

class Point:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init

class GripperDataAugmentation:
    init_crop_width = 400
    init_crop_height = 400
    output_img_width = 280
    output_img_height = 280
    img_filename_pattern = 'pcd{}r.png'
    img_rc_pos_filename_pattern = 'pcd{}cpos.png'
    img_rc_neg_filename_pattern = 'pcd{}cneg.png'
    depth_img_filename_pattern = 'pcd{}_d.png'
    depth_output_img_filename_pattern = 'pcd{}_d.png'
    rc_pos_filename_pattern = 'pcd{}cpos.txt'
    rc_neg_filename_pattern = 'pcd{}cneg.txt'

    col_green = mcolors.cnames['green']
    col_yellow = mcolors.cnames['yellow']
    col_red = mcolors.cnames['red']
    col_blue = mcolors.cnames['blue']

    def __init__(self, file_path, img_num, output_file_path):
        self.file_path = file_path
        self.img_num = img_num
        self.img_filename = os.path.join(file_path, self.img_filename_pattern.format(img_num))
        self.depth_img_filename = os.path.join(file_path, '..\\depths', self.depth_img_filename_pattern.format(img_num))
        self.output_file_path = output_file_path
        self.rc_pos_filename = os.path.join(file_path, self.rc_pos_filename_pattern.format(img_num))
        self.rc_neg_filename = os.path.join(file_path, self.rc_neg_filename_pattern.format(img_num))
        self.width = 640
        self.height = 480
        self.x_translate = 0
        self.y_translate = 0
        self.rotate_angle = 0
        self.output_img_num = ''
        self.output_img_filename = ''
        self.output_depth_img_filename = ''
        self.output_rc_pos_filename = ''
        self.output_rc_neg_filename = ''

    def randomize(self):
        self.x_translate = random.randint(-50, 21)
        self.y_translate = random.randint(-20, 51)
        self.rotate_angle = random.randint(0, 360)
        # print(self.x_translate, ' ', self.y_translate, ' ', self.rotate_angle)
        self.output_img_num = self.img_num + format(random.randint(0, 3000), '04')
        self.output_img_filename = os.path.join(self.output_file_path,
                                                 self.img_filename_pattern.format(self.output_img_num))
        self.output_depth_img_filename = os.path.join(self.output_file_path,
                                                self.depth_img_filename_pattern.format(self.output_img_num))
        self.output_rc_pos_filename = os.path.join(self.output_file_path,
                                                   self.rc_pos_filename_pattern.format(self.output_img_num))
        self.output_rc_neg_filename = os.path.join(self.output_file_path,
                                                   self.rc_neg_filename_pattern.format(self.output_img_num))



    def show_cropped_rectangle(self, img):
        w, h = img.size
        x = (w - self.output_img_width) / 2
        y = (h - self.output_img_height) / 2
        draw = ImageDraw.Draw(img)
        draw.line([x, y, x + self.output_img_width, y], width=2, fill=200)
        draw.line([x + self.output_img_width, y, x + self.output_img_width, y + self.output_img_height], width=2,
                  fill=200)
        draw.line([x + self.output_img_width, y + self.output_img_height, x, y + self.output_img_height], width=2,
                  fill=200)
        draw.line([x, y + self.output_img_height, x, y], width=2, fill=200)
        plt.imshow(img)
        plt.show()


    def data_augment(self):
        self.crop_rotate_crop(self.img_filename, self.output_img_filename)
        self.crop_rotate_crop(self.depth_img_filename, self.output_depth_img_filename)
        self.transform_gripper_rect(True)
        self.transform_gripper_rect(False)

    def crop_rotate_crop(self, img_filename, output_filename):
        try:
            im = Image.open(img_filename)
        except IOError:
            print(img_filename, 'could not be opened')
            return
        self.width, self.height = im.size
        # We take a center crop of 320x320 pixels, randomly
        # translate it by up to 50 pixels in both the x and y direction,
        # and rotate it by a random amount
        # This image is then resized to 224x224 to fit the input layer of our architecture
        new_x = ((self.width - self.init_crop_width) / 2) + self.x_translate
        new_y = ((self.height - self.init_crop_height) / 2) + self.y_translate

        crop_rect = [new_x, new_y, new_x + self.init_crop_width, new_y + self.init_crop_height]
        cropped_im = im.crop(crop_rect)
        rotated_im = cropped_im.rotate(self.rotate_angle, resample=Image.BICUBIC, expand=True)
        # self.show_cropped_rectangle(rotated_im.copy())

        w, h = rotated_im.size
        x = (w - self.output_img_width) / 2;
        y = (h - self.output_img_height) / 2;

        output_img = rotated_im.crop((x, y, x + self.output_img_width, y + self.output_img_height))

        [path, file, ext] = self.get_file_parts(output_filename)
        if not os.path.exists(path):
            os.makedirs(path)
        output_img.save(output_filename)

    def transform_gripper_rect(self, positive=True):
        theta = self.rotate_angle
        x = self.x_translate
        y = self.y_translate
        if positive:
            rc_file_name = self.rc_pos_filename
            output_file_name = self.output_rc_pos_filename
        else:
            rc_file_name = self.rc_neg_filename
            output_file_name = self.output_rc_neg_filename

        try:
            with open(rc_file_name, 'r') as rc_file:
                lines = [line.strip().split(" ") for line in rc_file.readlines()]
        except IOError:
            print(rc_file_name, 'could not be opened')
            return

        coords = [[float(num) for num in line] for line in lines]
        origin = Point(self.output_img_width / 2, self.output_img_height / 2)
        output_lines = []

        x_translate = (640 - self.output_img_width) / 2 + x
        y_translate = (480 - self.output_img_height) / 2 + y
        for coord in coords:
            pt = Point(coord[0]-x_translate, coord[1]-y_translate)
            rotated_pt = self.rotate_point(pt, origin, theta)
            str_x = format("%.2f" % round(rotated_pt.x, 2))
            str_y = format("%.2f" % round(rotated_pt.y, 2))
            output_lines.append(str_x + ' ' + str_y + '\n')

        [path, file, ext] = self.get_file_parts(output_file_name)
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            with open(output_file_name, 'w+') as rc_output_file:
                rc_output_file.writelines(output_lines)
        except IOError:
            print(output_file_name, 'could not be opened for writing')
            return

    def rotate_point(self, pt, origin, theta) -> Point:
        # rotate pt by theta
        theta_radians = - (theta * np.pi / 180.)
        px = np.cos(theta_radians) * (pt.x - origin.x) - np.sin(theta_radians) * (pt.y - origin.y) + origin.x
        py = np.sin(theta_radians) * (pt.x - origin.x) + np.cos(theta_radians) * (pt.y - origin.y) + origin.y
        return Point(px, py)

    # Grasping rectangle files contain 4 lines for each rectangle.
    # Each line contains the x and y coordinate of a vertex of that rectangle separated by a space.
    # The first two coordinates of a rectangle define the line representing the orientation of the gripper plate.
    # Vertices are listed in counter-clockwise order.
    def draw_gripper_rect(self, file_path, output_file_path, positive=True):
        if positive:
            pattern = self.rc_pos_filename_pattern
            img_pattern = self.img_rc_pos_filename_pattern
            col1 = self.col_yellow
            col2 = self.col_green
        else:
            pattern = self.rc_neg_filename_pattern
            img_pattern = self.img_rc_neg_filename_pattern
            col1 = self.col_red
            col2 = self.col_blue
        rc_file_name = os.path.join(file_path, pattern.format(self.output_img_num))
        with open(rc_file_name, 'r') as rc_file:
            lines = [line.strip().split(" ") for line in rc_file.readlines()]
        coords = [[float(num) for num in line] for line in lines]
        # print(coords)
        rcs = [] #list of rectangles
        for i in range(0, len(coords), 4):
            rc = np.array(coords[i:i + 4])
            rcs.append(rc)
        img_filename = os.path.join(file_path, self.img_filename_pattern.format(self.output_img_num))
        img = Image.open(img_filename)
        draw = ImageDraw.Draw(img)
        for rc in rcs:
            pt1 = {'x': rc[0][0], 'y': rc[0][1]}
            pt2 = {'x': rc[1][0], 'y': rc[1][1]}
            pt3 = {'x': rc[2][0], 'y': rc[2][1]}
            pt4 = {'x': rc[3][0], 'y': rc[3][1]}
            draw.line([int(pt1['x']), int(pt1['y']), int(pt2['x']), int(pt2['y'])], width=2, fill=col1)
            draw.line([int(pt2['x']), int(pt2['y']), int(pt3['x']), int(pt3['y'])], width=2, fill=col2)
            draw.line([int(pt3['x']), int(pt3['y']), int(pt4['x']), int(pt4['y'])], width=2, fill=col1)
            draw.line([int(pt4['x']), int(pt4['y']), int(pt1['x']), int(pt1['y'])], width=2, fill=col2)
        # plt.imshow(img)
        # plt.show()
        output_file_name = os.path.join(output_file_path, img_pattern.format(self.output_img_num))
        img.save(output_file_name)
        plt.imshow(img)
        plt.show()

    def get_file_parts(self, img_filename):
        # drive, path = os.path.splitdrive(img_filename)
        path, filename = os.path.split(img_filename)
        filename, ext = os.path.splitext(filename)
        return [path, filename, ext]

def main():
    # create 1000 images per image
    num_of_images_per_image = 1 #1000
    num_of_images_per_folder = 1 #100

    for folder_num in range(0, 11):
        folder_num_str = format(folder_num, '02')
        file_path = 'D:\Gali\CS231N_Project\CornellDataset\\' + folder_num_str
        output_file_path = 'D:\Gali\CS231N_Project\CornellDataset\\data_augmentation\\' + folder_num_str
        for img_num in range(0, num_of_images_per_folder):
            img_num_str = folder_num_str + format(img_num, '02')
            myobject = GripperDataAugmentation(file_path, img_num_str, output_file_path);
            for i in range(0, num_of_images_per_image):
                myobject.randomize()
                myobject.data_augment()

if __name__ == "__main__":
    main()