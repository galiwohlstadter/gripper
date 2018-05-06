from gripperDataAugmentation import GripperDataAugmentation

for folder_num in range(0, 11):
    folder_num_str = format(folder_num, '02')
    file_path = 'D:\Gali\CS231N_Project\CornellDataset\\' + folder_num_str
    output_file_path = 'D:\Gali\CS231N_Project\CornellDataset\\data_augmentation\\' + folder_num_str
    for img_num in range(0, 100):
        img_num_str = folder_num_str + format(img_num, '02')
        myobject = GripperDataAugmentation(file_path, img_num_str, output_file_path);
        # create 1000 images per image
        for i in range(0, 1000):
            myobject.randomize()
            myobject.data_augment()

# myobject.draw_gripper_rect(output_file_path, output_file_path, True)
# myobject.draw_gripper_rect(output_file_path, output_file_path, False)
