import PySimpleGUI as sg

# 1 - window_select

col_video_id = [
  [
    sg.Text("Input your video ID")
  ],
  [
    sg.In(size=(25,1), enable_events=True, key="VIDEO_ID"),
    sg.Button("OK", key="OK_ID")
  ]
]
col_info = [
  [sg.Text("No video selected.", key="VIDEO_NAME")],
  [sg.Text(key="VIDEO_DETAILS")],
  [sg.Button("View", disabled = True, key="VIEW_VIDEO")]
]

layout_select = [
  [
    sg.Column(col_video_id),
    sg.VSeperator(),
    sg.Column(col_info)
  ]
]

window_select = sg.Window("Abdec Solver - ???", layout_select)

# 2 - window_loading

layout_loading = [
  [sg.Text("Loading...", key="LOADING_STATUS")]
]

window_loading = sg.Window("Abdec Solver - Loading?", layout_loading)

# 3 - window_video

window_video = None

def get_window_video():
  return window_video

def generate_window_video(video):
  global window_video
  layout = [
      [
          sg.Graph(
              canvas_size=(1920 / 2, 1080 / 2),
              graph_bottom_left=(0, video['height']),
              graph_top_right=(video['width'], 0),
              key="FRAME"
          )
      ]
  ]

  window_video = sg.Window(f"Abdec Solver", layout)
  window_video.Finalize()
  window_video.bind('<Right>', 'NEXT_SOLVE')
  window_video.bind('<Left>', 'PREV_SOLVE')