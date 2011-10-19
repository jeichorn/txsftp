# txsftp
# Copyright (c) 2011 Phil Christensen
#
#
# See LICENSE for details

"""
Virtualized SFTP transfer support.
"""

import os.path

from twisted.conch import unix

class VirtualizedSFTPServer(unix.SFTPServerForUnixConchUser):
	pass
