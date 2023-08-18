import mne
from mne_bids import write_raw_bids, BIDSPath
from pathlib import Path

from utls.motiondata import MotionData

# specify BIDS root
bids_root = Path(r"./data/bids")

# load motion data to dataclass
test_motion_data = MotionData.import_hasomed_imu(file=r"./data/exDataHasomed.csv")

# transfer data to mne raw object
info = mne.create_info(
    ch_names=test_motion_data.channels.name,
    sfreq=test_motion_data.info.SamplingFrequency,
    ch_types="bio",
)
raw = mne.io.RawArray(test_motion_data.time_series, info)

# write to BIDS
bids_path = BIDSPath(
    subject=test_motion_data.info.SubjectId,
    task=test_motion_data.info.TaskName,
    datatype="beh",
    root=bids_root,
)
write_raw_bids(
    raw, bids_path, overwrite=True, allow_preload=True, format="EDF", verbose=True
)
