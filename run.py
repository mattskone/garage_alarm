import logging
import os
import alerts
import camera
import config
import features
import models
import shutil


logging.basicConfig(filename=os.path.join(config.INSTALL_DIR, 'app.log'),
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    model = models.get_trained_model()
    new_trial_dir = os.path.join(config.INSTALL_DIR, config.NEW_TRIAL_DIR)
    new_trial_file_name = camera.take_photo(new_trial_dir)
    full_trial_file_name = os.path.join(new_trial_dir, new_trial_file_name)
    logger.info('Classifying new trial {0}'.format(new_trial_file_name))
    new_trial_features = features.get_features_for_image(full_trial_file_name)
    labels = model.predict(new_trial_features)
    if labels[0] == 0:
        shutil.move(full_trial_file_name,
                    os.path.join(config.INSTALL_DIR,
                                 config.NEGATIVE_TRIAL_DIR,
                                 new_trial_file_name))
        logger.info('Classified negative')
    else:
        shutil.move(full_trial_file_name,
                    os.path.join(config.INSTALL_DIR,
                                 config.POSITIVE_TRIAL_DIR,
                                 new_trial_file_name))
        alerts.trigger_alert()
        logger.info('Classified positive')


if __name__ == '__main__':
    main()

