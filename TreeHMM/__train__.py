import numpy as __np
import time as __time
import EMBasins as orig
orig.pyInit()
from TreeHMM import utils

def __gatterHMMtrainResults(cross_val_folds, n_modes, \
            params, trans, P, emiss_prob, alpha, pred_prob, \
            hist, samples, stationary_prob, \
            train_log_li, test_log_li, eta, training_length, seed):
    res = {}
    res['params'] = params
    res['trans'] = trans
    res['P'] = P
    res['emiss_prob'] = emiss_prob
    res['alpha'] = alpha
    res['pred_prob'] = pred_prob
    res['hist'] = hist
    res['samples'] = samples
    res['stationary_prob'] = stationary_prob
    res['train_log_li'] = train_log_li
    res['test_log_li'] = test_log_li

    res["cross_val_folds"] = cross_val_folds
    res["n_modes"] = n_modes
    res["eta"] = eta
    res["training_length"] = training_length
    res["seed"] = seed
    return res

def trainHMM(spikes, n_modes, n_iter=100, eta=0.002, bin_size=1, cross_val_folds=0, seed=None, normalize_log_li=True):
    """
        Fit HMM model on spiking data.

        Args:
            spikes - spiking data of shape (number of neurons, number of bins)
            n_modes - number of modes in HMM
            n_iter - number of traning iterations
            eta - HMM regularization param
            bin_size - bin length
            cross_val_folds - number of cross validation folds,
                              if <= 1 no cross validation is performed, 
                              if > 1 only params trained on last fold are returned, 
                              but logli for all folds is written
            seed - seed integer value
            normalize_log_li - if True and cross_val_folds > 1 divide train_log_li by (cross_val_folds-1) to get the same range as test_log_li

        Return:
            Dictionary containing HMM params.
    """

    if seed is not None:
        __np.random.seed(seed)

    if cross_val_folds < 1:
        cross_val_folds = 1

    spike_times = utils.spikeRasterToSpikeTimes(spikes, bin_size)
    train_log_li = __np.zeros(shape=(cross_val_folds, n_iter))
    test_log_li = __np.zeros(shape=(cross_val_folds, n_iter))

    start = __time.time()
    if cross_val_folds > 1:
        _, bin_num = spikes.shape
        bins = __np.arange(bin_num, dtype=__np.float64) * bin_size
        shuffled_inds = __np.random.permutation(__np.arange(bin_num, dtype=__np.int32))
        n_test = int(bin_num / cross_val_folds)

        for k in range(cross_val_folds):
            test_inds = shuffled_inds[k*n_test:(k+1)*n_test]
            train_inds = __np.zeros(bin_num, dtype=__np.int32)
            train_inds[test_inds] = 1
            flips = __np.diff(__np.append([0], train_inds)) # contiguous 1s form a test chunk, i.e. are "unobserved"

            unobserved_lo = bins[flips == 1]
            unobserved_hi = bins[flips == -1]
            if (len(unobserved_hi) < len(unobserved_lo)):
                # just in case, a last -1 is not there to close the last chunk
                unobserved_hi = __np.append(unobserved_hi,[bin_num])

            params, trans, P, emiss_prob, alpha, pred_prob, hist, samples, stationary_prob, train_log_li_this, test_log_li_this = \
                orig.pyHMM(spike_times, unobserved_lo, unobserved_hi, float(bin_size), n_modes, n_iter, eta)

            print(f"Finished cross validation round {k} of fitting.\
                    \nTrain logL = {train_log_li_this[0][0]}\
                    \nTest logL = {test_log_li_this[0][0]}")

            train_log_li[k,:] = train_log_li_this.flatten()
            test_log_li[k,:] = test_log_li_this.flatten()

        if normalize_log_li:
            train_log_li /= (cross_val_folds-1)
    else:
        params, trans, P, emiss_prob, alpha, pred_prob, hist, samples, stationary_prob, train_log_li_this, test_log_li_this = \
            orig.pyHMM(spike_times, __np.array([]), __np.array([]), float(bin_size), n_modes, n_iter, eta)
        train_log_li[0, :] = train_log_li_this
        test_log_li[0, :] = test_log_li_this
    end = __time.time()
    training_length = end - start
    print(f"Finished training in {training_length} seconds.")

    return __gatterHMMtrainResults(cross_val_folds, n_modes, params, trans, P, emiss_prob, alpha, pred_prob, hist, samples, stationary_prob, train_log_li, test_log_li, eta, training_length, seed)

