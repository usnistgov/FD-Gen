import numpy as np
import pytest

import global_parm
import MHDR
import MRND


def v1_seed_list(seeds):
    # the seed list FD-Gen v1.0.0 handed out, in order
    np.random.seed(seeds)
    return np.random.randint(0, 100, size=200).tolist()


@pytest.fixture
def seeds_1(capsys):
    global_parm._INIT()
    MHDR.DEFINE_SEEDS(1)


def test_seeds_follow_v1_list_until_first_repeat(seeds_1):
    v1 = v1_seed_list(1)
    first_repeat = next(i for i in range(len(v1)) if v1[i] in v1[:i])
    seeds = [MRND.NEXT_RANDOM_SEED() for _ in range(first_repeat)]
    assert seeds == v1[:first_repeat]


def test_repeated_seed_replaced_without_shifting_later_seeds(seeds_1):
    v1 = v1_seed_list(1)
    seeds = [MRND.NEXT_RANDOM_SEED() for _ in range(60)]
    assert len(set(seeds)) == 60
    for i in range(60):
        if v1[i] not in v1[:i]:
            assert seeds[i] == v1[i]          # unaffected positions keep their v1.0.0 seed
        else:
            assert seeds[i] >= 100            # repeats get a replacement outside the v1.0.0 range


def test_no_crash_after_200_seeds_and_all_unique(seeds_1):
    seeds = [MRND.NEXT_RANDOM_SEED() for _ in range(1000)]
    assert len(set(seeds)) == 1000


def test_reserved_user_seeds_not_handed_out(seeds_1):
    v1 = v1_seed_list(1)
    MRND.RESERVE_RANDOM_SEEDS([v1[1], 12345])
    seeds = [MRND.NEXT_RANDOM_SEED() for _ in range(300)]
    assert seeds[0] == v1[0]
    assert v1[1] not in seeds and 12345 not in seeds


def test_same_project_seed_gives_same_sequence(seeds_1):
    first = [MRND.NEXT_RANDOM_SEED() for _ in range(300)]
    global_parm._INIT()
    MHDR.DEFINE_SEEDS(1)
    assert [MRND.NEXT_RANDOM_SEED() for _ in range(300)] == first
