"""
AWS DeepRacer reward function using only progress

NOTE: This is great for maximizing individual step rewards, but the 
total episode reward will always be 100.  
"""
import bisect
import math
import numpy as np
from shapely.geometry import Point, Polygon
from shapely.geometry.polygon import LinearRing, LineString

CANADA_RACE_LINE = \
np.array([[ 4.58690814,  1.62381599],
       [ 4.48738106,  1.65427416],
       [ 4.38725046,  1.68433614],
       [ 4.28650273,  1.71406729],
       [ 4.18493776,  1.74356116],
       [ 4.08163985,  1.77406108],
       [ 3.97832333,  1.80508233],
       [ 3.87512443,  1.83662263],
       [ 3.77211047,  1.86872584],
       [ 3.66931665,  1.90142676],
       [ 3.5667727 ,  1.93477735],
       [ 3.46450369,  1.96882859],
       [ 3.36251967,  2.00359792],
       [ 3.26080706,  2.03904586],
       [ 3.15932308,  2.07506231],
       [ 3.05802492,  2.11153893],
       [ 2.95687354,  2.14837789],
       [ 2.85585551,  2.18554509],
       [ 2.75883824,  2.22060616],
       [ 2.66230625,  2.25419253],
       [ 2.56644797,  2.28554876],
       [ 2.47140549,  2.31398797],
       [ 2.37731947,  2.33884628],
       [ 2.28436053,  2.35948844],
       [ 2.19273576,  2.37537617],
       [ 2.10270351,  2.38604352],
       [ 2.01457372,  2.39108769],
       [ 1.92870117,  2.39017183],
       [ 1.8455711 ,  2.38283127],
       [ 1.76540056,  2.36930326],
       [ 1.68843599,  2.34970859],
       [ 1.61491668,  2.3241611 ],
       [ 1.54562711,  2.29200111],
       [ 1.48021793,  2.25434192],
       [ 1.41931891,  2.21083539],
       [ 1.36380989,  2.16101989],
       [ 1.31511767,  2.10415835],
       [ 1.27611324,  2.03901854],
       [ 1.24632892,  1.96765326],
       [ 1.22479791,  1.89173628],
       [ 1.21095609,  1.81227247],
       [ 1.20433386,  1.73001781],
       [ 1.20472823,  1.64551202],
       [ 1.21191166,  1.55924072],
       [ 1.2256072 ,  1.47164742],
       [ 1.24549188,  1.38313076],
       [ 1.27120175,  1.29404115],
       [ 1.30233735,  1.2046781 ],
       [ 1.33847044,  1.11528869],
       [ 1.37915029,  1.02606771],
       [ 1.4239118 ,  0.93715971],
       [ 1.47239061,  0.84867972],
       [ 1.52395403,  0.76066762],
       [ 1.57824537,  0.67316842],
       [ 1.63479949,  0.58618964],
       [ 1.6931722 ,  0.49972327],
       [ 1.7529591 ,  0.41375199],
       [ 1.81381873,  0.32825241],
       [ 1.87554104,  0.24323706],
       [ 1.93603738,  0.15849485],
       [ 1.99578398,  0.07337039],
       [ 2.05473558, -0.01216384],
       [ 2.11286616, -0.09812402],
       [ 2.17012451, -0.18453837],
       [ 2.22650982, -0.27140824],
       [ 2.28208852, -0.35869942],
       [ 2.33699743, -0.44634066],
       [ 2.39133716, -0.53427951],
       [ 2.44519635, -0.62246971],
       [ 2.49858153, -0.71090791],
       [ 2.55315288, -0.80018441],
       [ 2.60840039, -0.88884569],
       [ 2.66457569, -0.97664089],
       [ 2.72193044, -1.06330053],
       [ 2.7807145 , -1.14853223],
       [ 2.84117098, -1.23201811],
       [ 2.9035955 , -1.31333661],
       [ 2.96806472, -1.39226498],
       [ 3.03478235, -1.46838728],
       [ 3.10384421, -1.54135851],
       [ 3.17529632, -1.61084721],
       [ 3.24914195, -1.67653683],
       [ 3.32534623, -1.7381322 ],
       [ 3.40384079, -1.79536844],
       [ 3.48452863, -1.84802159],
       [ 3.56728929, -1.89592025],
       [ 3.65198431, -1.93895751],
       [ 3.73846297, -1.97710206],
       [ 3.82656835, -2.01040731],
       [ 3.91614359, -2.03901717],
       [ 4.00703771, -2.06316761],
       [ 4.09910987, -2.08318352],
       [ 4.19223006, -2.09947197],
       [ 4.28627422, -2.11251339],
       [ 4.38111294, -2.12285416],
       [ 4.47659463, -2.13110561],
       [ 4.57252446, -2.13796276],
       [ 4.66872742, -2.14399834],
       [ 4.77000868, -2.1500424 ],
       [ 4.87130911, -2.15666494],
       [ 4.97263773, -2.16412528],
       [ 5.07400359, -2.17267168],
       [ 5.17541634, -2.18256141],
       [ 5.276882  , -2.19394462],
       [ 5.37840338, -2.20689502],
       [ 5.47997997, -2.22142266],
       [ 5.58160783, -2.23748358],
       [ 5.68327968, -2.25499019],
       [ 5.78498545, -2.27382221],
       [ 5.88671326, -2.29383597],
       [ 5.98845084, -2.31487017],
       [ 6.09018733, -2.33675134],
       [ 6.19191516, -2.35929273],
       [ 6.29362868, -2.38238388],
       [ 6.39532399, -2.4059246 ],
       [ 6.49699807, -2.42983908],
       [ 6.59782498, -2.45315915],
       [ 6.69849498, -2.47569571],
       [ 6.79894984, -2.49704858],
       [ 6.89913314, -2.51677778],
       [ 6.99897986, -2.53439931],
       [ 7.09842452, -2.54951355],
       [ 7.19737634, -2.56170081],
       [ 7.29572336, -2.5705693 ],
       [ 7.39333932, -2.57579568],
       [ 7.49005004, -2.57697023],
       [ 7.58564678, -2.57369543],
       [ 7.67988935, -2.56561554],
       [ 7.77249828, -2.55239836],
       [ 7.86316118, -2.53376514],
       [ 7.9515388 , -2.5095112 ],
       [ 8.03726886, -2.47951198],
       [ 8.11997016, -2.4437251 ],
       [ 8.19924737, -2.40219134],
       [ 8.27469619, -2.35503399],
       [ 8.3459086 , -2.30245627],
       [ 8.41247792, -2.2447372 ],
       [ 8.47400385, -2.18222628],
       [ 8.53009729, -2.11533745],
       [ 8.58038524, -2.04454242],
       [ 8.62451568, -1.97036359],
       [ 8.66216268, -1.89336638],
       [ 8.69303168, -1.81415101],
       [ 8.71686515, -1.73334328],
       [ 8.73344843, -1.65158445],
       [ 8.74261584, -1.56951973],
       [ 8.74425677, -1.48778563],
       [ 8.73832158, -1.40699594],
       [ 8.72482696, -1.32772683],
       [ 8.70386036, -1.25050128],
       [ 8.67558293, -1.17577369],
       [ 8.64023685, -1.10391207],
       [ 8.59852451, -1.03498832],
       [ 8.54979569, -0.96969581],
       [ 8.49515075, -0.90777692],
       [ 8.43520907, -0.84908712],
       [ 8.37033534, -0.79355949],
       [ 8.30107407, -0.74094638],
       [ 8.22800612, -0.69091177],
       [ 8.15174535, -0.64305094],
       [ 8.07294303, -0.59690999],
       [ 7.99227282, -0.55201739],
       [ 7.91043405, -0.50789554],
       [ 7.82183413, -0.45934669],
       [ 7.73385588, -0.40987187],
       [ 7.64675315, -0.35910129],
       [ 7.56075882, -0.30670408],
       [ 7.47607845, -0.25239782],
       [ 7.39287   , -0.19597687],
       [ 7.31123826, -0.1373178 ],
       [ 7.23123156, -0.07638045],
       [ 7.15283838, -0.01320887],
       [ 7.07598551,  0.05206999],
       [ 7.00053998,  0.11925234],
       [ 6.92631822,  0.18807251],
       [ 6.85309405,  0.25821532],
       [ 6.78067486,  0.32941673],
       [ 6.70890695,  0.40146852],
       [ 6.6378418 ,  0.47162292],
       [ 6.56615283,  0.54079899],
       [ 6.49373643,  0.60882247],
       [ 6.42044865,  0.67545007],
       [ 6.34617612,  0.74048232],
       [ 6.27081516,  0.80373199],
       [ 6.19423915,  0.86497245],
       [ 6.1163545 ,  0.92403245],
       [ 6.03709717,  0.98079546],
       [ 5.9564273 ,  1.03519585],
       [ 5.87432458,  1.08721547],
       [ 5.79078409,  1.1368797 ],
       [ 5.70581254,  1.18425258],
       [ 5.61942522,  1.22943081],
       [ 5.53164382,  1.27253724],
       [ 5.44249526,  1.31371417],
       [ 5.35201168,  1.35311694],
       [ 5.26023149,  1.39090822],
       [ 5.16720118,  1.42725323],
       [ 5.07297767,  1.46231616],
       [ 4.97763079,  1.49625767],
       [ 4.88124504,  1.52923333],
       [ 4.78391895,  1.5613916 ],
       [ 4.68575941,  1.59286997],
       [ 4.58690814,  1.62381599]])

OVAL_RACE_LINE = \
np.array([[2.98364267, 0.99085028],
       [3.17421598, 0.97620247],
       [3.36671419, 0.96649433],
       [3.56058581, 0.960703  ],
       [3.75535101, 0.95777286],
       [3.95062567, 0.95669888],
       [4.14610792, 0.95653044],
       [4.34159153, 0.95639902],
       [4.53707359, 0.95630106],
       [4.7325572 , 0.9562338 ],
       [4.92803925, 0.95619736],
       [5.12352151, 0.95618474],
       [5.31900376, 0.95620671],
       [5.51448601, 0.95624661],
       [5.70979907, 0.95683811],
       [5.90453462, 0.95904602],
       [6.09820605, 0.96402984],
       [6.2902894 , 0.97289169],
       [6.48020848, 0.98670902],
       [6.66733244, 1.00652711],
       [6.85092153, 1.03345045],
       [7.0301681 , 1.06852883],
       [7.20417779, 1.11277401],
       [7.37191408, 1.16722165],
       [7.5320838 , 1.23304026],
       [7.68318939, 1.31135122],
       [7.82337587, 1.40332219],
       [7.95010759, 1.5102931 ],
       [8.05936795, 1.63382532],
       [8.1520362 , 1.77028048],
       [8.22819348, 1.9172171 ],
       [8.28787224, 2.07238766],
       [8.3308672 , 2.23370267],
       [8.35693826, 2.39905148],
       [8.36600944, 2.56628126],
       [8.35817837, 2.73328038],
       [8.3337493 , 2.89807127],
       [8.29289897, 3.05877775],
       [8.23595591, 3.21364943],
       [8.16298155, 3.36089086],
       [8.07359073, 3.49836566],
       [7.9671104 , 3.62340215],
       [7.8425753 , 3.73235683],
       [7.70459723, 3.82715581],
       [7.55530675, 3.90855117],
       [7.39646948, 3.97742213],
       [7.22950707, 4.03458291],
       [7.05575741, 4.08103305],
       [6.87635781, 4.11772732],
       [6.69236277, 4.14572764],
       [6.50477569, 4.16628195],
       [6.3144696 , 4.18067204],
       [6.12216363, 4.19011328],
       [5.92844134, 4.19573362],
       [5.73377501, 4.19857523],
       [5.53854858, 4.19960687],
       [5.34308058, 4.19975659],
       [5.14759562, 4.19980232],
       [4.95211356, 4.19981647],
       [4.75663015, 4.19980096],
       [4.56114789, 4.19975794],
       [4.36566429, 4.19968663],
       [4.17018339, 4.19958005],
       [3.97470114, 4.19944052],
       [3.79232065, 4.19861421],
       [3.62484561, 4.19654801],
       [3.46494018, 4.19276608],
       [3.30661124, 4.18665152],
       [3.14553467, 4.17732632],
       [2.97916312, 4.16360559],
       [2.80731174, 4.14417676],
       [2.63194691, 4.11772299],
       [2.45616369, 4.08308572],
       [2.28299749, 4.03924655],
       [2.11489618, 3.98520214],
       [1.9537057 , 3.92004072],
       [1.80126696, 3.84251329],
       [1.65974801, 3.75114985],
       [1.53187772, 3.64444942],
       [1.42163922, 3.52095515],
       [1.32850831, 3.38416482],
       [1.25247416, 3.23670747],
       [1.19359575, 3.08103347],
       [1.15181546, 2.91953305],
       [1.12709231, 2.75444834],
       [1.11919456, 2.5878978 ],
       [1.12767868, 2.42180181],
       [1.15224643, 2.25790639],
       [1.19257573, 2.09783843],
       [1.24854056, 1.94320292],
       [1.32072641, 1.79597821],
       [1.40962022, 1.65837756],
       [1.51614302, 1.53330828],
       [1.64132309, 1.42464859],
       [1.77997335, 1.3300841 ],
       [1.92991192, 1.24882412],
       [2.08935204, 1.17997642],
       [2.2568989 , 1.12278679],
       [2.43128201, 1.07640317],
       [2.6112811 , 1.03978189],
       [2.79573133, 1.0116745 ],
       [2.98364267, 0.99085028]])

TARGET_NUMBER_STEPS = 150
RACE_LINE_WAYPOINTS = CANADA_RACE_LINE

# Globals
g_last_progress_value = 0.0
g_start_offset_percent = 0.0
g_race_line_string = LineString(RACE_LINE_WAYPOINTS)
# for getting current race line waypoint distances
g_race_line_dists = [LineString(RACE_LINE_WAYPOINTS).project(Point(p), normalized=True) for p in LineString(RACE_LINE_WAYPOINTS).coords[:-1]] + [1.0]


#===============================================================================
#
# REWARD
#
#===============================================================================

def reward_function(params):
    p = progress_factor(params)
    h = race_line_heading_factor(params)
    d = race_line_distance_factor(params)
    print("progress_factor ", p, " heading_factor ", h, " distance factor ", d)
    reward = p + h + d
    return float(max(reward, 1e-3)) # make sure we never return exactly zero

#===============================================================================
# PROGRESS
#===============================================================================

# Using the race-line coords, calculate progress the same way
# that params['progress'] is calculated (without support for reverse direction)
def current_progress_along_race_line(params):
    global g_start_offset_percent
    global g_race_line_string

    #print("params ", params)
    race_line_position_percent = g_race_line_string.project(Point(params['x'], params['y']), normalized=True)
    #print("race_line_position_percent (absolute): ", race_line_position_percent)

    # reset the "zero" position along the race line string
    # We add params['progress'] here  since
    #    a) it's always non-zero for the standard progress, so the number will just be closer
    #    b) if its near zero, we risk some small chance of it being negative and 
    #       screwing up calculations of rewards
    if params['steps'] == 0:
        g_start_offset_percent = race_line_position_percent - (params['progress'] / 100.0)
        #print("Resetting zero-position to ", g_start_offset_percent )

    race_line_progress_percent = race_line_position_percent - g_start_offset_percent
    #print("race_line_progress_percent (relative to start): ", race_line_progress_percent)
    if race_line_progress_percent < 0.0:
        race_line_progress_percent = race_line_progress_percent + 1.0
    race_line_progress_hundreds = 100 * race_line_progress_percent
    return race_line_progress_hundreds
    
def progress_factor(params):
    # Progress range:  0..100
    # Step is roughly a 1/15s timeslice so can account for time-factor
    # Expected real value: [0,~1.0]
    global g_last_progress_value
    
    # Simple reward for outlier case of first step in the episode
    if params['steps'] == 0:
        g_last_progress_value = 0.0

    # Find the source of progress
    #progress_hundreds = params['progress'] # Use this for centerline progress
    progress_hundreds = current_progress_along_race_line(params) # Use this for race-line progress
    #print("progress_hundreds ", progress_hundreds)
    
    # Do rewards calculation based on progress delta
    delta = progress_hundreds - g_last_progress_value
    g_last_progress_value = progress_hundreds
    
    progress_target_per_step = 100.0 / TARGET_NUMBER_STEPS # use 1 instead of 100 to match progress_since_last magnitude
    progress_factor = delta / progress_target_per_step
    return progress_factor

#===============================================================================
#
# HEADING
#
#===============================================================================

def race_line_heading_factor(params):
    global RACE_LINE_WAYPOINTS
    global g_race_line_string
    global g_race_line_dists
    
    # Find the nearest waypoints. Environment does this for us w.r.t. center line,
    # so we repeat it here for race-line
    current_position = Point(params['x'], params['y'])
    current_ndist = g_race_line_string.project(current_position, normalized=True)

    next_index = bisect.bisect_right(g_race_line_dists, current_ndist)
    prev_index = next_index - 1
    if next_index == len(g_race_line_dists):
        next_index = 0
        
    # Target heading in euler reference coordinates
    target_heading = angle_of_vector(RACE_LINE_WAYPOINTS[prev_index], RACE_LINE_WAYPOINTS[next_index])

    heading_delta = abs(target_heading - params['heading'])
    if heading_delta > 180: 
        heading_delta = 360 - heading_delta

    # Gradient factor from 1.0 to 0.0, with
    #  1.0 :  delta is zero
    #  0.0 :  delta is >= 30deg
    allowance = 30.0
    heading_factor = 1.0 - heading_delta / allowance
    return max(heading_factor, 0.0)

def angle_of_vector(point1, point2):
    rad = math.atan2(point2[1] - point1[1], point2[0] - point1[0])
    return math.degrees(rad)


#===============================================================================
#
# TRACK POSITION
#
#===============================================================================

def race_line_distance_factor(params):
    global g_race_line_string

    # Reward for track position
    current_position = Point(params['x'], params['y'])
    distance = current_position.distance(g_race_line_string)

    # clamp reward to range (0..1) mapped to distance (track_width..0).
    # This could be negative since the car center can be off the track but
    # still not disqualified.
    allowance = params['track_width'] / 2.0 # gradient up to half width of track, then zero afterwards
    distance_factor = 1.0 - distance / allowance
    #print("x %0.2f y %0.2f distance %0.2f track_width %0.2f factor %0.7f" % (params['x'], params['y'], distance, params['track_width'], factor))
    return float(max(distance_factor, 0.0))

