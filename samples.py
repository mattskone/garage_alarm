import logging
import numpy as np
from sklearn.utils import shuffle
import features


logger = logging.getLogger(__name__)


def get_samples(pos_samples_dir, neg_samples_dir, reduced=False):
    """Produce sample data ready for training a classifier.

    :param pos_samples_dir: path to directory containing positive samples
    :param neg_samples_dir: path to directory containing negative samples
    :param reduced: when True, apply dimensionality reduction to the samples
    :returns: two numpy arrays.  The first (x, f) contains the feature data for
        x samples, and the second (y, ) contains the classifications for each
        of the samples.
    """

    logger.info('Getting training samples')
    pos_samples = features.get_features_for_dir(pos_samples_dir)
    pos_classes = np.ones(pos_samples.shape[0])
    neg_samples = features.get_features_for_dir(neg_samples_dir)
    neg_classes = np.zeros(neg_samples.shape[0])
    samples = np.vstack([pos_samples, neg_samples])
    if reduced:
        samples = features.reduce_features(samples, False)
    classes = np.hstack([pos_classes, neg_classes])
    samples, classes = shuffle(samples, classes)
    logger.info('Got training samples')

    return samples, classes

