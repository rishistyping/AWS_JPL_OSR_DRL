The original README for this repo is left intact so that we can easily sync upstream changes.


# End-to-end Training & Submission Process: First Pass

# Option A: Local Training


Verify Core System

```
$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 18.04.3 LTS
Release:	18.04
Codename:	bionic
```

List GPU (optional)
```
$ nvidia-smi
Thu Dec 12 03:24:22 2019       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 435.21       Driver Version: 435.21       CUDA Version: 10.1     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce GTX 1070    Off  | 00000000:06:00.0 Off |                  N/A |
|  0%   44C    P5    18W / 151W |      0MiB /  8119MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```

Sort out any issues with packages by updating
```
$ sudo apt-get upgrade
$ sudo apt --fix-broken install
$ dpkg --list | grep 'Robot OS' | awk '{print $2 }' | xargs sudo apt-get -y remove
```

Install Gazebo (9 referenced in robomakerSettings.json)

```
$ dpkg --list | grep gazebo
$ apt-get install gazebo9
```

Install ROS Melodic [http://wiki.ros.org/melodic/Installation/Ubuntu](http://wiki.ros.org/melodic/Installation/Ubuntu)

```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu `lsb_release -cs` main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
sudo apt update
sudo apt-get install ros-desktop-full-dev
sudo apt-get install python3-colcon-common-extensions
```

## Option B: RoboMaker / Cloud9 Training

Open RoboMaker Console

[https://console.aws.amazon.com/robomaker/home?region=us-east-1#welcome](https://console.aws.amazon.com/robomaker/home?region=us-east-1#welcome)

Development Environments -> Create Environment

	Name					JPLChallenge
	Pre-installed ROS distribution		ROS Melodic
	Instance type				m4.large
	IAM Role				AWSServiceRoleForAWSCloud9
	VPC					<default>
	Subnets					<default>


t2.large 0.0928
t2.xlarge 0.1856
m4.large 0.10
m4.xlarge 0.20

Configure Git in Cloud9

```
ubuntu:~/environment $ git config --global user.name 'Chris Thompson'
ubuntu:~/environment $ git config --global user.email 'chris@veeta.tv'
ubuntu:~/environment $ git config --global --list
core.editor=/usr/bin/nano
user.name=Chris Thompson
user.email=chris@veeta.tv
```

Add an ssh identity to use with github [https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh](https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh)

```
ubuntu:~/environment $ ssh-keygen -t rsa -b 4096 -C "chris@veeta.tv"
Generating public/private rsa key pair.
Enter file in which to save the key (/home/ubuntu/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/ubuntu/.ssh/id_rsa.
Your public key has been saved in /home/ubuntu/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:7Si+RrJiAcYJ31TCDdXr7St7aMJ+TMNfLKESU/T9BHY chris@veeta.tv
The key's randomart image is:
+---[RSA 4096]----+
|   .o=oo.   o E  |
|.   o.. o. o o   |
|o..o   . .. . .  |
|.+. . o ...  o   |
|..     =So.o  .  |
|  . . o *oo o    |
|   . =.+.=.o     |
|  o ..+.* +      |
| . . o+=.+..     |
+----[SHA256]-----+
ubuntu:~/environment $ ls ~/.ssh/
authorized_keys  id_rsa  id_rsa.pub  known_hosts
```

Improper setup

```
ubuntu:~/environment $ git clone git@github.com:cdthompson/jpl-challenge.git                                                                                 
Cloning into 'jpl-challenge'...
Warning: Permanently added the RSA host key for IP address '192.30.253.112' to the list of known hosts.
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.
Please make sure you have the correct access rights
and the repository exists.
ubuntu:~/environment $ 
```

Set up SSH key in github.com https://github.com/settings/ssh/new

```
ubuntu:~/environment $ cat ~/.ssh/id_rsa.pub 
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDA45v1ocNRXVdo4BH78jK2L2oaBfZH7Wi5ebh94ihAlcL7O5gBXKxOJjGuLxZBnSpR8OurvXDOZ5ZVOVedFqzgCM9fTmpUj4Y0TZ97eQYqU6eVQ84XdTuMEmWTCr2dcSgLrSZtGgmsVFPNXdjIUmfrt6a2IrBsW+Chb/4xSqXuHjG0+x3iZQfblhK9LRSb/Wjm6uyMAMK0NdywiXrEFzpANEdOkz9dDUMZjFyNOjG0bQVKjvE1SdzVT8NG8SNJ7PQTx0eT/h77FUal8RK2OkEG/DwhgC+eG8LL6vzwd2JwNCxwrBK+yvP3paD+E7Y/+n5ORcaIUPRs0fGGYANZC7S/kaluVN0RdrBv189QXbWoDcC4/RCaSvuRET0OtAPROYanzhUjFvRcxTfZ4rEMxVs+KkabkazWqX7vLe6s5wzc1Z0Zx5M6wNDHENRxfsUNl/QwqB1eGISjtoxaxC0mj9HNJuZiJ/FxqbVIKAp4JTkVNXCaoMssFkEhEQqrLL16vMiIy1X2/ykyI4RUe0SBDs1jipExvnsO+34KVIJkSU6w0sWM+GiYysiOq8wy87HR/11GLHGaWiqc8gXRYuBdrz+2Aae7odMeCHOk3Vf68dg0uFCVC60IeXDmHbysJJm5gIZuh+YJ0H6EtipQH3PATLKOm+9I3ZY24d6zoYeyjHSF1Q== chris@veeta.tv
```


	Name	"JPLChallenge Cloud9"
	Key	<copied from cloud9 terminal>


Remove unnecessary default files

```
ubuntu:~/environment $ rm -rf .c9 README.md roboMakerLogs/ roboMakerSettings.json 
```

Clone repo from github

```
ubuntu:~/environment $ git clone git@github.com:cdthompson/jpl-challenge.git .
Cloning into '.'...
Warning: Permanently added the RSA host key for IP address '140.82.113.4' to the list of known hosts.
remote: Enumerating objects: 335, done.
remote: Counting objects: 100% (335/335), done.
remote: Compressing objects: 100% (239/239), done.
remote: Total 335 (delta 74), reused 335 (delta 74), pack-reused 0
Receiving objects: 100% (335/335), 18.33 MiB | 19.69 MiB/s, done.
Resolving deltas: 100% (74/74), done.
```

Set up bucket for the project (only once for the whole project and team)

[https://s3.console.aws.amazon.com/s3/home?region=us-east-1](https://s3.console.aws.amazon.com/s3/home?region=us-east-1)

Create Bucket (use `uuidgen` to create UUID)

	Bucket name		jpl-challenge-9a600102-20c7-4cb4-ac70-174e44fb972f
	Region			US East


Configure bucket access

Permissions -> Block public access => "Off"

Set up role for Cloud9/RoboMaker to modify S3

https://docs.aws.amazon.com/robomaker/latest/dg/auth-and-access-control.html#auth_access_required-permissions


IAM console -> Create Policy

- name: "JPLChallengeBucketFullAccess"
- S3FullAccess
- Retricted to new bucket `jpl-challenge-9a600102-20c7-4cb4-ac70-174e44fb972f`

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "s3:ListBucket",
            "Resource": [
                "arn:aws:s3:::jpl-challenge-9a600102-20c7-4cb4-ac70-174e44fb972f"
            ],
            "Effect": "Allow"
        },
        {
            "Action": [
                "s3:Get*",
                "s3:List*"
            ],
            "Resource": [
                "arn:aws:s3:::jpl-challenge-9a600102-20c7-4cb4-ac70-174e44fb972f/*"
            ],
            "Effect": "Allow"
        },
        {
            "Action": [
		"s3:Put*",
		"s3:Delete*"
	    ],
            "Resource": [
                "arn:aws:s3:::jpl-challenge-9a600102-20c7-4cb4-ac70-174e44fb972f/*"
            ],
            "Effect": "Allow"
        },
        {
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogStreams"
            ],
            "Resource": [
                "arn:aws:logs:*:345864641105:log-group:/aws/robomaker/SimulationJobs*"
            ],
            "Effect": "Allow"
        }
    ]
}
```

IAM console -> Create Role

- name: "JPLChallengeRole"
- Policies: JPLChallengeBucketFullAccess


Trust Relationship

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "cloud9.amazonaws.com",
          "robomaker.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```



Configure workspace

- bucket ws created in s3 in previous step
- subnet is in the robomaker console development environment details
- security group is in the robomaker console development environment details
- region is probably just us-east-1
- iam role ARN is found by searching for AWSServiceRoleForAWSCloud9 in IAM console Roles

```
	YOUR_S3_BUCKET		jpl-challenge-9a600102-20c7-4cb4-ac70-174e44fb972f
	YOUR_OUTPUT_S3_BUCKET	jpl-challenge-9a600102-20c7-4cb4-ac70-174e44fb972f
	"YOUR IAM ROLE"		"arn:aws:iam::345864641105:role/JPLChallengeRole"
	YOUR_SUBNET_A		subnet-0dc467cac82496ec7
              			subnet-063c10dafed2bb5a6
	YOUR_SUBNET_B		<none>
	YOUR_SECURITY_GROUP	sg-02a18bb29a9b2fd2a
	s3Bucket		jpl-challenge-9a600102-20c7-4cb4-ac70-174e44fb972f
	YOUR_AWS_REGION		us-east-1
	MODEL_S3_PREFIX		"training-grounds-no-rl/"
				"mars-env-no-rl/"
				"training-grounds-with-rl/"
	/burnsca-.*/		jpl-challenge-9a600102-20c7-4cb4-ac70-174e44fb972f
```


Open and save robomakerSettings.json for the Cloud9 UI to refresh the 'Run' menu. Should show "Run->Build->build-all" option, as well as others


Run `build-all` target

```
Running colcon build for build-all...
<...>
#All required rosdeps installed successfully
Starting >>> hector_gazebo_plugins
Finished <<< rover_description [13.7s]                                                                                   
Starting >>> markov
Finished <<< markov [1.12s]                                                             
Starting >>> message_to_tf
Finished <<< message_to_tf [28.9s]                                                                                       
Starting >>> mars
Finished <<< mars [10.4s]                                                                                      
Starting >>> training_grounds
Finished <<< training_grounds [10.7s]                                                                                  
[Processing: hector_gazebo_plugins]                                       
Finished <<< hector_gazebo_plugins [1min 53s]                                        
Summary: 6 packages finished [1min 54s]
```

Run `bundle-all` target

```
<...>
Successfully installed Jinja2-2.10.3 MarkupSafe-1.1.1 Pillow-4.3.0 PyJWT-1.7.1 PyOpenGL-3.1.4 PyWavelets-1.1.1 PyYAML-4.2b1 absl-py-0.8.1 adal-1.2.2 annoy-1.16.2 astor-0.8.1 attrs-19.3.0 bokeh-1.4.0 boto3-1.9.23 botocore-1.12.253 cachetools-3.1.1 catkin-pkg-0.4.15 certifi-2019.11.28 cffi-1.13.2 chardet-3.0.4 cryptography-2.8 cycler-0.10.0 decorator-4.4.1 docutils-0.15.2 future-0.18.2 futures-3.1.1 gast-0.3.2 google-auth-1.8.2 grpcio-1.25.0 gym-0.10.5 h5py-2.10.0 idna-2.8 imageio-2.6.1 importlib-metadata-1.3.0 jmespath-0.9.4 keras-applications-1.0.8 keras-preprocessing-1.1.0 kiwisolver-1.1.0 kubernetes-7.0.0 markdown-3.1.1 matplotlib-3.1.2 minio-4.0.5 more-itertools-8.0.2 networkx-2.4 numpy-1.14.5 oauthlib-3.1.0 olefile-0.46 packaging-19.2 pandas-0.22.0 pluggy-0.13.1 protobuf-3.11.1 py-1.8.0 pyasn1-0.4.8 pyasn1-modules-0.2.7 pycparser-2.19 pygame-1.9.3 pyglet-1.4.8 pyparsing-2.4.5 pytest-5.3.1 python-dateutil-2.8.1 pytz-2019.3 redis-2.10.6 requests-2.22.0 requests-oauthlib-1.3.0 rl-coach-slim-0.11.1 rospkg-1.1.7 rsa-4.0 s3transfer-0.1.13 scikit-image-0.16.2 scipy-0.19.0 setuptools-42.0.2 six-1.13.0 tensorboard-1.12.2 tensorflow-1.12.2 termcolor-1.1.0 tornado-6.0.3 urllib3-1.25.7 wcwidth-0.1.7 websocket-client-0.56.0 werkzeug-0.16.0 wheel-0.33.6 zipp-0.6.0
Creating bundle archive V2...
Archiving complete!
```

Verify bundle in terminal

```
ubuntu:~/environment (master) $ ls -l simulation_ws/bundle/output.tar 
-rw-rw-r-- 1 ubuntu ubuntu 925696000 Dec 12 19:01 simulation_ws/bundle/output.tar
```

Launch the mars env with no RL agent control, just to verify all connectivity to RoboMaker

```
 [2:04:02 PM] --> Uploading bundle
 s3 cp /home/ubuntu/environment//simulation_ws/bundle/output.tar s3://jpl-challenge-9a600102-20c7-4cb4-ac70-174e44fb972f/simulation_ws/bundle/output.tar
 upload: environment/simulation_ws/bundle/output.tar to s3://jpl-challenge-9a600102-20c7-4cb4-ac70-174e44fb972f/simulation_ws/bundle/output.tar
 [2:04:19 PM] --> Bundle upload succeeded.
```

```
 [5:47:44 PM] --> Starting simulation job.
 robomaker create-simulation-job --output json --cli-input-json {"clientRequestToken":"f3ef3d91-a0e3-c75d-c78c-a30be998a6ba","iamRole":"arn:aws:iam::345864641105:role/JPLChallengeRole","outputLocation":{"s3Bucket":"jpl-challenge-9a600102-20c7-4cb4-ac70-174e44fb972f","s3Prefix":"SimulationLog_360216457171"},"maxJobDurationInSeconds":86400,"failureBehavior":"Continue","simulationApplications":[{"application":"arn:aws:robomaker:us-east-1:345864641105:simulation-application/mars-env-no-rl/1576186693540","applicationVersion":"$LATEST","launchConfig":{"packageName":"mars","launchFile":"mars_env_only.launch","environmentVariables":{"MARKOV_PRESET_FILE":"mars_presets.py","ROS_AWS_REGION":"us-east-1","MODEL_S3_BUCKET":"jpl-challenge-9a600102-20c7-4cb4-ac70-174e44fb972f","MODEL_S3_PREFIX":"mars-env-no-rl/"}}}],"tags":{}}
 {
    "arn": "arn:aws:robomaker:us-east-1:345864641105:simulation-job/sim-q71zq8r305h7",
    "status": "Pending",
    "lastUpdatedAt": 1576190866.0,
    "failureBehavior": "Continue",
    "clientRequestToken": "f3ef3d91-a0e3-c75d-c78c-a30be998a6ba",
    "outputLocation": {
        "s3Bucket": "jpl-challenge-9a600102-20c7-4cb4-ac70-174e44fb972f",
        "s3Prefix": "SimulationLog_360216457171"
    },
    "loggingConfig": {
        "recordAllRosTopics": true
    },
    "maxJobDurationInSeconds": 86400,
    "simulationTimeMillis": 0,
    "iamRole": "arn:aws:iam::345864641105:role/JPLChallengeRole",
    "simulationApplications": [
        {
            "application": "arn:aws:robomaker:us-east-1:345864641105:simulation-application/mars-env-no-rl/1576186693540",
            "applicationVersion": "$LATEST",
            "launchConfig": {
                "packageName": "mars",
                "launchFile": "mars_env_only.launch",
                "environmentVariables": {
                    "MARKOV_PRESET_FILE": "mars_presets.py",
                    "MODEL_S3_BUCKET": "jpl-challenge-9a600102-20c7-4cb4-ac70-174e44fb972f",
                    "MODEL_S3_PREFIX": "mars-env-no-rl/",
                    "ROS_AWS_REGION": "us-east-1"
                }
            }
        }
    ],
    "tags": {}
}
 [5:47:46 PM] --> Your simulation job was created.
```


## Option C: Hybrid Local / Cloud9 Training


## Inputs (Reward function)

Sensors:

`training_env.py`:

```
# Subscribe to ROS topics and register callbacks
rospy.Subscriber('/odom', Odometry, self.callback_pose)
rospy.Subscriber('/scan', LaserScan, self.callback_scan)
rospy.Subscriber('/robot_bumper', ContactsState, self.callback_collision)
rospy.Subscriber('/camera/image_raw', sensor_image, self.callback_image)
```

## Outputs (Logs, Score)

Training grounds evaluation logs:
sim-421rr8pd3ljs/2019-12-13T15-40-11.474Z_935b2aea-d46a-4909-86c3-8435f7a3ee62/SimulationApplicationLogs

```
/home/robomaker/workspace/applications/simulation-application/workspace/opt/built_workspace/training_grounds/share/training_grounds/launch/eval.launch
ERROR: cannot launch node of type [training_grounds/run_model_evaluation.sh]: can't locate node [run_model_evaluation.sh] in package [training_grounds]
```

Training grounds simulation logs:
sim-h5gjmx447vb5/2019-12-13T14-30-28.255Z_eda7745e-d714-420e-8c27-4e7097a919b0/SimulationApplicationLogs

```
12:28:39 Step:159.00 Steering:0.000000 R:1.00 DTCP:52.763653 DT:9.101053 CT:0.54 CTCP:0.000000 PSR: 1841.000000 IMU: 8.437992
12:28:39 Step:160.00 Steering:1.000000 R:1.00 DTCP:52.827974 DT:9.165757 CT:0.49 CTCP:0.000000 PSR: 1840.000000 IMU: 8.437992
12:28:39 Rover has sustained sideswipe damage
12:28:39 Step:161.00 Steering:1.000000 R:0.00 DTCP:52.873931 DT:9.225544 CT:0.46 CTCP:0.000000 PSR: 1839.000000 IMU: 8.437992
12:28:39 Training - Name: main_level/agent Worker: 0 Episode: 1 Total reward: 238.75 Steps: 161 Training iteration: 0
12:28:39 Total Episodic Reward=238.75 Total Episodic Steps=161.00
12:28:39 Step:0.00 Steering:0.000000 R:0.00 DTCP:44.616115 DT:0.019151 CT:3.11 CTCP:0.000000 PSR: 2000.000000 IMU: 0.657325
...
14:44:33 Training - Name: main_level/agent Worker: 0 Episode: 20 Total reward: 292.0 Steps: 1154 Training iteration: 0
14:44:33 Policy training - Surrogate loss: 0.04290153458714485 KL divergence: 0.08382605016231537 Entropy: 1.011546015739441 training epoch: 0 learning_rate: 0.0003
14:44:33 Policy training - Surrogate loss: 0.0024791033938527107 KL divergence: 0.010965879075229168 Entropy: 1.0578904151916504 training epoch: 1 learning_rate: 0.0003
14:44:33 Policy training - Surrogate loss: 0.0015449454076588154 KL divergence: 0.007285808678716421 Entropy: 1.0769550800323486 training epoch: 2 learning_rate: 0.0003
14:44:33 Policy training - Surrogate loss: 0.00017525668954476714 KL divergence: 0.010297714732587337 Entropy: 1.0847886800765991 training epoch: 3 learning_rate: 0.0003
14:44:33 Policy training - Surrogate loss: 0.0009491141536273062 KL divergence: 0.005759113468229771 Entropy: 1.0711051225662231 training epoch: 4 learning_rate: 0.0003
14:44:33 Policy training - Surrogate loss: -0.002687961794435978 KL divergence: 0.005736241117119789 Entropy: 1.048622727394104 training epoch: 5 learning_rate: 0.0003
14:44:33 Policy training - Surrogate loss: -0.004708338063210249 KL divergence: 0.00992491189390421 Entropy: 1.0814813375473022 training epoch: 6 learning_rate: 0.0003
14:44:33 Policy training - Surrogate loss: -0.003770434996113181 KL divergence: 0.008360052481293678 Entropy: 1.051531434059143 training epoch: 7 learning_rate: 0.0003
14:44:33 Policy training - Surrogate loss: -0.0069019547663629055 KL divergence: 0.008427591994404793 Entropy: 1.058234691619873 training epoch: 8 learning_rate: 0.0003
14:44:33 Policy training - Surrogate loss: -0.006749548017978668 KL divergence: 0.006937786005437374 Entropy: 1.0705825090408325 training epoch: 9 learning_rate: 0.0003
14:44:33 Checkpoint - Saving in path: ['./checkpoint/1_Step-1154.ckpt']
14:44:33 Saved TF frozen graph!
14:44:33 Total Episodic Reward=292.00 Total Episodic Steps=94.00
```

Code to write the logs:
```
        print('Step:%.2f' % self.steps,
              'Steering:%f' % action[0],
              'R:%.2f' % reward,                                # Reward
              'DTCP:%f' % self.current_distance_to_checkpoint,  # Distance to Check Point
              'DT:%f' % self.distance_travelled,                # Distance Travelled
              'CT:%.2f' % self.collision_threshold,             # Collision Threshold
              'CTCP:%f' % self.closer_to_checkpoint,            # Is closer to checkpoint
              'PSR: %f' % self.power_supply_range)              # Steps remaining in Episode
```


