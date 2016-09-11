defaults={
    "window_width": 651,
    "window_height": 651,
    "font_size": 36,
    "button_height": 45,

  #Audio settings
    "mixer_frequency": 44100,
    "mixer_size": -16,
    "mixer_channels": 2,
    "mixer_buffer_size": 2048,
    "mixer_volume_music": 0.3,
    "music_file": "bg_music.ogg",

    #GameBoard Changeables
    "level": 1,
    "rows_shifted": 0,
    "rows": 21,
    "columns": 14,
    "show_grid": False,
    "font_color": (255, 255, 255),
    "background_color": (0, 0, 0),
    "string_next": "NEXT",
    "string_level": "LEVEL: {}",
    "string_rows": "LINES: {}",
    "string_score": "SCORE: {}",

    #Shape Mechanics
    "shape_speed": 400,
    "slow_time": False,
    "slow_time_shape_speed": 500,
    "down_key_shape_speed": 25,
    "speed_change_per_level": 85,
    "speed_minimum": 50,
    "strafe_rate": 50,
    "strafe_tick_lag": 250,

    #Scoring
    "level": 0,
    "score": 0,
    "score_row_exponent": 2,
    "score_row_multiplier": 100,
    "score_accumulator_multiplier": 2000,

    #GameBoard NonChangeables
    "coordinate_x": 0,
    "coordinate_y": 0,
    "cell_width": 31,
    "cell_height": 31,
    "display_depth":32,
    "display_flags":0,
    "queue_dimensions": (162, 162),
    "show_grid": False,
}
