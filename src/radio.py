#!/usr/bin/python3

import vlc
import time
import sys
import signal
import asyncio

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

signal.signal(signal.SIGINT, signal.SIG_DFL)

radioplayprefix: str = '?direct=true&listenerid=undefined&aw_0_1st.bauer_listenerid=undefined&aw_0_1st.playerid=BMUK_inpage_html5&aw_0_1st.skey=' + str(
	int(time.time()) - 4) + '&aw_0_1st.bauer_loggedin=false&aw_0_req.userConsentV2=false'

channels = [
	{
		"YLE Puhe": "https://yleradiolive.akamaized.net/hls/live/2027677/in-YlePuhe/abr.smil/chunklist_b256000_ao.m3u8",
		"YLE X": "https://yleradiolive.akamaized.net/hls/live/2027674/in-YleX/master.m3u8",
	},
	{
		'Top51': 'https://stream.radioplay.fi/top51/top51_64.aac',
		"Järviradio": "https://jarviradio.radiotaajuus.fi:9000/jr",
		"Radio Helsinki": "http://77.86.233.1:8004/",
	},
	{
		'SuomiRap': 'https://stream.radioplay.fi/suomirap/suomirap_64.aac',
		'NRJ': 'https://stream.radioplay.fi/nrj/nrj_64.aac',
	}
]


class MainWindow(QtWidgets.QMainWindow):

	async def update_volume(self) -> None:

		await asyncio.sleep(1)

		media_volume = self.media_player.audio_get_volume()
		self.sl.setValue(media_volume)
		self.label.setText(str(media_volume))

	def render_stop_button(self) -> None:

		mipmap = getattr(QtWidgets.QStyle, 'SP_MediaStop')
		icon = self.style().standardIcon(mipmap)

		stop_button = QtWidgets.QPushButton(None, self)
		stop_button.setIcon(icon)
		stop_button.clicked.connect(lambda: self.stop_radio())
		stop_button.resize(50, 32)
		stop_button.move(335, 155)

	def render_slider(self) -> None:

		self.sl = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
		self.sl.setMinimum(0)
		self.sl.setMaximum(100)
		self.sl.setValue(25)
		self.sl.setTickPosition(QtWidgets.QSlider.TicksBelow)
		self.sl.setTickInterval(5)
		self.sl.setGeometry(50, 160, 270, 30)
		self.sl.valueChanged.connect(self.update_label)

		self.label = QtWidgets.QLabel('25', self)
		self.label.setMinimumWidth(80)
		self.label.move(13, 154)

	def update_label(self, value: int) -> None:

		self.media_player.audio_set_volume(value)
		self.label.setText(str(value))

	def __init__(self) -> None:

		QtWidgets.QMainWindow.__init__(self)

		self.setMinimumSize(QtCore.QSize(400, 200))
		self.setWindowTitle("r A d I o")

		self.sl = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
		self.label = QtWidgets.QLabel('25', self)

		self.render_slider()
		self.render_stop_button()

		self.media_player = vlc.MediaPlayer()

		position_y = 10
		for channelGroups in channels:
			position_x = 10
			for name, url in channelGroups.items():
				self.build_button(name, position_x, position_y)
				position_x += 130
			position_y += 40

	def build_button(self, name: str, left: int, top: int) -> QtWidgets.QPushButton:

		button = QtWidgets.QPushButton(name, self)
		button.clicked.connect(lambda: self.play_radio(name))
		button.resize(120, 32)
		button.move(left, top)

		return button

	def stop_radio(self) -> None:

		self.media_player.stop()

	@staticmethod
	def get_station_url(channel: str) -> str:

		for channelGroups in channels:
			for name, url in channelGroups.items():
				if name == channel:
					if 'radioplay' in url:
						return url + radioplayprefix

					return url

	def play_radio(self, channel: str) -> None:

		self.stop_radio()

		media = vlc.Media(self.get_station_url(channel))
		self.media_player.set_media(media)
		self.media_player.play()

		print('selected channel: ', channel)

		asyncio.run(self.update_volume())


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.show()
	sys.exit(app.exec_())
