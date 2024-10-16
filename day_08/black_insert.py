run("Close All");
print("\\Clear");

var
null;
// black_line_lp is use
to
control
the
length
of
black
line;
// the
greater
the
value
of
black_line_lp, the
shorter
the
black
line.
black_line_lp = 100;

// lower_value is lower
limit
of
the
black
line
pixel
value
lower_value = 200;
// max_value is max
limit
of
the
black
line
pixel
value
max_value = 10000;

b_w_path = "C:/BrowserDownload/CT_pro/"

black_tif = b_w_path + "black.tif";
white_tif = b_w_path + "white.tif";

// target
picture
chooseDirectory = getDirectory("Choose the directory containing your images");
if (chooseDirectory == null) {
print("User canceled the directory selection.");
return;
}
list_s = getFileList(chooseDirectory);
print("   list_s.length: " + list_s.length);

// make
directory
// directory
for raw to tiff
file_out_tiff = chooseDirectory + "out_tiff" +"\\";
File.makeDirectory(file_out_tiff);
// directory for subtract black image and delete black line
file_out_p = chooseDirectory + "out_p" +"\\";
File.makeDirectory(file_out_p);
// directory for divide white image
file_out_p_d = chooseDirectory + "out_p_d" +"\\";
File.makeDirectory(file_out_p_d);

// raw to tiff
for (list_i = 0; list_i < list_s.length; list_i++) {
file_raw = chooseDirectory + list_s[list_i];
if (endsWith(file_raw, ".raw")) {
run("Raw...", "open="+"["+file_raw+"]" +"image=[16-bit Unsigned] width=2340 height=2882 little-endian");
saveAs("Tiff", file_out_tiff + getTitle());
close(getTitle());
}
}

// black
image
open(black_tif);
width = getWidth();
height = getHeight();
black_line_length = Math.round(height / black_line_lp);
print(black_line_length);

// white
image
open(white_tif);

// white
image
subtract
black
image and delete
black
line
imageCalculator("Subtract create 32-bit", "white.tif", "black.tif");
selectImage("Result of " + "white.tif");
lower_value_number = newArray(width, 1);
value_column = newArray(width, 1);
for (i = 0; i < width; i++)
{
value = 0;
lower_value_number[i] = 0;
for (j = 0; j < height; j++){
if (getPixel(i, j) < max_value) {
value = getPixel(i, j)+value;
}
if (getPixel(i, j) <= lower_value | | getPixel(i, j) >= max_value) {
lower_value_number[i] ++;
}
}
value_column[i] = value / height;
}
print(value_column[width - 1]);
Array.getStatistics(value_column, min_vc, max_vc, mean_vc);
print("   min: " + min_vc);
print("   max: " + max_vc);
print("   mean: " + mean_vc);

for (i = 1; i < width-1; i++)
{
if (lower_value_number[i] > black_line_length) {
for (j = 0; j < height; j++){
pixel_value = (getPixel(i-1, j) + getPixel(i+1, j)) / 2;
setPixel(i, j, pixel_value);
}
}
}
// 淇濆瓨澶勭悊杩囩殑鍥惧儚
saveAs("Tiff", b_w_path + "w_sub_b_dbl");
run("Close All");

list = getFileList(file_out_tiff);
// black
picture

open(black_tif);

selectImage('black.tif');

lower_value_number = newArray(width, 1);
value_column = newArray(width, 1);
for (i = 0; i < width; i++)
{
value = 0;
lower_value_number[i] = 0;
for (j = 0; j < height; j++){
if (getPixel(i, j) < max_value) {
value = getPixel(i, j)+value;
}
if (getPixel(i, j) < lower_value | | getPixel(i, j) > max_value) {
lower_value_number[i] ++;
}
}
value_column[i] = value / height;
}


for (i = 1; i < width-1; i++){
    if (lower_value_number[i] > black_line_length) {
    for (j = 0; j < height; j++){

    pixel_value = (getPixel(i-1, j) + getPixel(i+1, j)) / 2;

    setPixel(i, j, pixel_value);
    }
    }
}

saveAs("Tiff", "C:/BrowserDownload/CT_pro/" + "processed.tif");

close();
close('balck.tif');

for (list_i = 0; list_i < list.length; list_i++)
{
if (endsWith(list[list_i], ".tif") | | endsWith(list[list_i], ".tiff")) {
// 鎵撳紑鍥惧儚
open(file_out_tiff + list[list_i]);
open("C:/BrowserDownload/CT_pro/processed.tif");
imageCalculator("Subtract create 32-bit", list[list_i], "processed.tif");
selectImage("Result of "+list[list_i]);
lower_value_number = newArray(width, 1);
value_column = newArray(width, 1);
for (i = 0; i < width; i++){
value = 0;
lower_value_number[i] = 0;
for (j = 0; j < height; j++){
if (getPixel(i, j) < max_value) {
value = getPixel(i, j)+value;
}
if (getPixel(i, j) < lower_value | | getPixel(i, j) > max_value) {
lower_value_number[i] ++;
}
}
value_column[i] = value / height;
}
print(value_column[width-1]);
Array.getStatistics(value_column, min_vc, max_vc, mean_vc);
print("   min: "+min_vc);
print("   max: "+max_vc);
print("   mean: "+mean_vc);

for (i = 1; i < width-1; i++){
if (lower_value_number[i] > black_line_length ) {
for (j = 0; j < height; j++){
pixel_value = (getPixel(i-1, j) + getPixel(i+1, j)) / 2;
setPixel(i, j, pixel_value);
}
}
}

// 淇濆瓨澶勭悊杩囩殑鍥惧儚
saveAs("Tiff", file_out_p + list[list_i]);

// 鍏抽棴褰撳墠琚鐞嗙殑鍥惧儚
close(list[list_i]);
// 鍏抽棴褰撳墠鍥惧儚
close();
}
}

list_d = getFileList(file_out_p);
for (list_i = 0; list_i < list_d.length; list_i++)
{
open(file_out_p + list_d[list_i]);
open(b_w_path + "w_sub_b_dbl.tif");
imageCalculator("Divide create 32-bit", list_d[list_i], "w_sub_b_dbl.tif");
// 淇濆瓨澶勭悊杩囩殑鍥惧儚
saveAs("Tiff", file_out_p_d + list_d[list_i]);

// 鍏抽棴褰撳墠琚鐞嗙殑鍥惧儚
close(list_d[list_i]);
// 鍏抽棴褰撳墠鍥惧儚
close();
}

print("All images in the folder have been processed.");
