# txsftp
# Copyright (c) 2011 Phil Christensen
#
#
# See LICENSE for details

"""
twistd plugin support

This module adds a 'txsftp' server type to the twistd service list.
"""

import os, warnings

from zope.interface import classProvides, implements

from twisted import plugin
from twisted.python import usage, log
from twisted.internet import reactor
from twisted.application import internet, service

from twisted.conch.ssh.keys import Key
from twisted.conch.ssh.factory import SSHFactory
from twisted.conch.unix import UnixSSHRealm
from twisted.cred.checkers import ICredentialsChecker
from twisted.cred.credentials import IUsernamePassword
from twisted.cred.portal import Portal

from txsftp import conf

class DummyChecker(object):
	credentialInterfaces = (IUsernamePassword,)
	implements(ICredentialsChecker)

	def requestAvatarId(self, credentials):
		return credentials.username

class txsftp_plugin(object):
	"""
	The txsftp application server startup class.
	"""

	classProvides(service.IServiceMaker, plugin.IPlugin)

	tapname = "txsftp"
	description = "Run a txsftp server."

	class options(usage.Options):
		"""
		Implement option-parsing for the txsftp twistd plugin.
		"""
		optParameters = [
			["conf", "f", "/etc/txsftp.json", "Path to configuration file, if any.", str],
		]

	@classmethod
	def makeService(cls, config):
		"""
		Create the txsftp service.
		"""
		if(conf.get('suppress-deprecation-warnings')):
			warnings.filterwarnings('ignore', r'.*', DeprecationWarning)
		
		get_key = lambda path: Key.fromString(data=open(path).read())
		public_key = get_key(conf.get('public-key'))
		private_key = get_key(conf.get('private-key'))

		factory = SSHFactory()
		factory.privateKeys = {'ssh-rsa': private_key}
		factory.publicKeys = {'ssh-rsa': public_key}
		factory.portal = Portal(UnixSSHRealm())
		factory.portal.registerChecker(DummyChecker())

		return internet.TCPServer(conf.get('sftp-port'), factory)
