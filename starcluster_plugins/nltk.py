#!/usr/bin/python

# Copyright 2011, Joe Pranevich

# This file is distributed under the GNU Lesser General Public License.
# http://www.gnu.org/licenses/lgpl.html

from starcluster.clustersetup import ClusterSetup
from starcluster import threadpool
from starcluster.logger import log

class PackageInstaller(ClusterSetup):

	def install_nltk(self, node):
		node.ssh.execute('apt-get -y install python-nltk')
		node.ssh.execute('python -m nltk.downloader all')
		node.ssh.execute('mv -f /root/nltk_data /usr/lib/')
		node.ssh.execute('chmod -R a+r /usr/lib/nltk_data')

	def __init__(self, pkg_to_install):
		self.pkg_to_install = pkg_to_install

	def run(self, nodes, master, user, user_shell, volumes):
		log.info("Installing NLTK...")
		pool = threadpool.ThreadPool(size=20)
		for node in nodes:
			pool.simple_job(self.install_nltk, (node,))
			pool.wait(numtasks=len(nodes))


