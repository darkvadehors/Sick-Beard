# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of Sick Beard.
#
# Sick Beard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sick Beard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sick Beard.  If not, see <http://www.gnu.org/licenses/>.

import sickbeard
from sickbeard import version, ui
from sickbeard import logger
from sickbeard import scene_exceptions
from sickbeard.exceptions import ex
from sickbeard import network_timezones

import os, platform, shutil
import subprocess, re
import urllib, urllib2
import zipfile, tarfile

from urllib2 import URLError
import gh_api as github

class CheckVersion():
    """
    Version check class meant to run as a thread object with the SB scheduler.
    """

    def __init__(self):
        self.install_type = self.find_install_type()

        if self.install_type == 'win':
            self.updater = WindowsUpdateManager()
        elif self.install_type == 'git':
            self.updater = GitUpdateManager()
        elif self.install_type == 'source':
            self.updater = SourceUpdateManager()
        else:
            self.updater = None

    def run(self):
        self.check_for_new_version()
        
        # refresh scene exceptions too
        scene_exceptions.retrieve_exceptions()
        
        # refresh network timezones
        network_timezones.update_network_dict()

    def find_install_type(self):
        """
        Determines how this copy of SB was installed.
        
        returns: type of installation. Possible values are:
            'win': any compiled windows build
            'git': running from source using git
            'source': running from source without git
        """

        # check if we're a windows build
        if version.SICKBEARD_VERSION.startswith('build '):
            install_type = 'win'
        elif os.path.isdir(os.path.join(sickbeard.PROG_DIR, '.git')):
            install_type = 'git'
        else:
            install_type = 'source'

        return install_type

    def check_for_new_version(self, force=False):
        """
        Checks the internet for a newer version.
        
        returns: bool, True for new version or False for no new version.
        
        force: if true the VERSION_NOTIFY setting will be ignored and a check will be forced
        """

        if not sickbeard.VERSION_NOTIFY and not force:
            logger.log(u"La v&eacute;rification de version est d&eacute;sactiv&eacute;, pas la v&eacute;rification de la nouvelle version")
            return False

        logger.log(u"V&eacute;rification si "+self.install_type+" besoin une mise &agrave; jour")
        if not self.updater.need_update():
            logger.log(u"Aucune mise &agrave; jour n&eacute;cessaire")
            if force:
                ui.notifications.message('Aucune mise &agrave; jour n&eacute;cessaire')
            return False

        self.updater.set_newest_text()
        return True

    def update(self):
        if self.updater.need_update():
            return self.updater.update()

class UpdateManager():
    def get_update_url(self):
        return sickbeard.WEB_ROOT+"/home/update/?pid="+str(sickbeard.PID)

class WindowsUpdateManager(UpdateManager):

    def __init__(self):
        self._cur_version = None
        self._cur_commit_hash = None
        self._newest_version = None

        self.releases_url = "https://github.com/" + self.github_repo_user + "/" + self.github_repo + "/" + "releases" + "/"
        self.version_url = "https://raw.github.com/" + self.github_repo_user + "/" + self.github_repo + "/" + self.branch + "/updates.txt"

    def _find_installed_version(self):
        return int(sickbeard.version.SICKBEARD_VERSION[6:])

    def _find_newest_version(self, whole_link=False):
        """
        Checks git for the newest Windows binary build. Returns either the
        build number or the entire build URL depending on whole_link's value.

        whole_link: If True, returns the entire URL to the release. If False, it returns
                    only the build number. default: False
        """

        regex = ".*SickBeard\-win32\-alpha\-build(\d+)(?:\.\d+)?\.zip"

        svnFile = urllib.urlopen(self.version_url)

        for curLine in svnFile.readlines():
            logger.log(u"v&eacute;rification en ligne "+curLine, logger.DEBUG)
            match = re.match(regex, curLine)
            if match:
                logger.log(u"Correspondance trouv&eacute;", logger.DEBUG)
                if whole_link:
                    return curLine.strip()
                else:
                    return int(match.group(1))

        return None

    def need_update(self):
        self._cur_version = self._find_installed_version()
        self._newest_version = self._find_newest_version()

        logger.log(u"nouvelle version: "+repr(self._newest_version), logger.DEBUG)

        if self._newest_version and self._newest_version > self._cur_version:
            return True

    def set_newest_text(self):
        new_str = 'Il y a une <a href="'+self.gc_url+'" onclick="window.open(this.href); return false;">nouvelle version disponible</a> (build '+str(self._newest_version)+')'
        new_str += "&mdash; <a href=\""+self.get_update_url()+"\">Mettre &agrave; jour maintenant</a>"
        new_str += ' - Ou cliquez <a href="'+self.gc_url+'" onclick="window.open(this.href); return false;">ICI</a> pour voir les nouvelles mises &agrave; niveau'
        sickbeard.NEWEST_VERSION_STRING = new_str

    def update(self):

        new_link = self._find_newest_version(True)

        logger.log(u"new_link: " + repr(new_link), logger.DEBUG)

        if not new_link:
            logger.log(u"Impossible de trouver une nouvelle version en lien sur google code, pas de mise &agrave; jour")
            return False

        # download the zip
        try:
            logger.log(u"T&eacute;l&eacute;chargement de fichier de mise &agrave; jour "+str(new_link))
            (filename, headers) = urllib.urlretrieve(new_link) #@UnusedVariable

            # prepare the update dir
            sb_update_dir = os.path.join(sickbeard.PROG_DIR, 'sb-update')
            logger.log(u"D&eacute;gager le dossier de mise &agrave; jour "+sb_update_dir+" avant la d&eacute;compression")
            if os.path.isdir(sb_update_dir):
                shutil.rmtree(sb_update_dir)

            # unzip it to sb-update
            logger.log(u"d&eacute;compression de "+str(filename)+" dans "+sb_update_dir)
            update_zip = zipfile.ZipFile(filename, 'r')
            update_zip.extractall(sb_update_dir)
            update_zip.close()
            
            # find update dir name
            update_dir_contents = os.listdir(sb_update_dir)
            if len(update_dir_contents) != 1:
                logger.log("Les donn&eacute;es de mise &agrave; jour invalides, mise &agrave; jour &agrave; &eacute;chou&eacute;. Peut-&ecirc;tre essayer de supprimer votre dossier sb-update &agrave; jour?", logger.ERROR)
                return False

            content_dir = os.path.join(sb_update_dir, update_dir_contents[0])
            old_update_path = os.path.join(content_dir, 'updater.exe')
            new_update_path = os.path.join(sickbeard.PROG_DIR, 'updater.exe')
            logger.log(u"Copie du nouveau fichier update.exe de "+old_update_path+" dans "+new_update_path)
            shutil.move(old_update_path, new_update_path)

            # delete the zip
            logger.log(u"Suppr&eacute;ssion du fichier Zip de "+str(filename))
            os.remove(filename)

        except Exception, e:
            logger.log(u"Erreur lors de la mise &agrave; jour: "+ex(e), logger.ERROR)
            return False

        return True

class GitUpdateManager(UpdateManager):

    def __init__(self):
        self._cur_commit_hash = None
        self._newest_commit_hash = None
        self._num_commits_behind = 0

        self.git_url = 'http://code.google.com/p/sickbeard/downloads/list'

        self.branch = self._find_git_branch()

    def _git_error(self):
        error_message = 'Impossible de trouver votre git ex&eacute;cutable - soit supprimer votre dossier .git et ex&eacute;cuter de la source OU <a href="http://code.google.com/p/sickbeard/wiki/AdvancedSettings" onclick="window.open(this.href); return false;">r&eacute;gler git_path dans votre config.ini</a> pour permettre des mises &agrave; jour.'
        sickbeard.NEWEST_VERSION_STRING = error_message
        
        return None

    def _run_git(self, args):
        
        if sickbeard.GIT_PATH:
            git_locations = ['"'+sickbeard.GIT_PATH+'"']
        else:
            git_locations = ['git']
        
        # osx people who start SB from launchd have a broken path, so try a hail-mary attempt for them
        if platform.system().lower() == 'darwin':
            git_locations.append('/usr/local/git/bin/git')

        output = err = None

        for cur_git in git_locations:

            cmd = cur_git+' '+args
        
            try:
                logger.log(u"Ex&eacute;cut&eacutez "+cmd+" avec votre Shell dans "+sickbeard.PROG_DIR, logger.DEBUG)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, cwd=sickbeard.PROG_DIR)
                output, err = p.communicate()
                logger.log(u"git output: "+output, logger.DEBUG)
            except OSError:
                logger.log(u"La Commande "+cmd+" ne fonctionne pas, git non trouv&eacute;.")
                continue
            
            if p.returncode != 0 or 'not found' in output or "pas reconnu comme une commande interne ou externe" in output:
                logger.log(u"Impossible de trouver git avec la commande "+cmd, logger.DEBUG)
                output = None
            elif 'fatal:' in output or err:
                logger.log(u"Git &agrave; retourn&eacute; une mauvaise information, &ecirc;tes-vous s&ucirc;r que ce soit une installation de git?", logger.ERROR)
                output = None
            elif output:
                break

        return (output, err)

    
    def _find_installed_version(self):
        """
        Attempts to find the currently installed version of Sick Beard.

        Uses git show to get commit version.

        Returns: True for success or False for failure
        """

        output, err = self._run_git('rev-parse HEAD') #@UnusedVariable

        if not output:
            return self._git_error()

        logger.log(u"Sortie Git: "+str(output), logger.DEBUG)
        cur_commit_hash = output.strip()

        if not re.match('^[a-z0-9]+$', cur_commit_hash):
            logger.log(u"La sortie ne ressemble pas &agrave; un hachage, ne l'utilisez pas", logger.ERROR)
            return self._git_error()
        
        self._cur_commit_hash = cur_commit_hash
            
        return True

    def _find_git_branch(self):

        branch_info = self._run_git('symbolic-ref -q HEAD')

        if not branch_info or not branch_info[0]:
            return 'master'

        branch = branch_info[0].strip().replace('refs/heads/', '', 1)

        return branch or 'master'


    def _check_github_for_update(self):
        """
        Uses pygithub to ask github if there is a newer version that the provided
        commit hash. If there is a newer version it sets Sick Beard's version text.

        commit_hash: hash that we're checking against
        """

        self._num_commits_behind = 0
        self._newest_commit_hash = None

        gh = github.GitHub()

        # find newest commit
        for curCommit in gh.commits('darkvadehors', 'Sick-Beard', self.branch):
            if not self._newest_commit_hash:
                self._newest_commit_hash = curCommit['sha']
                if not self._cur_commit_hash:
                    break

            if curCommit['sha'] == self._cur_commit_hash:
                break

            self._num_commits_behind += 1

        logger.log(u"plus r&eacute;cent: "+str(self._newest_commit_hash)+" et courant: "+str(self._cur_commit_hash)+" et num_commits: "+str(self._num_commits_behind), logger.DEBUG)

    def set_newest_text(self):

        # if we're up to date then don't set this
        if self._num_commits_behind == 100:
            message = "ou bien vous &ecirc;tes en avance sur la master"

        elif self._num_commits_behind > 0:
            message = "Il y a %d commit" % self._num_commits_behind
            if self._num_commits_behind > 1: message += 's'
            message += ' en retard'

        else:
            return

        if self._newest_commit_hash:
            url = 'http://github.com/darkvadehors/Sick-Beard/compare/'+self._cur_commit_hash+'...'+self._newest_commit_hash
        else:
            url = 'http://github.com/darkvadehors/Sick-Beard/commits/'

        new_str = 'Il y a une <a href="'+url+'" onclick="window.open(this.href); return false;">nouvelle version disponible</a> ('+message+')'
        new_str += "&mdash; <a href=\""+self.get_update_url()+"\">Mettre &agrave; jour maintemant</a>"
        new_str += ' - Ou cliquez <a href="'+url+'" onclick="window.open(this.href); return false;">ICI</a> pour voir nouvelles mises &agrave; niveau'
        sickbeard.NEWEST_VERSION_STRING = new_str
    def need_update(self):
        self._find_installed_version()
        try:
            self._check_github_for_update()
        except Exception, e:
            logger.log(u"Impossible de contacter github, la mise &agrave; jour ne peut pas v&eacute;rifi&eacute; : "+repr(e), logger.ERROR)
            return False

        logger.log(u"Apr&eagrave;s contr&ocirc;le, cur_commit = "+str(self._cur_commit_hash)+", newest_commit = "+str(self._newest_commit_hash)+", num_commits_behind = "+str(self._num_commits_behind), logger.DEBUG)

        if self._num_commits_behind > 0:
            return True

        return False

    def update(self):
        """
        Calls git pull origin <branch> in order to update Sick Beard. Returns a bool depending
        on the call's success.
        """
        self._run_git('config remote.origin.url git://github.com/darkvadehors/Sick-Beard.git')
        self._run_git('stash')
        output, err = self._run_git('pull git://github.com/darkvadehors/Sick-Beard.git '+self.branch) #@UnusedVariable

        if not output:
            return self._git_error()

        pull_regex = '(\d+) .+,.+(\d+).+\(\+\),.+(\d+) .+\(\-\)'

        (files, insertions, deletions) = (None, None, None)

        for line in output.split('\n'):

            if 'Already up-to-date.' in line:
                logger.log(u"Aucune mise &agrave; jour disponible, pas de mise &agrave; jour")
                logger.log(u"Sortie: "+str(output))
                return False
            elif line.endswith('Aborting.'):
                logger.log(u"Impossible de mettre &agrave; jour &agrave; partir de git: "+line, logger.ERROR)
                logger.log(u"Sortie: "+str(output))
                return False

            match = re.search(pull_regex, line)
            if match:
                (files, insertions, deletions) = match.groups()
                break

        if None in (files, insertions, deletions):
            logger.log(u"Rien n'indique le succes de l&acute;opr&eacute;ration, en supposant git pull r&eacute;ussi", logger.DEBUG)
            logger.log(u"Sortie: "+str(output))
            return True

        return True



class SourceUpdateManager(GitUpdateManager):

    def _find_installed_version(self):

        version_file = os.path.join(sickbeard.PROG_DIR, 'version.txt')

        if not os.path.isfile(version_file):
            self._cur_commit_hash = None
            return

        fp = open(version_file, 'r')
        self._cur_commit_hash = fp.read().strip(' \n\r')
        fp.close()

        if not self._cur_commit_hash:
            self._cur_commit_hash = None

    def need_update(self):

        parent_result = GitUpdateManager.need_update(self)

        if not self._cur_commit_hash:
            return True
        else:
            return parent_result


    def set_newest_text(self):
        if not self._cur_commit_hash:
            logger.log(u"Version actuelle inconnu, je ne sais pas si nous devrions mettre &agrave; jour ou non", logger.DEBUG)

            new_str = "Version inconnu: Si vous n&apos;avez jamais utilis&eacute; le syst&egrave;me de mise &agrave; niveau Sick Beard alors je ne sais pas quelle version vous avez."
            new_str += "&mdash; <a href=\""+self.get_update_url()+"\">METTRE &Agrave; JOUR MAINTENANT"

            sickbeard.NEWEST_VERSION_STRING = new_str

        else:
            GitUpdateManager.set_newest_text(self)

    def update(self):
        """
        Downloads the latest source tarball from github and installs it over the existing version.
        """

        tar_download_url = 'https://github.com/darkvadehors/Sick-Beard/tarball/'+version.SICKBEARD_VERSION
        sb_update_dir = os.path.join(sickbeard.PROG_DIR, 'sb-update')
        version_path = os.path.join(sickbeard.PROG_DIR, 'version.txt')

        # retrieve file
        try:
            logger.log(u"T&eacute;l&eacute;chargement de la mise &agrave; jour depuis "+tar_download_url)
            data = urllib2.urlopen(tar_download_url)
        except (IOError, URLError):
            logger.log(u"Impossible de r&eacute;cup&eacute;rer nouvelle version de "+tar_download_url+", mise &agrave; jour impossible", logger.ERROR)
            return False

        download_name = data.geturl().split('/')[-1].split('?')[0]

        tar_download_path = os.path.join(sickbeard.PROG_DIR, download_name)

        # save to disk
        f = open(tar_download_path, 'wb')
        f.write(data.read())
        f.close()

        # extract to temp folder
        logger.log(u"Extraction du fichier "+tar_download_path)
        tar = tarfile.open(tar_download_path)
        tar.extractall(sb_update_dir)
        tar.close()

        # delete .tar.gz
        logger.log(u"Suppr&eacute;ssion du fichier "+tar_download_path)
        os.remove(tar_download_path)

        # find update dir name
        update_dir_contents = [x for x in os.listdir(sb_update_dir) if os.path.isdir(os.path.join(sb_update_dir, x))]
        if len(update_dir_contents) != 1:
            logger.log(u"Les donn&eacute;es de mise &agrave; jour sont invalides, la mise &agrave; jour a &eacute;chou&eacute;: "+str(update_dir_contents), logger.ERROR)
            return False
        content_dir = os.path.join(sb_update_dir, update_dir_contents[0])

        # walk temp folder and move files to main folder
        for dirname, dirnames, filenames in os.walk(content_dir): #@UnusedVariable
            dirname = dirname[len(content_dir)+1:]
            for curfile in filenames:
                old_path = os.path.join(content_dir, dirname, curfile)
                new_path = os.path.join(sickbeard.PROG_DIR, dirname, curfile)

                if os.path.isfile(new_path):
                    os.remove(new_path)
                os.renames(old_path, new_path)

        # update version.txt with commit hash
        try:
            ver_file = open(version_path, 'w')
            ver_file.write(self._newest_commit_hash)
            ver_file.close()
        except IOError, e:
            logger.log(u"Impossible d'&eacute;crire le fichier de version, mise &agrave; jour incomplete: "+ex(e), logger.ERROR)
            return False

        return True

