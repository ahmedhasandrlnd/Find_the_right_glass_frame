# Glass Frame Preview

<a id='index'></a>
## Table of Contents
- [Project Overview](#overview)
- [How AI works](#works)
- [Usage](#usage)
- [Code](#code)
- [References](#ref)


<a id='video'></a>
**_[Deployed App](http://exampleframe.com.s3-website.ca-central-1.amazonaws.com/)_**

![Right Frame Preview](gif/Glass_frame_preview.gif)

**_[Presentation](https://docs.google.com/presentation/d/1dR0kyp0K7dAWPLHHLWCjR6mkAK-vTtT0cLlMxEoJp7o/edit?usp=sharing)_**

![Presentation](gif/presentation.gif)
<hr/> 

[Back to Table of Content](#index)


<a id='overview'></a>
## Project Overview
When someone wants to get a new glass frame, he/she has to go through a process of trial and error. Maybe he/she finds some eyeglasses attractive on display in the optical shop, but not so great when he/she try them on. Depending on face shapes, skin tones, hair color and eye color, a certain glass frame looks awesome to a certain person. So, sometimes it become quite hard for a person to choose a right glass frame in a optical shop. <br/>
Artificial Intelligence (AI) can come as rescue in this scenario. AI is already changing almost every spheres of our lives. With the recent advancement of deep learning technology and easily available cloud computing power, we can leverage AI to help us choose the right frame for us. This web app will show a basic usage of AI to help a person to choose a right glass frame virtually without all the hassles and dilemma.
  <br/>
<hr/> 

[Back to Table of Content](#index)
 
<a id='works'></a>
## Algorithm steps

![Algorithm steps](gif/steps.gif)

### Step 1: Input Image Preprocessing

![Step 1](images/step1.JPG)

### Step 2: Facial Landmarks Estimation

![Step 2](images/step2.JPG)

### Step 3: Overlay Transparent Filter

![Step 3](images/step3.JPG)
<hr/> 

[Back to Table of Content](#index)

<a id='usage'></a>
## Usage
### Facial Landmarks model
```
python app.py -i "images/person1.jpg" -t "FACIAL" -m "models/facial-landmarks-35-adas-0002.xml"
```
### Overlay Glass Filter
```
python app.py -i "images/person1.jpg" -t "GLASS" -m "models/facial-landmarks-35-adas-0002.xml" -g "images/glasses/glass9.png"
```
### Age and Gender Model
```
python app.py -i "images/person1.jpg" -t "GENDER" -m "models/age-gender-recognition-retail-0013.xml"
```

<hr/> 

[Back to Table of Content](#index)

<a id='code'></a>
## Code
```

```

[Back to Table of Content](#index)

<a id='ref'></a>
## References
1. [Host a Static Website](https://aws.amazon.com/getting-started/projects/host-static-website/)
1. [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/sample-templates-services-us-west-2.html#w2ab1c28c58c13c35)
1. [URL of Deployed App](http://exampleframe.com.s3-website.ca-central-1.amazonaws.com/)
1. [The best glasses for your face shape and skin tone](https://www.allaboutvision.com/eyeglasses/eyeglasses_shape_color_analysis.htm)
<hr/> 

[Back to Table of Content](#index)