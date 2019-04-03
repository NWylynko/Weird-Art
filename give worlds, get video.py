import os, imageio, cv2, glob
from PIL import Image, ImageFilter

#user set vars

#search terms to get images of
#searchterms = ['White', 'silver', 'grey', 'black', 'navy', 'blue', 'cerulean', 'sky blue', 'turquoise', 'blue-green', 'azure', 'teal', 'cyan', 'green', 'lime', 'yellow', 'gold', 'amber', 'orange', 'brown', 'orange-red', 'red', 'maroon', 'rose', 'red-violet', 'pink', 'magenta', 'purple', 'blue-violet', 'indigo', 'violet', 'peach', 'apricot', 'ochre', 'plum']
#searchterms = ['amber', 'orange', 'brown', 'orange-red', 'red'] #reds
searchterms = ['navy', 'blue', 'cerulean', 'sky blue', 'turquoise', 'blue-green']

dir = "blue/" #directory to use
fps = 12 #the frames per second the video runs at
size = 1000 #the pixels height and width ways
video_name = "blue.mp4" #name of the outputed video

#make folders
if not os.path.exists(dir):
    os.makedirs(dir)
if not os.path.exists(dir+"tmp/html"):
    os.makedirs(dir+"tmp")
if not os.path.exists(dir+"tmp/html"):
    os.makedirs(dir+"tmp/html")
if not os.path.exists(dir+"tmp/in-images"):
    os.makedirs(dir+"tmp/in-images")
if not os.path.exists(dir+"tmp/out-images"):
    os.makedirs(dir+"tmp/out-images")

#downloads the html from the searchterms given
for terms in searchterms:
    #uses wget in terminal to download file, should use the wget for python but i cant be bothered
    os.system("wget https://www.pexels.com/search/" + terms + " -O '" + dir + "tmp/html/" + terms + ".html'")

#get urls of photos from html file
urls = []
names = []
tags = []

for terms in searchterms:
    filedir = dir + "tmp/html/" + terms + ".html" #get the html file
    file = open(filedir, "r") #open the file
    first = (file.read().split('data-large-src="')) #split the file text just before the link
    for i in range(1, len(first) - 1):
        second = first[i].split('" data-tiny-src="')[0] #split strings at end of url
        name = second.split("photos/")[1].split("/")[0] #get the name of the file from the url
        tag = second.split("photos/")[1].split(".")[1].split("?")[0] #get the file extension
        urls.append(second) #add to list
        names.append(name) #add to list
        tags.append(tag) #add to list

#download the images from the urls
if not glob.glob(dir+"tmp/in-images/*"):
    for i in range(len(urls)):
        cmd = ("wget -O '" + dir + "tmp/in-images/" + names[i] + "." + tags[i] + "' '" + urls[i] + "'")
        os.system(cmd)

images = []
combined = []

#get list of images
files = os.listdir(dir + "tmp/in-images") #get all photos in dir
for i in files: #for all files in the dir
    if i[:1] != ".": #if not a hidden file
        images.append(i) #add to list of images

#edit each photo
for i in images:
    photo = Image.open(dir + "tmp/in-images/" + i) #open photo from list
    width, height = photo.size #get width and height

    #makes the image square by getting the smaller length
    if width > height:
        sizeCrop = height
    else:
        sizeCrop = width

    photo = photo.crop((0, 0, sizeCrop, sizeCrop)) #crops image
    photo = photo.resize((size, size), Image.ANTIALIAS) #resizes to set size
    photo.save(dir + "tmp/out-images/" + i) #save image to file

    r, g, b = imageio.imread(dir + "tmp/out-images/" + i).mean(axis=(0,1)) #get average colour of image
    combined.append(r*g*b) #times together and add to list

    percentdone = (images.index(i) / len(images) * 100) #calculate percent done
    print("edited and got average: " + i + " | Done: " + str(percentdone)) #display image edited and percent donec

#make into video
sortedImages = [images for _,images in sorted(zip(combined,images))] #sort images by combine
video = cv2.VideoWriter(dir + video_name, 0, fps, (size, size)) #start creating video

for image in sortedImages:
    video.write(cv2.imread(dir + "tmp/out-images/" + image)) #adds frame to video
    percentdone = (sortedImages.index(image) / len(sortedImages) * 100) #calculate percent dome
    print("makevideo: " + image + " | Done: " + str(percentdone)) #display frame and percent done

cv2.destroyAllWindows()
video.release()
