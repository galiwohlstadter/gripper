function createDepthImage( filename, rotationMatrix, translationVector)

    ptCloud = loadpcd(filename);
    ptCloud = transpose(ptCloud);
    pointsNum = size(ptCloud, 1);
    
    img_height = 480;
    img_width = 640;
        
    worldPoints = ptCloud(:, 1:3);
    for i=1:pointsNum
        worldPoints(i, :) = worldPoints(i, 1:3) * rotationMatrix + translationVector;
    end
    
    %depths = worldPoints(:, 3);
    depths = sqrt(sum((worldPoints) .^ 2, 2));
    
    min_d = min(depths);
    max_d = max(depths);
    max_min_diff = max_d - min_d;
    normalized_depths = bsxfun(@minus, depths, min_d);
    normalized_depths = normalized_depths.*255;
    normalized_depths = 255 - normalized_depths./max_min_diff;

    depthImage = zeros(img_height, img_width, 'uint8');
    for i=1:pointsNum
        idx = ptCloud(i, 5);        
        col = mod(idx, img_width) + 1;
        row = floor(idx / img_width) + 1;
        depthImage(row, col) = normalized_depths(i);
    end       
    
    [filepath, filename, ext] = fileparts(filename);
    path = 'D:\Gali\CS231N_Project\CornellDataset\depths\';
    fileNameToSave = strcat(path, filename, '_d.png');
    imwrite(depthImage, fileNameToSave)
    %imshow(depthImage, [0 255]);
end

