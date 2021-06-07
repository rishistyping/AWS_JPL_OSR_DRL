![header image](images/2.png)


## Welcome to the AWS-JPL Open Source Rover Challenge repository.


<p>Here you will find everything you need to begin the challenge.</p>

We have also begun to create several videos to help you get started.  

Overview Video:

[![overview_video](https://img.youtube.com/vi/fK6Qsc01YHA/0.jpg)](https://www.youtube.com/watch?v=fK6Qsc01YHA)



<p>The main sections of this document are:</p>


1. [What is the challenge?](#whatis)

2. [What are the rules to the challenge](#whataretherules)

3. [Getting Started](#gettingstarted)

3. [Asset manifest and descriptions](#assetmanifest)

4. [Help and support](#help)


## <a name="whatis"> What is the Challenge?<a/>

<p> The AWS - JPL Open-Source Rover Challenge is an online, virtual, global competition to be held online starting on Monday, December 2, 2019 and 
ending on Friday, February 21, 2020.  Sponsored by Amazon Web Services, Inc. (“The Sponsor” or “AWS”) and is held in collaboration with JPL and AngelHack LLC (“Administrator”).</p>

## <a name="whataretherules"> What are the rules?</a>
<p> Simply put - you must train an RL agent to successfully navigate the Rover to a predetermined checkpoint on Mars.</p>

<p> The below images show the NASA-JPL Open Source Rover (on the left) and your digital version of the Rover on the right</p>

<p> We have simplified the action space to three discrete options:</p>
        
        Turn left
        Turn right
        Stay Straight

<p> We have set the Rover to use a constant, even linear acceleration, in other words, you cannot make the Rover go faster or slower at this time.
    Wall Time is not a factor in the scoring mechanism.
</p>

<p> The RL-agent leverages rl_coach to manage the training process.  This repo ships with a Clipped PPO algorithm but you are free to use a different algorithm</p>
        

![osr](images/sidebyside.png)


<p> To win the challenge, your RL-agent must navigate the Rover to the checkpoint and have the HIGHEST SCORE</p>
<p> There is currently a single [simulated] Martian environment that all participants will use.  </p>

![birdseye](images/start_destination.jpg)


<p> The scoring algorithm calculates a score when the Rover reaches the destination point, without collisions, in single episode</p>

        Begin with 10,000 basis points
        Subtract the number of (time) steps required to reach the checkpoint
        Subtract the distance travelled to reach the checkpoint (in meters)
        Subtract the Rover's average linear acceleration (measured in m/s^2)
        
<p> The scoring mechanism is designed to reflect the highest score for the Rover that:</p>

        Reaches the destination by means of the most optimized path (measured in time steps)
        Reaches the destination by means of the most optimized, shortest path (measured in distance traveled)
        Reaches the destination without experiencing unnecessary acceleration that could represent wheel hop or drops
    
## <a name="gettingstarted">Getting Started</a>
<p> While familiarity with RoS and Gazebo are not required for this challenge, they can be useful to understand how your RL-agent is controlling the Rover.
You will be required to submit your entry in the form of an AWS Robomaker simulation job.  This repo can be cloned directly into a (Cloud9) Robomaker development environment. 
It will not do a very good job training, however as the reward_function (more on that below) is empty.</p>

<p>All of the Martian world environment variables and Rover sensor data are captured for you and are then 
made available via global python variables.  You must populate the method known as the "reward_function()".  
The challenge ships with examples of how to populate the reward function (found in the Training Grounds Gym environment). 
However, no level of accuracy or performance is guaranteed as the code is meant to give you a learning aid, not the solution.</p>

<p> If you wish to learn more about how the Rover interacts with it's environment, you can look at the "Training Grounds" world that also
ships with this repo.  It is a very basic world with monolith type structures that the Rover must learn to navigate around.  You are free
to edit this world as you wish to learn more about how the Rover manuevers. </p>

<b>DO NOT EDIT THE ROVER DESCRIPTION (src/rover)</b> The Rover description that ships with this repo is the "gold standard" description and it will be
the Rover used to score your entries to the competition. 

<b>DO NOT EDIT THE MARTIAN WORLD (src/mars)</b> The Martian world that ships with this repo is the "gold standard" and it is the same one that will be
used to score your entry

## <a name="assetmanifest">Asset manifest and descriptions</a>

Project Structure:
	There are three primary components of the solution:
	![header image](images/3components.jpg)
	    
	    + src/rover/    A RoS package describing the Open Source Rover - this package is NOT editable
	    + src/mars/     A RoS/Gazebo package that describes and runs the simulated world
	    + src/rl-agent/ A Python3 module that contains a custom OpenAI Gym environment as well as wrapper code to initiate an rl_coach training session.  
	    within this module is a dedicated function 
	
    These three components work together to allow the Rover to navigate the Martian surface and send observation <-> reward tuples
	back to the RL-agent which then uses a TensorFlow algorithm to learn how to optimize actions.
	
	
Custom Gym Environment:
    This is gym environment exists as a single python file in src -> rl-agent -> environments -> mars_env.py
    
   mars_env.py is where you will create your reward function.  There is already a class method for you called:
    def reward_function(self)
    
   while you are free to add your own code to this method, you cannot change the signature of the method, or change the return types.
    
   the method must return a boolean value indicating if the episode has ended (see more about episode ending events below) 
   the method must also return a reward value for that time step.
    
   If you believe they are warranted, you are free to add additional global variables in the environment.  However, keep in mind
   if they are episodic values (values that should be reset after each episode) you will need to reset those values within the 
   reward_function method once you have determined the episode should end.
 
	
Recommended Episode ending scenarios:
    There are several scenarios that should automatically end an episode. To end an episode simple set the "done" variable in the reward_function method to True.
    
1. If the Rover collides with an object

![collision](images/collision.jpg)
    
    NOTE: If any part of the Rover other than the BOTTOM of the wheels comes into contact with a foreign object, it is considered a Collision. If an object comes into
    contact with the SIDE of the wheel, it is still considered a collision.

2. If the Rover's Power supply is drained
    This limit is currently set to 2,000 steps per episode


Creating your Robomaker Development Environment
    This GitHub repo should cloned to the root of your RoboMaker (Cloud9) development environment.

a.) Start by going to the Robomaker console and creating a new development environment.
    
![robomaker](images/create_env.jpg)
    
b.) Once your Cloud9 dev environment is launched, drop into a terminal window and delete everything in the root of the environment. (even the .c9 directory)

![deletethis](images/clear_environment.jpg)


C.) Clone this repo to the root of your Cloud9 dev environment by using the . (DOT) notation:
    git clone https://github.com/christopheraburns/AWS-JPL-OSR-Challenge .
    (note the . at the end of the git command - this prevents git from creating a local project directory)
    
    


There are several global constants and class scoped variables in the mars_env.py to help you build your Reward Function. These are known as "Episodic values" and will reset with each
new episode.  Do not remove any of these variables.

<b>steps (integer)</b>

    The number of [time] steps associated with the current episode.  
    This is an observation-action-reward process, not distance traveled

<b>current_distance_to_checkpoint (float)</b>

    The number of meters to the checkpoint, from the Rover's current position  
	
<b>closer_to_checkpoint (bool)</b>	

    A boolean value to tell you if the Rover's last step took it closer (True) 
    or further (False) from the Checkpoint
	
<b>distance_travelled (float)</b>
 
    The total distance, in meters the Rover has traveled in the current Episode
	
<b>collision_threshold (float)</b> 
    
    The Rover is quipped with a LIDAR and will detect the distance of the closest 
    object 45 degrees to the right or left, within 4.5 meters
	
<b>last_collision_threshold (float)</b>

    the collision_threshold of the previous [time] step
	
<b>x,y (float, float)</b>

    The current coordinate location of the Rover on the [simulated] Martian surface
	
<b>last_position_x, last_position_y (float, float)</b>

    Coordinate location of the Rover in the previous time step
	
<b>reward_in_episode (integer)</b>

    The cumulative reward for the current episode. As the participant determines 
    the reward signal this number should not be compared to any other participants 
    episodic reward
	
<b>power_supply_range (integer)</b>

    This is the range of the Rover in a given episode.  It decrements by time steps, 
    NOT distance traveled in order to prevent the Rover from getting stuck or 
    if it flips due to fall/collision and cannot respond to commands
	

If you believe they are warranted, you are free to add additional global variables in the environment.  <b>However</b>, keep in mind
   these are episodic values, or values that reset after each episode. You will need to write additional code to reset those values within the 
   reward_function method once you have determined the episode should end.

## <a name="help">Help and Support</a>

slack channel:  [awsjplroverchallenge.slack.com](https://awsjplroverchallenge.slack.com/)



# DeepRacer 2019 Sandbox

This is my full collection of tools, notebooks, scraps for participation in 2019 [AWS DeepRacer Virtual League](http://deepracerleague.com/).

What you'll find in this repo:

- Local training assets: container Dockerfiles, launch scripts mostly in bash, monitoring scripts
- AWS cloud-based training scripts: pre-dating local training, but also used to cloud evaluations of local training
- Analysis Notebook
- Models/Experiments: all the training sessions hyperparameters, reward functions, action space
- RoboMaker simapp: scripts to build the bundle, source files to add or replace files within the bundle
- Twitch streaming assets: UI (flask-based), ffmpeg tools to stream from simulation
- Airflow automation DAGs

**NB:** I am not an expert in ML/RL and participation in DeepRacer was a way to educate myself.  Forgive me any naive or wrong approaches taken.  Feel free to send me any observations, suggestions for different approaches, related papers or projects, or just to drop me a line.

**Race Results**

| Race                                                         | Standing        |
| ------------------------------------------------------------ | --------------- |
| August 2019 Virtual Race<br />[Shanghai Sudu](https://aws.amazon.com/deepracer/schedule-and-standings/leaderboard-virtual-shanghai-sudo-circuit-2019/) | **102** of 1375 |
| September 2019 Virtual Race<br />[Cumulo Carrera](https://aws.amazon.com/deepracer/schedule-and-standings/leaderboard-virtual-cumulo-carrera-2019/) | **132** of 1338 |
| October 2019 Virtual Race<br />[Toronto Turnpike](https://aws.amazon.com/deepracer/schedule-and-standings/leaderboard-virtual-toronto-turnpike-2019/) | **60** of 1983  |
| November 2019 Virtual Race<br />[Championship Cup Warm-up](https://console.aws.amazon.com/deepracer/home?region=us-east-1#leaderboard/Championship%20Cup%20Warm-up) | **8** of 904    |
| [AI Driving Olympics at NeurIPS](https://driving-olympics.ai/?page_id=24) | Phase I: Perception challenge: **Top 10**<br />Phase II: Simulation to Reality challenge: *did not place* |

The code and scripts are shared here unfiltered.  Some items may be broken or hacky.  The goal was to educate myself about reinforcement learning and train competitive models, sometimes at the expense of good coding practices.  I'll be starting a new repo for any work I do on the 2020 DeepRacer races and won't be adding any more changes to this code.

I'll follow here with some select items that I hope may be of interest to those looking to compete in the 2020 DeepRacer League.

----

# RoboMaker Bundle Management

The official SimApp bundle for DeepRacer is publicly readable and located at [https://s3.amazonaws.com/deepracer-managed-resources/deepracer-github-simapp.tar.gz](https://s3.amazonaws.com/deepracer-managed-resources/deepracer-github-simapp.tar.gz)

[robomaker/deepracer-simapp.tar.gz.md5](robomaker/deepracer-simapp.tar.gz.md5) - MD5 of the bundle to verify we're using the correct base for file patches

[airflow/monitor_deepracer_simapp.py](airflow/monitor_deepracer_simapp.py) - Script to monitor the hosted simapp bundle for changes.  Currently uses a date-based validation comparing official bundle to a copy stored in an S3 bucket I own

[patch/*](patch) - overlay files to add or replace files within the bundle.  These are mostly local edits to `markov` package, additional gazebo assets, added parameters to launch files.

[scripts/bundle.sh](scripts/bundle.sh) - Create a bundle using the base simapp and overlaying files from patch/.

[scripts/publish.sh](scripts/publish.sh) - Upload the patched bundle to an S3 bucket owned by me, consumable by RoboMaker for running patched simulations in the cloud

----

# Local Training

This was grown out of necessity and not out of convenience.  Therefore it is completely custom for my preferences and does not use the well-known DeepRacer Community training stack on GitHub.

**Goals for my local stack were:**

- Full access to the simapp bundle code to edit or add files
- Fast iteration on code changes to the simapp bundle using [Docker volumes](https://docs.docker.com/storage/volumes/) to patch containers
- Unified logging for later analysis
- Replication of all training artifacts to S3, effectively making local storage a "cache" that can be cleared

![](images/docker-compose.png)



**Components:**

- dr-training - Sagemaker/TensorFlow training
- dr-simulation - RoboMaker/ROS/Gazebo simulation
- dr-redis - pub/sub between dr-simulation and dr-training
- dr-logger - "sidecar" logger to aggregate all container logs and write them to JSON files
- dr-uploader - background synchronization of training assets and logs to S3 bucket
- minio - S3 replacement to store training checkpoints locally

**Interesting bits:**

[container/Dockerfile.*](container) - Dockerfiles for the local training setup

[scripts/launch_local.sh](scripts/launch_local.sh) - Entrypoint for local training kickoff

[models/*](models) - Inputs for local training, a unique folder for each training session with hyperparameters, action space, reward function

[docker-compose.yml](docker-compose.yml) - container configuration

----

# Twitch Streaming

I streamed training at [https://www.twitch.tv/deepstig](https://www.twitch.tv/deepstig) later in the season.  I used [OBS](https://obsproject.com/) to host a browser-based UI with a VLC stream overlay, sending frames out of my local training simulation via ffmpeg over udp.

![](twitch/images/offline.png)

[twitch/app.py](twitch/app.py) - Flask app to show a UI with some near-real-time metrics 

[container/streamer.sh](container/streamer.sh) - In-container script to listen to ROS camera node RGB image messages and pipe them directly to ffmpeg stdin in order to generate a mpegts stream over udp

[scripts/monitor_video.sh](scripts/monitor_video.sh) - Script to launch `streamer.sh` within the container, passing in the udp stream destination

----

# Log Analysis

Based on [AWS DeepRacer Workshop](https://github.com/aws-samples/aws-deepracer-workshops/blob/master/log-analysis/DeepRacer%20Log%20Analysis.ipynb) Jupyter notebook but heavily modified.  Any time I had a question about training progress or simulation behavior I would add some new features to this.  Its really overgrown now but gives me a full and complete picture of training as I run it.

For brevity, I'll pull out a few interesting sections but you can click to the [full notebook](log_analysis/DeepRacer Log Analysis.ipynb) to see the code.

| Description                                                  |                 |
| ------------------------------------------------------------ | --------------- |
| Training progress, loss.  I would watch this to discover points at which I would need to stop training or adjust hyperparameters. | ![](images/logs1.png)  |
| Action space usage.  This helped me to know if there were unused actions that could be culled out. | ![](images/logs2.png)  |
| Car performance during training. Mostly scatterplots of episodic metrics, with mean for the iteration overlaid in orange.  The most intersting is the fourth graph which shows progress per lap, but also ratio of completed laps.  If the completion ratio was between 20% (red) and 40% (green) lines, I would submit the model for racing.  If the completion ratio was more than 40%, I would push the speed a little further and retrain. | ![](images/logs17.png) |
| Correlate high rewards to high speed.  If they don't correlate then there is most likely a problem in the reward function. | ![](images/logs4.png)  |
| Heatmap showing rewards for each step.  A good indicator of the line that is rewarded traversing the track. | ![](images/logs5.png)  |
| Exit points plot.  Clumped exit points may indicate an action space can be modified to have a better turn angle, or that reward function might be rewarding a wrong action. | ![](images/logs6.png)  |
| Actions mapping.  Only really useful for an action space with one speed per steering angle.  Correlates actions with track waypoints. | ![](images/logs7.png)  |
| Single episode summary.  Shows: step location, heading angle (black), steering angle (red), episode pace | ![](images/logs8.png)  |
| Speed.  Blue line is the actual speed, measured as incremental distance between steps.  Yellow is throttle and cyan is steering.  This helps to easily see the effect of steering and throttle position on speed. | ![](images/logs9.png)  |
| Correlate steering with heading change.                      | ![](images/logs11.png) |
| Reward and Progress.  This graph verifies higher rewards for higher progress per step. | ![](images/logs12.png) |
| Try to detect slippage.  The car can wipe out on turns if speed is too high.  This graph shows when heading and direction of movement over ground don't correlate. | ![](images/logs13.png) |
| Run inference on an image to find its action probabilities.  This can indicate the health of the model. | ![](images/logs14.png) |
| GradCAM.  Finds the aspects of the image that the network is focusing on. | ![](images/logs15.png) |
| Convolutional layer activations.  This is mostly for making the convolutional layers more interpretable by seeing the features they activate on. | ![](images/logs16.png) |





**Interesting items**:

[log_analysis/DeepRacer Log Analysis.ipynb](log_analysis/DeepRacer%20Log%20Analysis.ipynb) - The notebook

[log_analysis/images/*](log_analysis/images/) - Still image captures of a variety of tracks to use in analysis, such as running it through the model to get action probabilities



---

# Airflow Automation

I had aspired to use airflow to work through a queue of training and evaluation jobs but ultimately didn't end up spending the time automating to that level.  The primary usage of airflow was to submit the model to the virtual league every ~30 minutes.  

It was unfortunate but the winners were so close that luck and brute force had a large part in getting to the top positions.  This would use Selenium and ChromeDriver submit the model, and also handle any authentication that might need to happen as part of that workflow.

[airflow/deepracer_submit_dag.py](airflow/deepracer_submit_dag.py) - Submit a model for evaluation every 30 minutes


---


# Resources

### Official AWS Resources

- AWS DeepRacer Documentation [https://docs.aws.amazon.com/deepracer/index.html#lang/en_us](https://docs.aws.amazon.com/deepracer/index.html#lang/en_us)
- AWS DeepRacer League [https://aws.amazon.com/deepracer/league/](https://aws.amazon.com/deepracer/league/)
- AWS Cost Management [https://console.aws.amazon.com/cost-reports/home?region=us-east-1#/dashboard](https://console.aws.amazon.com/cost-reports/home?region=us-east-1#/dashboard)
- AWS SageMaker Python SDK [https://github.com/aws/sagemaker-python-sdk](https://github.com/aws/sagemaker-python-sdk)

### Components of DeepRacer

- AWS SageMaker
- AWS RoboMaker
- AWS Kenesis
- AWS CloudWatch Logs
- AWS S3
- AWS Lambda

### Useful Tools

- rviz: rviz is a 3d visualization tool for ROS applications [https://docs.aws.amazon.com/robomaker/latest/dg/simulation-tools-rviz.html](https://docs.aws.amazon.com/robomaker/latest/dg/simulation-tools-rviz.html)
- rqt hosts a number of different plugins for visualizing ROS information [https://docs.aws.amazon.com/robomaker/latest/dg/simulation-tools-rqt.html](https://docs.aws.amazon.com/robomaker/latest/dg/simulation-tools-rqt.html)
- Gazebo lets you build 3D worlds with robots, terrain, and other objects [https://docs.aws.amazon.com/robomaker/latest/dg/simulation-tools-gazebo.html](https://docs.aws.amazon.com/robomaker/latest/dg/simulation-tools-gazebo.html)
- ROS: Robot Operating System which AWS RoboMaker is based on [https://www.ros.org/](https://www.ros.org/)
- TensorFlow ML which AWS SageMaker is based on [https://www.tensorflow.org/](https://www.tensorflow.org/)
- Pandas: Python Data Analysis Library [https://pandas.pydata.org/](https://pandas.pydata.org/)
- Actual RoboMaker simulation environment for DeepRacer [https://s3.amazonaws.com/deepracer-managed-resources/deepracer-github-simapp.tar.gz](https://s3.amazonaws.com/deepracer-managed-resources/deepracer-github-simapp.tar.gz)
- Coach is the implementation of RL algorithms (PPO, CPPO, TRPO, etc) used in the RLEstimator that aggregates training data back into the model in SageMaker [https://github.com/NervanaSystems/coach](https://github.com/NervanaSystems/coach)
- OpenVINO is used to execute the RL model on the car hardware or ROS simulator [https://01.org/openvinotoolkit](https://01.org/openvinotoolkit)
- PyTorch: ML framework that effectively is SageMaker; also usable on Google Cloud and Azure [https://pytorch.org/](https://pytorch.org/)

### Community Resources

- *AWS DeepRacer AMI* [https://github.com/jarrettj/deepracer-ami](https://github.com/jarrettj/deepracer-ami)
- *A repo for running deepracer locally* [https://github.com/crr0004/deepracer](https://github.com/crr0004/deepracer)
- *Train DeepRacer model locally with GPU support* [https://medium.com/@jonathantse/train-deepracer-model-locally-with-gpu-support-29cce0bdb0f9](https://medium.com/@jonathantse/train-deepracer-model-locally-with-gpu-support-29cce0bdb0f9)
- *Using Jupyter Notebook for analysing DeepRacer's logs* [https://codelikeamother.uk/using-jupyter-notebook-for-analysing-deepracer-s-logs](https://codelikeamother.uk/using-jupyter-notebook-for-analysing-deepracer-s-logs)
- *2019 AWS Summits DeepRacer Lab* [https://github.com/aws-samples/aws-deepracer-workshops/tree/master/Workshops/2019-AWSSummits-AWSDeepRacerService/Lab1](https://github.com/aws-samples/aws-deepracer-workshops/tree/master/Workshops/2019-AWSSummits-AWSDeepRacerService/Lab1)
- *AWS Samples: DeepRacer Workshop Content* [https://github.com/aws-samples/aws-deepracer-workshops](https://github.com/aws-samples/aws-deepracer-workshops)
- *Analyzing the AWS DeepRacer logs my way* [https://codelikeamother.uk/analyzing-the-aws-deepracer-logs-my-way](https://codelikeamother.uk/analyzing-the-aws-deepracer-logs-my-way)
- *Deep Reinforcement Learning Models: Tips & Tricks for Writing Reward Functions* [https://medium.com/@BonsaiAI/deep-reinforcement-learning-models-tips-tricks-for-writing-reward-functions-a84fe525e8e0](https://medium.com/@BonsaiAI/deep-reinforcement-learning-models-tips-tricks-for-writing-reward-functions-a84fe525e8e0)

- *Local Training GUI* [https://github.com/ARCC-RACE/deepracer-for-dummies](https://github.com/ARCC-RACE/deepracer-for-dummies)
- *Visualizations for AWS DeepRacer videos* [https://github.com/jochem725/deepracer-viz](https://github.com/jochem725/deepracer-viz)
- *How to Run DeepRacer Locally to Save your Wallet* [https://medium.com/@autonomousracecarclub/how-to-run-deepracer-locally-to-save-your-wallet-13ccc878687](https://medium.com/@autonomousracecarclub/how-to-run-deepracer-locally-to-save-your-wallet-13ccc878687)
- *AWS Samples: RoboMaker training for DeepRacer* [https://github.com/aws-robotics/aws-robomaker-sample-application-deepracer](https://github.com/aws-robotics/aws-robomaker-sample-application-deepracer)
- Fork of log analysis with many improvements [https://github.com/breadcentric/aws-deepracer-workshops/commits/enhance-log-analysis](https://github.com/breadcentric/aws-deepracer-workshops/commits/enhance-log-analysis)
- ACloud Guru DeepRacer course [https://acloud.guru/series/deepracer](https://acloud.guru/series/deepracer)
- Building a physical track [https://medium.com/@autonomousracecarclub/guide-to-creating-a-full-re-invent-2018-deepracer-track-in-7-steps-979aff28a6f5](https://medium.com/@autonomousracecarclub/guide-to-creating-a-full-re-invent-2018-deepracer-track-in-7-steps-979aff28a6f5)
- Ready-made track (apparently too reflective) [https://www.robocarstore.com/products/aws-deepracer-standard-track](https://www.robocarstore.com/products/aws-deepracer-standard-track)
- *Improving AWS DeepRacer log analysis even further* [https://codelikeamother.uk/improving-aws-deepracer-log-analysis-even-further](https://codelikeamother.uk/improving-aws-deepracer-log-analysis-even-further)
- AWS Promotional Credits for Alexa - Amazon Alexa (for cost reduction) [https://developer.amazon.com/en-US/alexa/alexa-skills-kit/alexa-aws-credits](https://developer.amazon.com/en-US/alexa/alexa-skills-kit/alexa-aws-credits)
- *PPO Hyperparameters and Ranges* [https://medium.com/aureliantactics/ppo-hyperparameters-and-ranges-6fc2d29bccbe](https://medium.com/aureliantactics/ppo-hyperparameters-and-ranges-6fc2d29bccbe)

### Education

- AWS Summit DeepRacer slide deck: [https://d2k9g1efyej86q.cloudfront.net/](https://d2k9g1efyej86q.cloudfront.net/)
- Stanford AI Courses: [https://onlinehub.stanford.edu/](https://onlinehub.stanford.edu/)
- ARCC [https://arcc.ai/](https://arcc.ai/)
- Udacity DeepRacer Scholarship [http://www.udacity.com/aws-deepracer-scholarship](http://www.udacity.com/aws-deepracer-scholarship)
- Deep Reinforcement Learning Course [https://simoninithomas.github.io/Deep_reinforcement_learning_Course/](https://simoninithomas.github.io/Deep_reinforcement_learning_Course/)
- Collection of DRL lectures [https://github.com/kmario23/deep-learning-drizzle](https://github.com/kmario23/deep-learning-drizzle)
- Hyperparameter tuning to avoid overfitting [https://pages.awscloud.com/Hyperparameter-Tuning-with-Amazon-SageMakers-Automatic-Model-Tuning_0704-MCL_OD.html?sc_campaign=pac_2018_exlinks_ondemand_OTT_evergreen&sc_channel=el&sc_country=mult%20&sc_geo=NAMER&sc_icampaign=pac_2018_exlinks_ondemand_OTT_evergreen&sc_ichannel=ha&sc_icontent=awssm-2276&sc_iplace=console-right&sc_outcome=PaaS_Digital_Marketing&trk=ep_card-el_a131L000005jldqQAA~ha_awssm-2276&trkCampaign=July_0704-MCL](https://pages.awscloud.com/Hyperparameter-Tuning-with-Amazon-SageMakers-Automatic-Model-Tuning_0704-MCL_OD.html?sc_campaign=pac_2018_exlinks_ondemand_OTT_evergreen&sc_channel=el&sc_country=mult%20&sc_geo=NAMER&sc_icampaign=pac_2018_exlinks_ondemand_OTT_evergreen&sc_ichannel=ha&sc_icontent=awssm-2276&sc_iplace=console-right&sc_outcome=PaaS_Digital_Marketing&trk=ep_card-el_a131L000005jldqQAA~ha_awssm-2276&trkCampaign=July_0704-MCL)
- MSE vs Huber loss [https://towardsdatascience.com/understanding-the-3-most-common-loss-functions-for-machine-learning-regression-23e0ef3e14d3](https://towardsdatascience.com/understanding-the-3-most-common-loss-functions-for-machine-learning-regression-23e0ef3e14d3)
- Autonomous car with Reinforcement Learning — part 1: obstacle avoidance [https://medium.com/@sdeleers/autonomous-car-with-reinforcement-learning-part-1-obstacle-avoidance-7c73a2567b7b](https://medium.com/@sdeleers/autonomous-car-with-reinforcement-learning-part-1-obstacle-avoidance-7c73a2567b7b)
- Autonomous car with Reinforcement Learning — part 2: track following [https://medium.com/@sdeleers/autonomous-car-with-reinforcement-learning-part-2-track-following-4ffbf7aa33d1](https://medium.com/@sdeleers/autonomous-car-with-reinforcement-learning-part-2-track-following-4ffbf7aa33d1)
- Video: *ML Infra @ Spotify: Lessons learned - Romain Yon (Dec 2018 NYC ML Meetup)* [https://www.youtube.com/watch?v=m19kqEojGJM&feature=youtu.be](https://www.youtube.com/watch?v=m19kqEojGJM&feature=youtu.be)
- Unity ML great description of PPO hyperparameters [https://github.com/Unity-Technologies/ml-agents/blob/master/docs/Training-PPO.md](https://github.com/Unity-Technologies/ml-agents/blob/master/docs/Training-PPO.md)
- Blog post covering many policy gradients with links to their papers [https://lilianweng.github.io/lil-log/2018/04/08/policy-gradient-algorithms.html#ppo](https://lilianweng.github.io/lil-log/2018/04/08/policy-gradient-algorithms.html#ppo)
- Collection of papers soliciting feedback before presentation [https://openreview.net/](https://openreview.net/)

### Other Useful Resources

- *Easing Functions* [https://easings.net/en](https://easings.net/en)
- Genograms (for graphing lineage, possibly applicable to models and training) [https://www.edrawsoft.com/genogram-software.php](https://www.edrawsoft.com/genogram-software.php) [https://www.genopro.com/genogram/](https://www.genopro.com/genogram/)
- Ackerman Steering explanation [https://www.xarg.org/book/kinematics/ackerman-steering/](https://www.xarg.org/book/kinematics/ackerman-steering/)
- OpenAI Baselines: implementations of many RL algorithms [https://github.com/openai/baselines/tree/master/baselines](https://github.com/openai/baselines/tree/master/baselines)

### Discussion Groups

- Official AWS DeepRacer Discussion Forums [https://forums.aws.amazon.com/forum.jspa?forumID=318](https://forums.aws.amazon.com/forum.jspa?forumID=318)
- Reddit r/deepracer [https://www.reddit.com/r/DeepRacer/](https://www.reddit.com/r/DeepRacer/)
- Slack group [http://deepracer-community.slack.com](http://deepracer-community.slack.com)

-----

## DeepRacer Service Map

![](docs/deepracer_components.png)

# Contributors:
@irisdroidology
@exynos-999


# Documentation
Acordrobotics.slack.com
https://photos.app.goo.gl/eZY941jNep7YMftm7 - good to see how we did/will do stuff...google photos album...

## Tasks 
Reinforcement Learning: https://stackoverflow.com/questions/46260775/what-is-a-policy-in-reinforcement-learning Commit 18/1/2020
