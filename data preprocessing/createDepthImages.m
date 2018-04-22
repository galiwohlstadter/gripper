
clear all;
close all;

datasetPath = 'D:\Gali\CS231N_Project\CornellDataset\';
load(strcat(datasetPath, 'calibration'), 'rotationMatrices', 'translationVectors');

files = getBackgroundMapping();
filesnum = length(files);

backgroundsPath = strcat(datasetPath, 'backgrounds\*.png');
backgrounds = dir(backgroundsPath);
backroungsNum = length(backgrounds);

for i=1:backroungsNum
    rotationMatrix = rotationMatrices(i);
    translationVector = translationVectors(i);
    backgroundName = backgrounds(i).name;
    for j = 1:filesnum
        if (strcmp(files(j, 2), backgroundName) == 1)
            pngfilename = char(files(j, 1));
            [filepath, filename, ext] = fileparts(pngfilename);
            filename = strcat(filename(1:end-1),'.txt');            
            createDepthImage(filename, rotationMatrix, translationVector);
        end
    end
end

