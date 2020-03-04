import cv2
import numpy as np


def handle_pose(output, input_shape):
    '''
    Handles the output of the Pose Estimation model.
    Returns ONLY the keypoint heatmaps, and not the Part Affinity Fields.
    '''
    # TODO 1: Extract only the second blob output (keypoint heatmaps)
    heatmaps = output['Mconv7_stage2_L2']
    # TODO 2: Resize the heatmap back to the size of the input
    # Create an empty array to handle the output map
    out_heatmap = np.zeros([heatmaps.shape[1], input_shape[0], input_shape[1]])
    # Iterate through and re-size each heatmap
    for h in range(len(heatmaps[0])):
        out_heatmap[h] = cv2.resize(heatmaps[0][h], input_shape[0:2][::-1])

    return out_heatmap


def handle_text(output, input_shape):
    '''
    Handles the output of the Text Detection model.
    Returns ONLY the text/no text classification of each pixel,
        and not the linkage between pixels and their neighbors.
    '''
    # TODO 1: Extract only the first blob output (text/no text classification)
    text_classes = output['model/segm_logits/add']
    # TODO 2: Resize this output back to the size of the input
    out_text = np.empty([text_classes.shape[1], input_shape[0], input_shape[1]])
    for t in range(len(text_classes[0])):
        out_text[t] = cv2.resize(text_classes[0][t], input_shape[0:2][::-1])

    return out_text


def handle_car(output, input_shape):
    '''
    Handles the output of the Car Metadata model.
    Returns two integers: the argmax of each softmax output.
    The first is for color, and the second for type.
    '''
    # TODO 1: Get the argmax of the "color" output
    color=output["color"].flatten()
    car_type=output["type"].flatten()
    color_class=np.argmax(color)
    # TODO 2: Get the argmax of the "type" output
    type_class=np.argmax(car_type)
    print(color_class)
    print(type_class)
    
    return color_class, type_class

def handle_facial(output, input_shape):
    '''
    Handles the output of the Facial landmarks Metadata model.
    Returns the coordinates of 35 facial landmarks.
    '''
    #print(output.keys())
    fc=output['align_fc3']
    
    coords=[]
    for i in range(0,len(fc[0]),2):
        x=int(fc[0][i]*input_shape[1])
        y=int(fc[0][i+1]*input_shape[0])
        coords.append(x)
        coords.append(y)
    return coords

def handle_glass(output, input_shape):
    '''
    Handles the output of the Facial landmarks Metadata model.
    Returns the coordinates of 35 facial landmarks.
    '''
    #print(output.keys())
    fc=output['align_fc3']
    
    coords=[]
    for i in range(0,len(fc[0]),2):
        x=int(fc[0][i]*input_shape[1])
        y=int(fc[0][i+1]*input_shape[0])
        coords.append(x)
        coords.append(y)
    return coords

def handle_gender(output, input_shape):
    '''
    Handles the output of the Gender and Age Metadata model.
    Returns the age and gender: argmax of softmax output
    '''
    #print(output.keys())
    age=int(output["age_conv3"].flatten()[0]*100)
    gender_type=output["prob"].flatten()
    gender_class=np.argmax(gender_type) 

    return age, gender_class


def handle_output(model_type):
    '''
    Returns the related function to handle an output,
        based on the model_type being used.
    '''
    if model_type == "POSE":
        return handle_pose
    elif model_type == "TEXT":
        return handle_text
    elif model_type == "CAR_META":
        return handle_car
    elif model_type=="FACIAL":
        return handle_facial
    elif model_type=="GENDER":
        return handle_gender
    elif model_type=="GLASS":
        return handle_glass    
    else:
        return None


'''
The below function is carried over from the previous exercise.
You just need to call it appropriately in `app.py` to preprocess
the input image.
'''
def preprocessing(input_image, height, width):
    '''
    Given an input image, height and width:
    - Resize to width and height
    - Transpose the final "channel" dimension to be first
    - Reshape the image to add a "batch" of 1 at the start 
    '''
    image = np.copy(input_image)
    image = cv2.resize(image, (width, height))
    image = image.transpose((2,0,1))
    image = image.reshape(1, 3, height, width)

    return image