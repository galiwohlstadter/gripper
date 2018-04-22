function [ rotationMatrix, translationVector ] = computeCameraCalibrationMatrix( filename, pointsNum )
    ptCloud = loadpcd(filename);
    ptCloud = transpose(ptCloud);
    allPointsNum = size(ptCloud, 1);
    %pointsNum = 1000; %size(ptCloud, 1);
    every = floor(allPointsNum / pointsNum);


    worldPoints = ptCloud(1:every:allPointsNum, 1:3);
    pointsNum = size(worldPoints, 1);
    imagePoints = zeros(pointsNum, 2, 'single');
    img_height = 480;
    img_width = 640;
    for i=1:pointsNum 
        j=(i - 1)* every + 1;
        %disp(j)
        idx = ptCloud(j, 5);        
        imagePoints(i,1) = mod(idx, img_width);
        imagePoints(i,2) = floor(idx / img_width);
    end
    %[cameraParams,imagesUsed,estimationErrors] = estimateCameraParameters(imagePoints,worldPoints);
    cameraParams = cameraParameters;
    [rotationMatrix,translationVector] = extrinsics(imagePoints, worldPoints, cameraParams);
    
%     save('calibrationMat','rotationMatrix','translationVector');
% 
%     %[orientation, location] = extrinsicsToCameraPose(rotationMatrix, translationVector);
% 
%     worldPoints = ptCloud(:, 1:3);
%     for i=1:allPointsNum
%         worldPoints(i, :) = worldPoints(i, 1:3) * rotationMatrix + translationVector;
%     end
%     %translatedPoints = bsxfun(@minus,worldPoints,translationVector);
%     %depths = sqrt(sum((translatedPoints) .^ 2, 2));
%     %depths = sqrt(sum((worldPoints) .^ 2, 2));
%     depths = worldPoints(:, 3);
% 
%     min_d = min(depths);
%     max_d = max(depths);
%     max_min_diff = max_d - min_d;
%     normalized_depths = bsxfun(@minus,depths,min_d);
%     normalized_depths = normalized_depths.*255;
%     normalized_depths = 255 - normalized_depths./max_min_diff;
% 
%     img_depth = zeros(img_height, img_width, 'uint32');
%     for i=1:allPointsNum
%         idx = ptCloud(i, 5);        
%         col = mod(idx, img_width) + 1;
%         row = floor(idx / img_width) + 1;
%         img_depth(row, col) = normalized_depths(i);
%     end       
% 
%     imshow(img_depth, [0 255]);
% 
end

