import parameters as env
import numpy as np

def validateParameters():
  global ENERGY_EXPONENT
  print("Skipped validation of parameters (energy)...")


def calculateTheoreticalMinimumEnergy(weightsByEpoch, epochIndexForConvergence):
    return round(np.sum(np.abs(weightsByEpoch[epochIndexForConvergence] - weightsByEpoch[0])), 3)

def calculateMetabolicEnergy(weightsByEpoch):
  # Synapse weights is currently rowed by epoch, rearrange so that each row is the same synapse but over time
  weightsByTime = np.transpose(weightsByEpoch)
  changeInWeightsPerTimeStep = np.diff(weightsByTime)
  return round(np.sum(abs(changeInWeightsPerTimeStep)**env.ENERGY_EXPONENT), 3)


def calculateEfficiency(metabolicEnergy, theoreticalMinimumEnergy):
  return round((metabolicEnergy - theoreticalMinimumEnergy), 3)


def calculateTheoreticalEfficiency():
  K = 2*env.N_PATTERN/(2-env.N_PATTERN/env.X_PATTERN_FEATURE)**2
  m_perceptron = env.N_PATTERN * K * env.LEARNING_RATE
  m_minimum = ((2/np.pi)**(1/2))*env.LEARNING_RATE*(K**(1/2))
  try:
    value = m_perceptron / m_minimum
  except :
    value = 0
  return round(value, 3)

def calculateEnergyFromMaintenance(weightsByEpoch):
  # Synapse weight changes are currently rowed by epoch, rearrange so that each row is the same synapse but over time
  weightsByEpoch = np.transpose(weightsByEpoch)
  #∑_t|s_i(t)|)
  summedWeightsForAllTimes = np.sum(np.abs(weightsByEpoch), axis=1)  
  
  #∑_i( ∑_t|s_i(t)|) )
  summedWeightsForAllTimesByMemoryType = np.sum(
      summedWeightsForAllTimes, axis=1)
  
  energyConstantsByMemoryType = np.asarray([x['cost_of_maintenance'] for x in env.SYNAPSE_MEMORY_TYPES.values()])
  
  # c * ∑_i( ∑_t|s_i(t)|) )
  energyConsumedByMaintenance = np.multiply(
      summedWeightsForAllTimesByMemoryType, energyConstantsByMemoryType)
  return round(np.sum(energyConsumedByMaintenance), 3)


def calculateEnergyFromConsolidations(consolidationsByEpoch):
  # Synapse weight changes are currently rowed by epoch, rearrange so that each row is the same synapse but over time
  consolidationsByTime = np.transpose(
      consolidationsByEpoch)

  # | l_i(t) - l_i (t-1) |
  # THIS IS WRONG: changeInWeightsPerTimeStep = np.abs(np.diff(consolidationsByTime))


  # ∑_t (| l_i(t) - l_i (t-1) |)
  summedConsolidationsForAllTimes = np.sum(np.abs(consolidationsByTime), axis=1)

  # ∑_i ∑_t (| l_i(t) - l_i (t-1) |)
  summedConsolidationsForAllTimesAndMemoryTypes = np.sum(summedConsolidationsForAllTimes, axis=1)
  

  energyConstantsByMemoryType = np.asarray(
      [x['cost_of_consolidation'] for x in env.SYNAPSE_MEMORY_TYPES.values()])

  
  # c * ∑_i ∑_t (| l_i(t) - l_i (t-1) |)
  # NOTE: The paper considers c=1 for consolidations. I.e., the cost of consolidation is equal to the change in weight.
  consolidationEnergyByMemoryType = np.multiply(
      summedConsolidationsForAllTimesAndMemoryTypes, energyConstantsByMemoryType)
  
  # The consolidation energy so far, is stored as a vector. With each element representing the consolidation energy required per memory type (e.g., persistent, persisent2, transient). 
  # NOTE: The paper considers only persistent memory as a memory type that accepts consolidation.

  # Get sum of vector.
  summedConsolidationEnergy = np.sum(consolidationEnergyByMemoryType)
  return round(summedConsolidationEnergy, 3)


def calculateEnergyJustBeforeThreshold():
  # Multiply this by the energy constant.
  return env.ENERGY_USED_TO_REACH_THRESHOLD_TALLY * env.MAINTENANCE_COST_OF_TRANSIENT_MEMORY


def calculateOptimalThreshold():
  P = env.N_PATTERN
  N = env.X_PATTERN_FEATURE
  # For this, we assume that the last memory type is transient memory!
  # TODO: Tidy this up.
  c = env.SYNAPSE_MEMORY_TYPES[list(env.SYNAPSE_MEMORY_TYPES)[-1]]['cost_of_maintenance']
  #T = epochIndexForConvergence
  T = (P**(3/2)) / ((2-(P/N))**2)

  K = (2*P)/((2-(P/N))**2) #Numerically found

  return (env.LEARNING_RATE**2) * ( (3*K) / (1+c*T) )