import argparse
import cv2
import numpy as np

from handle_models import handle_output, preprocessing
from inference import Network


CAR_COLORS = ["white", "gray", "yellow", "red", "green", "blue", "black"]
CAR_TYPES = ["car", "bus", "truck", "van"]
GENDER_TYPES=["female","male"]


def get_args():
    '''
    Gets the arguments from the command line.
    '''

    parser = argparse.ArgumentParser("Basic Edge App with Inference Engine")
    # -- Create the descriptions for the commands

    c_desc = "CPU extension file location, if applicable"
    d_desc = "Device, if not CPU (GPU, FPGA, MYRIAD)"
    i_desc = "The location of the input image"
    m_desc = "The location of the model XML file"
    t_desc = "The type of model: POSE, TEXT , CAR_META, FACIAL or GENDER"

    # -- Add required and optional groups
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # -- Create the arguments
    required.add_argument("-i", help=i_desc, required=True)
    required.add_argument("-m", help=m_desc, required=True)
    required.add_argument("-t", help=t_desc, required=True)
    optional.add_argument("-c", help=c_desc, default=None)
    optional.add_argument("-d", help=d_desc, default="CPU")
    args = parser.parse_args()

    return args


def get_mask(processed_output):
    '''
    Given an input image size and processed output for a semantic mask,
    returns a masks able to be combined with the original image.
    '''
    # Create an empty array for other color channels of mask
    empty = np.zeros(processed_output.shape)
    # Stack to make a Green mask where text detected
    mask = np.dstack((empty, processed_output, empty))

    return mask


def create_output_image(model_type, image, output):
    '''
    Using the model type, input image, and processed output,
    creates an output image showing the result of inference.
    '''
    if model_type == "POSE":
        # Remove final part of output not used for heatmaps
        output = output[:-1]
        # Get only pose detections above 0.5 confidence, set to 255
        for c in range(len(output)):
            output[c] = np.where(output[c]>0.5, 255, 0)
        # Sum along the "class" axis
        output = np.sum(output, axis=0)
        # Get semantic mask
        pose_mask = get_mask(output)
        # Combine with original image
        image = image + pose_mask
        return image
    elif model_type == "TEXT":
        # Get only text detections above 0.5 confidence, set to 255
        output = np.where(output[1]>0.5, 255, 0)
        # Get semantic mask
        text_mask = get_mask(output)
        # Add the mask to the image
        image = image + text_mask
        return image
    elif model_type == "CAR_META":
        # Get the color and car type from their lists
        color = CAR_COLORS[output[0]]
        car_type = CAR_TYPES[output[1]]
        # Scale the output text by the image shape
        scaler = max(int(image.shape[0] / 1000), 1)
        # Write the text of color and type onto the image
        image = cv2.putText(image, 
            "Color: {}, Type: {}".format(color, car_type), 
            (50 * scaler, 100 * scaler), cv2.FONT_HERSHEY_SIMPLEX, 
            2 * scaler, (0,255, 0), 3 * scaler)
        return image
    elif model_type == "FACIAL":
        image_copy = np.copy(image)
        glasses=cv2.imread('images/glasses/glass9.png',-1)
        #print(glasses.shape)
        scale=((output[36]-output[68])**2+(output[37]-output[69])**2)**(1/2.0)
        glasses=cv2.resize(glasses,(int(scale),int(scale*glasses.shape[0]/glasses.shape[1])))
        #print(glasses.shape)
        #print(image.shape)
        p0=(output[0]+10,output[1]+10)
        p1=(output[24],output[1]+10)
        p12=(output[24]-5,output[25])
        p13=(output[26],output[27])
        p14=(output[0]+15,output[25])
        #print(output[36],output[37],output[68],output[69])
        #print(output[0],output[1],output[4],output[5])
        #image_midpoint=[(output[0]+output[4])/2 (output[1]+output[5])/2]
        #print(image_midpoint)
        #glass_midpoint=glass.shape/2
        #print(glass_midpoint)
        translation_vertical=int((output[1]+output[5])/2-glasses.shape[1]/2)
        #print(translation_vertical)
        translation_horizontal=int((output[0]+output[4])/2-glasses.shape[0]/2)
        #print(translation_horizontal)
        pr1=(output[4]-10,output[35])
        pr2=(output[34]+5,output[5]+10)
        #cv2.resize(glasses,[image.shape[1],image.shape[0]])
        for i in range(0,len(output),2):
            cv2.circle(image, (output[i],output[i+1]), 4, (255, 0, 0), -1)

            font                   = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (output[i],output[i+1])
            fontScale              = 0.7
            fontColor              = (255,255,255)
            lineType               = 2

            cv2.putText(image,'p'+str(int(i/2)), 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)             
            #cv2.putText(image, i, (image.shape[0]/2,image.shape[1]/2), cv2.FONT_HERSHEY_SIMPLEX, 1 * scaler, (0,0,255), 2 * scaler)
        #cv2.circle(image, (26,17), 1, (0, 0, 255), -1)
        #cv2.circle(image, (17,26), 1, (0, 255, 0), -1)
        #cv2.circle(image, (80,80), 1, (255, 0, 0), -1)
        #cv2.circle(image, (111,56), 1, (0, 255, 0), -1)
        #cv2.circle(image, (84,50), 1, (0, 0, 255), 2)
        #image=cv2.add(image,glasses)
        #image = cv2.putText(image, "{},{} ".format("person1","glass9"), (20, image.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 1 * scaler, (0,255, 0), 2 * scaler)
        points = np.array([p0, p1, p12,p14])
       
        #cv2.fillConvexPoly(image,points,(0,0,0))
        #cv2.rectangle(image,p12,p0,(0,0,255),2)
        #cv2.rectangle(image,pr1,pr2,(0,0,255),2)
        gw,gh,gc = glasses.shape
        #for i in range(0,gw):       # Overlay the filter based on the alpha channel(mustache1 male4)
        #    for j in range(0,gh):
        #        if glasses[i,j][3] != 0:
        #            image[i+133,j+62]=glasses[i,j][:-1]
        #print(image.shape)
        #for i in range(0,gw):       # Overlay the filter based on the alpha channel(glass)
        #    for j in range(0,gh):
        #        if glasses[i,j][3] != 0:
        #            image[i+translation_vertical,j+translation_horizontal]=glasses[i,j][:-1]
                    #print(image.shape)
        return image
    elif model_type == "GENDER":
        print(output[0], output[1])
        age = output[0]
        print(age)
        gender_type = GENDER_TYPES[output[1]]
        
        print(gender_type)
        # Scale the output text by the image shape
        scaler = max(int(image.shape[0] / 5000), 1)
        # Write the text of color and type onto the image
        image = cv2.putText(image, 
            "{},{} ".format(age,gender_type), 
            (20, image.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 
            1 * scaler, (0,255, 0), 2 * scaler)
        return image
    else:
        print("Unknown model type, unable to create output image.")
        return image


def perform_inference(args):
    '''
    Performs inference on an input image, given a model.
    '''
    # Create a Network for using the Inference Engine
    inference_network = Network()
    # Load the model in the network, and obtain its input shape
    n, c, h, w = inference_network.load_model(args.m, args.d, args.c)

    # Read the input image
    image = cv2.imread(args.i)

    ### TODO: Preprocess the input image
    preprocessed_image = preprocessing(image, h, w)

    # Perform synchronous inference on the image
    inference_network.sync_inference(preprocessed_image)

    # Obtain the output of the inference request
    output = inference_network.extract_output()

    ### TODO: Handle the output of the network, based on args.t
    ### Note: This will require using `handle_output` to get the correct
    ###       function, and then feeding the output to that function.
    process_func=handle_output(args.t)
    processed_output = process_func(output, image.shape)

    # Create an output image based on network
    try: 
        output_image = create_output_image(args.t, image, processed_output)
        print("Success")
    except:
        output_image=image
        print("Error")

    # Save down the resulting image
    #cv2.imwrite("outputs/model0/{}-output9.png".format(args.t), output_image)
    cv2.imwrite("outputs/{}-output_marks.png".format(args.t), output_image)

def main():
    args = get_args()
    perform_inference(args)


if __name__ == "__main__":
    main()
