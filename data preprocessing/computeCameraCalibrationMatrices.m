%clear all;
%backgroundMapping.txt
clear all;
close all;
files = getBackgroundMapping();

datasetPath = 'D:\Gali\CS231N_Project\CornellDataset\';
backgroundsPath = strcat(datasetPath, 'backgrounds\*.png');
backgrounds = dir(backgroundsPath);
pointsNum = 5000;
backroungsNum = length(backgrounds);
rotationMatrices = zeros(3,3,backroungsNum);
translationVectors = zeros(backroungsNum, 3);
filesnum = length(files);

for i = 1:backroungsNum
    backgroundName = backgrounds(i).name;
    
    matrices = zeros(3,3,filesnum);
    vectors = zeros(filesnum, 3);
    matricesNum = 0;
    for j = 1:filesnum
        if (strcmp(files(j, 2), backgroundName) == 1)
            pngfilename = char(files(j, 1));
            [filepath, filename, ext] = fileparts(pngfilename);
            filename = strcat(filename(1:end-1),'.txt');            
            if exist(filename, 'file')
                [ rotationMatrix, translationVector ] = computeCameraCalibrationMatrix(filename, pointsNum);
                matrices(:,:,j) = rotationMatrix;                
                vectors(j, :) = translationVector;
                matricesNum = matricesNum + 1;
            end
        end
        if (j == filesnum) %save the mean matrix and vector
            rotationMatrices(:,:, i) = sum(matrices, 3) / matricesNum;
            translationVectors(i, :) = sum(vectors, 1) / matricesNum;
        end
    end
end

save(strcat(datasetPath, 'calibration'), 'rotationMatrices', 'translationVectors');


