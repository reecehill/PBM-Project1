# CONSTANT PARAMETERS
from numpy import random, linspace
SEEDS = list(range(0,5))

LEARNING_RATES = [1]

# The number of pattern features will always be equal to the number of weights.
# Could be 8200, according to https://pubmed.ncbi.nlm.nih.gov/2778101/
X_PATTERN_FEATURES = [250]


# Ensure N_PATTERNS is not zero, and not equal to double X_PATTERN_FEATURES
#amounts = linspace(0.0001, 1.99, 100)
#N_PATTERNS = [int(x*X_PATTERN_FEATURES[0]) for x in amounts]
N_PATTERNS = [250]
# X_PATTERNS = X_PATTERN_FEATURES

# Skips simulations where N_PATTERNS != X_PATTERN_FEATURES
ENSURE_N_PATTERNS_EQUALS_X_PATTERNS_FEATURES = False

# Max epochs before concluding convergence is not possible
MAX_EPOCHS = 1000

ENERGY_EXPONENT = 1

VERBOSE = False
STORE_WEIGHTS_TO_SPREADSHEET = False

# WEIGHTS_INITIALISED_AS can be set to  one of the following strings:
# 'zeros'
# 'uniform' (where min and max are taken from the memory_types min and max values)
# 'lognormal' (mean=0, sd=1)
WEIGHTS_INITIALISED_AS = 'zeros'

# Set simulation parameters according to preset scenarios. Enter an integer, as follows:
# 1: Synapses have behaviour alike that in the paper.
# 2: Prevent synapses from switching between excitatory/inhibitory (and deactivate them/set to zero if they try)
PRESET_SIMULATION = 1

# Type of synapse consolidation:
# 'local-local': Any one synapse that exceeds a threshold (local), will lead to just that synapse consolidating (local).
# 'local-global': Any one synapse that exceeds a threshold (local), will lead to all synapses of that synapse consolidating (global).
# 'global-global': Once all synapses exceed a threshold (global), all synapses of that synapse will be consolidated (global).
CACHE_ALGORITHMS = ['local-global']

# Only in effect when synapses are allowed to have transient/consolidated memory types.
# Accepts:
# - List of values to set
# ['optimal']: to find the optimal threshold.
#MAX_SIZES_OF_TRANSIENT_MEMORY = [2]
MAX_SIZES_OF_TRANSIENT_MEMORY = linspace(0.001, 40, 100)

# Only in effect when synapses are allowed to have transient/consolidated memory types.
# Used for figure 4 of paper.
MAINTENANCE_COSTS_OF_TRANSIENT_MEMORY = [1]

# insert comments for  DECAY_TAUS_OF_TRANSIENT_MEMORY
DECAY_TAUS_OF_TRANSIENT_MEMORY = [0.002]

# Only compatible with local-global cache algorithm!!
ONLY_CONSOLIDATE_AMOUNT_ABOVE_THRESHOLD = False

ALSO_CALCULATE_ENERGY_TO_REACH_THRESHOLD = True


# *-*-*-*-*-*-
# !! STOP !!
# For most simulations, the settings below this line do not need to be edited.
# *-*-*-*-*-*-
# Do not edit
ENERGY_USED_TO_REACH_THRESHOLD_TALLY = 0


if(PRESET_SIMULATION == 1):
    SYNAPSES_CAN_CHANGE_TYPE_MID_SIMULATION = True
    MEMORY_IS_TRANSIENT_OR_CONSOLIDATED = True
    SYNAPSE_TYPES_BEGIN_EITHER_INHIBITORY_OR_EXCITATORY = False
elif(PRESET_SIMULATION == 2):
    SYNAPSES_CAN_CHANGE_TYPE_MID_SIMULATION = False
    MEMORY_IS_TRANSIENT_OR_CONSOLIDATED = True
    SYNAPSE_TYPES_BEGIN_EITHER_INHIBITORY_OR_EXCITATORY = True


def setCacheAlgorithm(cacheAlgorithm):
    global CACHE_ALGORITHM
    CACHE_ALGORITHM = cacheAlgorithm


def setSeed(seed):
    global RANDOM_GENERATOR
    RANDOM_GENERATOR = random.default_rng(seed)


def setLearningRate(learningRate):
    global LEARNING_RATE
    LEARNING_RATE = learningRate


def setMaxSizeOfTransientMemory(maxSizeOfTransientMemory):
    global MAX_SIZE_OF_TRANSIENT_MEMORY
    MAX_SIZE_OF_TRANSIENT_MEMORY = maxSizeOfTransientMemory


def setMaintenaceCostOfTransientMemory(maintenanceCostOfTransientMemory):
    global MAINTENANCE_COST_OF_TRANSIENT_MEMORY
    MAINTENANCE_COST_OF_TRANSIENT_MEMORY = maintenanceCostOfTransientMemory

def setDecayTauOfTransientMemory(decayTauOfTransientMemory):
    global DECAY_TAU_OF_TRANSIENT_MEMORY
    DECAY_TAU_OF_TRANSIENT_MEMORY = decayTauOfTransientMemory

def setNPattern(nPattern):
    global N_PATTERN
    N_PATTERN = nPattern


def setXPatternFeature(xPatternFeature):
    global X_PATTERN_FEATURE
    global N_WEIGHTS
    X_PATTERN_FEATURE = xPatternFeature

    #WEIGHT_MODEL = WEIGHT_SYNAPSE_TYPES
    N_WEIGHTS = X_PATTERN_FEATURE +1 # Add an extra weight for the bias term.


def setWeightModel():
    global WEIGHT_MODEL
    WEIGHT_MODEL = generateWeightModel()


def generateWeightModel():
    global SYNAPSE_MEMORY_TYPES
    global WEIGHT_SYNAPSE_TYPES
    # This dictionary stores the different types of synapses, and is set according to SYNAPSE_TYPES_BEGIN_EITHER_INHIBITORY_OR_EXCITATORY
    if (SYNAPSE_TYPES_BEGIN_EITHER_INHIBITORY_OR_EXCITATORY):
        WEIGHT_SYNAPSE_TYPES = {
            0: {
                'name': 'excitatory',
                'max': 1.0,
                'min': 0,
                'default': 0,
                'percentage_quantity_of_synapses': 80,
                'cumulative': [],
                'memoryTypes': {}
            },
            1: {
                'name': 'inhibitory',
                'max': 0,
                'min': -1.0,
                'default': 0,
                'percentage_quantity_of_synapses': 20,
                'cumulative': [],
                'memoryTypes': {}
            }
        }
    else:
        WEIGHT_SYNAPSE_TYPES = {
            0: {
                'name': 'all',
                'max': 1.0,
                'min': -1.0,
                'default': 0,
                'percentage_quantity_of_synapses': 100,
                'cumulative': [],
                'memoryTypes': {}
            },
        }

    if(MEMORY_IS_TRANSIENT_OR_CONSOLIDATED):
        SYNAPSE_MEMORY_TYPES = {
            0: {
                'name': 'consolidated',
                'memory_size': False,
                'decay_tau': '0',
                'cost_of_maintenance': 0,
                'cost_of_consolidation': 2,
            },
            1: {
                'name': 'transient',
                'memory_size': MAX_SIZE_OF_TRANSIENT_MEMORY,
                'decay_tau': DECAY_TAU_OF_TRANSIENT_MEMORY,  # amount memory decays per time step
                'cost_of_maintenance': MAINTENANCE_COST_OF_TRANSIENT_MEMORY,
                # The highest memory type does not receive weights for consolidation.
                'cost_of_consolidation': 0
            },
        }
    else:
        SYNAPSE_MEMORY_TYPES = {
            0: {
                'name': 'consolidated',
                'memory_size': False,
                'decay_tau': 0,
            }
        }

    WEIGHT_MODEL = {}
    for synapse_name, synapse_info in WEIGHT_SYNAPSE_TYPES.items():
        WEIGHT_MODEL[synapse_name] = synapse_info
        for memory_name, memory_info in SYNAPSE_MEMORY_TYPES.items():
            WEIGHT_MODEL[synapse_name]['memoryTypes'][memory_name] = memory_info
    return WEIGHT_MODEL