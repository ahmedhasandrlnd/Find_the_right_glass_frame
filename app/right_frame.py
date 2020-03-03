from flask import Flask, render_template, url_for, redirect
from forms import FindForm
from flask import flash
import os, secrets
import argparse
import cv2
import numpy as np

#from handle_models import handle_output, preprocessing
from inference import Network

GENDER_TYPES=["female","male"]

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

#posts=[{'image_file':'default.jpg','title':'title','content':'Content'}]
posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018',
        'image_file':'default.jpg'
    }
]

def perform_inference(i,m,t,c=None,d="CPU"):
    '''
    Performs inference on an input image, given a model.
    '''
    # Create a Network for using the Inference Engine
    inference_network = Network()
    # Load the model in the network, and obtain its input shape
    n, c, h, w = inference_network.load_model(m, d, c)

    # Read the input image
    image = cv2.imread(i)

    ### TODO: Preprocess the input image
    preprocessed_image = preprocessing(image, h, w)

    # Perform synchronous inference on the image
    inference_network.sync_inference(preprocessed_image)

    # Obtain the output of the inference request
    output = inference_network.extract_output()

    ### TODO: Handle the output of the network, based on args.t
    ### Note: This will require using `handle_output` to get the correct
    ###       function, and then feeding the output to that function.
    process_func=handle_output(t)
    processed_output = process_func(output, image.shape)

    # Create an output image based on network
    try: 
        output_image = create_output_image(t, image, processed_output)
        print("Success")
    except:
        output_image=image
        print("Error")

    # Save down the resulting image
    cv2.imwrite("outputs/{}-output_m2.png".format(t), output_image)

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
        glasses=cv2.imread('images/glasses/glassf3.png',-1)
        print(glasses.shape)
        scale=((output[36]-output[68])**2+(output[37]-output[69])**2)**(1/2.0)
        glasses=cv2.resize(glasses,(int(scale),int(scale*glasses.shape[0]/glasses.shape[1])))
        print(glasses.shape)
        print(image.shape)
        p0=(output[0]+10,output[1]+10)
        p1=(output[24],output[1]+10)
        p12=(output[24]-5,output[25])
        p13=(output[26],output[27])
        p14=(output[0]+15,output[25])
        print(output[36],output[37],output[68],output[69])
        print(output[0],output[1],output[4],output[5])
        #image_midpoint=[(output[0]+output[4])/2 (output[1]+output[5])/2]
        #print(image_midpoint)
        #glass_midpoint=glass.shape/2
        #print(glass_midpoint)
        translation_vertical=int((output[1]+output[5])/2-glasses.shape[1]/2)
        print(translation_vertical)
        translation_horizontal=int((output[0]+output[4])/2-glasses.shape[0]/2)
        print(translation_horizontal)
        pr1=(output[4]-10,output[35])
        pr2=(output[34]+5,output[5]+10)
        #cv2.resize(glasses,[image.shape[1],image.shape[0]])
        #for i in range(0,len(output),2):
        #    cv2.circle(image, (output[i],output[i+1]), 1, (0, 0, 255), -1)
        #cv2.circle(image, (26,17), 1, (0, 0, 255), -1)
        #cv2.circle(image, (17,26), 1, (0, 255, 0), -1)
        #cv2.circle(image, (80,80), 1, (255, 0, 0), -1)
        #cv2.circle(image, (111,56), 1, (0, 255, 0), -1)
        #cv2.circle(image, (84,50), 1, (0, 0, 255), 2)
        #image=cv2.add(image,glasses)
        points = np.array([p0, p1, p12,p14])
        #cv2.fillConvexPoly(image,points,(0,0,0))
        #cv2.rectangle(image,p12,p0,(0,0,255),2)
        #cv2.rectangle(image,pr1,pr2,(0,0,255),2)
        gw,gh,gc = glasses.shape
        #for i in range(0,gw):       # Overlay the filter based on the alpha channel(mustache1 male4)
        #    for j in range(0,gh):
        #        if glasses[i,j][3] != 0:
        #            image[i+133,j+62]=glasses[i,j][:-1]
        print(image.shape)
        for i in range(0,gw):       # Overlay the filter based on the alpha channel(glass)
            for j in range(0,gh):
                if glasses[i,j][3] != 0:
                    image[i+translation_vertical,j+translation_horizontal]=glasses[i,j][:-1]
        print(image.shape)
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
    Handles the output of the Car Metadata model.
    Returns two integers: the argmax of each softmax output.
    The first is for color, and the second for type.
    '''
    # TODO 1: Get the argmax of the "color" output
    fc=output['align_fc3']
    #print(fc[0][0],fc[0][1],fc[0][2],fc[0][3] )
    coords=[]
    for i in range(0,len(fc[0]),2):
        x=int(fc[0][i]*input_shape[1])
        y=int(fc[0][i+1]*input_shape[0])
        coords.append(x)
        coords.append(y)
    #print(input_shape)
    print(len(coords))
    return coords

def handle_gender(output, input_shape):
    #print(output.keys())
    print(output["prob"].shape)
    age=int(output["age_conv3"].flatten()[0]*100)
    gender_type=output["prob"].flatten()
    gender_class=np.argmax(gender_type) 
    print(gender_class)
    print(age)  
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


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/uploaded_pics', picture_fn)
    #picture_path = '/static/uploaded_pics/'+ picture_fn
    output_size = (125, 125)
    #i = Image.open(form_picture)
    #i.thumbnail(output_size)
    form_picture.save(picture_path)
    return picture_fn

@app.route("/find", methods=['GET','POST'])
def find():
	form=FindForm()
	if form.validate_on_submit():
		flash(f'Image selected with filename {form.picture.data.filename}!','success')
		picture_file = save_picture(form.picture.data)
		posts[0]['image_file'] = picture_file
		flash(f'Image saved with filename {picture_file}!','success')
		perform_inference(i="static/uploaded_pics"+picture_file,m="models/age-gender-recognition-retail-0013.xml",t="GENDER")
		return redirect(url_for('home'))

	return render_template('find.html', title='Find Frame', form=form)


if __name__ == '__main__':
    app.run(debug=True)