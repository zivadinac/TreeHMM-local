import numpy as __np


def spikeRasterToSpikeTimes(spike_raster, bin_size):
    """
        From spike raster create a neurons list of lists of spike times

        Args:
            spike_raster - spike raster
            bin_size - size of a bin
        Return:
            List of neuron spiking times.

        This function was originally written by Aditya:
        https://github.com/adityagilra/UnsupervisedLearningNeuralData/blob/master/EMBasins_sbatch.py#L73
    """
    n_neurons, bin_num = spike_raster.shape
    nrn_spike_times = []
    # multiply by bin_size, so that spike times are given in units of sampling indices
    bins = __np.arange(bin_num, dtype=float) * bin_size
    for n in range(n_neurons):
        # am passing a list of lists, convert numpy.ndarray to list,
        #  numpy.ndarray is just used to enable multi-indexing
        nrn_spike_times.append(list(bins[spike_raster[n,:] != 0]))
    return nrn_spike_times

