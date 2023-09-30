from gymnasium.envs.registration import register

register(
    id="race_track/RaceTrack-v0",
    entry_point="race_track.envs:RaceTrackEnv",
)

