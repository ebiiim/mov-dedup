from pathlib import Path
from de_duplication.dedup import MovDeDup
from logging import getLogger
logger = getLogger(__name__)


class MultiDeDup(object):

    @staticmethod
    def get_paths(src_dirs, threshold):
        src_dirs_base = Path(src_dirs[0]).resolve().parent
        similarity_files = [src_dirs_base.joinpath('psnr_' + '{:04g}'.format(i + 1) + '.csv').as_posix()
                            for i in range(len(src_dirs))]
        threshold_values = [threshold, ] * len(src_dirs)
        dst_dirs = [src_dir.replace('input', 'output') for src_dir in src_dirs]

        logger.info('src_dirs: ' + str(src_dirs))
        logger.info('dst_dirs: ' + str(dst_dirs))
        logger.info('similarity_files: ' + str(similarity_files))
        logger.info('threshold_values: ' + str(threshold_values))

        mk_path = Path(dst_dirs[0]).parent
        if not mk_path.exists():
            logger.debug('mkdir: ' + mk_path.as_posix())
            mk_path.mkdir()

        return src_dirs, dst_dirs, similarity_files, threshold_values

    @staticmethod
    def multi_copy1(src_dirs, threshold):
        src_dirs, dst_dirs, similarity_files, threshold_values = MultiDeDup.get_paths(src_dirs, threshold)
        for src, dst, sf, tv in zip(src_dirs, dst_dirs, similarity_files, threshold_values):
            mdp = MovDeDup(path_input=src, path_tmp=dst, path_output=dst)
            mdp.init_check()

            del_l, src_l = MovDeDup.get_copy_lists(sf, tv)
            mdp.copy_dedup(del_l)

        return dst_dirs

    @staticmethod
    def multi_copy2(src_dirs, threshold):
        src_dirs, dst_dirs, similarity_files, threshold_values = MultiDeDup.get_paths(src_dirs, threshold)
        for src, dst, sf, tv in zip(src_dirs, dst_dirs, similarity_files, threshold_values):
            mdp = MovDeDup(path_input=src, path_tmp=dst, path_output=dst)
            mdp.init_check()

            del_l, src_l = MovDeDup.get_copy_lists(sf, tv)
            mdp.copy_dup(del_l, src_l)

        return dst_dirs
