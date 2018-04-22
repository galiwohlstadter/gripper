function [ files ] = getBackgroundMapping(  )
%path = 'D:\Gali\CS231N_Project\CornellDataset\backgrounds\';
    fname = 'backgroundMapping.txt';
    fp = fopen(fname, 'r');    
    c = textscan(fp, '%s%s');
    files = [];
    for j=1:length(c)
        files = [files; c{j}'];
    end
    files = files';
end

