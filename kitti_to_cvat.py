#------------------------------------------------------------------------------
#
#  Code to generate cvat-xml file from kitti_with_attributes files
#
#  Works for kitti_with_attributes files only and not on kitti file
#
#  kitti_with_attributes should be generated by the cvat-kitti script
#
#  creates a xml file similiar to CVAT XML V1.1
#------------------------------------------------------------------------------


# Library for creating the xml tree

from xml.etree.ElementTree import Element, SubElement, Comment, tostring 

# Library for pretty printing of the generated xml tree

from bs4 import BeautifulSoup         

# Library for traversing folders

import os       

# Library for accessing time

import datetime                                                           

# To generate time for created tag

generated_on = str(datetime.datetime.now())

# Path_to_folder : Path of folder containing the kitti_with_attributes files
# attribute_separator : character separating the attributes in kitti_with_attributes label name


def kitti_to_cvat_xml(Path_to_folder,attribute_separator = "*"):
    
    # Path of directory containing the kitti_with_attributes folder

    Path_to_dir =os.path.dirname(Path_to_folder)

    # Accessing all the files in the kitti_with_attributes folder through kitti_files

    kitti_files=os.listdir(Path_to_folder)

    # Creating a directory for the xml file generated

    os.mkdir(Path_to_dir+'/'+'xml_generated')

    # Initialising lists for storing labels and attributes for metadata

    labels_list=list()
    labels_attribute_list=list()
    image_id_map=dict()

    # Generating labels for xml metadata by traversing every kitti file in directory

    for file in kitti_files:
    
        # Opening each kitti file and storing them into a variable
    
        f=open(Path_to_folder+"/"+file,'r')
        kitti_file=f.readlines()
        f.close()
    
        # Getting the extra attributes which are present in the description on every kitti_with_attributes file
    
        kitti_attrib = kitti_file[2].rsplit("-")[1].split(",")
    
        # Converting the extra attributes into suitable list format.
    
        kitti_attrib[0]=kitti_attrib[0][2:]
        kitti_attrib[-1]=kitti_attrib[-1][:len(kitti_attrib[-1])-2]

        # skipping the description text in kitti_with_attributes and accessing the kitti_with_attributes format
    
        for line in kitti_file[7:(len(kitti_file)-1)]:
        
            # splitting class name from attributes and appending them to the list if they are not presented already
        
            if line.rsplit()[0].split(attribute_separator,-1)[-1] not in labels_list:
            
                labels_list.append(line.rsplit()[0].split(attribute_separator,-1)[-1])
            
                temp_list=list()
            
                for k in range(0,len(line.rsplit()[0].split(attribute_separator,-1))-1):
                
                    if line.rsplit()[0].split(attribute_separator,-1)[k] != "NaN":
                    
                        temp_list.append(kitti_attrib[k])
            
                labels_attribute_list.append(temp_list)            


    # Building the xml tree 

    root=Element("annotations")

    version = SubElement(root,'version')
    version.text="1.1"

    meta = SubElement(root,'Meta')

    task = SubElement(meta,'task')

    Id = SubElement(task,'Id')
    Id.text="to insert id"

    name = SubElement(task,'name')
    name.text=os.path.basename(Path_to_dir)

    size = SubElement(task,'size')
    size.text="to insert size of file"

    mode = SubElement(task,'mode')
    mode.text = "annotation"

    overlap = SubElement(task,'overlap')
    overlap.text="0"

    bugtracker = SubElement(task,'bugtracker')

    created = SubElement(task,'created')
    created.text=generated_on

    updated = SubElement(task,'updated')
    updated.text="insert updated time"

    start_frame = SubElement(task,'start_frame')
    start_frame.text="0"

    stop_frame = SubElement(task,'stop_frame')
    stop_frame.text="0"

    frame_filter = SubElement(task,'frame_filter')

    z_order = SubElement(task,'z_order')
    z_order.text=False

    labels = SubElement(task,'labels')

    # constructing the label tag in the xml tree

    for label_index in range(0,len(labels_list)):
    
        label = SubElement(labels,'label')
        name = SubElement(label,'name')
        name.text = labels_list[label_index]
    
        attributes = SubElement(label,'attributes')
    
        # constructing the attribute tag for respective label
    
        for attrb in labels_attribute_list[label_index]:
        
            attribute = SubElement(attributes,'attribute')   

            name = SubElement(attribute,'name')
            name.text = attrb.replace("\'","")

            mutable = SubElement(attribute,'mutable')
            mutable.text = "False"

            input_type = SubElement(attribute,'input_type')
            input_type.text="select"

            default_value = SubElement(attribute,'default_value')

            values = SubElement(attribute,'values')
            values.text =""

    segments=SubElement(task,'segments')

    segment = SubElement(segments,'segment')

    Id=SubElement(segment,'Id')
    Id.text="insert id"

    start=SubElement(segment,'start')
    start.text='insert start'

    stop = SubElement(segment,'stop')
    stop.text = 'insert stop'

    url = SubElement(segment,'url')
    url.text='insert url'

    owner = SubElement(task,'owner')

    username = SubElement(owner,'username')
    username.text = "admin"

    email = SubElement(owner,'email')
    email.text = "nikhil@detecttehnologies.com"

    assignee=SubElement(task,"assignee")

    dumped = SubElement(meta,'dumped')
    dumped.text="insert time"
  
    # Accessing kitti files for generating image tag in XML tree

    for file in kitti_files:
    
        # Reading files in the folder
    
        f=open(Path_to_folder+"/"+file,'r')
        kitti_format=f.read()
        f.close()
    
        # generating the image tag
    
        image = SubElement(root,'image')
        image.set('Id',"generate id")
        image.set("name",file)
        image.set("height","enter height")
        image.set("width","enter width")  
    
        image_id_map[file]=None

        for j in kitti_format.split("\n")[7:]:
        
            # Generating the box tag for the corresponding image tag
        
            box = SubElement(image,'box')
            box.set('label',j.split(" ")[0].rsplit(attribute_separator)[-1])
            box.set('occluded',j.split(" ")[2])
            box.set('xtl',j.split(" ")[4])
            box.set('ytl',j.split(" ")[5])
            box.set('xbr',j.split(" ")[6])
            box.set('ybr',j.split(" ")[7])
        
            for t in range(0,len(max(labels_attribute_list))):
            
                # Creating a attribute for a box if the corresponding value in the attribute column is not 0.00
            
                if(j.split(" ")[0].rsplit(attribute_separator)[t] != "NaN"):
                
                    attribute = SubElement(box,'attribute')
                    attribute.set('name',max(labels_attribute_list)[t].replace("\'", ""))
                    attribute.text=j.split(" ")[0].rsplit(attribute_separator)[t]


    # Writing the xml file into the file
                
    soup=BeautifulSoup(tostring(root),'xml')
    
    l1=Path_to_dir+'/'+'xml_generated'+'/'+os.path.basename(Path_to_dir)
    path_to_xml_file=l1+'.xml'

    path_to_imagemap_file=Path_to_dir+'/'+'xml_generated'+'/'+'id_imagemap.txt'
    f2=open(path_to_imagemap_file,"a")
    f2.write(str(image_id_map))
    f2.close()
    
    f1=open(path_to_xml_file,"a")
    f1.write(soup.prettify())
    f1.close()

###___END___###
